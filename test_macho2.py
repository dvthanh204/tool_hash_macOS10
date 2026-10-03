import struct

def check_macho(path):
    with open(path, 'rb') as f:
        magic = f.read(4)
        if magic == b'\xcf\xfa\xed\xfe':
            endian = '<'
        else:
            print("Not 64-bit macho")
            return
        
        cputype = struct.unpack(endian + 'I', f.read(4))[0]
        cpusubtype = struct.unpack(endian + 'I', f.read(4))[0]
        filetype = struct.unpack(endian + 'I', f.read(4))[0]
        ncmds = struct.unpack(endian + 'I', f.read(4))[0]
        sizeofcmds = struct.unpack(endian + 'I', f.read(4))[0]
        flags = struct.unpack(endian + 'I', f.read(4))[0]
        reserved = struct.unpack(endian + 'I', f.read(4))[0]
        
        for _ in range(ncmds):
            pos = f.tell()
            cmd = struct.unpack(endian + 'I', f.read(4))[0]
            cmdsize = struct.unpack(endian + 'I', f.read(4))[0]
            if cmd == 0x24: # LC_VERSION_MIN_MACOSX
                version = struct.unpack(endian + 'I', f.read(4))[0]
                print(f'LC_VERSION_MIN_MACOSX: {(version >> 16) & 0xffff}.{(version >> 8) & 0xff}.{version & 0xff}')
            elif cmd == 0x32: # LC_BUILD_VERSION
                platform = struct.unpack(endian + 'I', f.read(4))[0]
                version = struct.unpack(endian + 'I', f.read(4))[0]
                print(f'LC_BUILD_VERSION (platform {platform}): {(version >> 16) & 0xffff}.{(version >> 8) & 0xff}.{version & 0xff}')
            f.seek(pos + cmdsize)

check_macho('ma_hoa_mac10/SlideLock.app/Contents/MacOS/SlideLock')
