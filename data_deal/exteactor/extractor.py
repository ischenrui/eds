# 提取正文

import re

reBody = r'<body.*?>[\s\S]*?<\/body>'
reCOMM = r'<!--.*?-->'
reTRIM = r'<{0}.*?>[\s\S]*?<\/{0}>'
reTAG = r'<[\s\S]*?>|[ \t\r\f\v]'
reLINK = r'<a.*?>[\s\S]*?<\/a>'
reStyle = r'&nbsp;'
reS = r'<.*?>'


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
        self.body = re.sub(r' ', "", self.body)

    # 提取正文
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
        if e > s + 10:
            e = s + 10
        return "\n".join([txt_list[i] for i in range(s, e)])

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
                print("==+++++++::::%s" % txt_list[i])
                s = i
                break
        if e > s + 30:
            e = s + 30
        return "\n".join([txt_list[i] for i in range(s, e)])

    def get_context(self, name=""):
        # bo = re.findall(reBody, self.htmlText)
        # if len(bo) == 0:
        self.body = self.htmlText
        # else:
        #     self.body = bo[0]
        self.process_tags()
        return self.process_blocks_from_name(name)

    def set_html(self, html_text):
        self.htmlText = html_text


if __name__ == "__main__":
    # text = open("tttt.txt", encoding="utf-8").read()
    # ext = Extractor(html_text=text, block_size=20)
    # print(ext.get_context())
    pass
