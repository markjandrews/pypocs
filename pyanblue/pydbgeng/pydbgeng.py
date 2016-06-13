import os
import weakref
import comtypes.client
import comtypes
from comtypes.hresult import S_OK
from comtypes.automation import IID

from ctypes import *

SCRIPT_DIR = os.path.dirname(__file__)

comtypes.client.GetModule(os.path.join(SCRIPT_DIR, r"dbgeng.tlb"))
from comtypes.gen import DbgEng


dbgeng_dll = WinDLL('dbgeng')
DebugCreate = dbgeng_dll.DebugCreate
DebugCreate.argtypes = [POINTER(IID), POINTER(c_void_p)]
DebugCreate.restype = HRESULT


class PyDbgEng(object):

    @staticmethod
    def create_debug_client():
        client = POINTER(DbgEng.IDebugClient5)()
        result = DebugCreate(byref(DbgEng.IDebugClient5._iid_), byref(client))

        if result != S_OK:
            raise Exception('Failed to create debug client (%x)' % result)

        # client.AddRef()
        return client

    def __init__(self):
        comtypes.CoInitialize()
        self.finalizer = weakref.finalize(self, self.finalize)
        self.client = self.create_debug_client()
        self.advanced = self.client.QueryInterface(DbgEng.IDebugAdvanced3)
        self.control = self.client.QueryInterface(DbgEng.IDebugControl2)
        self.dataspaces = self.client.QueryInterface(DbgEng.IDebugDataSpaces4)
        self.registers = self.client.QueryInterface(DbgEng.IDebugRegisters2)
        self.symbols = self.client.QueryInterface(DbgEng.IDebugSymbols3)
        self.systemobjects = self.client.QueryInterface(DbgEng.IDebugSystemObjects4)

        print(self.registers.OutputRegisters(DbgEng.DEBUG_OUTCTL_LOG_ONLY, DbgEng.DEBUG_REGISTERS_INT32))

    def finalize(self):
        self.client.Release()
        comtypes.CoUninitialize()
