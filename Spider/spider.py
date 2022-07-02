import re
import requests
from bs4 import BeautifulSoup
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
def get_link(url):
    res = requests.get(url=url,headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.content, 'html.parser')
    new=soup.find_all('span')
    new=str(new)
    pattern='<span><a href="(.*?)" target="_blank">(.*?)</a>(.*?)</span>'
    link=re.findall(pattern,new)
    return link



def get_intent(name,title,links):
    f = open(name, 'a', encoding='utf-8')
    f.write(title+'\n')
    col = '诗名'+','+'作者'+','+'朝代'+','+'古诗'+','+'译文'
    f.write(col + '\n')
    count=1
    for link in links:
        url='https://so.gushiwen.cn'+str(link[0])
        #url=str(link[0])
        print(count)
        count+=1
        print(url)

        s = requests.session()
        res = s.get(url, headers=headers, verify=False)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.content, 'html.parser')
        new=soup.find_all('div',class_='contson')
        #print(new[0])
        #处理古诗词
        new=str(new[0])
        new=new.replace('\n','')
        new=new.replace('<br/>','')
        new = new.replace('<p>', '')
        new = new.replace('</p>', '')
        #print(new)
        pattern = '<div class="contson" id="(.*?)">(.*?)</div>'
        poem=re.findall(pattern,new)
        for i in poem:
            poem=i[1]
        #print(poem)
        #处理作者和朝代
        title=soup.find_all('p',class_='source')
        pattern = '<div class="contson" id="(.*?)">(.*?)</div>'
        title=str(title[0])
        title= title.replace('\n', '')
        #print(title)
        pattern='<p class="source"><a href="(.*?)">(.*?)</a> <a href="(.*?)">〔(.*?)〕</a></p>'
        title=re.findall(pattern,title)
        for i in title:
           poet=i[1]
           dynasty=i[3]
        #获得译文
        new = soup.find_all('div', class_='contyishang')
        soup = BeautifulSoup(str(new), 'html.parser')
        new = soup.find_all('p')
        if len(new)==0:
            yiwen='无'
        else:
            yiwen=str(new[0])
        yiwen=yiwen.replace('<br/>','')
        yiwen = yiwen.replace('</a>', '')
        yiwen = yiwen.replace('<strong>韵译</strong>', '')
        #处理译文
        #print(yiwen)
        pattern='<p><strong>译文</strong>(.*?)</p>'
        yi=re.findall(pattern,yiwen)
        if len(yi)==0:
            pattern = '<p>译文(.*?)</p>'
            yi = re.findall(pattern, yiwen)
            if len(yi)==0:
                pattern='<p>(.*?)</p>'
                yi = re.findall(pattern, yiwen)
        #print(yi)
        if len(yi)==0:
            yi='无'
        else:
            yi=str(yi[0])
        #print(yi)
        f = open(name, 'a', encoding='utf-8')
        poem = poem.strip()
        yi = yi.strip()
        f.write(link[1]+'/'+poet+'/'+dynasty+'/'+poem+'/'+yi+'\n')
    f.close()
#url='https://so.gushiwen.cn/gushi/dushu.aspx'
name = "poems.txt"
#唐诗三百首
#url="https://so.gushiwen.cn/gushi/tangshi.aspx"
#古诗三百首
url='https://so.gushiwen.cn/gushi/sanbai.aspx'
#宋词三百首
#url='https://so.gushiwen.cn/gushi/songsan.aspx'
#初中古诗
#url='https://so.gushiwen.cn/gushi/chuzhong.aspx'
#高中古诗
#url='https://so.gushiwen.cn/gushi/gaozhong.aspx'
#小学文言文
#url='https://so.gushiwen.cn/wenyan/xiaowen.aspx'
#初中文言文
#url='https://so.gushiwen.cn/wenyan/chuwen.aspx'
#高中文言文
url='https://so.gushiwen.cn/wenyan/gaowen.aspx'
#写景
#url='https://so.gushiwen.cn/gushi/xiejing.aspx'
link=get_link(url)
print(len(link))
get_intent(name,url,link)


