


import gensim
import json
from algorithm.base import dbs
#


# # institution_paper_list = dbs.getTuples(sql)
#
# institution_list= [line.strip() for line in open('institution.txt',encoding='utf-8').readlines()]
# for institution in institution_list:
#     i=institution.split(' ')
#     for l in range(1,len(i)):
#         sql="update teacher set institution=%s where institution=%s"
#         dbs.exe_sql(sql,(i[0],i[l]))


def get_words():
    sql = "SELECT DISTINCT topic_value FROM `lda` where topic like '%计算机%'"
    result = dbs.getDics(sql)
    return result


model = gensim.models.Word2Vec.load("data2/word2vec.txt")
word_vectors = model.wv

result = get_words()
for r in result:
    dic=json.loads(r['topic_value'])
    dictSorted = sorted(dic.items(), key=lambda item: item[1], reverse=True)
    print("dict")
    print(dictSorted)
    similarDict = {}
    for k in dictSorted[0:10] :
        try:
            wordsList = word_vectors.most_similar(positive=k[0], topn=10)
        except:
            print("error:"+k[0])
        for tuple in wordsList:
            wordSimilar = tuple[0]
            weightSimilar = tuple[1]*k[1]
            if wordSimilar in similarDict:
                similarDict[wordSimilar] += weightSimilar
            else:
                similarDict[wordSimilar] = weightSimilar
    dictSorted = sorted(similarDict.items(), key=lambda item:item[1], reverse=True)
    print(dictSorted[0:5])
