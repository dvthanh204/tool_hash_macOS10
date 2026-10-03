import zipfile
import os
import shutil

outer_zip = 'outer.zip'
inner_zip = 'SlideLock-App-Shell-MacOS.zip'

print("Extracting outer zip...")
with zipfile.ZipFile(outer_zip, 'r') as z:
    z.extractall('.')
    
print("Removing old SlideLock.app in ma_hoa_mac10...")
dest_path = os.path.join('ma_hoa_mac10', 'SlideLock.app')
if os.path.exists(dest_path):
    shutil.rmtree(dest_path)
    
print("Extracting inner zip...")
with zipfile.ZipFile(inner_zip, 'r') as z:
    z.extractall('ma_hoa_mac10')
    
print("Done!")
