import argparse
import os
import sys
import subprocess
import shutil


os.chdir(os.path.dirname(__file__))


VHDFILE = r'c:\efi\efivm-disk1.vhd'
VHDLETTER = 'X'
AUTORUN_FILE = r'EFI/Boot/bootx64.efi'

VBOX_VM = r'Windows 8.1 EFI Clone'
VBOX_BIN = r'c:\Program Files\Oracle\VirtualBox\VBoxManage.exe'

ATTACH_SCRIPT = ("SELECT VDISK FILE=%s\n"
                 "ATTACH VDISK\n"
                 "RESCAN\n"
                 "LIST VOLUME\n")

ASSIGN_SCRIPT = ("RESCAN\n"
                 "SELECT VOLUME=%s\n"
                 "ASSIGN LETTER=%s\n"
                 "RESCAN\n"
                 "LIST VOLUME\n")

DETACH_SCRIPT = ("SELECT VOLUME=%s\n"
                 "REMOVE\n"
                 "SELECT VDISK FILE=%s\n"
                 "DETACH VDISK\n"
                 "RESCAN\n"
                 "LIST VOLUME\n")

SCRIPT_FILE = 'dpscript.txt'


def cmd_mount(vhd, letter, machine):

    print('Stopping Machine "%s"' % machine)
    out, err = subprocess.Popen('%s controlvm "%s" poweroff' % (VBOX_BIN, machine), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if len(err) > 0:
        if 'Invalid machine state: PoweredOff (must be Running, Paused or Stuck)' in err:
            print('*** WARNING *** Machine "%s" not running - could not be stopped' % machine)
        elif '...100%' in err:
            print(err)
        else:
            raise Exception('Failed to power off VM "%s" (%s)' % (machine, err))

    script = ATTACH_SCRIPT % vhd

    with open(SCRIPT_FILE, 'wb') as outf:
        #print(script)
        outf.write(script)

    out, err = subprocess.Popen('DISKPART /s %s' % SCRIPT_FILE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if len(err) > 0:
        raise Exception('Failed to attach VHD "%s"' % vhd)

    if 'DiskPart has encountered an error' in out:
        print('ATTACH ERROR:\n%s' % out)
        raise Exception('Failed to attach VHD "%s"' % vhd)

    volumenumber = None
    for line in out.splitlines():
        tokens = line.split()
        if len(tokens) >= 8:

            volumetype = tokens[2]
            volumevisible = tokens[7]

            if volumetype.upper() == 'FAT32' and volumevisible.upper() == 'HIDDEN':
                volumenumber = tokens[1]
                print('Found EFI Volume: %s' % line)
                break

    if volumenumber is None:
        raise Exception('Failed to attach/mount volume: %s' % vhd)

    script = ASSIGN_SCRIPT % (volumenumber, letter)
    with open(SCRIPT_FILE, 'wb') as outf:
        #print(script)
        outf.write(script)

    out, err = subprocess.Popen('DISKPART /s %s' % SCRIPT_FILE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if len(err) > 0:
        raise Exception(r'Failed to assign (%s:\) to VHD file "%s"' % (letter, vhd))

    #print('ASSIGN:\n%s' % out)
    print(r'Volume: "%s" (%s:\) appears to have been attached/mounted successfully' % (vhd, letter))

    if os.path.exists('%s:/%s' % (letter, AUTORUN_FILE)):
        try:
            os.unlink('%s:/%s' % (letter, AUTORUN_FILE))
        except (IOError, WindowsError) as e:
            print('Failed to remove AUTORUN file "%s"' % (AUTORUN_FILE % letter))


def cmd_unmount(vhd, letter, **wkargs):

    script = DETACH_SCRIPT % (letter, vhd)

    with open(SCRIPT_FILE, 'wb') as outf:
       #print(script)
        outf.write(script)

    out, err = subprocess.Popen('DISKPART /s %s' % SCRIPT_FILE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if len(err) > 0:
        raise Exception('Failed to attach VHD "%s"' % vhd)

    #print('DETACH:\n%s' % out)
    print('Volume: "%s" (%s:\) appears to have been removed/detached successfully' % (vhd, letter))


def cmd_update(bin, dest, machine, vhd, letter, **kwargs):

    cmd_mount(vhd, letter, machine)

    try:
        if bin is not None:
            if dest is None:
                dest = '%s:/%s' % (letter, os.path.basename(bin))
            else:
                dest = '%s:/%s' % (letter, dest)

            dest_dir = os.path.dirname(dest)
            if not len(dest_dir) > 0 and os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            shutil.copy2(bin, dest)
            print('Copied "%s" => "%s"' % (bin, dest))
        else:
            print('Removed AUTORUN from EFI partition')
    finally:
        cmd_unmount(vhd, letter)


def cmd_test(bin, machine, vhd, letter, **kwargs):

    if bin is not None:
        assert os.path.exists(bin)

    cmd_update(bin, AUTORUN_FILE, machine, vhd, letter)

    print('Starting Machine "%s" ...' % machine)
    out, err = subprocess.Popen('%s startvm "%s"' % (VBOX_BIN, machine), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if len(err) > 0:
        raise Exception('Failed to start VM "%s" (%s)' % (machine, err))

    print(out)

def main(argv):

    parser = argparse.ArgumentParser(description='Debug/Dev VHD Manager')
    subparser = parser.add_subparsers(help='sub-command help')

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-v', '--vhd', default=VHDFILE, help='File to VHD file')
    parent_parser.add_argument('-l', '--letter', default=VHDLETTER, help='Driver letter to mount VHD on')

    mount_parser = subparser.add_parser('mount', parents=[parent_parser])
    mount_parser.add_argument('-m', '--machine', default=VBOX_VM, help='VM with EFI bin to test')
    mount_parser.set_defaults(func=cmd_mount)

    unmount_parser = subparser.add_parser('unmount', parents=[parent_parser])
    unmount_parser.set_defaults(func=cmd_unmount)

    update_parser = subparser.add_parser('update', parents=[parent_parser])
    update_parser.add_argument('bin', nargs='?', default=None, help='Path to EFI Bin to copy to EFI partition')
    update_parser.add_argument('dest', nargs='?', default=None, help='Relative destination in EFI partition to copy bin')
    update_parser.add_argument('-m', '--machine', default=VBOX_VM, help='VM with EFI bin to test')
    update_parser.set_defaults(func=cmd_update)

    test_parser = subparser.add_parser('test', parents=[parent_parser])
    test_parser.add_argument('bin', help='Path to EFI Bin to test')
    test_parser.add_argument('-m', '--machine', default=VBOX_VM, help='VM with EFI bin to test')
    test_parser.set_defaults(func=cmd_test)

    shell_parser = subparser.add_parser('shell', parents=[parent_parser])
    shell_parser.add_argument('-m', '--machine', default=VBOX_VM, help='VM with EFI bin to test')
    shell_parser.set_defaults(func=cmd_test, bin=None)  # Tests with "None" bin so will run a shell

    args = parser.parse_args(argv)

    try:
        args.func(**vars(args))
    finally:
        if os.path.exists(SCRIPT_FILE):
            try:
                os.unlink(SCRIPT_FILE)
            except (WindowsError, IOError) as e:
                print('Failed to remove script file "%s" (%s)' % (SCRIPT_FILE, str(e)))


if __name__ == '__main__':
    main(sys.argv[1:])
