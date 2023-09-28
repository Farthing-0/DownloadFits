import os
import wget
import requests
import time
import argparse

def find_sh_files(dir,verify = False):
    for file in os.listdir(dir):
        if file.endswith(".sh") and file.startswith("tess"):
            return dir + file
    return None 

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
    elif(file_type == 'ffi'):
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

def download_multi_files(file_list,file_type,file_size = 0):
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(download_file,file_name,file_type,file_size) for file_name in file_list]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    parser = argparse.ArgumentParser('A little script to download TESS data. You can specify the type and sn of the sector to download. Or you can just run this script in the directory where the download script is located.')
    parser.add_argument('-t', '--type', help='Type of the file to download, lc, dvt or ffi.',)
    parser.add_argument('-n', '--sn', help='sn of the sector to download.',)
    args = parser.parse_args()
    if(args.type == None and args.sn != None):
        print('Please specify the type of the file to download.')
        exit()
    elif(args.type != None and args.sn == None):
        print('Please specify the sn of the sector to download.')
        exit()
    elif(args.type != 'lc' and args.type != 'dvt' and args.type != None):
        print('File type must be lc or dvt.')
        exit()
    if(args.sn != None):
        try:
            int(args.sn)
        except TypeError :
            print('sn must be an integer.')
            exit()
        except ValueError :
            print('sn must be an integer.')
            exit()
    dir = './'
    script_prefix = 'https://archive.stsci.edu/missions/tess/download_scripts/sector/'
    url_prefix = 'https://mast.stsci.edu/api/v0.1/Download/file/?uri=mast:TESS/product/'
    
    dir_file_list = os.listdir(dir)
    if(len(dir_file_list) != 1 and args.type != None and args.sn != None):
        print('Specify download must be in empty directory except this file.')
        exit()
    elif(len(dir_file_list) == 1 and args.type == None and args.sn == None):
        print('Please specify the type and sn of the sector to download.')
        exit()
    if(args.type == 'lc'):
        wget.download(script_prefix + 'tesscurl_sector_' + args.sn + '_lc.sh', out='tesscurl_sector_' + args.sn + '_lc.sh')
        # time.sleep(0.5)
    elif(args.type == 'dvt'):
        # https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_55_dv.sh
        wget.download(script_prefix + 'tesscurl_sector_' + args.sn + '_dv.sh', out='tesscurl_sector_' + args.sn + '_dvt.sh')
        # time.sleep(0.5)
    elif(args.type == 'ffi'):
        # https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_68_ffic.sh
        wget.download(script_prefix + 'tesscurl_sector_' + args.sn + '_ffic.sh', out='tesscurl_sector_' + args.sn + '_ffic.sh')
    
    sh_file = find_sh_files(dir)
    if(sh_file == None ):
        print('Finding sh file error.')
        exit()

    with open(sh_file, 'r') as f:
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
    elif(file_list[0].endswith('ffic.fits')):
        print('File type is ffi.')
        print('Searching ffi file size...')
        remote_size = int(requests.head(url_prefix + file_list[0]).headers['content-length'])
        download_multi_files(file_list,'ffi',remote_size)