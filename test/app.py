# encoding=utf-8
from flask import Flask, render_template, request, flash, send_from_directory, make_response, redirect, url_for
import json
import jieba
from gensim.models import word2vec
from gensim.models import KeyedVectors
import gensim
import os
import Crawler
import paddle
import jieba.posseg as pseg
from gensim.models import word2vec
from gensim.models import KeyedVectors
app = Flask(__name__)

namelist = []
genderlist = []
nationlist = []
homelandlist = []
reasonlist = []
courtlist = []
other_nlist = []
vlist = []
adjlist = []

def biaozhu(filename):
    fenhang(filename)
    qubiaodian()
    cikufenci()
    runmodel()

def fenhang(filename):
    stopwords = [line.strip() for line in open(r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\stopword.txt', encoding='UTF-8').readlines()]
    # p = open(r"../文本数据集/fenci.txt", 'r', encoding ='utf-8')
    with open(os.path.join('files', filename), encoding='utf-8') as x:
        s = x.readlines()
        x.close()
    m = open(r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\分行result.txt', 'w', encoding='utf-8')

    for line in s:
        words = pseg.cut(line)
        # words=pseg.cut(line, use_paddle=True)
        for word, flag in words:
            if word == '' or word == ' ':
                continue
            if word == '。':
                m.write("\n")
            else:
                m.write(word)
    m.close()


def qubiaodian():
    signs = [line.strip() for line in open(r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\sign.txt', encoding='utf-8').readlines()]

    m=open(r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\分行result.txt', 'r', encoding ='utf-8')
    q = open(r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\去标点result.txt', 'w', encoding ='utf-8')

    for line in m.readlines():
        line = jieba.cut(line)
        #words=pseg.cut(line, use_paddle=True)
        sw = ''
        for word in line:
            flag = 0
            for sh in signs:
                if sh == word:
                    flag = 1
                    break
            if flag == 0:
                sw = sw + word
        q.write(sw)

    q.write('\n')
paddle.enable_static()
pseg.enable_paddle()
def cikufenci():
    def read_in_chunks(filePath, chunk_size=1024*1024):
        file_object = open(filePath,'r',encoding='utf-8')
        while True:
            chunk_data = file_object.read(chunk_size)
            if not chunk_data:
                break
            yield chunk_data
    p = open(r"C:\Users\Administrator\Desktop\test ver5\test\文本数据集\去标点result.txt", 'r', encoding ='utf-8')
    q = open(r"C:\Users\Administrator\Desktop\test ver5\test\文本数据集\fenci_result.txt", 'a', encoding ='utf-8')
    dict=open(r"C:\Users\Administrator\Desktop\test ver5\test\文本数据集\dict.txt", 'w', encoding ='utf-8')
    nounfile = open(r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\名词.txt', 'w', encoding ='utf-8')
    verbfile= open(r"C:\Users\Administrator\Desktop\test ver5\test\动词.txt", 'w',encoding ='utf-8')
    adjfile=open(r"C:\Users\Administrator\Desktop\test ver5\test\形容词.txt", 'w', encoding ='utf-8')
    namefile=open(r"C:\Users\Administrator\Desktop\test ver5\test\当事人.txt", 'w', encoding ='utf-8')
    orgfile=open(r"C:\Users\Administrator\Desktop\test ver5\test\文本数据集\组织名.txt",'w',encoding='utf-8')
    placefile=open(r"C:\Users\Administrator\Desktop\test ver5\test\出生地.txt",'w',encoding='utf-8')
    spefile=open(r"C:\Users\Administrator\Desktop\test ver5\test\文本数据集\专有名词.txt",'w',encoding='utf-8')
    zufile= open(r"C:\Users\Administrator\Desktop\test ver5\test\文本数据集\族.txt", 'w',encoding ='utf-8')
    nounlist=[]
    verblist=[]
    adjlist=[]
    namelist=[]
    orglist=[]
    placelist=[]
    spelist=[]
    zulist=[]
    filePath=r"C:\Users\Administrator\Desktop\test ver5\test\文本数据集\去标点result.txt"
    #jieba.load_userdict("../文本数据集/dict.txt")
    #jieba.set_stop_words("../文本数据集/stopword.txt")
    text_split_no=[]
    stopwords = [line.strip() for line in open(r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\stopword.txt', encoding='UTF-8').readlines()]
    #print(text_split_no)
    #for word in text_split_no:
    #    print(word)
    #fW = open('../文本数据集/fenci_result.txt','w',encoding = 'UTF-8')
    #fW.write(' '.join(text_split_no))
    #fW.close()
    ##for chunk in read_in_chunks(filePath):
    #    words = pseg.cut(chunk,use_paddle=True)
    for line in open(r"C:\Users\Administrator\Desktop\test ver5\test\文本数据集\去标点result.txt", "r",encoding='utf-8'):
        if line == '\n':
            continue
        for word, flag in pseg.cut(line,use_paddle=True):
           # print(word, flag)
            if word not in stopwords:
                # if flag!='w':

                 q.write(str(word)+" ")
                 if flag in ['n', 'nt', 'nr', 'ns', 'r'] and word not in nounlist:
                    nounlist.append(word)

                 if flag in ['v'] and word not in verblist:
                    verblist.append(word)
                 if flag in ['a'] and word not in adjlist:
                    adjlist.append(word)
                 if flag in ['PER'] and word not in namelist:
                    namelist.append(word)
                 if word.endswith('法院') and word not in orglist:
                    orglist.append(word)
                 if flag in ['LOC'] and word not in placelist:
                    placelist.append(word)
                 if word.endswith("罪") and word not in spelist:
                    spelist.append(word)
                 if word.endswith("族"):
                     zulist.append(word)
        q.write("\n")
    for word in nounlist:
            nounfile.write(str(word) + " ")
    for word in verblist:
            verbfile.write(str(word) + " ")
    for word in adjlist:
            adjfile.write(str(word) + " ")
    for word in namelist:
            namefile.write(str(word) + " ")
    for word in orglist:
            orgfile.write(str(word) + " ")
    for word in placelist:
            placefile.write(str(word) + " ")
    for word in spelist:
            spefile.write(str(word) + " ")
    for word in zulist:
            zufile.write(str(word) + " ")

    q.write('\n')


def train():
    sentences=word2vec.LineSentence(r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\fenci_result.txt')

    model=word2vec.Word2Vec(sentences,hs=1,min_count=1,window=5,vector_size=100,epochs=400)
    model.save('./newmodel')


def runmodel():
    model = gensim.models.Word2Vec.load('newmodel')  # 案由  涉嫌

    def sortrank(m, ciku):
        dict = {}  # dict为排序时用到的字典
        outcome = []  # 返回的结果列表
        for i in ciku:
            dict[i] = model.wv.similarity(m, i)  # similarity为计算相似度的函数
        temp = sorted(dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        for i in range(0, len(temp)):
            outcome.append(temp[i][0])
        return outcome

    def readfile_sort(filepath1, filepath2, key):  # C:\Users\Administrator\Desktop\NLP\导出结果数据集\出生地名.txt
        nouns = []  # ',\'
        file1 = open(filepath1, 'w', encoding='utf-8')
        file2 = open(filepath2, encoding='utf-8')
        for line in file2.readlines():
            words = line.split(" ")
            for word in words:
                if word != '':
                    nouns.append(word)

        nouns = sortrank(key, nouns)
        for word in nouns:
            file1.write(word + " ")

   # file1 = open(r'C:\Users\Administrator\Desktop\test ver5\test\出生地.txt', 'w', encoding='utf-8')
    file2 = open(r'C:\Users\Administrator\Desktop\test ver5\test\相关法院.txt', 'w', encoding='utf-8')
    file3 = open(r'C:\Users\Administrator\Desktop\test ver5\test\民族.txt', 'w', encoding='utf-8')
    file4 = open(r'C:\Users\Administrator\Desktop\test ver5\test\案由.txt', 'w', encoding='utf-8')

   # readfile_sort(r'C:\Users\Administrator\Desktop\test ver5\test\出生地.txt', r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\地名.txt', "户籍所在地")
    readfile_sort(r'C:\Users\Administrator\Desktop\test ver5\test\相关法院.txt', r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\组织名.txt', "法院")
    # readfile_sort('../导出结果数据/当事人.txt','../文本数据集/人名.txt',"法院")
    readfile_sort(r'C:\Users\Administrator\Desktop\test ver5\test\案由.txt', r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\专有名词.txt', "涉嫌")
    readfile_sort(r'C:\Users\Administrator\Desktop\test ver5\test\民族.txt', r'C:\Users\Administrator\Desktop\test ver5\test\文本数据集\族.txt', "汉族")
    # model=gensim.models.Word2Vec.load('newmodel')#案由  涉嫌

def tolist(filename):
    f = open(filename + '.txt', mode='r', encoding='utf-8')
    list = f.readline().split(" ")
    words =[]
    for word in list:
        if word!="":
            words.append(word)
    return words
@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    global namelist
    global genderlist
    global nationlist
    global homelandlist
    global reasonlist
    global courtlist
    global other_nlist
    global vlist
    global adjlist
    global s
    if request.method == 'POST':
        content1 = request.form.get('content')
        f = request.files['file']
        if f:
            filename = f.filename
            f.save(os.path.join('files', filename))  # 保存文件
            with open(os.path.join('files', filename), encoding='utf-8') as x:
                #s = x.read()
                s=x.read()
                x.close()
            if content1:
                return "请选择其中一种方式"
        else:
            s = content1
        biaozhu(filename)
        namelist = tolist('当事人')
        genderlist = ['男','女']
        nationlist = tolist('民族')
        homelandlist = tolist('出生地')
        reasonlist = tolist('案由')
        courtlist = tolist('相关法院')
        other_nlist = []
        vlist = tolist('动词')
        adjlist = tolist('形容词')
        return render_template('index.html', namelist=namelist, genderlist=genderlist, nationlist=nationlist,
                               homelandlist=homelandlist, reasonlist=reasonlist, courtlist=courtlist,
                               other_nlist=other_nlist, vlist=vlist, adjlist=adjlist)
    return render_template('index.html', namelist=namelist, genderlist=genderlist, nationlist=nationlist,
                           homelandlist=homelandlist, reasonlist=reasonlist, courtlist=courtlist,
                           other_nlist=other_nlist, vlist=vlist, adjlist=adjlist)


@app.route('/auto', methods=['GET', 'POST'])
def auto():
    start = request.form.get('start')
    end = request.form.get('end')
    if (start != None) & (end != None):
        Crawler.mainPro(start, end)
    return render_template('auto.html')


@app.route('/introduce', methods=['GET', 'POST'])
def introduce():
    filename = 'introduce.pdf'
    directory = os.getcwd()  # 假设在当前目录
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response


@app.route('/delv/<v>', methods=['GET', 'POST'])
def delv(v):
    global vlist
    vlist.remove(v)
    return redirect(url_for('hello_world'))


@app.route('/deladj/<adj>', methods=['GET', 'POST'])
def deladj(adj):
    global adjlist
    adjlist.remove(adj)
    return redirect(url_for('hello_world'))


@app.route('/deln/<n>', methods=['GET', 'POST'])
def deln(n):
    global other_nlist
    other_nlist.remove(n)
    return redirect(url_for('hello_world'))


@app.route('/changename/<n>', methods=['GET', 'POST'])
def changename(n):
    global namelist, other_nlist
    namelist.remove(n)
    other_nlist.insert(0, n)
    return redirect(url_for('hello_world'))


@app.route('/changegender/<n>', methods=['GET', 'POST'])
def changegender(n):
    global genderlist, other_nlist
    genderlist.remove(n)
    other_nlist.insert(0, n)
    return redirect(url_for('hello_world'))


@app.route('/changenation/<n>', methods=['GET', 'POST'])
def changenation(n):
    global nationlist, other_nlist
    nationlist.remove(n)
    other_nlist.insert(0, n)
    return redirect(url_for('hello_world'))


@app.route('/changehomeland/<n>', methods=['GET', 'POST'])
def changehomeland(n):
    global homelandlist, other_nlist
    homelandlist.remove(n)
    other_nlist.insert(0, n)
    return redirect(url_for('hello_world'))


@app.route('/changereason/<n>', methods=['GET', 'POST'])
def changereason(n):
    global reasonlist, other_nlist
    reasonlist.remove(n)
    other_nlist.insert(0, n)
    return redirect(url_for('hello_world'))


@app.route('/changecourt/<n>', methods=['GET', 'POST'])
def changecourt(n):
    global courtlist, other_nlist
    courtlist.remove(n)
    other_nlist.insert(0, n)
    return redirect(url_for('hello_world'))


# 以下是添加
@app.route('/addname/<n>', methods=['GET', 'POST'])
def addname(n):
    global namelist, other_nlist
    other_nlist.remove(n)
    namelist.append(n)
    return redirect(url_for('hello_world'))


@app.route('/addgender/<n>', methods=['GET', 'POST'])
def addgender(n):
    global genderlist, other_nlist
    other_nlist.remove(n)
    genderlist.append(n)
    return redirect(url_for('hello_world'))


@app.route('/addnation/<n>', methods=['GET', 'POST'])
def addnation(n):
    global nationlist, other_nlist
    other_nlist.remove(n)
    nationlist.append(n)
    return redirect(url_for('hello_world'))


@app.route('/addhomeland/<n>', methods=['GET', 'POST'])
def addhomeland(n):
    global homelandlist, other_nlist
    other_nlist.remove(n)
    homelandlist.append(n)
    return redirect(url_for('hello_world'))


@app.route('/addreason/<n>', methods=['GET', 'POST'])
def addreason(n):
    global reasonlist, other_nlist
    other_nlist.remove(n)
    reasonlist.append(n)
    return redirect(url_for('hello_world'))


@app.route('/addcourt/<n>', methods=['GET', 'POST'])
def addcourt(n):
    global courtlist, other_nlist
    other_nlist.remove(n)
    courtlist.append(n)
    return redirect(url_for('hello_world'))


@app.route('/downloadmark', methods=['GET', 'POST'])
def downloadmark():
    global namelist
    global genderlist
    global nationlist
    global homelandlist
    global reasonlist
    global courtlist
    global other_nlist
    global vlist
    global adjlist
    biaozhu = {
        '当事人': namelist,
        '性别': genderlist,
        '民族': nationlist,
        '出生地': homelandlist,
        '案由': reasonlist,
        '相关法院': courtlist
    }
    data = json.dumps(biaozhu, ensure_ascii=False)
    response = make_response(data)
    response.headers['content-type'] = 'application/octet-stream;charset=utf8'
    response.headers['content-disposition'] = 'attachment;filename=mark.json'
    return response


@app.route('/downloadtxt', methods=['GET', 'POST'])
def downloadtxt():
    global s
    response = make_response(s)
    response.headers["Content-Disposition"] = "attachment; filename=case.txt"
    return response


if __name__ == '__main__':
    app.run(debug=True)

