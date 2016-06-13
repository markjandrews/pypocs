from ctypes import *
import os
import shlex
import struct


class ExtentHeader(Structure):
    _pack_ = 1
    _fields_ = [('magicNumber', c_uint32),
                ('version', c_uint32),
                ('flags', c_uint32),
                ('capacity', c_uint64),
                ('grainSize', c_uint64),
                ('descriptorOffset', c_uint64),
                ('descriptorSize', c_uint64),
                ('numGTEsPerGT', c_uint32),
                ('rgdOffset', c_uint64),
                ('gdOffset', c_uint64),
                ('overHead', c_uint64),
                ('uncleanShutdown', c_bool),
                ('singleEndLineChar', c_char),
                ('nonEndLineChar', c_char),
                ('doubleEndLineChar1', c_char),
                ('doubleENdLineChar2', c_char),
                ('compressAlgorithm', c_uint16),
                ('pad', c_uint8 * 433)]


class Extent(object):
    def __init__(self, access, size, extent_type, filename, offset=0, descriptor=None):
        self.access = access
        self.size = int(size)
        self.type = extent_type
        self.filename = filename
        self.offset = int(offset)

        assert descriptor is not None, 'Must provide an owning descrpiptor'
        self.descriptor = descriptor

    def __str__(self):
        return 'Extent(access="%s", size=%s, extent_type="%s", filename="%s", offset=%s)' % (self.access,
                                                                                             self.size,
                                                                                             self.type,
                                                                                             self.filename,
                                                                                             self.offset)

    def __repr__(self):
        return 'Extent(access="%s", size=%s, extent_type="%s", filename="%s", offset=%s)' % (self.access,
                                                                                             self.size,
                                                                                             self.type,
                                                                                             self.filename,
                                                                                             self.offset)

    @property
    def filepath(self):
        return os.path.realpath(os.path.join(os.path.dirname(self.descriptor.vmdk.filepath), self.filename))

    def read(self, offset, size):

        data = []

        with open(self.filepath, 'rb') as inf:
            extent_header = ExtentHeader()
            inf.readinto(extent_header)

            grainsize = extent_header.grainSize
            # if extent_header.flags & 2:
            gd = extent_header.rgdOffset
            # else:
            # gd = extent_header.gdOffset

            coverage = extent_header.numGTEsPerGT * grainsize

            while size > 0:

                gde_index = int(offset / coverage)
                gde = Vmdk.sectors_to_bytes(gd) + (gde_index * Vmdk.UINT32_SIZE)

                inf.seek(gde)
                gt = struct.unpack('L', inf.read(4))[0]
                gte_index = int((offset % coverage)/grainsize)

                gte = Vmdk.sectors_to_bytes(gt) + (gte_index * Vmdk.UINT32_SIZE)
                inf.seek(gte)
                grain = struct.unpack('L', inf.read(4))[0]

                relative_offset = offset % grainsize
                read_size = min(size, grainsize - relative_offset)

                if grain == 0:
                    parent = self.descriptor.parent
                    if parent is not None:
                        print('Reading from parent')
                        data.append(parent.read(offset, size))
                    else:
                        data.append(b'0' * read_size)
                elif grain == 1:
                    data.append(b'0' * read_size)
                else:
                    sector_offset = grain + relative_offset
                    sector_offset_bytes = Vmdk.sectors_to_bytes(sector_offset)
                    inf.seek(sector_offset_bytes)
                    temp_data = inf.read(Vmdk.sectors_to_bytes(read_size))
                    data.append(temp_data)

                offset += read_size
                size -= read_size

                print('%s remaining' % size)

        return b''.join(data)


class Descriptor(object):
    def __init__(self, data):

        self.vmdk = None
        self._parent = None

        eof = data.find(b'\x00')

        if eof >= 0:
            data = data[:data.find(b'\x00') - 1]

        self.extents = []
        self.dbentries = {}
        self.entries = {}

        for line in data.splitlines():
            if len(line) == 0 or line.startswith(b'#'):
                continue

            if b'RW' == line[:2] or b'RDONLY' == line[:6] or b'NOACCESS' == line[:8]:
                extent = Extent(*shlex.split(line.decode()), descriptor=self)
                self.extents.append(extent)
            elif b'ddb.' == line[:4]:
                key, value = line.decode().split('=', 1)
                self.dbentries[key.strip()] = value.strip().strip('"')
            else:
                key, value = line.decode().split('=', 1)
                self.entries[key.strip()] = value.strip().strip('"')

    @property
    def parent(self):

        if 'parentFileNameHint' in self.entries:
            if self._parent is None:
                self._parent = Vmdk.from_filepath(os.path.realpath(
                    os.path.join(os.path.dirname(self.vmdk.filepath), self.entries['parentFileNameHint'])))

            return self._parent

        return None


class Vmdk(object):
    VMDK_MAGICNUMBER = b'KDMV'
    COWD_MAGICNUMBER = b'DWOC'

    SECTOR_BIT_SIZE = 9
    SECTOR_SIZE = 512
    UINT32_SIZE = 4

    @classmethod
    def sectors_to_bytes(cls, csectors):
        result = csectors << cls.SECTOR_BIT_SIZE
        return result

    @classmethod
    def bytes_to_sectors(cls, cbytes):
        assert cbytes % cls.SECTOR_SIZE == 0, 'Bytes "%s" must be a multiple of sector size "%s"' % (
            cbytes, cls.SECTOR_SIZE)

        return cbytes >> cls.SECTOR_BIT_SIZE

    @classmethod
    def from_filepath(cls, filepath):

        with open(filepath, 'rb') as inf:
            magic_number = inf.read(4)

            if magic_number == cls.COWD_MAGICNUMBER:
                raise NotImplementedError('VMDK File not supported')
            elif magic_number == cls.VMDK_MAGICNUMBER:
                inf.seek(0)

                extent_header = ExtentHeader()
                inf.readinto(extent_header)

                descriptor_offset = cls.sectors_to_bytes(extent_header.descriptorOffset)
                descriptor_size = cls.sectors_to_bytes(extent_header.descriptorSize)

                inf.seek(descriptor_offset)
                data = inf.read(descriptor_size)
            else:
                inf.seek(0)
                data = inf.read()

            descriptor = Descriptor(data)
            return cls(descriptor, filepath)

    def __init__(self, descriptor, filepath=None):
        self.descriptor = descriptor
        self.descriptor.vmdk = self

        self.filepath = filepath

    def read(self, offset, size):

        data = []
        for extent in self.descriptor.extents:
            if size <= 0:
                break

            if offset < extent.size:
                read_offset = offset
                read_size = min(size, extent.size - read_offset)

                offset = 0
                size -= read_size
                data.append(extent.read(read_offset, read_size))

            if offset > 0:
                offset -= extent.size

        return b''.join(data)
