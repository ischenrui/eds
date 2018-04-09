import jieba
import jieba.posseg as psg
from databaseUtils import *
from sklearn.externals import joblib
import time
from sklearn.decomposition import LatentDirichletAllocation


db = DataUtils(db='ceshi')
# 把停用词汇表存到stpwordslst里面以便使用
stpwordslst = joblib.load('stopwordsLst.pkl')

def add_fields():
    sql = """select fields from teacher_add"""
    result = db.select_all(sql)
    fieldsLst = []
    for tuple in result:
        if tuple[0]:
            for filed in tuple[0].strip().split(','):
                if filed not in fieldsLst:
                    fieldsLst.append(filed)
    Lst68 = [field.strip() for field in open('fields\\result\\68.txt', mode='r', encoding='utf-8').readlines()]
    Lst = open('fields\\result\\68.txt', mode='a', encoding='utf-8')

    for field in fieldsLst:
        if(field not in Lst68):
            Lst.write(field+'\n')

def add_to_doclda():
    sql = """select id, paper_md5,  author_id, abstract, keyword, year from paper_add"""
    result = db.select_all(sql)
    for tuple in result:
        id_paper = tuple[0]
        md5_paper = tuple[1]
        id_teacher = tuple[2]
        institution_teacher = '计算机科学与工程学院'
        abstract_paper = tuple[3]
        keyword_paper = tuple[4]
        year_paper = tuple[5]
        topic_paper = 'test'

        try:
            sql_insert = """insert into doclda values(%s, '%s', '%s', "%s", '%s', '%s', '%s', '%s')""" \
                         % (id_paper, md5_paper, id_teacher, institution_teacher,abstract_paper,keyword_paper,year_paper, topic_paper)
            db.insert_one(sql_insert)
        except:
            print(id_paper, md5_paper, id_teacher, institution_teacher, abstract_paper, keyword_paper, year_paper,
                  topic_paper)


def jieba_util(str_list):
    """
    jieba分词,返回切分好的词语
    :param str: 需要处理的字符串
    :return: str
    """
    jieba.load_userdict('userdict.txt')
    lst_ret = []
    for str in str_list:
        str_cut = psg.cut(str)
        str_ret = ''
        word_reserve = ('v', 'n', 'vn')
        for word, key in str_cut:
            if (key in word_reserve):
                str_ret = str_ret + ' ' + word
        lst_ret.append(str_ret)
    return lst_ret

def get_corpus(institution_teacher):
    """
    从数据库里面选择摘要和关键词,拼接成字符串,作为文本
    处理之后 返回一个列表 列表的每一项为一篇论文的jieba分词
    每篇论文作为一个样例, 存储在corpus 作为预料库
    :param institution_teacher: 要处理的学院
    :return:
            id_paperLst: doclda里面paper的id,为之后查出该paper的topic之后,插入时候用来作为查询条件 list
            corpus: list
    """
    id_paperLst = []
    sql = """select abstract_paper, keyword_paper, id_paper  from doclda where institution_teacher = '%s'""" % institution_teacher
    result = db.select_all(sql)
    str_list = []
    for i in range(0, len(result)):
        str = result[i][0] + result[i][1]
        str_list.append(str)
        id_paperLst.append(result[i][2])
    corpus = jieba_util(str_list)
    return corpus, id_paperLst

def tf_extract(corpus):
    """
    将corpus(文本) 矩阵化 (tf矩阵)
    :param corpus: 语料库
    :return:
            tf : array, [n_samples, n_features]
            tf_tf_features_names : list
    """
    from sklearn.feature_extraction.text import CountVectorizer
    countVectorizer = CountVectorizer(stop_words=stpwordslst)
    tf = countVectorizer.fit_transform(corpus)
    tf_features_names = countVectorizer.get_feature_names()
    return tf, tf_features_names

def lda_test(tf, n_topics):
    """
    用矩阵拟合LDA模型
    :param tf: 矩阵化的语料库
    :param n_topics: 学院所应该分的topic数目
    :return:
            docres: sklearn.decomposition.online_lda.LatentDirichletAllocation
            docres_transform : numpy.ndarray
    """

    lda = LatentDirichletAllocation(n_components=n_topics, random_state=0, max_iter=100, learning_method='batch')
    # docres用于词频分辨比较
    # 为之后总结topic标签做准备
    docres = lda.fit(tf)
    # docres_transform用于自动把paper标注类型
    docres_transform = lda.fit_transform(tf)
    return docres, docres_transform

def topic_insert(features_names, docres, docres_transform, id_paperLst, institution_teacher):
    """
    将处理好的数据,依次插入doclda里面的topic_paper和topiclda里面
    :param features_names: 特征词
    :param docres: 用于发现特征词的下标
    :param docres_transform: 用于发现paper的
    :param id_paperLst:
    :param institution_teacher:
    :return:
    """
    conn = db.conn()
    cursor = conn.cursor()
    for topic_idx, topic in enumerate(docres.components_):
        topic_str = ''
        for i in topic.argsort()[: -21: -1]:
            topic_str = topic_str +features_names[i] + ' '
        sql = """insert into topiclda values('%s', '%s', '%s', '%s', '%s')""" % \
              (institution_teacher, topic_idx, topic_str, 'null', 'test')
        cursor.execute(sql)
    for i in range(0, len(docres_transform)):
        topic_paper = list(docres_transform[i]).index(max(docres_transform[i]))
        sql = """update doclda set topic_paper=%s where id_paper=%s""" % (topic_paper, id_paperLst[i])
        cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def main():
    corpus, id_paperLst = get_corpus('计算机科学与工程学院')
    tf, tf_features_names = tf_extract(corpus)
    docres, docres_transform = lda_test(tf, 70)
    topic_insert(tf_features_names, docres, docres_transform, id_paperLst, '计算机科学与工程学院')

if __name__ == '__main__':
    main()


