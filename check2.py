import struct

def check_macho(path):
    with open(path, 'rb') as f:
        magic = f.read(4)
        if magic in (b'\xca\xfe\xba\xbe', b'\xca\xfe\xba\xbf'):
            f.seek(16)
            offset = struct.unpack('>I', f.read(4))[0]
            f.seek(offset)
            submagic = f.read(4)
            endian = '<' if submagic == b'\xcf\xfa\xed\xfe' else '>'
            f.seek(offset + 16)
        elif magic == b'\xcf\xfa\xed\xfe':
            endian = '<'
            f.seek(16)
        else:
            return
            
        ncmds = struct.unpack(endian + 'I', f.read(4))[0]
        f.seek(12, 1) 
        
        for _ in range(ncmds):
            pos = f.tell()
            cmd = struct.unpack(endian + 'I', f.read(4))[0]
            cmdsize = struct.unpack(endian + 'I', f.read(4))[0]
            
            if cmd == 0x24: 
                v = struct.unpack(endian + 'I', f.read(4))[0]
                print(f"LC_VERSION_MIN_MACOSX: {(v>>16)&0xffff}.{(v>>8)&0xff}.{v&0xff}")
            elif cmd == 0x32: 
                platform = struct.unpack(endian + 'I', f.read(4))[0]
                v = struct.unpack(endian + 'I', f.read(4))[0]
                if platform == 1:
                    print(f"LC_BUILD_VERSION: {(v>>16)&0xffff}.{(v>>8)&0xff}.{v&0xff}")
            f.seek(pos + cmdsize)

check_macho('result_mac10/SlideLock.app/Contents/MacOS/SlideLock')
