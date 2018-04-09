import os
import re
from util import dbs
import jieba
import jieba.posseg as pseg

DIR = os.path.dirname(os.path.abspath(__file__))

reTime = r'(19|20)\d{2}'


class Extractor:
    def __init__(self, orginal_text="", block_size=100):
        self.orginal_text = orginal_text
        self.blockSize = block_size
        self.col = []
        self.blocks = []

    def process_blocks(self):
        sentence_list = self.orginal_text.split('\n')
        num = 0
        i = 0
        length = len(sentence_list)
        while i < length:
            if num > 2:
                break
            t = re.search(reTime, sentence_list[i], flags=0)
            if not t:
                i += 1
                continue
            text = ""
            col = i
            for j in range(i, len(sentence_list)):
                text += sentence_list[j]
                if len(text) > 100:
                    i = j
                    self.blocks.append(text)
                    self.col.append(str(col))
                    num += 1
                    break
            i += 1
            pass
        print(self.blocks)
        # return ";".join(self.col) + "\n" + "\n".join(self.blocks)
        return self.col, self.blocks

    def get_texts(self):
        return self.process_blocks()

    def set_text(self, orginal_text):
        self.orginal_text = orginal_text
        self.col = []
        self.blocks = []


if __name__ == "__main__":
    sql = "select id, institution, cleaninfo from teacherdata WHERE length(cleaninfo)>0"
    info_list = dbs.getDics(sql)
    print("222222222222222")

    jieba.load_userdict(DIR + "\\dicts\\userdict.txt")
    ext = Extractor()
    institution = info_list[0]["institution"]
    num = 0
    dir = DIR + "\\Step3\\"
    file = open(dir + str(num) + ".txt", "w", encoding="utf-8")
    file_seg = open(DIR + "\\Step5\\" + str(num) + ".txt", "w", encoding="utf-8")
    for item in info_list:
        if not item["institution"] == institution:
            num += 1
            institution = item["institution"]
            print(institution)
            file.close()
            file = open(dir + str(num) + ".txt", "w", encoding="utf-8")
            file_seg.close()
            file_seg = open(DIR + "\\Step5\\" + str(num) + ".txt", "w", encoding="utf-8")
        ext.set_text(item["cleaninfo"])
        cols, te = ext.get_texts()
        file.write("%s\n" % cols)
        file_seg.write("%s\n" % cols)
        for t in te:
            file.write(t)
            segs = pseg.cut(t)
            file_seg.write("%s\n" % (" ".join([w.word + '/' + w.flag for w in segs])))
        file.write("++++++++++++++++++++++++++++++\n")
        file_seg.write("++++++++++++++++++++++++++++++\n")

    file.close()
    file_seg.close()

    # sql = "select id, institution ,cleaninfo from teacherdata WHERE length(cleaninfo)>0"
    # info_list = dbs.getDics(sql)
    # ext = Extractor()
    # for item in info_list:
    #     ext.set_text(item["cleaninfo"])
    #     cols, blocks = ext.get_texts()
    #     if not cols:
    #         continue
    #     sql_3 = "insert into texts(text, col, teacher_id) values(%(text)s, %(col)s, %(teacher_id)s)"
    #     for i in range(0, len(blocks)):
    #         params_dict = {"text": blocks[i], "col": cols[i], "teacher_id": item["id"]}
    #         dbs.exe_sql(sql_3, params=params_dict)
    # pass
