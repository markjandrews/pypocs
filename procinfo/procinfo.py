from binascii import hexlify
import sys
from ctypes import *

ntdll = windll.ntdll
kernel32dll = windll.kernel32

HANDLE = c_void_p
DWORD = c_ulong
NTSTATUS = DWORD
BOOL = c_bool

NtQueryInformationProcess = ntdll.NtQueryInformationProcess
NtQueryInformationProcess.argtypes = [HANDLE, DWORD, c_void_p, DWORD, POINTER(DWORD)]
NtQueryInformationProcess.restype = NTSTATUS

OpenProcess = kernel32dll.OpenProcess
OpenProcess.argtypes = [DWORD, BOOL, DWORD]
OpenProcess.restype = HANDLE

CloseHandle = kernel32dll.CloseHandle
CloseHandle.argtypes = [HANDLE]
CloseHandle.restype = BOOL

ReadProcessMemory = kernel32dll.ReadProcessMemory
ReadProcessMemory.argtypes = [HANDLE, c_void_p, c_void_p, c_size_t, POINTER(c_size_t)]
ReadProcessMemory.restype = BOOL

GetLastError = kernel32dll.GetLastError
GetLastError.argtypes = []
GetLastError.restype = DWORD

# constants
PROCESS_QUERY_INFORMATION = 0x400

class PROCESS_BASIC_INFORMATION(Structure):
    _fields_ = [('ExitStatus', NTSTATUS),
                ('PebBaseAddress', c_void_p),
                ('AffinityMask', POINTER(c_ulong)),
                ('BasePriority', DWORD),
                ('UniqueProcessId', HANDLE),
                ('InheritedFromUniqueProcessId', HANDLE)]


class PEB(Structure):
    _fields_ = [('Reserved1', c_byte*2),
                ('BeingDebugged', c_bool),
                ('Reserved2', c_byte),
                ('Reserved3', c_byte*2),
                ('Ldr', c_void_p),
                ('ProcessParameters', c_void_p),
                ('Reserved4', c_byte*104),
                ('Reserved4', c_void_p*52),
                ('PostProcessInitRoutine', c_void_p),
                ('Reserved6', c_byte*128),
                ('Reserved7', c_void_p),
                ('SessionId', c_ulong)]


def main(argv):

    pbi = PROCESS_BASIC_INFORMATION()
    proc = OpenProcess(PROCESS_QUERY_INFORMATION, True, 6664)

    if 0 != NtQueryInformationProcess(proc, 0, byref(pbi), sizeof(pbi), None):
        raise Exception('Failed to retrieve process basic informaiton')

    peb = PEB()
    bytesRead = c_size_t()

    print(ReadProcessMemory(proc, pbi.PebBaseAddress, cast(byref(peb), c_void_p), sizeof(PEB), byref(bytesRead)))

    print(GetLastError())
    print(sizeof(PEB))
    print(bytesRead)
    CloseHandle(proc)



if __name__ == '__main__':
    main(sys.argv[1:])
