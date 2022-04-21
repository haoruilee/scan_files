import enum
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import os
import time
import heapq
import pickle

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

def get_TopvarIndex(topnum):
    """
    该函数可以获取文件中topnum个方差最大的索引
    """
    # 读取当前目录
    temp = os.path.abspath('.')
    all_files = scan_files(temp,None,".xlsx")
    all_files.sort()
    All_B = [[0 for ik in range(26)] for jk in range(8192)]
    for File_Index,filename in enumerate(all_files):
        print("READING",filename)
        file = pd.read_excel(filename)
        for i,b in enumerate(file['B']):
            All_B[i][File_Index] = b
    res=[]
    for i,Blist in enumerate(All_B):
        res.append(np.var(Blist))
    top20 = map(res.index, heapq.nlargest(20, res)) #求最大的20个索引
    return top20

if __name__ == '__main__':
    # 预定义
    Store_Data = [[0 for ik in range(5)] for jk in range(20*26) ]
    # 选用的索引
    key_index = [755,2925,2911,2898,2890,2884,6920, 6640, 6918, 6919, 6917, 7351, 6916, 6617, 7352, 6921, 6641, 7854, 6639, 7593]
    # 读取当前目录
    temp = os.path.abspath('.')
    all_files = scan_files(temp,None,".xlsx")
    all_files.sort()
    Store_Data_ind = 0
    for File_Index,filename in enumerate(all_files):
        # 循环26次
        print("READING",filename)
        file = pd.read_excel(filename)
        for kindex in key_index:
            # 循环20次
            for inde, fileKey in enumerate("ABNTY"):
                # 插入5次，换行
                Store_Data[Store_Data_ind][inde] = file[fileKey][kindex]
            Store_Data_ind += 1
    # 保存数据
    f = open('./Final.pkl', 'wb')
    pickle.dump(Store_Data, f)
    f.close()
