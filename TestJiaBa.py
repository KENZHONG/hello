#!/usr/bin/env python
#-*-coding:utf8-*-

import jieba
import jieba.posseg as psg
import pandas as pd
import operator
import math




class classifier:
    def __init__(self, getfeatures, filename = None):
        self.fc={}
        self.cc={}
        self.getfeatures = getfeatures
    ###每个单词在不同类中的数量，如{‘文化’:{'8200':10, '8293':5}..}
    def incf(self,f,cat):
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat,0)
        self.fc[f][cat] += 1

    def incc(self, cat):
        self.cc.setdefault(cat,0)
        self.cc[cat] += 1

    def fcount(self,f,cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    def catcount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])

    def totalcount(self):
        return sum(self.cc.values())

    def categories(self):
        return self.cc.keys()

    def train(self, item, cat):
        features = self.getfeatures(item)
        for f in features:
            self.incf(f,cat)
        self.incc(cat)

    def fprob(self,f,cat):
        if self.catcount(cat) == 0:
            return 0
        return self.fcount(f,cat)/self.catcount(cat)

    def weightedprob(self, f, cat, prf, weight=1.0, ap = 0.5):
        basicprob = prf(f,cat)
        totals = sum([self.fcount(f,c) for c in self.categories()])
        bp = ((weight*ap) + (totals*basicprob))/(weight+totals)
        return bp


###贝叶斯定理 P(A|B) = P(B|A)*P(A)/P(B)
class naivebays(classifier):
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.thresholds={}

    def setthreshold(self,cat,t):
        self.thresholds[cat] = t

    def getthreshold(self,cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]

    def docprob(self,item,cat):
        features=self.getfeatures(item)

        p=1
        for f in features:
            p *= self.weightedprob(f,cat,self.fprob)
        return p

    def prob(self,item,cat):
        catprob = self.catcount(cat)/self.totalcount()
        docprob = self.docprob(item,cat)
        print cat,catprob,docprob,docprob*catprob
        return docprob*catprob

    def classify(self, item, default=None):
        probs={}
        max = 0.0
        for cat  in self.categories():
            probs[cat] = self.prob(item,cat)
            #print cat,probs[cat]
            if probs[cat]>max:
                max=probs[cat]
                best=cat
        for cat in probs:
            if cat == best:
                continue
            if probs[cat]*self.getthreshold(best)> probs[best]:
                return default
        return best


