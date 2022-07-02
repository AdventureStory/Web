import json
import re
txt_path = "/Users/qi/Downloads/workspace/vscode/python/python_zhihu-master/唐诗.txt"

def read_txt(txt_path):
    poem_list = []
    content = []

    with open(txt_path, 'r') as f:
        flag = 0
        for line in f.readlines():
            
            flag += 1
            if flag > 2:
                poem_dict = {}
                item_list = line.strip('\n').split('/')             
                title, poet, dynasty, poem, trans = item_list[0],item_list[1],item_list[2],item_list[3], item_list[4]
                poem_dict['title'] = title
                poem_dict['poet'] = poet
                poem_dict['dynasty'] = dynasty
                poem_dict['poem'] = poem
                poem_dict['trans'] = trans

                str=re.sub('[^\u4e00-\u9fa5]+','',poem)
                content.append(str)
                
                poem_list.append(poem_dict)
    return  content, poem_list

def readJson(path):

    content=[]
    raw_content = []
    # 数据路径
    f = open(path, "r",encoding='utf8')
    row_data = json.load(f)

    # 读取每一条json数据
    for d in row_data:
        t = d['id'],d['content']
        str=re.sub('[^\u4e00-\u9fa5]+','',d['content'])
        content.append(str)
        raw_content.append(d['content'])

    #print(content)
    return content, raw_content