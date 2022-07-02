from django.shortcuts import render
from django.http import HttpResponse
from requests import request
import jieba
from poetry.utils import *
from poetry.tf_idf import TfIdf
txt_path = "/Users/qi/Downloads/workspace/vscode/python/python_zhihu-master/唐诗.txt"
json_path = "/Users/qi/Downloads/workspace/vscode/python/PoetryInfoSystem/poetry/CollectedPoetries/poetry.json"
# Create your views here.
def Hello(request):
    return HttpResponse("Hello Woeld!")

def reg(request):
    _, poem_list, list_word_cut = initSearch()
    
    if request.method == 'POST':
        mykey=request.POST.get('mykey')
        query_word_cut = queryProcess(mykey)
        similarit_list = getSimilarity(list_word_cut, query_word_cut)
        result, similarity,result_poem_list = display(similarit_list,poem_list)
        
        
        return render(request,'home.html',{'result':result, 'similarity':similarity, 'poem_list':result_poem_list})
    else:
        
        return render(request,'index.html')

def queryProcess(mykey):
    query_word_cut = jieba.lcut_for_search(mykey)
    return query_word_cut

def initSearch():
    content, poem_list = read_txt(txt_path)
    list_word_cut = word_cut(content)
    return content, poem_list, list_word_cut
    #similarit_list = getSimilarity(list_word_cut)

def word_cut(list):
    list_word_cut = []
    for line in list:
        single_line_word_cut = jieba.lcut_for_search(line)
        list_word_cut.append(single_line_word_cut)
    
    return list_word_cut


def getSimilarity(list_word_cut, query_word_cut):
    table = TfIdf()
    for idx, single_line_word_cut in enumerate(list_word_cut):
        table.add_document(idx, single_line_word_cut)
    similarit_list = table.similarities(query_word_cut)
    similarit_list.sort(key=lambda x:x[1], reverse=True)
    return similarit_list

def display(similarit_list,poem_list):
    result = []
    similarity = []
    result_poem_list = []
    cnt = 0;
    for item in similarit_list:
        result_dict = {}
        if cnt > 4:
            break;
        cnt +=1
        result.append(poem_list[item[0]]['poem'])
        similarity.append(round(item[1],2))
        result_dict['title'] = poem_list[item[0]]['title']
        result_dict['poet'] = poem_list[item[0]]['poet']
        result_dict['dynasty'] = poem_list[item[0]]['dynasty']
        result_dict['poem'] = poem_list[item[0]]['poem']
        result_dict['trans'] = poem_list[item[0]]['trans']
        
        result_poem_list.append(result_dict)

    poetry = "独在异乡为异客，每逢佳节倍思亲。遥知兄弟登高处，遍插茱萸少一人。"
    strip_chars = '。，“”'

    single_line = poetry
    single_line = single_line.translate(str.maketrans(dict.fromkeys(strip_chars, '#')))

    single_line = single_line.split('#')
        
    for i, item in enumerate(result):
        item = item.translate(str.maketrans(dict.fromkeys(strip_chars, '#')))
        result[i] = item.split('#')
        
    
    return result, similarity, result_poem_list
