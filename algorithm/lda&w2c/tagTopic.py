from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from databaseUtils import *
import numpy as np
from time import time

db = DataUtils()

def top1words(tfidf_fit_transform, features_names):
    """
    返回tfidf词汇,按照下标对应就可以
    :param tfidf_fit_transform: tfidf矩阵
    :param features_names: 特征词
    :return: list
    """
    top1wordsLst = []
    for i in range(0, tfidf_fit_transform.shape[0]):
        index = np.argmax(tfidf_fit_transform[i].toarray())
        top1wordsLst.append(features_names[index])
    return top1wordsLst


def topicWords_extract(institution_teacher):
    """
    从topiclda里面把topicwords提取出来,每个学院作为一个corpus进行处理
    :param institution_teacher: 学院名
    :return: list
    """
    corpus = []
    sql = """select topicwords_institution from topiclda where institution_teacher = '%s'""" % institution_teacher
    result = db.select_all(sql)
    for index, tuple in enumerate(result):
        corpus.append(tuple[0])
    return corpus

def tfidf_words(corpus):
    """
    对topiclda进行矩阵化
    :param corpus:
    :return:
    """
    tfidfVectorizer = TfidfVectorizer()
    tfidf_fit = tfidfVectorizer.fit(corpus)
    tfidf_fit_transform = tfidfVectorizer.fit_transform(corpus)
    features_names = tfidf_fit.get_feature_names()
    return tfidf_fit_transform, features_names

def topicTag_insert(top1wordsLst, institution_teacher):
    """
    把标签插入到指定列
    :param top1wordsLst: 标签列表
    :param institution_teacher: 学院名
    :return:
    """
    sql_result_topic_paper = """select id_paper, topic_paper from doclda where institution_teacher = '%s'""" % institution_teacher
    result_topic_paper = db.select_all(sql_result_topic_paper)

    conn = db.conn()
    cursor = conn.cursor()
    for index in range(0, len(top1wordsLst)):

        sql_topiclda = """update topiclda set tag_topic = '%s'  where institution_teacher = '%s' and topicid_institution = '%s' """\
                       %(top1wordsLst[index], institution_teacher, index)
        cursor.execute(sql_topiclda)
    for id_paper, topic_paper in enumerate(result_topic_paper):
        id_paper = int(topic_paper[0])
        topic_paper = int(topic_paper[1])
        sql_doclda = """update doclda set tag_topic = '%s'  where id_paper = '%s' """ \
                     % (top1wordsLst[topic_paper], id_paper)
        cursor.execute(sql_doclda)
    conn.commit()
    cursor.close()
    conn.close()

def test():
    s1 = time()
    corpus = topicWords_extract('哲学系宗教学系')
    s2 = time()
    print('time2-1 = ', s2 - s1)
    tfidf_fit_transform, features_names = tfidf_words(corpus)
    s3 = time()
    print('time3-2 = ', s3 - s2)
    top1wordsLst = top1words(tfidf_fit_transform, features_names)
    s4 = time()
    print('time4-3 = ', s4 - s3)
    topicTag_insert(top1wordsLst, '哲学系宗教学系')
    s5 = time()
    print('time5-4 = ', s5 - s4)

def main():
    institutionLst = joblib.load('institutionDoclda.pkl')
    for institution_teacher in institutionLst:
        start = time()
        corpus = topicWords_extract(institution_teacher)
        tfidf_fit_transform, features_names = tfidf_words(corpus)
        top1wordsLst = top1words(tfidf_fit_transform, features_names)
        topicTag_insert(top1wordsLst, institution_teacher)
        print('%s', institution_teacher, ' time ->', time() - start)
if __name__ == '__main__':
    start = time()
    main()
    # test()
    print('time used -> ', time() -start)
    pass
