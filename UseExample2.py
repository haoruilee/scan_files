"""
合并所有/处理文件 下的excel表格
"""

import xlrd
import xlwt
from xlutils.copy import copy
import os 
import sys
import time
def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")
 
 
def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i+rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")
 
 
def read_excel_xls(path):
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    for i in range(0, worksheet.nrows):
        for j in range(0, worksheet.ncols):
            print(worksheet.cell_value(i, j), "\t", end="")  # 逐行逐列读取数据
        print()

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

if __name__ == '__main__':
    sys.stdout = open('处理文件记录.log', 'a',encoding='utf-8')
    #读取当前目录下的"处理文件
    temp = os.path.abspath('./处理文件')
    all_files = scan_files(temp)
    all_files.sort()
    datalist = []
    value_title = []
    step = 0
    for files in all_files:
        temp_data = xlrd.open_workbook(files)
        temp_table = temp_data.sheets()[0]#获取第一个sheet
        rowData = temp_table.row_values(0)
        value_title.append(rowData)
        if step == 0:
            print("第{}步，生成合并表格".format(step))
            book_name_xls = '2021623合并表格.xls'    
            sheet_name_xls = 'sheet1'
            write_excel_xls(book_name_xls, sheet_name_xls, value_title)
        for i in range(1,temp_table.nrows):
            temp_writewhat = []
            temp_writewhat.append(temp_table.row_values(i))
            write_excel_xls_append(book_name_xls, temp_writewhat)
            print("写入了表{}的第{}行".format(files,i))
            temp_writewhat.pop()
        print("表{}写入完成！该表含表头共计{}行".format(files,temp_table.nrows))
        time.sleep(3)
        step += 1
        
"""
    # 通过文件名获得工作表,获取工作表1
    table0 = data0.sheet_by_name('sheet1')
    table1 = data1.sheet_by_name('sheet1')
    table2 = data2.sheet_by_name('sheet1')

    book_name_xls = 'xls20210622测试.xls'
    sheet_name_xls = 'xls格式测试表'
    value_title = [["id", "video name", "video class", "description"],]
    write_excel_xls(book_name_xls, sheet_name_xls, value_title)
"""




'''
for i in range(1,table0.nrows):
    print(table0.row_values(i))
    print(table1.row_values(i))
    print(table2.row_values(i))
    temp=[]
    temp.append(table0.row_values(i))
    write_excel_xls_append(book_name_xls, temp)
    temp.pop()
    temp.append(table1.row_values(i))
    write_excel_xls_append(book_name_xls, temp)
    temp.pop()
    temp.append(table2.row_values(i))
    write_excel_xls_append(book_name_xls, temp)
    temp.pop()
'''


'''
book_name_xls = 'xls格式测试工作簿.xls'
sheet_name_xls = 'xls格式测试表'
value_title = [["id", "video name", "video class", "description"],]
write_excel_xls(book_name_xls, sheet_name_xls, value_title)
temp=[]
temp.append(table0.row_values(1))
write_excel_xls_append(book_name_xls, temp)
temp.pop()
print(temp)
'''
