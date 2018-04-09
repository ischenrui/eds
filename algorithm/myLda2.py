
import jieba
import jieba.posseg as pseg
import gensim
import json
from gensim import corpora
import time
from algorithm.base import dbs

def strToMap(s):
    dic={}
    list=s.split(' + ')
    for l in list:
        v=l.split('*')
        key=v[1][1:-1]
        dic[key]=float(v[0])

    return dic

sql = 'select id,name,abstract,keyword from paper'
institution_paper_list = dbs.getTuples(sql)
stopwords = [line.strip() for line in open('stopwords.txt',encoding='utf-8').readlines()]
fill = ['v', 'vd', 'vn', 'vf ', 'vx ', 'vi', 'vl', 'vg', 'n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf',
                'nt', 'nz', 'nl', 'ng']
print('词典更新')
jieba.load_userdict('userdict.txt')
print('分词')
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
DocWord = []
for paper in institution_paper_list:
    line = paper[1].strip('\n').strip('\t') + ' ' + paper[2].strip('\n').strip('\t') + ' ' + paper[3].strip('\n').strip(
        '\t')
    seg_list = pseg.cut(line)
    words = []
    for word, flag in seg_list:
        if flag in fill and word not in stopwords:
            words.append(word)
    DocWord.append(words)

print('生成文本向量')

dictionary = corpora.Dictionary(DocWord)
dictionary.filter_extremes(no_below=8,no_above=16)
corpus = [dictionary.doc2bow(text) for text in DocWord]
time1 = time.time()
print('已生成训练集文本向量。正在进行模型训练......')
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
num_topics =600
num_words = 50
print('本院系文章总数为%d，即将分为主题数%d个，关键字%d个......' % (len(corpus), num_topics, num_words))
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=50)
result = ldamodel.print_topics(num_topics=num_topics, num_words=num_words)
time2 = time.time()
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print('模型训练用时：', time2 - time1)
print('LDA模型训练完成。插入数据库......')

doc_lda = ldamodel[corpus]
for n in range(len(doc_lda)):
    Topic = doc_lda[n]
    wordTopic = [i[1] for i in result if int(Topic[0][0]) == i[0]]
    d = strToMap(wordTopic[0])

    t = {}
    for key in DocWord[n]:
        if key in d.keys():
            t[key] = d[key]
    topic = Topic[0][0]
    prams = (institution_paper_list[n][0], "topic" + str(topic), json.dumps(d, ensure_ascii=False),
             json.dumps(t, ensure_ascii=False))
    sql = 'insert into lda2 values(%s,%s,%s,%s)'
    list = dbs.exe_sql(sql, prams)
print("结束")
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))