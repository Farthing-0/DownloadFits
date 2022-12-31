# DownloadFits
A script to download TESS fits file (lightcurve or datavalidation) quickly.

Welcome to use my script to speed up your downloading TESS data.

The file 'tesscurl_sector_6_lc.sh' is just for example and you can delete it.

You have two options to use this script.
## Specify the sector number and the file type in the script.
You can follow the help to pass the arguments to the script. For example, if you want to download the lightcurve data of sector 6, you can run the script like this:
```
python download.py -t lc -n 6
```
Remember put the download script in a empty folder.
## Put the download script in the same folder with the data.
You may select the data you want to download and download the origin data download script from [here](https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html). Then put it in the same folder with this script.
