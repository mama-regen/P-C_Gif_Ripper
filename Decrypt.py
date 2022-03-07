import regex as re
from math import ceil
from typing import List
from ByteReader import Reader, SeekOrigin as so
from DataTypes import int_32

class rpg_file:
    offset: int_32 = int_32(0)
    size: int_32 = int_32(0)
    key: int_32 = int_32(0)
    name: str

def decrypt_name(data: bytes, key: int|int_32) -> str:
    if type(key) != int_32: key = int_32(key)
    key.to_unsigned()
    decrypted_name: bytes = b""
    key_bytes = key.to_bytes()

    j = 0
    for i in range(len(data)):
        if j == 4:
            j = 0
        decrypted_name += int_32(data[i] ^ (key_bytes[j] if j < len(key_bytes) else 0)).to_bytes()
        j += 1
    
    return decrypted_name.decode("utf-8")

def read_archive(file_path: str, match_str: str = None) -> List[rpg_file]:
    reader: Reader = Reader(file_path)
    reader.seek(8, so.Begin)

    key = reader.read_int32().to_unsigned()
    key *= 9
    key += 3

    files: List[rpg_file] = []

    while(1):
        file = rpg_file()
        file.offset = int_32(reader.read_int32() ^ key)
        file.size = int_32(reader.read_int32() ^ key)
        file.key = int_32(reader.read_int32() ^ key).to_unsigned()
        length = int_32(reader.read_int32() ^ key)

        if file.offset < 0 or reader._p + length >= len(reader._data): break

        try:
            file.name = decrypt_name(reader.read_bytes(length), key).replace("\\", "/")

            if match_str is not None and not re.match(match_str, file.name, flags=re.IGNORECASE): continue

            files.append(file)
        except Exception as e:
            print('skipping: ' + str(e))
            break
    
    return files

def decrypt(files: List[rpg_file], file_location: str, save_location: str) -> None:
    reader = Reader(file_location)
    for file in files:
        file_name = file.name.split("/")[-1:][0]
        reader.seek(file.offset, so.Begin)
        data: bytes = reader.read_bytes(file.size)
        decrypted_file = b""

        key = file.key.to_unsigned()
        key_bytes = key.to_bytes() + b'\x00\x00\x00\x00'
        j = 0

        for i in range(len(data)):
            if j == 4:
                j = 0
                key *= 7
                key += 3
                key_bytes = key.to_bytes() + b'\x00\x00\x00\x00'

            result = data[i] ^ key_bytes[j]
            decrypted_file += result.to_bytes(1, 'little')
            j += 1

        open(f"{save_location.rstrip('/')}/{file_name}", "wb").write(decrypted_file)