from IPython.display import Markdown, display
from IPython.display import clear_output
import json
import copy
import time
import numpy as np
import os,sys

import matplotlib.pyplot as plt

def plot_progress(progress_file = r'C:\Users\bonul\Downloads\translate_json\test\progress.npy'):
    Ntasks_file = progress_file.replace('progress.npy','Ntasks_file.npy')
    Ntasks = np.load(Ntasks_file)
    done_tsks = np.load(progress_file)[1]
    labels = 'Done', '//TODO'
    sizes = [done_tsks, Ntasks-done_tsks]
    explode = (0.1, 0)
    fig1, ax1 = plt.subplots()
    aux=ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    aux=ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

def printmd(mystr):
    display(Markdown(mystr))
    
def getFromDict(dataDict, mapList):    
    for k in mapList: dataDict = dataDict[k]
    return dataDict

def setInDict(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value
    
def edit_element(toedit_filename,keys_list,new_v):
    '''
    Nested dics edition
    https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys/14692747#14692747
    '''
    # funcs to access nested dics...
    '''
    def getFromDict(dataDict, mapList):
        return reduce(operator.getitem, mapList, dataDict)
    def setInDict(dataDict, mapList, value):
        getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value
    '''
    #
    # read the file to edit
    with open(toedit_filename, 'rb') as f:
        new_d = json.load(f)
    #
    # reach and edit the element
    setInDict(new_d, keys_list, new_v)
    #
    # save to disk
    with open(toedit_filename, 'w+',encoding='utf-8') as f:
        json.dump(new_d, f,ensure_ascii=False)

def edition_by_user(v1,v2,progress_file):
    time.sleep(0.001)
    printmd('# '+v1)
    time.sleep(0.001)
    printmd('# '+v2)
    time.sleep(0.001)
    new_v = input('')
    if new_v == '':
        new_v = v2
    time.sleep(0.001)
    plot_progress()
    time.sleep(0.001)
    clear_output()
    if new_v=='STOP':
        np.save( progress_file , [0,np.load(progress_file)[1]] )
        print('Saving progress and exiting...')
        time.sleep(3)
        print('exited')
        exit
    return new_v

def recursive_dics(d1, d2,toedit_filename,keys_list):
    same_lvl_count=-1
    for k1 in d1:
        if k1 in d2:
            same_lvl_count = same_lvl_count + 1
            if same_lvl_count==0:
                keys_list.append(k1)
            else:
                keys_list[-1] = k1
            #
            if type(d1[k1]) is not dict:
                #
                progress_file = os.path.join( os.path.dirname(toedit_filename) , 'progress.npy' )
                curr,target = np.load(progress_file)
                if curr<target:
                    Skiper = True
                    np.save( progress_file , np.load(progress_file)+np.asarray([1,0]) )
                else:
                    Skiper = False
                if not Skiper:
                    np.save( progress_file , np.load(progress_file)+np.asarray([1,1]) )
                    new_v = edition_by_user(d1[k1],d2[k1],progress_file)
                    edit_element(toedit_filename,keys_list,new_v)
            else:
                recursive_dics(d1[k1], d2[k1],toedit_filename,keys_list)

d1_str = r'C:\Users\bonul\Downloads\translate_json\test\locale-en(1).json'
d2_str = r'C:\Users\bonul\Downloads\translate_json\test\locale-zh-CN.json'

progress_file = os.path.join( os.path.dirname(d2_str) , 'progress.npy' )
if not os.path.exists(progress_file):
    np.save( progress_file , [0,0] )

with open(d1_str, 'rb') as f:
    d1 = json.load(f)
with open(d2_str, 'rb') as f:
    d2 = json.load(f)
Skiper = True
recursive_dics(d1, d2,d2_str,[])

aux = """

filename=r...
output_filename = filename.replace('.json','_out.json')
with open(filename, 'rb') as f:
    mydict = json.load(f)

new_d=copy.copy(mydict)
def my_looper(d):
    for k, v in d.items():
        if isinstance(v, dict):
            my_looper(v)
        else:
            time.sleep(0.01)
            printmd('# '+k)
            time.sleep(0.01)
            printmd('# '+v)
            time.sleep(0.01)
            new_v = input('')
            time.sleep(0.01)
            if new_v!='':
                new_d[k] = new_v
            clear_output()
#
my_looper(mydict)
#
with open(output_filename, 'w',encoding='utf-8') as fp:
    json.dump(new_d, fp,ensure_ascii=False)
    
"""