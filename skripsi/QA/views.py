# 14650036 - DINDA OCKTA N  - INFORMATICS ENGGINERRING
# UIN MAULANA MALIK IBRAHIM MALANG

# import ssl
#----------------------- DJANGO -----------------------
from __future__         import unicode_literals
from django.shortcuts   import render
from django.template    import loader
from django.http        import HttpResponse
from QA.models          import question as Ques
from QA.models          import classification_ephyra as Clas


#----------------------- PREPROCESSING -----------------------
import nltk
# nltk.download()
from nltk.tokenize      import sent_tokenize, word_tokenize #tokonize
from nltk.corpus        import stopwords #stopwords
from nltk.stem          import PorterStemmer #stemming
from nltk.corpus        import state_union #POS
from nltk.tokenize      import PunktSentenceTokenizer #POS
from nltk.stem          import WordNetLemmatizer  #lemmatizer
from nltk.corpus        import stopwords
from nltk.tag           import StanfordNERTagger #NER
from nltk.tag.stanford  import StanfordNERTagger
from nltk               import ngrams #ngrams

#----------------------- BABELNET -----------------------
import  urllib3
import  requests
# from    urllib.request  import urlopen
import  json, ast
import  gzip
# from    urllib.request  import urlopen
import  re
 
#----------------------- DBPEDIA & WIKIPEDIA-----------------------
from    SPARQLWrapper    import SPARQLWrapper, JSON
import  rdflib
import  wikipediaapi


#----------------------- ETC -----------------------
import  json
import  math    #LOGaritma, EXPonen, SQRT
import  numpy   #tf idf - make a matrix/array , transpose
import  random
# from    bs4             import BeautifulSoup
import  time


start                   = 0
Question                = ""
output_preprocessing    = {}
Titless                 = ""
output_title            = {}

def skripsi(request):
    return render(request, 'layout/base.php')


def semua(request):
    global Question 
    global start 
    global output_preprocessing 
    global output_title  
    global Titless
    start = time.time()  
    if request.method   == 'POST':
        Question                = request.POST["question"]
        output_preprocessing    = dict(preprocessing(Question))
        if output_preprocessing['key_word'] ==[]:
            return render(request,'layout/base.php',{
                'wrong_topics' : Question
            })

        output_title            = dict(title_wikipedia(" ".join(output_preprocessing['key_word'])))
        if len(output_title['topics']) >1 :
            return render(request,'layout/base.php',{
                'option_topics' : output_title['topics']
            })

        else:
            Titless = output_title['topics'][0]
            return proses(request)
    else:
        return render(request, 'layout/base.php')


def proses(request):
    output_graph_word   = dict(word_graph_babelnet(output_preprocessing["lexical_word"]))
    keyy                = []
    key                 = []
    wPrev               = None
    # print (output_preprocessing["lexical_word"])
    # if output_preprocessing["lexical_word"] != None:
    #     for op in output_preprocessing["lexical_word"]:
    #         for i in word_tokenize(Titless):
    #             if i.lower() != op.lower():
    #                 if op not in key:
    #                     key.append(op.lower())
            

    # if output_graph_word['all_word'] != None:
    #     for ogw in output_graph_word['all_word']:
    #         key.append(ogw)
    
    
    if output_preprocessing["lexical_word"] != None:
        for op in output_preprocessing["lexical_word"]:
            for i in word_tokenize(Titless):
                if i.lower() != op.lower():
                    if op not in keyy:
                        keyy.append(op.lower())
            

    if output_graph_word['all_word'] != None:
        for ogw in output_graph_word['all_word']:
            keyy.append(ogw)
    
    for w in sorted(set(keyy)):
        if not wPrev or (wPrev and not w.startswith(wPrev)):
            key.append(w)
        wPrev = w
        
    # print(len(keyy)," ",keyy)
    # print("-------------key----\n",len(key)," ",key)
    # key=keyy
    output_CNN              = dict(cnn(output_preprocessing['question_word'],output_preprocessing["detectNER"],key))
    print("cnn : ", output_CNN['class'])
    if output_CNN['class']!=[]:
        for pc in numpy.array(output_CNN['class']):
            key.append(pc[1].lower())
    
    answer_sparql           = dict(check_answer_sparql(Titless,key, output_preprocessing["lexical_word"]))
    # answer_cosinus          = dict(crawl_artikel(Question,Titless,output_preprocessing["lexical_word"],output_CNN['class']))
    answer_cosinus          = dict(crawl_artikel(Question,Titless,output_preprocessing["lexical_word"],output_graph_word['all_word']))

    end = time.time()
    print(end - start)
    return render(request, 'layout/base.php', {
        'Question'              : Question,
        'result_preprocessing'  : output_preprocessing,
        'result_graph_word'     : output_graph_word,
        'result_cnn'            : output_CNN,
        'result_title'          : output_title,
        'finally_title'         : Titless,
        'answer_sparql'         : answer_sparql,
        'answer_wikipedia'      : answer_cosinus,
    })

