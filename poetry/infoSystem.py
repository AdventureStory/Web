# -*- coding: utf-8 -*-
import json
import jieba
from utils import *
from tf_idf import TfIdf
#去除特殊字符，只保留汉子，字母、数字
import re

json_file_path = 'InfoSystem/poetry.json'
def word_cut(list):
    list_word_cut = []
    for line in list:
        single_line_word_cut = jieba.lcut_for_search(line)
        list_word_cut.append(single_line_word_cut)
    
    return list_word_cut


def getSimilarity(list_word_cut):
    table = TfIdf()
    for idx, single_line_word_cut in enumerate(list_word_cut):
        table.add_document(idx, single_line_word_cut)
    query=['花','你']
    similarit_list = table.similarities(query)
    similarit_list.sort(key=lambda x:x[1])
    return similarit_list

def display(similarit_list,raw_content):
    for item in similarit_list:
        if item[1] > 0:
            print("Hello",raw_content[item[0]])

    
if __name__ == "__main__":
    content, raw_content = readJson(json_file_path)
    list_word_cut = word_cut(content)
    #print(list_word_cut)
    
    similarit_list = getSimilarity(list_word_cut)
    display(similarit_list, raw_content)

    
  



