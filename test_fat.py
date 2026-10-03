import struct
def check_fat(path):
    with open(path, 'rb') as f:
        magic = f.read(4)
        if magic == b'\xca\xfe\xba\xbe' or magic == b'\xca\xfe\xba\xbf':
            nfat_arch = struct.unpack('>I', f.read(4))[0]
            for _ in range(nfat_arch):
                cputype = struct.unpack('>I', f.read(4))[0]
                cpusubtype = struct.unpack('>I', f.read(4))[0]
                offset = struct.unpack('>I', f.read(4))[0]
                size = struct.unpack('>I', f.read(4))[0]
                align = struct.unpack('>I', f.read(4))[0]
                
                cur = f.tell()
                f.seek(offset)
                m = f.read(4)
                endian = '<' if m == b'\xcf\xfa\xed\xfe' else '>'
                f.read(12) # skip cpi, sub, filetype
                ncmds = struct.unpack(endian+'I', f.read(4))[0]
                f.read(12) # skip sizeofcmds, flags, reserved
                
                for __ in range(ncmds):
                    pos = f.tell()
                    cmd = struct.unpack(endian+'I', f.read(4))[0]
                    cmdsize = struct.unpack(endian+'I', f.read(4))[0]
                    if cmd == 0x32:
                        platform = struct.unpack(endian+'I', f.read(4))[0]
                        v = struct.unpack(endian+'I', f.read(4))[0]
                        ver = f'{(v>>16)&0xffff}.{(v>>8)&0xff}.{v&0xff}'
                        print(f'CPU {cputype}: platform {platform} version {ver}')
                    elif cmd == 0x24:
                        v = struct.unpack(endian+'I', f.read(4))[0]
                        ver = f'{(v>>16)&0xffff}.{(v>>8)&0xff}.{v&0xff}'
                        print(f'CPU {cputype}: LC_VERSION_MIN_MACOSX {ver}')
                    f.seek(pos + cmdsize)
                f.seek(cur)

check_fat('test_extract3/KhoaHoc_Mac/SlideLock.app/Contents/MacOS/SlideLock')