def get_topic(request):
    global output_title
    global Titless
    if request.method   == 'POST':
        Topic                = request.POST["topic"]
        output_title         = dict(title_wikipedia(Topic)) 
        if len(output_title['topics']) >1 :
            return render(request,'layout/base.php',{
                'option_topics' : output_title['topics']
            })

        else:
            output_preprocessing['result_ner']={"ENTITY":Titless}
            Titless = output_title['topics'][0]
            return proses(request)

        
def get_title(request):
    global Titless
    global output_title
    if request.method   == 'POST':
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        Titless                             = request.POST["titless"]
        output_preprocessing['result_ner']  = {"ENTITY":Titless}
        print(output_preprocessing['result_ner'])
        return proses(request)
       

def preprocessing(Question):  
    print("\n\n -----------------------,/------------------------------- PREPROCESSING --------------------------------------------")
    print(Question)
    
    print("\n\n------------------------------Hasil Tokenizing------------------------------")
    result_tokenizing   = []
    tokenize            = lambda x : ast.literal_eval(json.dumps(word_tokenize(x)))
    result_tokenizing   = tokenize(Question)
    print(result_tokenizing)

    
    print("\n\n------------------------------DELIMITER------------------------------")
    symbols             = ['!','@','#','$','%','^',"&",'*','(',')','-','_','=','+','[',']','{','}',';',':','"',"'",',','<','>','.','?','/',"|"]
    symbols             = set(symbols)
    result_delimiter    = [w for w in result_tokenizing if w not in symbols]
    print(result_delimiter)


    print("\n\n------------------------------STOPWORDS------------------------------")
    result_stopword     = []
    stop_words          = set(stopwords.words('english'))
    for rslt in result_delimiter:
        if rslt in stop_words:
            result_stopword.append(ast.literal_eval(json.dumps(rslt)))
    print(result_stopword)


    print("\n\n------------------------------POS------------------------------")
    result_POS          = []
    tagged              = nltk.pos_tag(result_delimiter)
    for p in tagged:
        result_POS.append(ast.literal_eval(json.dumps(p)))
    print(result_POS)
    
    
    print("\n\n------------------------------CHUNKED------------------------------")
    result_chuncked =[]
    # chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
    chunkGram           = r"""Chunk: {<.*>+}
                            }<.?|IN|DT|TO>+{"""
                            # }<.VBG?|IN|DT|TO>+{"""
    chunkParser         = nltk.RegexpParser(chunkGram)
    chunked             = chunkParser.parse(tagged)
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
        # subtree.leaves utk memetakan frase kata berdasarkan pos
        rslt   = ""
        for s in subtree.leaves():
            rslt+="%s " % s[0]
        result_chuncked.append(ast.literal_eval(json.dumps(rslt)))
    print(result_chuncked)
    
    
    print("\n\n------------------------------NER------------------------------")
    
    st          = StanfordNERTagger('/Users/ioa/CODE/S1-QAS_WIKIPEDIA-DGCNN/skripsi/assets/library/stanford-ner-2018-10-16/english.all.3class.distsim.crf.ser.gz',
                                    'C:/Users/ioa/CODE/S1-QAS_WIKIPEDIA-DGCNN/skripsi/assets/library/stanford-ner-2018-10-16/stanford-ner.jar', encoding='utf-8')  # CLASSPARTH
    result_ner  = []
    ner         = lambda x : ast.literal_eval(json.dumps(st.tag(x)))
    for rslt in result_chuncked:
        result_ner.append(ner(tokenize(rslt)))
    print(result_ner)


    #  --------------------- Identification Type - JSON ---------------------
    key_word        =[] 
    # Identification  ={"1.Question":[Question],"2.WQ":[],"4.OTHER":[]}
    Identification  ={"2.WQ":[],"4.OTHER":[]}
    word_question   =["what", "where","how","when","why","who"]
    word_ner        =["LOCATION","ORDINAL","PERSON","TIME","NUMBER","DURATION","ORGANIZATION", "CAUSE OF DEATH"]   
    try:
        for rs in result_ner:
         for it in rs:
            if it[0].lower() in word_question: #mencari kata tanya 
                Identification['2.WQ'].append(it[0].lower()) 
            elif it[1] in word_ner: #mencari kata2 yg memiliki NER
                if Identification.get("3.NER"):
                    if Identification["3.NER"].get(it[1]):
                        Identification["3.NER"][it[1]].append(it[0])
                        key_word.append(it[0])
                    else:
                        Identification["3.NER"]= {it[1]:[it[0]]}
                        key_word.append(it[0])
                else:
                    Identification["3.NER"]= {it[1]:[it[0]]}
                    key_word.append(it[0])
            else:
                Identification["4.OTHER"].append(it[0])

        if  "3.NER" not in Identification:
            Identification["3.NER"]= {}
        print(json.dumps(Identification,sort_keys=True, indent=2)) 
       
    except Exception as e: print(e)

    # key_word    = json.dumps(Identification["3.NER"][:])
    lexical_word  = Identification["4.OTHER"]
    detectNER=[]
    if Identification.get("3.NER"):
        for k,v in Identification["3.NER"].items():
            detectNER.append(k)
            


    print("\n\n------------------------------LEMMATIZATION------------------------------")
    lemmatizer          = WordNetLemmatizer()
    result_lemmatization= []
    for l in lexical_word:
        result_lemmatization.append(ast.literal_eval(json.dumps(lemmatizer.lemmatize(l))))
    print(result_lemmatization)

    # print("\n\n------------------------------STEMMING------------------------------")
    # ps                  = PorterStemmer()
    # result_stemming     = []
    # for s in result_lemmatization:
    #     result_stemming.append(ast.literal_eval(json.dumps(ps.stem(s))))
    # print(result_stemming)

    
    # lemste = numpy.unique(result_lemmatization+result_stemming)
    # lemstem = list(set(lemste)-set(result_stopword))
    lemstem = list(set(result_lemmatization)-set(result_stopword))
    print(lemstem)

    
    res = {
        'question_word'         : Identification['2.WQ'],
        'result_tokenizing'     : result_delimiter,
        'result_stopword'       : result_stopword,
        'result_POS'            : result_POS,
        'result_chuncked'       : result_chuncked,
        'result_ner'            : Identification["3.NER"],
        # 'result_lemmatization'  : result_stemming,
        'key_word'              : key_word,
        'lexical_word'          : lemstem,
        'Identification'        : Identification,
        'detectNER'             : detectNER,
    }
    return res
    # return HttpResponse("cek di cmd" )
  

