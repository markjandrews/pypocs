import os


class Vmx(object):
    @classmethod
    def open_from_file(cls, filepath):
        options = {}

        with open(filepath, 'r') as inf:
            for line in inf:
                line = line.strip()

                if len(line) == 0:
                    continue

                key, value = line.split('=')
                options[key.strip()] = value.strip().strip('"')

        return Vmx(options, filepath=filepath)

    def __init__(self, options=None, filepath=None):

        self.filepath = filepath

        if options is None:
            options = {}

        self._options = options

    def __getitem__(self, item):
        return self._options[item]

    def __setitem__(self, key, value):
        self._options[key] = value

    def __contains__(self, item):
        return item in self._options

    def __str__(self):
        return 'Vmx(%s)' % str(self._options)

    def __repr__(self):
        return 'Vmx(%s)' % repr(self._options)

    @property
    def storage(self):

        device_names = [key for key, value in self._options.items() if
                        key.startswith('ide') and key.endswith('fileName') and value.strip('"').lower().endswith(
                            'vmdk')]

        devices = {}
        for device_name in device_names:
            key = device_name.split('.', 1)[0]
            value = self._options[device_name]

            devices[key] = value

        return devices

    @property
    def workingdir(self):

        if self.filepath is not None:
            return os.path.dirname(self.filepath)

        return ''
