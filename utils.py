from IPython.display import Markdown, display
from IPython.display import clear_output
import json
import copy
import time

def printmd(mystr):
    display(Markdown(mystr))
    
d1_str = r'C:\Users\bonul\Downloads\translate_json\test\locale-en(1).json'
d2_str = r'C:\Users\bonul\Downloads\translate_json\test\locale-zh-CN.json'
output_filename = d2_str.replace('.json','_out.json')
with open(d1_str, 'rb') as f:
    d1 = json.load(f)
with open(d2_str, 'rb') as f:
    d2 = json.load(f)
#input('Paste the content from the reference file')
#input('Paste the content from the auto-translated file to correct').encode('utf-8')
#d1 = json.loads(d1_str.encode('utf-8'))
#d2 = json.loads(d2_str)

# Play with the common keys only
d1_new = {key:d1[key] for key in d1 if key in d2}
d2_new = {key:d2[key] for key in d1 if key in d2}

new_d=copy.copy(d2)
with open(output_filename, 'w',encoding='utf-8') as f:
    json.dump(new_d, f,ensure_ascii=False)

def my_looper(d1,d2):
    for [k1,v1],[k2,v2] in zip(d1.items(),d2.items()):
        if isinstance(v1, dict):
            my_looper(v1,v2)
        else:
            time.sleep(0.001)
            printmd('# '+v1)
            time.sleep(0.001)
            printmd('# '+v2)
            time.sleep(0.001)
            new_v = input('')
            time.sleep(0.001)
            if new_v!='':
                #new_d[k2] = new_v
                with open(output_filename, 'rb') as f:
                    new_d = json.load(f)
                new_d[k2]=new_v
                with open(output_filename, 'w',encoding='utf-8') as f:
                    json.dump(new_d, f,ensure_ascii=False)
            clear_output()
#
my_looper(d1_new,d2_new)

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