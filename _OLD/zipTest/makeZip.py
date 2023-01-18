# Zip imports
from zipfile import ZipFile
from os.path import basename
import shutil
import os


intoThisDir = './Dest/'
outputName = 'myZipBoi'


# copy readme and decrypt to the OUTBOUND folder and zip all the files (use "OUTBOUND")
def copyAndZip(destinationDirectory,outputZipFileName):
    # copy readme into "OUTBOUND" Directory
    shutil.copy('./Carmen (smaller).jpg', destinationDirectory)
    shutil.copy('./Peter (smaller).jpg', destinationDirectory)
    shutil.copy('./Anna.jpg', destinationDirectory)
    


    # make directory to be sent out via email
    with ZipFile(f'{outputZipFileName}.zip','w') as myzip:
        print("get all files in this directory")
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(destinationDirectory):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                myzip.write(filePath, basename(filePath))



####
copyAndZip(intoThisDir,outputName)