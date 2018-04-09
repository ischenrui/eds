

import jieba
import jieba.posseg as pseg
import gensim
import json
from gensim import corpora
import time
from algorithm.base import dbs
stop=['研究','方法']
print('研究' in stop)
print('方法' in stop)
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
    keywordsLst=[]
    keywords = open('keywords.txt', encoding='utf-8', mode='r').readlines()
    userdict = open('userdict.txt', encoding='utf-8', mode='w')
    for k in keywords:
        keywordsLst.extend(k.strip('\n').split(','))
    # 统计词频放入词典
    for word in keywordsLst:
        if(word in wordDict):
            wordDict[word] += 1
        else:
            wordDict[word] = 1
    # 把词典写入文件
    for word in wordDict:
        if wordDict[word]>=3:
            userdict.write(word + ' ' + str(wordDict[word]) + ' n' + '\n')

# userdict_extract()
print('查询教师院系')
sql='select id,institution from teacher'
list=dbs.getTuples(sql)
institution_dict={}
for institution in list:
    if institution[1] not in institution_dict.keys():
        institution_dict[institution[1]]=[]
        institution_dict[institution[1]].append(institution[0])
    else :
        institution_dict[institution[1]].append(institution[0])

max=0
min=100
for v in institution_dict:
    l=len(institution_dict[v])
    if l>max:
        max=l
    if l<min:
        min=l
print('max:'+str(max)+';min:'+str(min))

stopwords = [line.strip() for line in open('stopwords.txt',encoding='utf-8').readlines()]
fill = ['vn', 'n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf',
                'nt', 'nz', 'nl', 'ng']
print('词典更新')
jieba.load_userdict('userdict.txt')
def strToMap(s):
    dic={}
    list=s.split(' + ')
    for l in list:
        v=l.split('*')
        key=v[1][1:-1]
        dic[key]=float(v[0])
    return dic
find=False

for institution in institution_dict:

    print('读取%s论文'%institution)
    ids=''
    for t in institution_dict[institution]:
        ids+=str(t)+','
    ids=ids[0:len(ids)-1]
    sql='select id,name,abstract,keyword from paper where author_id in ('+ids+')'
    institution_paper_list = dbs.getTuples(sql)

    print('分词')
    DocWord=[]
    for paper in institution_paper_list:
        line = paper[1].strip('\n').strip('\t')+' '+paper[2].strip('\n').strip('\t')+' '+paper[3].strip('\n').strip('\t')
        seg_list = pseg.cut(line)
        words=[]
        for word, flag in seg_list:

            if flag in fill and word not in stopwords:
                words.append(word)
        DocWord.append(words)

    print('生成文本向量')

    dictionary = corpora.Dictionary(DocWord)
    corpus = [dictionary.doc2bow(text) for text in DocWord]
    if len(corpus) == 0:
        continue
    time1 = time.time()
    print('已生成训练集文本向量。正在进行模型训练......')
    num_topics = 2 + int(len(corpus) / 250)
    if num_topics>=20:
        num_topics=10
    num_words=(num_topics-2)*2+10
    print('本院系文章总数为%d，即将分为主题数%d个，关键字%d个......' % (len(corpus),num_topics,num_words))
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=50)
    result = ldamodel.print_topics(num_topics=num_topics, num_words=num_words)
    time2 = time.time()
    print('模型训练用时：', time2 - time1)
    print('LDA模型训练完成。插入数据库......')

    doc_lda = ldamodel[corpus]
    for n in range(len(doc_lda)):
        Topic=doc_lda[n]
        top={}
        c1 = sorted(Topic, key=lambda x: x[1], reverse=True)

        wordTopic = [i[1] for i in result if int(c1[0][0]) == i[0]]
        d=strToMap(wordTopic[0])

        t={}
        for key in DocWord[n]:
            if key in d.keys():
                t[key]=d[key]
        topic=c1[0][0]
        prams=(institution_paper_list[n][0],institution+str(topic),json.dumps(d,ensure_ascii=False),json.dumps(t,ensure_ascii=False))
        sql='insert into lda values(%s,%s,%s,%s)'
        list = dbs.exe_sql(sql, prams)




