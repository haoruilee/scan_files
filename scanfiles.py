import os

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

#读取当前目录的上级目录
temp = os.path.abspath('..')

#应用示例
all_files = scan_files(temp)
for i in all_files:
    print(i)
