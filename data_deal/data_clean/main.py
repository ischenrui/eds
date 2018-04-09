from mysql import Mysql
import random
def randomname():
    fnstr = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪'
    en = '车巨牙屯比互切瓦号田由史只央表拢顷转斩轮软到非叔肯齿些虎虏肾贤尚旺具果味昆国昌畅要咸威歪研砖厘厚砌砍面耐耍牵残殃轻鸦皆背战点临览竖省削尝是'
    name = fnstr[random.randint(0,len(fnstr)-1)]+en[random.randint(0,len(en)-1)]+en[random.randint(0,len(en)-1)]
    return name

def randomposition():
    pstr = ['博士生导师','硕士生导师']
    return pstr[random.randint(0,1)]

def randomtitle():
    tstr = ['教授','副教授','讲师']
    return tstr[random.randint(0, 2)]

def randomschool():
    tstr = ['北京大学', '东南大学', '清华大学','武汉大学','上海交通大学','华中科技大学','湖北大学']
    return tstr[random.randint(0, len(tstr)-1)]

def randominstitution():
    tstr = ['软件学院', '计算机学院', '外语学院','马克思主义学院','数学统计学院','建筑学院','物理学院']
    return tstr[random.randint(0, len(tstr)-1)]

def randomphone():
    tstr = ['13971392598', '15646854362', '16754856982','13156238469','157854123569','18845871035','17754125874']
    return tstr[random.randint(0, len(tstr)-1)]

def randomemail():
    tou = ['chenrui','liwei','zhangdaofeng','luyuelang','liuedefa','zhangjiulin']
    wei = ['@qq.com','@126.com','@163.com','@gmail.com']
    email = tou[random.randint(0, len(tou)-1)] + wei[random.randint(0, len(wei)-1)]
    return email

def randomhomepage():
    tou = ['chenrui','liwei','zhangdaofeng','luyuelang','liuedefa','zhangjiulin']
    web = 'www.'+ tou[random.randint(0, len(tou)-1)] + '.com'
    return web

def randomtheme():
    tstr = ['数据挖掘', '图像识别', '自然语言处理', '大数据', '计算机网络', '数据库系统原理', '深度学习']
    return tstr[random.randint(0, len(tstr) - 1)]

def randompapernum1980():
    tstr = [0, 0,0,0,0,0,0,0,0,0,0,1,1,2,2,3,3,4,5,6,7,8]
    return tstr[random.randint(0, len(tstr) - 1)]

def randompapernum2000():
    tstr = [0, 0,0,1,1,2,2,2,3,3,3,3,4,4,4,4,4,5,5,5,6,6,7,7,8,9,10]
    return tstr[random.randint(0, len(tstr) - 1)]

if __name__ == '__main__':
    sql = Mysql()

#-----------teacher-------------
    # for i in range(1,100):
    #     name=randomname()
    #     position=randomposition()
    #     title=randomtitle()
    #     school=randomschool()
    #     institution=randominstitution()
    #     phone=randomphone()
    #     eduexp='University of Wisconsin-Madison Computer Science, Doctor of Philosophy (Ph.D.) 1979 – 1983 National Institute of Industrial Engineering Industrial Engineering, Master of Technology (M.Tech.) 1974 – 1978 Indian Institute of Technology, Roorkee Electrical, Electronics and Communications Engineering, Bachelor of Engineering (B.E.) 1970 – 1975'
    #     email=randomemail()
    #     pic='demo'
    #     homepage=randomhomepage()
    #     author_id=i
    #     sql.InsertTeacher(name,position,title,school,institution,phone,eduexp,email,pic,homepage,author_id)

#-----------theme_year------------
    # for i in range(1,101):
    #     author_id=i
    #     paper_md5=1
    #     for j in range(1980,2000):
    #         year = j
    #         x=0
    #         while x<randompapernum1980():
    #             theme=randomtheme()
    #             sql.InsertTheme(author_id, paper_md5, year, theme)
    #             x+=1
    #     for j in range(2000,2018):
    #         year = j
    #         x=0
    #         while x<randompapernum2000():
    #             theme=randomtheme()
    #             sql.InsertTheme(author_id, paper_md5, year, theme)
    #             x+=1

# -----------radar------------
#     for i in range(1, 101):
#         author_id=i
#         paper_num=random.randint(0,100)
#         citation=random.randint(0,1000)
#         h_index=random.randint(0,200)
#         G_index=random.randint(0,200)
#         sociability=random.randint(0,10)
#         sql.InsertRadar(author_id, paper_num, citation, h_index,G_index,sociability)

# -----------ego_network------------
    for i in range(1,101):
        author_id=i
        x = random.randint(0,50)
        list = random.sample(range(1, 101), x)
        for node in list:

            coauthor=node
            w=random.randint(1,10)
            sql.InsertEgonetwork(author_id, coauthor,w)



    pass
