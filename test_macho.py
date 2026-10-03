import struct

def parse_macho_min_version(file_path):
    with open(file_path, 'rb') as f:
        magic = f.read(4)
        print('Magic:', magic.hex())
        if magic in (b'\xca\xfe\xba\xbe', b'\xca\xfe\xba\xbf'):
            print('Fat binary detected.')
            # Let's just read the first architecture's offset
            f.seek(4)
            nfat_arch = struct.unpack('>I', f.read(4))[0]
            print(f'Number of architectures: {nfat_arch}')
            for _ in range(nfat_arch):
                cputype = struct.unpack('>I', f.read(4))[0]
                cpusubtype = struct.unpack('>I', f.read(4))[0]
                offset = struct.unpack('>I', f.read(4))[0]
                size = struct.unpack('>I', f.read(4))[0]
                align = struct.unpack('>I', f.read(4))[0]
                current = f.tell()
                f.seek(offset)
                parse_single_macho(f)
                f.seek(current)
        elif magic in (b'\xcf\xfa\xed\xfe', b'\xce\xfa\xed\xfe'):
            print('Mach-O 64-bit detected.')
            parse_single_macho(f)
        else:
            print('Not a valid Mach-O file or unsupported magic.')
            
def parse_single_macho(f):
    magic = f.read(4)
    if magic == b'\xcf\xfa\xed\xfe':
        endian = '<'
    elif magic == b'\xfe\xed\xfa\xcf':
        endian = '>'
    else:
        print('Unsupported architecture inside fat binary.')
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
            v1 = (version >> 16) & 0xffff
            v2 = (version >> 8) & 0xff
            v3 = version & 0xff
            print(f'LC_VERSION_MIN_MACOSX found: {v1}.{v2}.{v3}')
        elif cmd == 0x32: # LC_BUILD_VERSION
            platform = struct.unpack(endian + 'I', f.read(4))[0]
            version = struct.unpack(endian + 'I', f.read(4))[0]
            v1 = (version >> 16) & 0xffff
            v2 = (version >> 8) & 0xff
            v3 = version & 0xff
            print(f'LC_BUILD_VERSION (platform {platform}) found: {v1}.{v2}.{v3}')
        f.seek(pos + cmdsize)

import os
paths = ['ma_hoa_mac10/SlideLock.app/Contents/MacOS/SlideLock']
for p in paths:
    if os.path.exists(p):
        print(f"Parsing: {p}")
        parse_macho_min_version(p)
    else:
        print(f"File not found: {p}")
