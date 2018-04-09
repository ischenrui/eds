import pickle

import jieba
import jieba.posseg as pseg
import gensim
import time,os
from algorithm.base import dbs

def strToMap(s):
    dic={}
    list=s.split(' + ')
    for l in list:
        v=l.split('*')
        key=v[1][1:-1]
        dic[key]=float(v[0])

    return dic

def keywords_save():
    # 把所有keyword写入文件
    keywords = open('keywords.txt', encoding='utf-8', mode='w')

    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    for i in range(0, 90000000, 1000000):
        print(i)
        sql = 'select keyword from paper_citeorref limit ' + str(i) + ',1000000'
        paper_list = dbs.getDics(sql)
        if len(paper_list) == 0:
            break
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        for paper in paper_list:
            if (paper['keyword']):
                keywords.write(paper['keyword'] + '\n')
    keywords.close()
def judge_pure_english(keyword):
    return all(ord(c) < 128 for c in keyword)
def userdict_extract():
    """
    抽取关键字作为用户字典
    :return: 存储在 userdict.txt里面
    """
    # print('查询数据')
    #
    # keywords_save()
    print('生成词典')

    # 把keyword读出来, 并且统计词频写入userdict.txt里面
    wordDict = {}
    keywordsLst = []
    keywords = open('keywords.txt', encoding='utf-8', mode='r').readlines()
    userdict = open('userdict.txt', encoding='utf-8', mode='w')
    for k in keywords:
        keywordsLst.extend(k.strip('\n').split(','))
    # 统计词频放入词典
    for word in keywordsLst:
        if judge_pure_english(word):
            continue
        if (word in wordDict):
            wordDict[word] += 1
        else:
            wordDict[word] = 1
    # 把词典写入文件
    for word in wordDict:
        if wordDict[word] >= 3:
            userdict.write(word + ' ' + str(wordDict[word]) + ' n' + '\n')

# userdict_extract()
stopwords = [line.strip() for line in open('stopwords.txt',encoding='utf-8').readlines()]
fill = [ 'vn', 'n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf',
                'nt', 'nz', 'nl', 'ng']
print('词典更新')
jieba.load_userdict('userdict.txt')
for i in range(0,10000000,500000):
    sql = 'select id,name,abstract,keyword from paper_citeorref limit '+str(i)+',500000'
    paper_list = dbs.getDics(sql)
    if len(paper_list)==0:
        break
    print('分词')
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    DocWord = []
    for paper in paper_list:
        line = paper['name'].strip('\n').strip('\t') + ' ' + paper['abstract'].strip('\n').strip('\t') + ' ' + paper["keyword"].strip('\n').strip(
            '\t')
        if judge_pure_english(line):
            continue
        seg_list = pseg.cut(line)
        words = []
        for word, flag in seg_list:
            if flag in fill and word not in stopwords:
                words.append(word)
        DocWord.append(words)
    print('保存分词')
    pickle.dump(DocWord, open('data/fenci'+str(i)+'.txt', 'wb'))

# class MySentences(object):
#     def __init__(self, path):
#         self.time=0
#         self.path= path
#
#     def __iter__(self):
#         self.time+=1
#         pathDir = os.listdir(self.path)
#         for file in  pathDir:
#             print("open "+file+" "+str(self.time)+'time')
#             sentence = pickle.load(open("data/"+file, 'rb'))
#             for line in sentence:
#                 yield  line
# print('开始训练')
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
# sen = MySentences('data')
# model = gensim.models.Word2Vec(sen,size=180,window=10,iter=12,min_count=5)
# print('保持模型')
# model.save("data2/word2vec.txt")
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
# model = gensim.models.Word2Vec.load("data2/word2vec.txt")
# word_vectors = model.wv
# print(word_vectors.most_similar(positive=['宗教','教育部']))