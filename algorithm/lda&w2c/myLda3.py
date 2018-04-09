import gensim
from time import time
from databaseUtils import *
#


# # institution_paper_list = dbs.getTuples(sql)
#
# institution_list= [line.strip() for line in open('institution.txt',encoding='utf-8').readlines()]
# for institution in institution_list:
#     i=institution.split(' ')
#     for l in range(1,len(i)):
#         sql="update teacher set institution=%s where institution=%s"
#         dbs.exe_sql(sql,(i[0],i[l]))

dbs = DataUtils(db='ceshi')

def get_words(ins):
    sql = "SELECT topicwords_institution FROM topiclda where institution_teacher = '%s'" % ins
    result = dbs.select_all(sql)
    sql = "SELECT topicid_institution FROM topiclda where institution_teacher = '%s'" % ins
    id_result = dbs.select_all(sql)
    idLst = []
    for id in id_result:
        idLst.append(id[0])
    print(idLst)
    return result, idLst

institution={'马克思主义法治史研究所': '77',
 '中国语言文学（自定）': '1',
 '材料科学与工程学院': '42',
 '数据科学与工程学院': '38',
 '城市与环境学院': '21',
 '比较文学研究所': '1',
 '经济管理学院': '59',
 '化学学院': '12',
 '文学院': '1',
 '艺术与传媒学院': '66',
 '交通运输工程': '3',
 '化学与分子科学学院': '12',
 '天然产物源靶向药物国家地方联合工程实验室': '27',
 '中药学院': '0',
 '土木工程（自定）': '20',
 '基础医学院': '23',
 '地质学': '22',
 '地球科学与技术学院': '21',
 '地球科学学院': '21',
 '化学化工学院': '12',
 '信息资源管理学院': '5',
 '控制科学与工程学院': '35',
 '思想政治教育研究所': '33',
 '航空科学与工程学院': '64',
 '纺织学院': '58',
 '数学': '38',
 '生态学（自定）': '52',
 '环境科学与工程学院': '50',
 '新闻学院': '40',
 '现代工程与应用科学学院': '51',
 '管理学院': '56',
 '化学系': '12',
 '国际经济贸易学院': '19',
 '电气工程学院': '53',
 '力学与工程科学系': '10',
 '多媒体技术教研中心': '25',
 '生命科学学院': '52',
 '生物科学与医学工程学院': '52',
 '设计创意学院': '69',
 '计算机科学与技术': '68',
 '水产学院': '44',
 '电子与信息工程学院': '53',
 '药学': '67',
 '海洋微型生物blahblah': '48',
 '物理学系': '49',
 '公共卫生学院': '7',
 '历史学院': '15',
 '心理学院': '32',
 '土木工程学院': '20',
 '生态学': '52',
 '医学部': '14',
 '中国近现代史研究所': '2',
 '测绘与地理信息学院': '47',
 '经济与管理学院': '59',
 '环境与资源学院': '50',
 '信息与通信工程': '74',
 '海洋与地球学院': '48',
 '国际关系学院': '19',
 '食品学院': '76',
 '心理与认知科学学院': '32',
 '数学科学学院': '38',
 '力学': '10',
 '科学社会主义研究所': '55',
 '材料科学学系': '42',
 '海洋生物多样性和全球变化研究中心': '48',
 '北京体育大学': '13',
 '石油与天然气工程': '54',
 '政治与国际关系学院': '36',
 '国际关系与公共事务学院': '19',
 '园艺林学学院': '18',
 '自动化学院': '63',
 '马克思主义中国化研究所': '77',
 '法学院': '46',
 '计算机科学与工程学院': '68',
 '大气科学学院': '26',
 '公共管理学院': '7',
 '资源加工与生物': '71',
 '哲学系宗教学系': '17',
 '交通运输管理学院': '3',
 '管理与经济学部': '56',
 '交通学院': '3',
 '机械与动力工程学院': '41',
 '电子科学与工程学院': '53',
 '哲学学院': '17',
 '系统科学学院': '57',
 '植物保护学院': '8',
 '政府管理学院': '36',
 '电气工程、信息与通信工程': '53',
 '文艺理论教研室': '39',
 '地球科学与工程学院': '21',
 '考古文博学院': '61',
 '动力工程及工程热物理': '10',
 '计算机科学与技术学院': '68',
 '统计与管理学院': '60',
 '资源学院': '71',
 '核科学技术学院': '43',
 '机械工程学院': '41',
 '大气科学': '26',
 '化学与分子工程学院': '12',
 '安全科学与工程': '28',
 '能力与动力学院': '62',
 '化学（自定）': '12',
 '材料科学与工程系': '42',
 '化工学院': '12',
 '社会学系': '55',
 '古代汉语教研室': '16',
 '海洋地球科学学院': '48',
 '信息管理学院': '5',
 '植物科学技术学院': '8',
 '历史学系': '15',
 '草学': '8',
 '统计学院': '60',
 '护理学院': '34',
 '工学院': '30',
 '电子与光学工程学院': '53',
 '电气与电子工程学院': '53',
 '动物医学院': '11',
 '机械工程': '41',
 '航空航天系': '64',
 '数学系': '38',
 '农学院': '8',
 '药学院': '67',
 '光学与电子信息学院': '6',
 '石油工程学院': '54',
 '哲学院': '17',
 '当代文学教研室': '1',
 '基础医学系': '23',
 '生态与环境科学学院': '52',
 '安全工程学院': '28',
 '作物学（自定）': '8',
 '化学工程与技术': '12',
 '机械科学与工程学院': '41',
 '冶金与环境学院': '9',
 '经济学院': '59',
 '化学': '12',
 '化学工程与技术（自定）': '12',
 '天文学系': '26',
 '安全科学与工程系': '28',
 '土木与资源工程学院': '20',
 '基础医学': '23',
 '电气工程（自定）': '53',
 '光电科学与工程': '6',
 '通信网技术教研中心': '73',
 '设计学院': '69',
 '动物科学技术学院': '11',
 '水利水电学院': '45',
 '测绘学院': '47',
 '环境学院': '50',
 '中医学': '0',
 '近海海洋环境科学国家重点实验室': '48',
 '语言学实验室': '70',
 '林学院': '8',
 '古代文学教研室': '16',
 '材料学院': '42',
 '应用经济学（自定）': '29',
 '电子科学与技术': '53',
 '农业与农村发展学院': '8',
 '生物工程学院': '52',
 '社会与人口学院': '55',
 '地理科学与规划学院': '21',
 '船舶工程学院': '65',
 '建筑系': '31',
 '地理学与遥感科学学院': '21',
 '材料科学与工程': '42',
 '马克思主义学院': '77',
 '医学院': '14',
 '数学与统计学院': '38',
 '艺术学院': '66',
 '冶金与生态工程学院': '9',
 '安泰经管学院': '29',
 '数学学院': '38',
 '仪器科学与光电工程学院': '4',
 '哲学系': '17',
 '现代汉语教研室': '1',
 '教育学部': '37',
 '软件学院': '72',
 '民间文学教研室': '1',
 '环境科学与工程系': '50',
 '政治经济学研究所': '36',
 '国外马克思主义研究所': '77',
 '水声通信与海洋信息技术教育部重点实验室': '48',
 '农业与生物技术学院': '8',
 '生命科学技术学院': '52',
 '材料与化学化工学部': '42',
 '能源与动力工程学院': '62',
 '古典文献学教研室': '16',
 '化学生物学系': '12',
 '生物系统工程与食品科学学院': '52',
 '现代文学教研室': '1',
 '资源与环境学院': '71',
 '农学': '8',
 '音乐学系': '75',
 '矿业工程学院': '54',
 '地质资源与地质工程': '22',
 '哲学系（珠海）': '17',
 '滨海湿地生态系统教育部重点实验室': '48',
 '水产与生命学院': '44',
 '机械工程（自定）': '41',
 '物理学院': '49',
 '外国语学院': '24',
 '马克思主义基本原理研究所': '77',
 '宇航学院': '26',
 '地球和空间科学学院': '21',
 '管理科学与工程、工商管理': '56',
 '机电工程学院': '41',
 '语言学教研室': '70',
 '天文与空间科学学院': '26',
 '化学工程学院': '12'}
