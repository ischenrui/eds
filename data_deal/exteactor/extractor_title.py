# 提取正文

import re
from util import dbs

reBody = r'<body.*?>[\s\S]*?<\/body>'
reCOMM = r'<!--.*?-->'
reTRIM = r'<{0}.*?>[\s\S]*?<\/{0}>'
reTAG = r'<[\s\S]*?>|[ \t\r\f\v]'
reLINK = r'<a.*?>[\s\S]*?<\/a>'
reStyle = r'&nbsp;'
reS = r'<.*?>'
reSpace = r' '


class Extractor:
    def __init__(self, html_text="", block_size=10):
        self.htmlText = html_text
        self.blockSize = block_size
        self.ctexts = []
        self.cblocks = []
        self.body = ""
        self.start = 0
        self.end = 0

    def process_tags(self):
        # self.body = re.sub(reCOMM, "", self.body)
        # self.body = re.sub(reLINK, "", self.body)
        self.body = re.sub(reTRIM.format("script"), "", re.sub(reTRIM.format("style"), "", self.body))
        # self.body = re.sub(reTAG, "", self.body)
        self.body = re.sub(reS, "", self.body)
        self.body = re.sub(reStyle, "", self.body)
        self.body = re.sub(reSpace, "", self.body)

    def process_blocks(self):
        self.ctexts = self.body.split("\n")
        text_lens = [len(txt) for txt in self.ctexts]
        self.cblocks = [0]*(len(self.ctexts) - self.blockSize - 1)
        lines = len(self.ctexts)
        for i in range(self.blockSize):
            self.cblocks = list(map(lambda x, y: x + y, text_lens[i: lines - 1 - self.blockSize + i], self.cblocks))
        max_textl = max(self.cblocks)
        start = end = self.cblocks.index(max_textl)
        while start > 0 and self.cblocks[start] > min(text_lens):
            start -= 1
        while end < lines - self.blockSize - 1 and self.cblocks[end] > min(text_lens):
            end += 1
        return "\n".join([txt for txt in self.ctexts[start:end] if not txt == ""])

    def process_blocks_from_name(self, name):

        self.ctexts = self.body.split("\n")
        txt_list = [txt for txt in self.ctexts if not txt == ""]
        s = 0
        e = len(txt_list)
        name = re.sub(pattern=" ", string=name, repl="")
        for i in range(s, e):
            if txt_list[i] == name or name in txt_list[i]:
                print("==+++++++::::%s" % name)
                print(txt_list[i])
                s = i
                break
        if e > s + 15:
            e = s + 15
        return [txt_list[i] for i in range(s, e)]

    def process_blocks_title(self):
        bo = re.findall(reBody, self.htmlText)
        if len(bo) == 0:
            bo = self.htmlText
        else:
            self.body = bo[0]
        self.process_tags()
        self.ctexts = self.body.split("\n")
        txt_list = [txt for txt in self.ctexts if not txt == ""]
        s = 0
        e = len(txt_list)
        for i in range(s, e):
            if "职称" in txt_list[i] or "职" in txt_list[i] and "称" in txt_list[i+1]:
                print("%s" % txt_list[i])
                s = i
                break
        if e > s + 10:
            e = s + 10
        return [txt_list[i] for i in range(s, e)]

    def get_context(self, name=""):
        self.body = self.htmlText
        self.process_tags()
        if name == "":
            return self.process_blocks_title()
        return self.process_blocks_from_name(name)

    def set_html(self, html_text):
        self.htmlText = html_text


if __name__ == "__main__":
    title_dict = ["教授", "副教授", "讲师", "助教", "助理教授", "副研究员", "助理研究员", "研究员", "高级工程师", "高级实验师", "高工", "工程师", "实验师"]
    ex = Extractor()
    sql = "select * from teacherdata"
    teacher_list = dbs.getDics()
    for item in teacher_list:
        if not item["original_html"]:
            continue
        html_text = re.sub(pattern="<br>", repl="", string=item[6])
        html_text = re.sub(pattern=">", repl=">\n", string=html_text)
        html_text.strip(" ")
        ex.set_html(html_text)
        texts = ex.get_context(item["name"])
        # texts = ex.get_context()
        title = ""
        for text in texts:
            if title_dict[0] in text and title_dict[1] not in text:
                title = title_dict[0]
            elif title_dict[1] in text:
                title = title_dict[1]
            elif title_dict[2] in text:
                title = title_dict[2]
            elif title_dict[3] in text:
                title = title_dict[3]
            elif title_dict[4] in text:
                title = title_dict[4]
            elif title_dict[5] in text:
                title = title_dict[5]
            elif title_dict[6] in text:
                title = title_dict[6]
            elif title_dict[7] in text:
                title = title_dict[7]
            elif title_dict[8] in text:
                title = title_dict[8]
            elif title_dict[9] in text:
                title = title_dict[9]
            elif title_dict[10] in text:
                title = title_dict[8]
            elif title_dict[11] in text:
                title = title_dict[11]
            elif title_dict[12] in text:
                title = title_dict[12]

            if title:
                print(title)
                update_sql = "update eteacher set title='" + title + "' where _id = " + item["id"]
                dbs.exe_sql(update_sql)
                break

    pass
