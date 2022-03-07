import os
from GifMaker import GifMaker
from Decrypt import decrypt, read_archive

dump_folder = './pic_dump'
archive = '../Game.rgss3a'

filter_str = "Graphics\/Pictures\/[a-z\d\s]+f\d+[a-z\d\s]*\.pn\w*"
file_list = read_archive(file_path=archive, match_str=filter_str)

decrypt(file_list, file_location=archive, save_location=dump_folder)

maker = GifMaker(dump_folder)
maker.scan()
maker.generate()

for file in os.listdir(dump_folder):
    if file.endswith('.png'): os.remove(f"{dump_folder}/{file}")