class fisherclassifier(classifier):
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.minimums={}

    def setminimum(self,cat,min):
        self.minimums[cat]=min

    def getminimum(self,cat):
        if cat not in self.minimums:
            return 0
        return self.minimums[cat]

    def cprob(self,f,cat):
        clf=self.fprob(f,cat)
        if clf==0:
            return 0
        freqsum= sum([self.fprob(f,c) for c in self.categories()])

        p = clf/(freqsum)
        return p

    def invchi2(self,chi,df):
        m = chi/2.0
        sum=term=math.exp(-m)
        for i in range(1, df//2):
            term *= m/i
            sum += term
        return min(sum, 1.0)

    def fisherprob(self, item,cat):
        p=1
        features=self.getfeatures(item)
        for f in features:
            p*=(self.weightedprob(f,cat,self.cprob))

        fscore=-2*math.log(p)
        return self.invchi2(fscore,len(features)*2)

    def classify(self,item,default=None):
        best=default
        max=0.0
        for c in self.categories():
            p = self.fisherprob(item,c)
            if p>self.getminimum(c) and p>max:
                best=c
                max=p
        return best

def ScanFile(file):
    file_data = pd.read_table('D:\\tmp\\'+file, sep = '|',index_col = 'com_buss_no')
    return file_data




def StringPro(str):
    global words
    for x in psg.cut(str):
        if ( words.has_key(x.word)):
            words[x.word] += 1
        else:
            if x.flag == 'x' or x.flag =='uj' or x.flag == 'c' or x.flag == 'p' or x.flag == 't':
                continue
            words[x.word] = 1
    return

def getwords(str):
    wordlist = []
    for x in psg.cut(str):
        if x.flag == 'x' or x.flag =='uj' or x.flag == 'c' or x.flag == 'p' or x.flag == 't':
                continue
        wordlist.append(x.word)
    ####distinct 每个单词
    return dict([w,1] for w in wordlist)

#cl=classifier(getwords)

def FilePro(file_data,cat=None):
    #global cl
    #print set(file_data.index)
    #cl = classifier(getwords)
    # cl = naivebays(getwords)
    cl = fisherclassifier(getwords)
    #print set(file_data.index)
    for catitem in set(file_data.index):
        #catitemstr = str(catitem).decode('utf8')
        catitemstr = catitem
        #print catitemstr
        for x in file_data.ix[catitemstr]['com_buss']:

            com_buss = x.decode('utf8')
            # print com_buss
            #print str
            #StringPro(str)
            # print com_buss, catitemstr
            cl.train(com_buss, catitemstr)
    return cl


def LoadToFile(test_file, cl, ret_file):
    with open(ret_file,'w+') as f:
        for i in range(len(test_file['com_id'])):
            test_data = test_file['com_buss'].values[i].decode('utf8')
            lines = '%s|%s|\n' % (test_file['com_id'].values[i], cl.classify(test_data, default='unknown'))
            f.writelines(lines)
    return


def main():
    data = ScanFile('haha_comedu_train.txt')
    # FilePro( data.ix['8290'])

    # cl = classifier(getwords)
    # for x in cl.getfeatures(u'学前教育'):
    #     print x


    cl = FilePro( data )

    test_file = ScanFile('fo2.txt')
    LoadToFile(test_file,cl,'D:\\tmp\\ret.txt')


    # print  test_file['com_buss']
    # print len(test_file['com_id'])
    # print type(test_file['com_buss'])
    # print test_file['com_buss'].values[0]

    # for i in range(len(test_file['com_id'])):
    #     test_data = test_file['com_buss'].values[i].decode('utf8')
    #     print test_file['com_id'].values[i],cl.classify(test_data, default='unknown')


    #print cl.classify(u'中小学',default='unknown')

    # print cl.prob(u'文化',u'8293')
    # print cl.prob(u'文化',u'8200')
    # print cl.fcount(u'文化',u'8293')
    # print cl.fprob(u'学前教育',u'8210')
    # print cl.fprob(u'学前教育',u'8293')
    # print cl.weightedprob(u'学前教育',u'8210', cl.fprob)
    # print cl.weightedprob(u'学前教育',u'8293', cl.fprob)





    # print cl.fc
    # for x in cl.fc.keys():
    #     print x


    # cl = classifier(getwords)
    # cl.train(u'教育文化',u'8200')
    # cl.train(u'教育',u'8200')
    # cl.train(u'文化艺术培训', u'8293')
    # print cl.fcount(u'教育',u'8200')

    #print words
    #print words[u'教育']

    # sorted_words = sorted( words.iteritems(), key=operator.itemgetter(1),reverse=True)
    # print type(sorted_words)
    # for x in sorted_words:
    #     print x[0],x[1]

    # for x in words.keys():
    #     print
    #print data['com_buss'][0]
    #str = data['com_buss'][0].decode('utf8')
    #print str
    #StringPro(str)
    #print words




    # s = u'根据珠海财政业务管理需要，提出国土出让金征收纳入非税收入管理系统统一管理，并要求土地出让资金能当天划入专户（当前一般非税收入是T+1日的模式）'
    # # cut = jieba.cut(s)
    # # cutstr =  ','.join(cut)
    # # cutpsg =  psg.cut(s)
    #
    # # print [(x.word, x.flag) for x in psg.cut(s)]
    #
    # # print cutstr.decode('utf')
    # # print cutstr
    # # print isinstance(cutstr, unicode)
    #
    # wordlist = []
    #
    # for x in psg.cut(s):
    #     #print x.word, x.flag
    #     wordlist.append(x.word)
    # print len(wordlist)
    #
    # print set(wordlist)
    # print isinstance(x.word[0],unicode)
    # print str(list(cut)).encode('utf8')

    # with  open('D:\\tmp\\word.txt','w') as f:
    #     for x in psg.cut(s):
    #         print x.flag
    #         f.writelines(x.word.encode('utf8')+ '|' + x.flag.encode('utf8') +"\n")
            # f.write(x.flag)
        # f.write(cutstr.encode('utf8'))
        # for word in x.word:
        #     f.write(word.encode('GBK'))


if __name__ == '__main__':
    # s = u'根据珠海财政业务管理需要，提出国土出让金征收纳入非税收入管理系统统一管理，并要求土地出让资金能当天划入专户（当前一般非税收入是T+1日的模式）'
    # for x in psg.cut(s):
    #     print x.word, x.flag
    main()