def word_graph_babelnet(leksical_word):
    print("\n\n ------------------------------------------------------ BABELNET --------------------------------------------")
    service_url     = "https://babelnet.io/v5/getSenses"
    lang            = "EN"
    keyAPI          = "f409b37a-a4a2-4b8d-a56a-6599ee701b50"
    no              = 0    
    graph_word      = []
    for lemma in leksical_word:
        params      = "lemma="+lemma+"&"+"searchLang="+lang+"&"+"key="+keyAPI
        url	        = service_url + '?' + params
        r           = requests.get(url=url) 
        graph_word.append({lemma:[]})  
        for result1 in r.json():    
            if len(graph_word[no][lemma])<=15:
                va  = result1["properties"]["fullLemma"].lower()
                if va.isalpha(): #utk check crachter,number,space
                    if  va not in graph_word[no][lemma]:
                        graph_word[no][lemma].append(va)
            else:
                break          
        no+=1

    key = []
    for gw in graph_word:
        for k,v in gw.items():
            for vv in v:
                
                key.append(vv)
    print(json.dumps(graph_word,sort_keys=True, indent=3))
    # print("-----ALL-----")
    # print(key)

    res = {
        'result_graph_word' :graph_word,
        'all_word'          :key
    }
    return res

                  
def cnn(word_question,detectNER,keyy):
    print("\n\n ------------------------------------------------------ CNN --------------------------------------------")
    matrix=[['kategori']]
    if word_question!= None:
        for q in word_question:
            keyy.append(q)
    if detectNER!=None:
        for dn in detectNER:
            keyy.append(dn)
    DATAQUESALL = Clas.objects.values_list('id',flat=True) #get - ID classfication
    ALL         = Clas.objects.all().count()

    print("-----------------------------GET DATA SQL-------------------------")
    n=1
    for iden in DATAQUESALL :
        for e in Clas.objects.filter(id=iden).values_list('classification',flat=True):
            matrix[0].append(e)

    for y in keyy:
        matrix.append([y])
        for x in DATAQUESALL:
            dataClas    = Clas.objects.filter(question_template__contains=y).filter(pk=x).count() | Clas.objects.filter(answer__contains=y).filter(pk=x).count()
            data        = Ques.objects.filter(id_class_id=x)
            if  data :
                dataQues= Ques.objects.filter(pattern__contains=y).filter(id_class_id=x).count() 
            else:
                dataQues = 0
            matrix[n].append(dataClas+dataQues)
        n=n+1
        
    for ab in matrix:
        print(ab,"\n")

    print("\n\n----------------------------- TF-------------------------")
    for q in matrix[1:]:
        hasil=0
        for b in q[1:]:
            if b !=0 :
                hasil = hasil+1
        if hasil >0:
            hitung = round(math.log(ALL/(hasil)),2)
            q.append(hitung)
        else:
            matrix.remove(q)           
        
    for q in matrix:           
        print(q)
    
    print("----------------------------- IDF-------------------------")
    idf =[['hasil']]
    a=1
    for z in matrix:
        idf.append([z[0]])
        q=1
        for n in z[1:]:
            if a==1:
                idf[a].append(n)
            else:
                idf[a].append(n*z[-1])
                if  a==2:
                    idf[0].append(n*z[-1])
                else:
                    idf[0][q]=idf[0][q]+(n*z[-1])
                    q=q+1
        a=a+1
    
 
    for q in idf:           
        print(q)
    

    print("\n\n-------------------------CLASS MAX @ALL------------------------")
    classmax=sorted(zip(idf[0][1:], idf[1][1:]), reverse=True)[:10]
    print(classmax)

    cllass=[]
    for cl in classmax:
        if str(cl[0]) !=str(0.0):
            cllass.append((cl[0],cl[1]))
    print(cllass)

    matrixfilter    = [[random.randrange(1,10)/10,random.randrange(1,10)/10],[random.randrange(1,10)/10,random.randrange(1,10)/10]]
    matrixfilterdua = [[random.randrange(1,10)/10,random.randrange(1,10)/10],[random.randrange(1,10)/10,random.randrange(1,10)/10]]
    allsoftmax      = 0
    print("\n\n-------------------------CONVOLUTIONAL/HIDDEN LAYER------------------------")
    print("MATRIX FILTER : %s" % matrixfilter)
    softmax=[[],[]]
    nnn=2

    for c in cllass:
        name=c[1]
        print("Clllassss : ", c[1])
        matrixsatu=[]
        n=0
        for y in idf[2:]:
            name=c[1]
            matrixsatu.append([y[0]])
            CLASSID     = Clas.objects.filter(classification=c[1]).values_list('id',flat=True)
            CLASSNAME   = Clas.objects.filter(classification__contains=y[0]).filter(classification=c[1]).count()
            CLASSQUES   = Clas.objects.filter(question_template__contains=y[0]).filter(classification=c[1]).count()
            CLASSANSWER = Clas.objects.filter(answer__contains=y[0]).filter(classification=c[1]).count()
            print()
            matrixsatu[n].append(CLASSNAME)
            matrixsatu[n].append(CLASSQUES)
            matrixsatu[n].append(CLASSANSWER)

            for g in CLASSID:
                QUES    = Ques.objects.filter(id_class_id=c).values_list('pattern',flat=True)
                for q in QUES :
                    if y[0] in q:
                        matrixsatu[n].append(1)
                    else:
                        matrixsatu[n].append(0)
            n=n+1
        for z in matrixsatu:
            print('Mx Satu : ',z)

        matrixdua   = []
        num         = 0
        for g in range(0,len(matrixsatu)):
            if g!=(len(matrixsatu)-1):
                matrixdua.append([])
                for n in range(0,len(matrixsatu[g])):
                    if  n!=0 and n!=(len(matrixsatu[g])-1):
                        a=0
                        b=0
                        c=0
                        d=0
                        if matrixsatu[g][n]!=0.0 or matrixsatu[g][n]!=0:
                            a   = (matrixsatu[g][n]*matrixfilter[0][0])
                        elif matrixsatu[g][n+1]!=0.0 or matrixsatu[g][n+1]!=0:
                            b   = (matrixsatu[g][n+1]*matrixfilter[0][1])
                        elif matrixsatu[g+1][n]!=0.0 or matrixsatu[g+1][n]!=0:
                            c   = (matrixsatu[g+1][n]*matrixfilter[1][0])
                        elif matrixsatu[g+1][n+1]!=0.0 or matrixsatu[g+1][n+1]!=0:
                            d   = (matrixsatu[g+1][n+1]*matrixfilter[1][1])
                        hasil = a+b+c+d

                        # hasil = (matrixsatu[g][n]*matrixfilter[0][0])+(matrixsatu[g][n+1]*matrixfilter[0][1])+(matrixsatu[g+1][n]*matrixfilter[1][0])+(matrixsatu[g+1][n+1]*matrixfilter[1][1])
                        matrixdua[num].append(hasil)
                num=num+1

        
        print("\n ----------------matrixduaa----------------")
        for ziig in matrixdua:
            print(ziig)
        haasssiill = numpy.sum(matrixdua,dtype = numpy.float32)
        print(haasssiill)
        if  haasssiill== 0.0:
            continue;
        else:
            matrixtiga=[]
            num = 0
            if len(matrixdua)==1:
                hasilmax = numpy.amax(matrixdua)
            else:
                for g in range(0,len(matrixdua)):
                    if g!=(len(matrixdua)-1):
                        matrixtiga.append([])
                        for n in range(0,len(matrixdua[g])):
                            if   n!=(len(matrixdua[g])-1):
                                a=0
                                b=0
                                c=0
                                d=0
                                if matrixdua[g][n]!=0.0 or matrixdua[g][n]!=0:
                                    a   = (matrixdua[g][n]*matrixfilterdua[0][0])
                                elif matrixdua[g][n+1]!=0.0 or matrixdua[g][n+1]!=0:
                                    b   = (matrixdua[g][n+1]*matrixfilterdua[0][1])
                                elif matrixdua[g+1][n]!=0.0 or matrixdua[g+1][n]!=0:
                                    c   = (matrixdua[g+1][n]*matrixfilterdua[1][0])
                                elif matrixdua[g+1][n+1]!=0.0 or matrixdua[g+1][n+1]!=0:
                                    d   = (matrixdua[g+1][n+1]*matrixfilterdua[1][1])
                                hasil = a+b+c+d
                                # hasil = (matrixdua[g][n]*matrixfilterdua[0][0])+(matrixdua[g][n+1]*matrixfilterdua[0][1])+(matrixdua[g+1][n]*matrixfilterdua[1][0])+(matrixdua[g+1][n+1]*matrixfilterdua[1][1])
                                matrixtiga[num].append(hasil)
                        num=num+1

                print("\n ----------------MATRIX TIGA----------------")
                for t in matrixtiga:
                    print (t)

                
                hasilmax = numpy.amax(matrixtiga) 

            # a = numpy.array(matrixtiga)
            # unique, counts = numpy.unique(a, return_counts=True)
            # hasilmax = dict(zip(unique, counts))
            print("^^^^^^^") 
            print(hasilmax)
            hasilexp = round(math.exp(hasilmax),2)
            # print(hasilexp)
            allsoftmax= hasilexp+allsoftmax
            softmax.append([name,hasilmax, hasilexp])
            # softmax.append([name])
            # softmax[nnn].append(hasilmax)
            # softmax[nnn].append(hasilexp)
            softmax[0].append(name)
            nnn+=1
        
        # softmax.append(max(matrixtiga.values()))
        # print(max(matrixtiga.values()))
            
    print("\n\n-------------SOFTMAX SPECIFIC CLASS------------------")
    print(softmax)
    for so in softmax[2:]:
            so.append(round(so[2]/allsoftmax,2))
            softmax[1].append(round(so[2]/allsoftmax,2))
            # print(so)

    for ss in softmax:
            print(ss)
    
    classmax=sorted(zip(softmax[1], softmax[0]), reverse=True)[:3]
    print("\n---------FINALLY CLASS =-" , classmax, "------------ ")

    res = {
        'class'     :classmax,
    }
    return res

    # return HttpResponse("cek di cmd" )
    # return render(request, 'layout/base.php', 'data':data)

