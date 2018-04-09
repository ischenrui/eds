# coding = utf-8

import re
from util import dbs
import os

DIR = os.path.dirname(os.path.abspath(__file__))
reEmail = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?"


# 更新机构邮箱地址集合
def update_institution_dicts():
    fw = open(DIR + "\\dicts\\institution_email.txt", "w+", encoding="utf-8")
    email_lines = fw.readlines()
    email_lines = [ins.strip('\n') for ins in email_lines]

    list_ = []
    sql = "select * from teacherdata"
    info = dbs.getDics(sql)
    # 生成机构邮箱词典 判定方法为：重复出现的邮箱暂定为机构邮箱
    for item in info:
        if not item[6]:
            continue
        info_text = item[6]
        info_text = info_text.replace("[at]", "@")
        info_text = info_text.replace(" ", "")
        info_text = info_text.replace("\n", "")
        email_text = re.findall(reEmail, info_text)

        if email_text:
            l2 = sorted(set(email_text), key=email_text.index)  # 处理同一个页面重复出现的邮箱地址
            list_.extend(l2)
        else:
            print('There is no Email address!!')

    list_1 = []
    l3 = sorted(set(list_))
    for item in l3:
        n = list_.count(item)
        if n > 2 and item not in email_lines:
            list_1.append(item)
    print(list_1)
    fw.write("\n".join(list_1))
    fw.close()


def extract_email():
    sql = "select * from teacherdata"
    info = dbs.getTuples(sql)

    ins_dict = open(DIR + "\\dicts\\institution_email.txt", "r", encoding="utf-8").readlines()
    ins_dict = [ins.strip('\n') for ins in ins_dict]
    id_list = []

    sum = 0
    num = 0
    institution = info[0][4]
    file = open(DIR + "\\Step1\\email\\" + str(num) + ".txt", "w", encoding="utf-8")

    for item in info:
        if not item[6]:
            continue
        info_text = item[6]
        print(item[0])
        info_text = info_text.replace("[at]", "@")
        info_text = info_text.replace(" ", "")
        info_text = info_text.replace("\n", "")
        email_text = re.findall(reEmail, info_text)

        if email_text:
            list_email = sorted(set(email_text), key=email_text.index)  # 去除相同邮箱地址
            list_email = [item for item in list_email if item not in ins_dict]  # 去除机构邮箱地址
            if len(list_email) > 0:
                if not item[4] == institution:
                    num += 1
                    institution = item[4]
                    print(institution)
                    file.close()
                    file = open(DIR + "\\Step1\\email\\" + str(num) + ".txt", "w", encoding="utf-8")
                file.write(str(item[0]) + "\n")
                file.write(item[1] + "\n")
                file.write(item[5] + "\n")
                sum += len(list_email)
                file.write("%s\n===================\n" % ";".join(list_email))
                id_list.append(item[0])

    file.close()


if __name__ == "__main__":
    # update_institution_dicts()
    # extract_email()
    pass
