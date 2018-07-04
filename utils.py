from IPython.display import Markdown, display
from IPython.display import clear_output
import json
import copy
import time

def printmd(mystr):
    display(Markdown(mystr))

filename=r'C:\Users\pau.galles\Downloads\jsonedit\jsefiles\locale-zh-CN.json'
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