
import pymysql.cursors
import jieba
import jieba.posseg as pseg
import gensim
import json
from gensim import corpora
import time

def strToMap(s):
    dic={}
    list=s.split(' + ')
    for l in list:
        v=l.split('*')
        key=v[1][1:-1]
        dic[key]=float(v[0])

    return dic

# 连接数据库
class Mysql(object):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Cr648546845',
        db='projectdata',
        charset='utf8'
)
# 获取游标
    cursor = connect.cursor()

    # 查询专家编号
    def SltAbstract(self,sql):
        # sql = "SELECT a.id,a.abstract FROM paper a, test b WHERE a.author_id=b.id AND a.abstract!=''"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

if __name__ == '__main__':
    db = Mysql()

#---------查询摘要数据（以计算机为test）----------
    sql = "SELECT a.id,a.name,a.abstract,a.keyword FROM paper a, test b WHERE a.author_id=b.id AND a.abstract!='' LIMIT 10"
    institution_paper_list = db.SltAbstract(sql)

    stopwords = [line.strip() for line in open('data/stopwords.txt', encoding='utf-8').readlines()]
    fill = ['v', 'vd', 'vn', 'vf ', 'vx ', 'vi', 'vl', 'vg', 'n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf',
            'nt', 'nz', 'nl', 'ng']
    jieba.load_userdict('data/userdict.txt')

    print('分词ing...')
    DocWord = []
    for paper in institution_paper_list:
        line = paper[1].strip('\n').strip('\t') + ' ' + paper[2].strip('\n').strip('\t') + ' ' + paper[3].strip(
            '\n').strip('\t')
        seg_list = pseg.cut(line)
        words = []
        for word, flag in seg_list:
            if flag in fill and word not in stopwords:
                words.append(word)
        DocWord.append(words)
    # print(DocWord)

    dictionary = corpora.Dictionary(DocWord)
    corpus = [dictionary.doc2bow(text) for text in DocWord]

    time1 = time.time()
    print('已生成训练集文本向量。正在进行模型训练......')

    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=50, id2word=dictionary, passes=50)
    result = ldamodel.print_topics(num_topics=50, num_words=20)
    time2 = time.time()
    print('模型训练用时：', time2 - time1)

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
        # print(d)
        print(t)
        # prams = (institution_paper_list[n][0], institution + str(topic), json.dumps(d, ensure_ascii=False),
        #          json.dumps(t, ensure_ascii=False))
        # sql = 'insert into lda values(%s,%s,%s,%s)'
        # list = dbs.exe_sql(sql, prams)





    pass