def title_wikipedia(title):
    print("\n\n ------------------------------------------------------ TITLE WIKIPEDIA - NGRAMS --------------------------------------------")
    service_url         = "https://en.wikipedia.org/w/api.php" #URL Wikipedia
    data_title          = {"unigram":[],"bigram":[],"trigram":[]}
    titles              = []
    for n in range(1,4):
        Ngrams  = ngrams(title.split(), n) #memotong kalimat menjadi NGrams (uni,bi, trigrams)
        Ng      =""
        if   n==1: Ng="unigram"
        elif n==2: Ng ="bigram"
        else     : Ng="trigram"
        no=0
        for grams in list(Ngrams) :
            gram        = " ".join(grams)
            data_title[Ng].append({gram:[]})
            params      = "action=query&format=json&list=allpages&apfrom="+(" ".join(grams))+"&aplimit=15&cmtitle=Category:Mathematicians" #parameter API wikipedia
            url	        = service_url + '?' + params #gabungin URL
            r           = requests.get(url=url) 
            for k,y in r.json().items(): 
                if k=="query":
                    for z in y['allpages']:
                        wiki_wiki   = wikipediaapi.Wikipedia('en')
                        page_py     = wiki_wiki.page(z['title'])
                        res = page_py.exists()
                        if  res == True:
                            if page_py.title not in data_title[Ng][no][gram]:
                                if '\''not in page_py.title:
                                    titles.append(page_py.title)
                                    data_title[Ng][no][gram].append(page_py.title)
            #                     print(page_py.title)
            # print("----------------------")
            no=no+1

    print(json.dumps(data_title,sort_keys=True, indent=3))
    print("\n")

    a               = numpy.array(titles)
    unique, counts  = numpy.unique(a, return_counts=True)
    hasil           = dict(zip(unique, counts))
    print(hasil)

    max_value       = max(hasil.values()) #mencari judul dengan kemunculan terbanyak
    topics          = []
    for x,y in hasil.items():
        if y == max_value:
            topics.append(x)
    print (topics)
    res = {
        'unigram'   :data_title["unigram"],
        'bigram'    :data_title["bigram"],
        'trigram'   :data_title["trigram"],
        'topics'    : topics
    }
    return res

