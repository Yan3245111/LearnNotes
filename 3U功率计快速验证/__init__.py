import struct


a = b'\xaa\xbb\xbb\xaa\x01\x00\x00\x00'

if a[: 4] == b'\xaa\xbb\xbb\xaa':
    print(struct.unpack("I", a[4:])[0])
