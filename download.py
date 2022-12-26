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

def download_multi_task(file_list,url_prefix,task_index,task_num,start_time):
    lc_full_size = 0
    dvt_full_size = 0
    full_file_counter = 0
    for index,file in enumerate(file_list):
        if(index % task_num == task_index):
            if os.path.isfile(file):
                if(file.endswith('s_lc.fits')):
                    size = os.path.getsize(dir+file)
                    if lc_full_size == 0:
                        print('Evaluate full size of lc file By' + file)
                        wget.download(url_prefix + file, out=file)
                        lc_full_size = os.path.getsize(dir+file)
                        print('Full size of lc file is ' + str(lc_full_size))
                        continue
                    if size < lc_full_size:
                        full_file_counter = 0
                        os.remove(dir+file)
                        print('File is not complete, downloading ' + file)
                        wget.download(url_prefix + file, out=file)                    
                    else:
                        full_file_counter += 1
                        print('Skip ' + str(full_file_counter) + ' files',end='\r',flush=True)
                elif(file.endswith('dvt.fits')):
                    size = os.path.getsize(dir+file)
                    remote_size = int(requests.head(url_prefix + file).headers['content-length'])
                    if size < remote_size:
                        full_file_counter = 0
                        os.remove(dir+file)
                        print('File is not complete, downloading ' + file)
                        wget.download(url_prefix + file, out=file)
                    else:
                        full_file_counter += 1
                        print('Skip ' + str(full_file_counter) + ' files',end='\r',flush=True)
            else:
                print('Downloading ' + file)
                wget.download(url_prefix + file, out=file)
            print('Download '+str(index)+'/'+str(len(file_list))+' complete.')
            print('assumed time left: ' + str((time.time() - start_time) / (index + 1) * (len(file_list) - index - 1) ))
    print('Download complete.')

def download_multi(file_list):
    from multiprocessing import  Process
    start_time = time.time()
    process_num = 30
    process_list = []
    url_prefix = 'https://mast.stsci.edu/api/v0.1/Download/file/?uri=mast:TESS/product/'
    for i in range(process_num):
        p = Process(target=download_multi_task,args=(file_list,url_prefix,i,process_num,start_time))
        p.start()
        process_list.append(p)
    for i in process_list:
        p.join()

if __name__ == "__main__":
    dir = './'
    file_list = []
    with open(find_sh_files(dir), 'r') as f:
        file_list = read_file_list(f)
    download_multi(file_list)