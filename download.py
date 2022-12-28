import os
import wget
import requests
import time

def find_sh_files(dir,verify = False):
    for file in os.listdir(dir):
        if file.endswith(".sh") and file.startswith("tess"):
            return dir + file

def read_file_list(file):
    file_list = []
    lines = file.readlines()
    for line in lines:
        file = line.split(' ')[-1].split('/')[-1][:-1]
        # if file.endswith('.fits') or file.endswith('.xml') or file.endswith('.pdf'):
        if file.endswith('.fits'):
            file_list.append(file)
    return file_list

def download_file(file_name,file_type,file_size = 0):
    url_prefix = 'https://mast.stsci.edu/api/v0.1/Download/file/?uri=mast:TESS/product/'
    # wget.download(url_prefix + file_name, out=file_name)
    if(file_type == 'lc'):
        if(os.path.isfile(file_name)):
            size = os.path.getsize(file_name)
            if size < file_size:
                os.remove(file_name)
                print('File is not complete, downloading ' + file_name)
                wget.download(url_prefix + file_name, out=file_name)
            else:
                print('Skip ' + file_name)
        else:
            print('Downloading ' + file_name)
            wget.download(url_prefix + file_name, out=file_name)
    elif(file_type == 'dvt'):
        if(os.path.isfile(file_name)):
            size = os.path.getsize(file_name)
            remote_size = int(requests.head(url_prefix + file_name).headers['content-length'])
            if size < remote_size:
                os.remove(file_name)
                print('File is not complete, downloading ' + file_name)
                wget.download(url_prefix + file_name, out=file_name)
            else:
                print('Skip ' + file_name)
        else:
            print('Downloading ' + file_name)
            wget.download(url_prefix + file_name, out=file_name)

def download_multi_files(file_list,file_type,file_size = 0):
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(download_file,file_name,file_type,file_size) for file_name in file_list]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    dir = './'
    url_prefix = 'https://mast.stsci.edu/api/v0.1/Download/file/?uri=mast:TESS/product/'
    file_list = []
    with open(find_sh_files(dir), 'r') as f:
        file_list = read_file_list(f)
    print('Downloading ' + str(len(file_list)) + ' files in total.')
    if(file_list[0].endswith('s_lc.fits')):
        print('File type is lc.')
        print('Searching lc file size...')
        remote_size = int(requests.head(url_prefix + file_list[0]).headers['content-length'])
        download_multi_files(file_list,'lc',remote_size)
    elif(file_list[0].endswith('dvt.fits')):
        print('File type is dvt.')
        download_multi_files(file_list,'dvt')