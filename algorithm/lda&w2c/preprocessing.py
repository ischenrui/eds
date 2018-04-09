"""
结巴分词之前的预处理
提取userdict
tf转换之前的预处理
提取stopwords

统计自定义词典
统计每个学院发表的论文
根据发表论文的数量 自定义每个学院的topics

后续步骤需要用到userdict.txt,stopwordsLst.pkl和topicNumFinal.pkl


之后在paper表不变的情况下
keywords_save + userdict_extract
stop_words_extract
可以不重新提取

但是如果学院有变化(如学院合并之类)
paper_institution
topics_institution
topics_remove0
"""
from databaseUtils import *
from sklearn.externals import joblib

db = DataUtils()
def keywords_save():
    # 把所有keyword写入文件
    keywords = open('keywords.txt', encoding='utf-8', mode='w')

    sql = """select keyword_paper from doclda"""
    result = db.select_all(sql)
    for i in range(0, len(result)):
        if (result[i][0]):
            keywords.write(result[i][0] + ',')

def userdict_extract():
    """
    抽取关键字作为用户字典
    :return: 存储在 userdict.txt里面
    """
    keywords_save()

    # 把keyword读出来, 并且统计词频写入userdict.txt里面
    wordDict = {}
    keywordsLst = open('keywords.txt', encoding='utf-8', mode='r').read().split(',')
    userdict = open('userdict.txt', encoding='utf-8', mode='w')

    # 统计词频放入词典
    for word in keywordsLst:
        if(word in wordDict):
            wordDict[word] += 1
        else:
            wordDict[word] = 1
    # 把词典写入文件
    for word in wordDict:
        userdict.write(word + ' ' + str(wordDict[word]) + ' n' + '\n')

def stop_words_extract():
    """
    整理停用词汇表成list类型存起来
    :return: list
    """
    stplst = []
    lineLst = open('StopWords.txt', encoding='utf-8', mode='r').readlines()
    for line in lineLst:
        line = line.strip().strip('\n')
        stplst.append(line)
    joblib.dump(stplst, 'stopwordsLst.pkl')

def paper_institution():
    """
    统计每个学院的论文量
    :return: dict
    """
    numDict = {}
    institutionLst = joblib.load('institution.pkl')
    for institution in institutionLst:
        sql = """select count(*) from doclda where institution_teacher = '%s'""" % institution
        result = db.select_one(sql)
        # print(result[0])
        numDict[institution] = result[0]
    joblib.dump(numDict, 'paperNum.pkl')
    return numDict

def topics_institution(numDict):
    """
    根据每个学院的论文数量 动态选择该学院的topic数目
    包括了0个topic的
    :return: dict
    """
    topicDict = {}
    paperNum = numDict
    # paperNum = joblib.load('paperNum.pkl')
    print(type(paperNum))
    for institution, papers in paperNum.items():
        if(papers <= 10):
            topicDict[institution] = 0
        elif(papers <= 100):
            topicDict[institution] = 5
        elif (papers <= 1000):
            topicDict[institution] = 10
        elif (papers <= 2000):
            topicDict[institution] = 15
        elif (papers <= 4000):
            topicDict[institution] = 25
        elif (papers <= 8000):
            topicDict[institution] = 35
        else:
            topicDict[institution] = 50
    joblib.dump(topicDict, 'topicNum.pkl')
    return topicDict

def topics_remove0(topicDict):
    """
    最终每个学院应该分配的方向, 较之前的Dict,去除了没有论文发表的学院
    除去零
    :return: dict
    """
    topicNum = topicDict
    # topicNum = joblib.load('topicNum.pkl')

    topicFinal = {}
    for institution, topics in topicNum.items():
        if(topics):
            topicFinal[institution] = topics
    joblib.dump(topicFinal, 'topicNumFinal.pkl')
    return topicFinal

def institution_extract(topicFinal):
    topicNumDict = topicFinal
    # topicNumDict = joblib.load('topicNumFinal.pkl')
    institutionDoclda = []
    for institution in topicNumDict:
        institutionDoclda.append(institution)
    joblib.dump(institutionDoclda, 'institutionDoclda.pkl')

def test():
    print(joblib.load('topicNumFinal.pkl'))
    print(len(joblib.load('institutionDoclda.pkl')))

def main():
    numDict = joblib.load('paperNum.pkl')
    topicDict = topics_institution(numDict)
    topicFinal = topics_remove0(topicDict)
    institution_extract(topicFinal)

if __name__ == '__main__':
    test()
    # main()
