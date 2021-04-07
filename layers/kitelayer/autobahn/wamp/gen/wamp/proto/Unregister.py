# automatically generated by the FlatBuffers compiler, do not modify

# namespace: proto

import flatbuffers

class Unregister(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsUnregister(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Unregister()
        x.Init(buf, n + offset)
        return x

    # Unregister
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Unregister
    def Request(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Unregister
    def Registration(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

def UnregisterStart(builder): builder.StartObject(2)
def UnregisterAddRequest(builder, request): builder.PrependUint64Slot(0, request, 0)
def UnregisterAddRegistration(builder, registration): builder.PrependUint64Slot(1, registration, 0)
def UnregisterEnd(builder): return builder.EndObject()
