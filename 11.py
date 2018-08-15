import lxml
import requests  # 导入网页请求库
from bs4 import BeautifulSoup  # 导入网页解析库
import pprint  # 使打印出来的列表更方便看
import json  # 用于将列表字典（json格式）转化为相同形式字符串，以便存入文件
import pandas as pd


# 发起请求
def start_requests(url):
    print(url)  # 用这条命令知道当前在抓取哪个链接，如果发生错误便于调试
    r = requests.get(url)
    return r.content


def parse(text):
    soup = BeautifulSoup(text, 'lxml')
    movie_list = soup.find_all('div', class_='subDoctor_state_info')
    for movie in movie_list:
        mydict = {}
        mydict['name'] = movie.find('h3').text
        mydict['zhiwei'] = movie.find('i').text
        email = movie.find_all('p')[2].text
        mydict['email'] = email if email else None  # 抓取10页就总会遇到这种特殊情况要处理
        xi = movie.find('div', class_='right')
        mydict['xi'] = xi.find_all('i')[-1].text
        result_list.append(mydict)  # 向全局变量result_list中加入元素
    nextpage = soup.find('a', class_='next')  # 找到“下一页”位置
    if nextpage:  # 找到的就再解析，没找到说明是最后一页，递归函数parse就运行结束
        nexturl = baseurl + nextpage['href']
        text = start_requests(nexturl)
        if nextpage['href'] != 'index4.htm':  # 多次使用这个函数，可以看出定义函数的好处，当请求更复杂的时候好处更明显
            parse(text)
        else:
            soup = BeautifulSoup(text, 'lxml')
            movie_list = soup.find_all('div', class_='subDoctor_state_info')
            for movie in movie_list:
                mydict = {}
                if movie.find('h3').text != '姚方':
                    mydict['name'] = movie.find('h3').text
                    mydict['zhiwei'] = movie.find('i').text if movie.find('i').text else None
                    email = movie.find_all('p')[2].text
                    mydict['email'] = email if email else None  # 抓取10页就总会遇到这种特殊情况要处理
                    xi = movie.find('div', class_='right')
                    xi1 = xi.find_all('i')[-1].text
                    mydict['xi'] = xi1 if xi1 else None
                    result_list.append(mydict)  # 向全局变量result_list中加入元素


def write_json(result):
    s = json.dumps(result, indent=4, ensure_ascii=False)
    with open('movies.json', 'w', encoding='utf-8') as f:
        f.write(s)


def main():
    text = start_requests(baseurl)
    parse(text)
    write_json(result_list)  # 所有电影都存进去之后一起输出到文件


if __name__ == '__main__':
    baseurl = 'http://www.math.pku.edu.cn/jsdw/js_20180628175159671361/'
    result_list = []
    main()