#!C:\Users\17198\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding:utf-8 -*-


import os

def extract_events_id(fpath):
    events_id = []
    all_file_list = os.listdir(fpath)
    for f in all_file_list:
        file_path = os.path.join(fpath, f)
        if os.path.isdir(file_path):
            if "S" in f:
                events_id.append(f)
    return events_id
        

def write_floods(fpath, events_id):
    fname = "floods.txt"
    with open(fpath+"\\"+fname, "w") as out:
        for ID in events_id:
            out.write(ID + "\n")

if __name__ == "__main__":
    fpath = r".\\"
    events_id = extract_events_id(fpath)
    write_floods(fpath, events_id)                        
