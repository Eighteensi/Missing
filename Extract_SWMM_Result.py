import pandas as pd
from swmmtoolbox import swmmtoolbox as SW

swmm_out_filename = "RR_HD_WQ.out"
csv_filename = "RR_HD_WQ.csv"

f = SW.SwmmExtract(swmm_out_filename)
type_mydic = dict(zip(range(len(f.itemlist)),f.itemlist))
for num,item in type_mydic():
    print(num,item)
print("请输入模型对象序号")
type_number = int(input())
if len(f.name[type_number])==0:
    print("结果中不存在%s对象，请重新输入模型对象序号："%(type_mydic[type_number]))
    print("-"*20)
    type_number = int(input())
    print("-"* 20)
for key,val in f.varcode[type_number].items():
    print(key,val)
print("请输入结果类型序号：")
item_number = int(input())
print("-"*20)

data = SW.extract(swmm_out_filename,str(type_mydic[type_number]+','+','+f.varcode[type_number]))
name_list = [data.replace(type_mydic[type_number],"").replace(f.varcode)[type_number]]

data.columns = name_list
frame = data[0:1].copy()
frame.index = [f.startdata]
data = pd.concat([frame,data])
data.to_csv(csv_filename.replace(".csv",str("_"+f.varcode[type_number][item_number])))

print("结果输出完成")