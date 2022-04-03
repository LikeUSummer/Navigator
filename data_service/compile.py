import compileall
import os
import shutil

if __name__=='__main__':
    fileFilter = ['compile']
    compileall.compile_dir('.')
    for file in os.listdir(os.getcwd() + "/__pycache__"):
        # (fileName, fileType) = os.path.splitext(file)
        fileName = file[0 : file.find('.')]
        if fileName not in fileFilter:
            shutil.copyfile("./__pycache__/" + file,
                "../release/data_service/" + fileName + ".pyc")
