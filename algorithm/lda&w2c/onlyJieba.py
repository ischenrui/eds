import pickle
from sklearn.externals import joblib
import jieba
import jieba.posseg as pseg
import time
from databaseUtils import *


# dbs = DataUtils()
# stopwords = joblib.load('stopwordsLst.pkl')
# fill = ['v', 'vd', 'vn', 'vf ', 'vx ', 'vi', 'vl', 'vg', 'n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf',
#                 'nt', 'nz', 'nl', 'ng']
# print('词典更新')
# jieba.load_userdict('userdict.txt')
#
# for i in range(5000000,10000000,500000):
#     sql = 'select id,name,abstract,keyword from paper_citeorref limit '+str(i)+',500000'
#     paper_list = dbs.select_all(sql)
#     if len(paper_list)==0:
#         break
#     print('分词')
#     print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
#     DocWord = []
#     for paper in paper_list:
#         line = paper[1].strip('\n').strip('\t') + ' ' + paper[2].strip('\n').strip('\t') + ' ' + paper[3].strip('\n').strip(
#             '\t')
#         seg_list = pseg.cut(line)
#         words = []
#         for word, flag in seg_list:
#             if flag in fill and word not in stopwords:
#                 words.append(word)
#         DocWord.append(words)
#     print('保存分词')
#     pickle.dump(DocWord, open('data/fenci'+str(i)+'.txt', 'wb'))


sentence = pickle.load(open('data/fenci8500000.txt', 'rb'))
print()
# sentence=sentence[0:300000]
# class MySentences(object):
#     def __init__(self, sentence):
#         self.sentence = sentence
#
#     def __iter__(self):
#         for line in  self.sentence:
#             yield line

# print('开始训练')
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
# sen = MySentences(sentence)
# model = gensim.models.Word2Vec(sen,size=200,window=10,iter=20,min_count=5)
# print('保持模型')
# model.save("data/word2vec.txt")
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
# model = gensim.models.Word2Vec.load("data/word2vec.txt")
# word_vectors = model.wv
# print(word_vectors.most_similar(positive=['宗教','教育部']))
