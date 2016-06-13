import os
import sys
import vmdk


def main(argv):
    vmx = vmdk.Vmx.open_from_file(argv[0])

    vmdk_filepath = os.path.join(vmx.workingdir, vmx.storage['ide0:0'])
    vmdk_obj = vmdk.Vmdk.from_filepath(vmdk_filepath)

    print(vmdk_obj.read(9000000, 16659280))
    data = vmdk_obj.read(0, 1)
#    print(data)
    print(len(data))

if __name__ == '__main__':
    main(sys.argv[1:])
