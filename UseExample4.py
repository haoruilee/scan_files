from asyncio.windows_events import NULL
import os
import re
import imageio
import numpy as np
from matplotlib.image import imread
import scipy.misc
import cv2

def scan_files(directory,prefix=None,postfix=None):
    """
    参数directory表示目录名，prefix和postfix是目录的前后缀，默认是没有的
    该函数可以循环扫描directory目录及其子目录下所有的文件，以列表形式返回
    """
    files_list=[]
    
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root,special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root,special_file))
            else:
                files_list.append(os.path.join(root,special_file))
               
    return files_list

def mkdir(path):
    """
    在当前目录下生成一个文件夹
    自动跳过已有的
    """
    makePath = "./" + path
    folder = os.path.exists(makePath)
    if not folder:
        os.makedirs(path)
        print("*******New folder: {} *******".format(path))
    else:
        print("*******There is {} folder, skip*******".format(path))
    

def toGrayImage(filePath, floderName):
    """
    把filePath的txt文件转存为floderName文件夹
    下面的灰色图像
    """
    matrix = np.loadtxt(filePath)
    imgName = filePath.split('\\',-1)[-1]
    scipy.misc.imsave("./{}/{}.jpg".format(floderName,imgName), matrix)#使用scipy 1.0.0，更高版本请使用imageio.imwrite代替
    
def toRGBImage(filePath, floderName):
    """
    把filePath的灰色图像
    转存为floderName下的彩色图像
    """
    grayFile = cv2.imread(filePath)
    singleChannel = cv2.cvtColor(grayFile, cv2.COLOR_BGR2GRAY)
    rgbFile = cv2.applyColorMap(singleChannel, cv2.COLORMAP_JET)#COLORMAP_TURBO, COLORMAP_HSV, COLORMAP_JET, COLORMAP_RAINBOW 都还可以
    imgName = filePath.split('\\',-1)[-1]
    scipy.misc.imsave("./{}/{}.jpg".format(floderName,imgName), rgbFile)#使用scipy 1.0.0，更高版本请使用imageio.imwrite代替

def files2Gif(filePaths, gifName, gifFps=5):
    """
    将filePath下一系列文件转为./gifRes/gifName.gif
    """
    ls = []
    for file in filePaths:
        fileMatrix = imread(file)
        ls.append(fileMatrix)
    #原数据为float64，注意转换为unit8的时候有可能丢失精度
    mkdir("gifRes")
    imageio.mimwrite("./{}/{}.gif".format("gifRes",gifName), np.array(ls), format='GIF', fps=gifFps)
    
def toGrayFiles(filePaths, floderName):
    mkdir(floderName)
    for file in filePaths:
        toGrayImage(file,floderName)
        
def toRGBFiles(filePaths, floderName):
    mkdir(floderName)
    for file in filePaths:
        toRGBImage(file,floderName)

if __name__ == "__main__":
    alphaImagePath = './FILEPATH/'
    gifResName = "GIFNAME"
    
    temp = os.path.abspath(alphaImagePath)
    all_files = scan_files(temp,'phi','0')   
    
    toGrayFiles(all_files,"grayRes")
    temp = os.path.abspath('./grayRes/')
    gray_files = scan_files(temp,'phi','jpg')
    
    toRGBFiles(gray_files,"rgbRes")
    temp = os.path.abspath('./rgbRes/')
    
    rgb_files = scan_files(temp,'phi','jpg')
    fns = lambda s: [(s,int(n))for s,n in re.findall('(\D+)(\d+)','a%s0'%s)]
    rgb_files = (sorted(rgb_files, key=fns))

    files2Gif(rgb_files,gifResName,5)