def check_answer_sparql(title,key,key_lemstem):

    print("\n\n ------------------------------------------------------ Answer DBPEDIA --------------------------------------------")   
    if "," in title:
        title.replace("\,",",")
    if "(" in title:
        title.replace("\(","(")
    if ")" in title:
        title.replace("\(",")")

    answer  =[]
    entity  = title.replace(" ","_")
    
    print(key_lemstem)
    for relation in key_lemstem:
        sparql  = sparql_dbpedia(entity,relation) 
        if sparql != None:
                if sparql not in answer:
                    answer.append(sparql)
                    print(relation," -->>> ",sparql)
                    
    for relation in key:
        sparql  = sparql_dbpedia(entity,relation) 
        if sparql != None:
                if sparql not in answer:
                    answer.append(sparql)
                    print(relation," -->>> ",sparql)
    
    print("\n\n---------ANSWER ALL---------")
    for ans in answer:
        print(ans)
    res = {
        'answer_sparql' :answer,
        'sum_key_answer': len(key),
        'sum_answer'    : len(answer)
    }
    return res


def sparql_dbpedia(entity,relation):
    sparql      = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX ontology: <https://dbpedia.org/ontology>
        PREFIX dbo: <https://dbpedia.org/ontology/>
        prefix dbc:<https://dbpedia.org/resource/Category:>
        prefix dct:<https://purl.org/dc/terms/>
        PREFIX dbp:<https://dbpedia.org/property/>
        SELECT*WHERE{
            dbr:"""+ entity+""" ?p ?o .
            # <https://en.wikipedia.org/wiki/"""+ entity+"""> ?p ?o .
            FILTER regex(str(?p),\""""+ relation+"""\","i")
            }
        """)
    sparql.setReturnFormat(JSON)
    result  = sparql.query().convert()
    results = json.dumps(result,sort_keys=True, indent=2)

    if result["results"]["bindings"]!=[]: 
        for a in  result["results"]["bindings"]:
            p=""
            o=""
            if re.match('https', a["p"]["value"]):
                p=a["p"]["value"].rsplit('/', 1)[-1]
            else:
                p=a["p"]["value"]

            if re.match('https', a["o"]["value"]) :
                o=a["o"]["value"].rsplit('/', 1)[-1]
            else:
                o=a["o"]["value"]
            return  p+""" : """+ o
    
    
        


# def  crawl_artikel(Question,title_wikipedia,lexical_word,class_cnn):
def  crawl_artikel(Question,title_wikipedia,key1,graph_word): 
    print("\n\n ------------------------------------------------------ CRAWL ARTICLE --------------------------------------------")
    crawlV              = ""
    result_tokenizing   = []
    key                 = []   
    result_tokenizing   = ast.literal_eval(json.dumps(word_tokenize(title_wikipedia.lower())))
    
    for op in key1:
        if op not in result_tokenizing:
            key.append(op.lower())
    print(key1)
    print()
    print(key)
    print()
    wiki_wiki   = wikipediaapi.Wikipedia('en')
    title       = " ".join(title_wikipedia).replace(" ","_")
    title       = title_wikipedia.replace(" ","_")
    page_py     = wiki_wiki.page(title)
    url         = page_py . fullurl
    wiki_wiki   = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    p_wiki      = wiki_wiki.page(title)
    # key=numpy.concatenate([key1,result_tokenizing]) #array
    arr     = [['tf']]
    no      = 1
    summ    = 0
    # print("keyy : ",key)
    for i in sent_tokenize(p_wiki.text):
        arr.append(['K%d'%(no)])  #append K1,k2, dst
        arr[no].append(i) #append kalimat
        for j in key :
            tf  = i.count(j) #menghitung jumlah kata dlm suatu kalimat
            arr[no].append(tf)
            summ+=tf #untuk mengecek apakah key ada di dalam artikel/tidak
        no+=1
    
    if summ!=0:
        arr.insert(1,['Q']) #memasukkan kalimat tanya utk dihitung tf nya
        arr[1].append(Question)
        for j in key :
            arr[1].append(Question.count(j))
        crawlV = "v1"
    else:
        arr.clear()
        key.clear()
        arr     = [['tf']]
        no      = 1
        key     = graph_word
        summm   = 0
        for i in sent_tokenize(p_wiki.text):
            if no ==1:
                arr.append(['Q'])
                arr[no].append(Question)
                for j in key :
                    arr[no].append(Question.count(j))
            else:
                arr.append(['K%d'%(no-1)])
                arr[no].append(i)
                for j in key :
                    tf= i.count(j)
                    arr[no].append(tf)
                    summm+=tf
            no+=1
            crawlV = "v2"
        if summm==0:
            arr.clear()
            key.clear()
            arr     = [['tf']]
            no      = 1
            summmm  = 0
            for i in sent_tokenize(title_wikipedia):
                key    += ast.literal_eval(json.dumps(word_tokenize(i)))
            for i in sent_tokenize(p_wiki.text):
                if no ==1:
                    arr.append(['Q'])
                    arr[no].append(Question)
                    for j in key :
                        arr[no].append(Question.count(j))
                else:
                    arr.append(['K%d'%(no-1)])
                    arr[no].append(i)
                    for j in key :
                        tf= i.count(j)
                        arr[no].append(tf)
                        summmm+=tf
                no+=1
            
            crawlV = "v3"



    
    print(key)
    # for aa in arr:
    #     print(aa)
    #     print("\n")

    # menghitung jumlah semua TF
    nn =1
    for y in arr[1:]:
        gg = 1
        for x in y[2:]:
            if  nn==1:
                arr[0].append(0+x)
            else:
                arr[0][gg]=x+ arr[0][gg]
            gg+=1
        nn+=1
    

    print("\n\n----------------------IDF--------------------------")
    arr.insert(0,['IDF'])
    jmlh = len(arr)-2
    for yz in arr[1][1:]:
        # print(yz)
        if yz != 0:
            arr[0].append(round(math.log(jmlh/(yz)),2))
        else:
            arr[0].append(0)
    
    print("\n\n -----------arr---------------")

    for gh in arr :
        print(gh)
        print("\n")
    
    print("\n\n -----------arr---------------")

    
    artikel_idf = []
    a=0
    for z in arr[2:]:
        # print(z)
        artikel_idf.append([z[0],z[1]])
        no=1
        arr_idf=[]
        sum_idf =0
        for zy in z[2:]:
            # if a==0:
            #     # artikel_idf[a].append(zy)
            #     sum_idf+=zy
            # else:
            idf =zy*arr[0][no]
            artikel_idf[a].append(idf)
            sum_idf+=idf
            
            no+=1
        if sum_idf !=0:
            artikel_idf[a].append(round(sum_idf,2))
            a=a+1
        else:
            artikel_idf.remove(artikel_idf[a])
            a=a

    print("\n\n\n-------------------------ARTICLE IDF------------------------")
    for bj in artikel_idf:
        print(bj)
        print("\n")

    idf_transpose=[]
    for aa in numpy.array(artikel_idf).T:
        idf_transpose.append(aa)
    
    # print(idf_transpose)
    print("---------------idf Transpose----------------")
    # for idt in idf_transpose:
    #     print(idt)

    print("\n\n-------------------------SENTENCE MAX------------------------")
    # classmax=sorted(zip(idf_transpose[-1][3:],idf_transpose[0][3:],idf_transpose[1][3:]), reverse=True)[:5]
    # classmax=sorted(zip(idf_transpose[-1][3:],idf_transpose[0][3:]), reverse=True)[:5]
    classmax=sorted(zip(idf_transpose[-1][1:],idf_transpose[0][1:]), reverse=True)[:5]
    for cs in classmax:
        print(cs[1]," ", cs[0])
        print(cs)
    
    
    print("\n\n-------------------------COSINUS SIMILARITY------------------------")
    print("-------------------------SKALAR & PANJANG VEKTOR COSINUS------------------------")

    # print(list(zip(*numpy.where(artikel_idf == 'K68'))))
    skalar=[]
    panjang_vektor=[]
    no_v=0
    no_s=0
    for arr in artikel_idf:
        # print(arr)
        if arr[0]=='Q':
            panjang_vektor.append(['Q'])
            num=1
            for ar in arr[2:][:-1]:
                # print(ar)
                panjang_vektor[no_v].append(ar*ar)
            hsl=0.0
            for p in panjang_vektor[no_v][1:]:
                hsl+=p
            
            panjang_vektor[no_v].append(hsl)
            if hsl!= 0:
                panjang_vektor[no_v].append(round(math.sqrt(hsl),2))
            else:
                panjang_vektor[no_v].append(hsl)
            panjang_vektor[no_v].append(arr[1])
            no_v+=1
        else:
            for ya in classmax:
                if arr[0] == ya[1]:
                    skalar.append([ya[1]])
                    panjang_vektor.append([ya[1]])
                    num=2
                    for ar in arr[2:][:-1]:
                        skalar[no_s].append(round(artikel_idf[0][num]*ar,2)) #menghitung panjang skalar Questian*Kalimat
                        panjang_vektor[no_v].append(ar*ar) #menghitung panjang vektor = pangkat 2 IDF @kalimat
                        num+=1
                    hsl_v=0.0
                    hsl_s=0.0
                    for p in skalar[no_s][1:]:
                        hsl_s+=p
                    for p in panjang_vektor[no_v][1:]:
                        hsl_v+=p
                    
                    skalar[no_s].append(hsl_s)
                    panjang_vektor[no_v].append(hsl_v)
                    if hsl_v !=0.0:
                        panjang_vektor[no_v].append(round(math.sqrt(hsl_v),2))
                    else:
                        panjang_vektor[no_v].append(hsl_v)
                    panjang_vektor[no_v].append(arr[1])
                    no_v+=1
                    no_s+=1
                    classmax.remove(ya) #opt
    
    print("\n-----------SKALAR----------")
    for s in skalar:
        print(s[0]," , ",s[-1])
        print(s)

    print("\n-----------PANJANG VEKTOR----------")
    for p in panjang_vektor:
        print(p[0]," , ", p[-3], " , ",p[-2])
        print(p)

    

    print("\n\n-----------COSINUS----------")
    cosinus=[]
    n=0
    # for p in panjang_vektor[1:]:
    for p in panjang_vektor[1:]:
        cos =0
        cosinus.append([p[0],p[-1]])
        # nn=1
        for s in skalar:
            if s[0] == p[0]:
                print(panjang_vektor[0][-2])
                if panjang_vektor[0][-2]==0.0 or s[-1] ==0.0 or p[-2]==0.0:
                    cosinus[n].append(0)
                    print('cs0' )
                else:
                    cos = round(s[-1]/(p[-2]*panjang_vektor[0][-2]),2)
                    print('cos ', cos)
                    cosinus[n].append(cos)
                # nn+=1
        n+=1
    for c in cosinus:
        print(c,"\n")

    cosinus_transpose=[]
    for aa in numpy.array(cosinus).T:
        cosinus_transpose.append(aa)

    print(cosinus_transpose)
   
    print("\n\n\n-------------------------COSINUS MAX------------------------")
    classmax_cosinus=sorted(zip(cosinus_transpose[-1],cosinus_transpose[0],cosinus_transpose[1]), reverse=True)[:5]
    for cc in classmax_cosinus:
        print(cc)
        print("\n")
    
    print(crawlV)
    print(arr[-1])
    res = {
        'answer_wikipedia' : classmax_cosinus,
        'url'              : url
    }
    return res

    # return HttpResponse("yyyeaaahhh")

