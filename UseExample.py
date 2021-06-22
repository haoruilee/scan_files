"""
author：李浩瑞 61518407

项目内容：

1、读取项目文件夹下所有同学的.py文件
2、将读取到的文件写入txt中
3、将文本中的中文剔除，英文字符串保存
4、用英文文件生成词云，词出现的频率越高，则显示越大
5、展示频率前十的词汇柱状图

"""

import collections
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import pandas


"""
全局变量
"""

#词频统计
counts = {}
# 读取上级目录的路径
temp = os.path.abspath(r"..")
print(temp)
#字体文件路径
font_path="simfang.ttf"

def is_chinese_or_symbol (c):

    """
    判断是否是中文或者符号或者数字
    如果是，返回True
    """
    x = ord (c)
    #使用Unicode编码
    #判断是否是中文字符编码
    if (x >= 0x2e80 and x <= 0x33ff) or (x>= 0xff00 and x <= 0xffef) or(x>= 0x4e00 and x <= 0x9fbb) or( x >= 0xf900 and x <= 0xfad9)  or(x >= 0x20000 and x <= 0x2a6d6) or(x >= 0x2f800 and x <= 0x2fa1d):
        return 1
    #判断是否是标点符号
    elif (x>=33 and x<=64) or (x>=91 and x<=96) or (x>=123 and x<=126):
        return 2
    #False表示英文字符
    else:
        return 0



def returnen(zh_en_str):
    """
    区分中英文和数字、并只返回英文字符串
    """
    en_group = ""
    for c in zh_en_str:
        flag=is_chinese_or_symbol(c)
        if (flag==0):#非中文或字符直接写入
            en_group=en_group+c
        elif (flag==2):
            en_group=en_group+" "#将符号替换成空格
    return en_group#将纯英文返回



def scan_files(directory, prefix=None, postfix=None):
    """
    参数directory表示目录名，prefix和postfix是目录的前后缀，默认是没有的
    该函数可以循环扫描directory目录及其子目录下所有的文件，以列表形式返回
    """
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))
    return files_list#返回目录和子目录下所有文件


def write_into_allpy():
    # 将所有.py文件写入allpy.txt中
    f = open("allpy.txt", "w", encoding='utf-8')
    all_files = scan_files(temp)
    for i in all_files:
        if os.path.splitext(i)[1] == ".py":   # 筛选py文件，
            print(i)                            # 输出所有的py文件
            f.write(open(i, encoding='utf-8-sig', errors='ignore').read() + "\n")
    f.close()
    
def conv_into_only_english():
    
    """
    将文件改写成纯英文文件
    保存新文件到onlyenglish.txt中
    """
    
    f = open("allpy.txt", "r", encoding='utf-8').read()
    save_file_path = 'onlyenglish.txt'
    savefile=open(save_file_path,"w",encoding='utf-8')#均使用utf-8编码
    for i in f:
        englishline=returnen(i)#调用返回纯英文的函数
        savefile.write(englishline)
    savefile.close()
    
def show_wordcloud():
    """
    本函数保留生成英文词云的代码，未使用jieba分词，加快运算速度
    如果有中文，则调用结巴分词，生成字符串

    中文词云代码如下
    import jieba #引用jieba分词，对中文的分词效果更好

    Python join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串
    cut_text =" ".join(jieba.cut(f))
    wordcloud = WordCloud(font_path="C:/Windows/Fonts/simfang.ttf",background_color="white",mask=background_image,collocations=False).generate(cut_text)
    """

    photo_coloring =plt.imread('xuanwuhu.JPG')
    #fontpath寻找到字体文件，collocations生成无重复的词云
    wordcloud = WordCloud(font_path,background_color="white",mask=photo_coloring,max_font_size=200,collocations=False).generate_from_frequencies(counts)
    # 显示图片
    #plt.imshow(wordcloud.recolor(color_func=photo_coloring), interpolation="bilinear")
    #进行词频统计时，使用染色会报错，因此采用下文的未染色方法
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("wc.jpg")
    plt.show()

    
def sort_word():    

    """
    词频统计
    输出前十名的柱状图
    """

    path_txt='onlyenglish.txt'
    f = open(path_txt,'r', encoding='utf-8').read()#不需要close
    txtArr = f.split()
    #遍历文件，记录每个词的出现次数
    for word in txtArr:
        counts[word] = counts.get(word, 0) + 1
    
    #转换格式，方便打印，将字典转换为列表
    countsList = list(counts.items())
    countsList.sort(key=lambda x:x[1], reverse=True)#按次数从大到小排序
    
    #打印词频统计
    name_list_top10=[]
    num_list_top10=[]
    for i in range(10):
        word, count = countsList[i]
        print('{0:<10}{1:>5}'.format(word,count))
        name_list_top10.append(word)
        num_list_top10.append(count)
    plt.bar(range(len(num_list_top10)), num_list_top10, color='lightsteelblue', tick_label=name_list_top10)
    plt.xticks(rotation=45)#倾斜45度防止错位
    plt.savefig("bar.jpg")
    plt.show()

#main函数
if __name__=="__main__":
    write_into_allpy()
    #读取所有.py文件创建初始文档
    conv_into_only_english()
    #将文档改写为纯英文文档
    sort_word()
    #词频统计
    show_wordcloud()
    #绘制词云
