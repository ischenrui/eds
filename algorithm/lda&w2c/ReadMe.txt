py文件: 序号为顺序
    databaseUtils:(1)
        集成操作数据库的方法
        把查询和插入方法封装, 以便后续使用

    databaseProess:(2)
        数据库的重新整合
        从teacherdata表中查找学院, 根据学院把专家分类到各个学院
        根据专家id,从paper表中提取有用信息,以便后学聚类和河流图的使用
        #如果teacher表不变,但是paper表变化了, 那么doclda需要重新提取#
        #不需要运行(1)(2), 只用之前存起来的(2)文件(teacherInstitution.pkl)即可#
            institution_dump():(1) 从teacher表里面把所有的学院提取出来(去重), 存储到institution.pkl, 为(2)做准备
            teacher_dump(institutionLst):(2) 根据(1)得到的学院,把对应的teacher的id提取出来,存储到teacherInstitution.pkl, 为(3)做准备
            insert_doclda(teacherDict):(3) 根据(2)得到的教师ID,把paper表里面的数据重新整理提取到doclda里面以备后用.

        #运行流程#
            teacherDict = joblib.load('teacherInstitution.pkl')
            insert_doclda(teacherDict)


    preprocessing:(3)
        数据预处理
        把jieba需要用到的词汇表,从doclda的keywords中提取出来
        把之后聚类处理时候需要用到的topics数量定义,根据各个学院的paper数量
        #(1)+(2), (3), (4)+(5)+(6)+(7)#
        #只要paper变了, 除了(3), 可以不重新运行外,其他都需要重新运行#
            keywords_save():(1) 从doclda中提取关键字,为(2)做准备
            userdict_extract():(2) 调用(1),生成关键字文件, 然后用关键字生词用户词典

            stop_words_extract():(3) 把停用词表,读取到list文件中

            paper_institution():(4) 统计每个学院的论文量,为(5)做准备
            topics_institution(numDict):(5) 根据(4)统计出来的每个学院的论文量,动态为每个学院分配topics数量
            topics_remove0(topicDict):(6)  根据(5)统计出来的数据,把没有论文发表的学院剔除
            institution_extract(topicFinal): (7) 根据(6)得到的dict,把有论文发表过的学院提取出来 (179个, 而不是之前的208个)
        #运行流程(4)+(5)+(6)+(7)#
            numDict = paper_institution()
            topicDict = topics_institution(numDict)
            topicFinal = topics_remove0(topicDict)
            institution_extract(topicFinal)
        #运行流程(1)+(2)#
            userdict_extract() #自动调用(1)


    jiebalda:(4)
        对数据库里面的doclda和topiclda进行操作
        从doclda取出abstract和keywords进行jieba分词
        对分词进行矩阵化然后lda模型拟合
        最后将预测的每篇论文的topic存在doclda里面
        将topic的词汇存在topiclda表里面,以便进行研究方向的总结
        #按照main方法运行即可#

    rivers:(5)
        根据teacherID在doclda里面提取对于河流图有用的字段
        存储到河流图需要的theme_year表里面

    tagTopic:(6)
        随机给主题定标签,通过tfidf来随机查找最合适的词

    ldaall:(7) (失败)
        把所有的论文同时进行聚类测试,用的是测试的表docldatest和topicldatest

        效果不好,几乎没有起到聚类的作用.
        原因在于topics的数量设置太小(300), 每个学院多则上万篇论文, 学院数180个左右,
        所以在lda聚类之后,相对论文较多的学院,几乎可以囊括所有topics, 没有起到聚类作用.
        而如果topics设置太大的话, 内存严重不足.

    gensimLDA : (8)....
        准备调gensim库里面的函数进行LDA, 尤其是试用hdp模型

    onlyJieba : 独立
        为做Word2Vec分词用
    aliyun : 独立
        为修改aliyun数据库里面的teacher表格里面的fields字段用	
	myLda3.py : (9)
        用word2voc单独提取tag
	seuADD : (10)
		单独处理东南大学计算机学院

文本文件:
    institution.pkl : 提取所有学院 dict
    teacherInstitution.pkl : 统计各个学院老师的id dict
    keywords.txt : 提取所有论文的关键词 txt
    userdict.txt : 提取用户自定义词典 txt
    stop_words.txt : 网上下载的停用词表 txt
    paperNum.pkl : 统计208个学院,每个学院的论文发表量 dict
    topicNum.pkl : 根据论文量,自定义的该学院的topic数量(过渡性文件) dict
    topicNumFinal.pkl : 把topicNum里面的论文为0的数据剔除(最终文件) dict
    institutionDoclda.pkl : 从topicNumFinal.pkl里面把doclda所有的学院提取出来 list (179个, 而不是之前的208个)
    testLsk.pkl : 作为测试表的test的分词特征表
    idTeacher.pkl : 无重复存储的doclda里面的id_teacher以便后续使用 list
    numTopics.pkl : 按照topics个数, 把topics个数相同的学院放在一起, 为在mysql里面查询方便, 停用词手动添加方便查找 dict (无用了)
    stops_zjl.txt : 把topiclda里面的词汇存起来,手动查找停用词 txt (过渡性文件)
    StopWords.txt : 导入手动查找的词汇之后的 停用词表 txt
    stopwordsLst.pkl : 把停用词表整理成countVectorizer的stop_words需要的类型, 主要是去掉'\n' list

    ldaall 因为没办法直接把所有的文档一起运行,内存不够,所以先把预处理存储起来
    corpusAll.pkl : 所有的字符串合并成一个list,然后jieba之后做的corpus list
    id_paperLstAll.pkl : doclda里面paper的id,为之后查出该paper的topic之后,插入时候用来作为查询条件 list
    tfAll.pkl : 全部语料库的tf矩阵 TfidfVectorizer
    tf_features_namesAll.pkl : 用于提取topicwords的 list