institution_topic={}
all_topic=[]
for ins in institution:
    if institution[ins] not in institution_topic:
        try:
            list = [line.strip() for line in open('fields/result/' + institution[ins] + '.txt', encoding='utf-8').readlines()]
        except:
            continue
        temp = []
        for l in list:
            temp.append(l.replace('\ufeff', ''))
        institution_topic[institution[ins]]=temp
        all_topic.extend(temp)
s1 = time()
model = gensim.models.Word2Vec.load("data3/word2vec.txt")
word_vectors = model.wv
s2 = time()
print('mode load :', s2 - s1)
institution = {'计算机科学与工程学院': '68'}
for ins in institution:
    print(ins)
    result, id_result = get_words(ins)
    for r in result:
        list_r = r[0].split(' ')
        dictSorted = {}
        sum = 0
        for word_r in list_r:
            dictSorted[word_r] = 1 - sum * 0.02
        dictSorted = sorted(dictSorted.items(), key=lambda item: item[1], reverse=True)
        similarDict = {}
        keyList=[]
        keyList.extend(dictSorted[0:10])
        for k in dictSorted[0:10] :
            try:
                wordsList = word_vectors.most_similar(positive=k[0], topn=10)
            except:
                wordsList = []
                print("error:"+k[0])
            for tuple in wordsList:
                wordSimilar = tuple[0]
                weightSimilar = tuple[1]*k[1]
                if wordSimilar in similarDict:
                    similarDict[wordSimilar] += weightSimilar
                else:
                    similarDict[wordSimilar] = weightSimilar
        dictSorted = sorted(similarDict.items(), key=lambda item:item[1], reverse=True)
        keyList.extend(dictSorted[0:10])
        print("word2vec:")
        print(dictSorted[0:5])
        try:
            temp=institution_topic[institution[ins]]
        except:
            temp=all_topic
        similarTopic={}
        for k in temp:
            for key in keyList:
                try:
                    v=word_vectors.similarity(k,key[0]) * key[1]
                except:
                    v=0
                if k in similarTopic:
                    similarTopic[k] += v
                else:
                    similarTopic[k] =v

        dictSorted = sorted(similarTopic.items(), key=lambda item: item[1], reverse=True)
        print("topic:")
        print(dictSorted[0:5])
        try:
            top=dictSorted[0][0]
        except:
            top='no_topic'
        print(top)
        topicid = id_result.pop(0)
        sql = "update topiclda set tag_word='"+top+"'  where institution_teacher = '" + ins + "' and topicid_institution = '" + topicid + " '"
        dbs.insert_one(sql)
