
import os
import re
from util import dbs
import jieba
import jieba.posseg as pseg

DIR = os.path.dirname(os.path.abspath(__file__))

jieba.load_userdict(DIR + "\\dicts\\userdict.txt")

stopwords = {}.fromkeys([line.rstrip() for line in open(DIR + "\\dicts\\stopword.txt", encoding='utf-8')])
stop_flag = ['b', 'eng']

reWords = r'研究方向|研究领域'


class Word:
    def __init__(self, word=None, flag=None):
        self.word = word
        self.flag = flag


class Extractor:
    def __init__(self, orginal_text="", block_size=30):
        self.orginal_text = orginal_text
        self.blockSize = block_size
        self.col = 0
        self.blocks = ""

    def process_blocks(self):
        sentence_list = self.orginal_text.split('\n')
        i = 0
        length = len(sentence_list)
        while i < length:
            t = re.search(reWords, sentence_list[i], flags=0)
            if not t:
                i += 1
                continue
            text = ""
            col = i
            for j in range(i, len(sentence_list)):
                text += sentence_list[j]
                if len(text) > self.blockSize or j == len(sentence_list)-1:
                    i = j
                    self.blocks = text
                    self.col = col
                    break
            if not self.blocks == "":
                break
            i += 1
            pass

        print(self.blocks)
        # return ";".join(self.col) + "\n" + "\n".join(self.blocks)
        return self.col, self.blocks

    def process_seg(self):
        self.process_blocks()
        te = re.findall(r'研究方向.*|研究领域.*', self.blocks)
        if not len(te) > 0:
            return []
        segs = pseg.cut(te[0])
        segs = [s for s in segs if s.flag not in stop_flag]
        words = []
        w = ""
        i = 0
        for wo in segs:
            if wo.flag == 'x' and wo.word != "-" or wo.word in stopwords:
                if w == "":
                    i += 1
                    continue
                words.append(w)
                w = ""
                i += 1
                continue
            w += wo.word
            i += 1
        if not w == "":
            words.append(w)
        return words

    def get_texts(self):
        return self.process_blocks()

    def set_text(self, orginal_text):
        self.orginal_text = orginal_text
        self.col = 0
        self.blocks = ""


if __name__ == "__main__":
    sql = "select id, institution, cleaninfo from teacherdata WHERE length(cleaninfo)>0"
    info_list = dbs.getDics(sql)

    ext = Extractor()
    institution = info_list[0]["institution"]
    num = 0
    count = 0
    dir = DIR + "\\Step7\\"
    file = open(dir + str(num) + ".txt", "w", encoding="utf-8")
    for item in info_list:
        if not item["institution"] == institution:
            num += 1
            institution = item["institution"]
            print(institution)
            file.close()
            file = open(dir + str(num) + ".txt", "w", encoding="utf-8")
        ext.set_text(item["cleaninfo"])
        cols, te = ext.get_texts()
        # te = "\t".join(ext.process_seg())
        if len(te) > 0:
            segs = pseg.cut(te)
            file.write("%s\n" % item["id"])
            file.write("%s\n" % (" ".join([w.word + '/' + w.flag for w in segs])))
            file.write("++++++++++++++++++++++++++++++\n")
            # file.write("%s\n" % item["id"])
            # file.write("%s\n" % te)
            # file.write("++++++++++++++++++++++++++++++\n")
            count += 1

    file.close()
