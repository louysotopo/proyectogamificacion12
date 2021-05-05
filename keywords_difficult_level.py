import gspread
import pandas 
import nltk
import re
import enchant
#import matplotlib.pyplot as plt 
import seaborn as sns
from scipy.sparse import coo_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from oauth2client.service_account import ServiceAccountCredentials
from os import path
#from PIL import Image
#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from difflib import SequenceMatcher as SM
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def STOPWORDS():

    stop_words = set(stopwords.words("spanish"))
    ##Creating a list of custom stopwords
    new_words2 = ['http', 'doi', 'org', 'comunicar', 'revista','cientifica', 'issn', 'www', 'revistacomunicarcom', 'com', 'páginas', 'aceptado' , 'publicado','journal']
    stop_words = stop_words.union(new_words2)
    stop_words=stop_words.union(set(stopwords.words("english")))
    return stop_words

def preprocesamiento(valor,stop_words):
    d = enchant.Dict("en_US")
    corpus = []
    for i in range(0, 1):
            
        a,b = 'áéíóúü','aeiouu'
        trans = str.maketrans(a,b)

        #text = dataset['abstract1'][i].translate(trans)  
        text= valor.translate(trans) 
    # texti= "psychometric property almost perfect scale individual difference http j lindif schuler p gifted adolescent journal gifted http jsge schwarz g estimating dimension model sciove s l application model criterion some problem in multivariate analysis psychometrika http shafran r cooper z fairburn c g clinical cognitive analysis http s"
        #text= texti 

        #Remove references 
        text = re.sub(r"\([^()]*\)", "", text)
        
        #Remove punctuations
        text = re.sub('[^a-zA-Z]', ' ', text)
        
        #Remove acronyms
        text= re.sub(r"\b[A-Z]{2,}\b", "", text)

        #Convert to lowercase
        text = text.lower()
        
        #remove tags
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
        
        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)
        
        ##Convert to list from string
        text = text.split()
        
        ##Stemming
        ps=PorterStemmer()
        #Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in  
                stop_words and d.check(word) == False] 
        text = " ".join(text)
        corpus.append(text)
    return corpus

def  VECTOR_TF_IFD(stop_words,corpus):
    cv=CountVectorizer(max_df=1,stop_words=stop_words, max_features=10000, ngram_range=(1,3))
    X=cv.fit_transform(corpus)
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(X)
    # get feature names
    feature_names=cv.get_feature_names()
    
    # fetch document for which keywords needs to be extracted
    doc=corpus[0]
    
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
    return(doc,tf_idf_vector,feature_names)

def get_top_n_words(corpus, n=None):
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                   vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                       reverse=True)
    return words_freq[:n]

def MONOGRAMA(corpus):
    top_words = get_top_n_words(corpus, n=20)
    top_df = pandas.DataFrame(top_words)
    top_df.columns=["Word", "Freq"]
    #print(top_df)
    #Barplot of most freq words
    sns.set(rc={'figure.figsize':(13,8)})
    g = sns.barplot(x="Word", y="Freq", data=top_df)
    g.set_xticklabels(g.get_xticklabels(), rotation=30)
    return top_df
def get_top_n2_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(2,2),  
            max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in     
                  vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                reverse=True)
    return words_freq[:n]

def BIGRAMA(corpus):
    top2_words = get_top_n2_words(corpus, n=20)
    top2_df = pandas.DataFrame(top2_words)
    top2_df.columns=["Bi-gram", "Freq"]
    #print(top2_df)
    #Barplot of most freq Bi-grams
    sns.set(rc={'figure.figsize':(13,8)})
    h=sns.barplot(x="Bi-gram", y="Freq", data=top2_df)
    h.set_xticklabels(h.get_xticklabels(), rotation=45)
    return top2_df
def get_top_n3_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(3,3), 
           max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in     
                  vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                reverse=True)
    return words_freq[:n]
def TRIGRAMA(corpus):
    top3_words = get_top_n3_words(corpus, n=30)
    top3_df = pandas.DataFrame(top3_words)
    top3_df.columns=["Tri-gram", "Freq"]
    #print(top3_df)
    #Barplot of most freq Tri-grams
    sns.set(rc={'figure.figsize':(13,8)})
    j=sns.barplot(x="Tri-gram", y="Freq", data=top3_df)
    j.set_xticklabels(j.get_xticklabels(), rotation=45)
    return top3_df
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 
def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def keywords_extract(doc,tf_idf_vector,feature_names):
    #sort the tf-idf vectors by descending order of scores
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    #extract only the top n; n here is 10
    keywords=extract_topn_from_vector(feature_names,sorted_items,20)
    return keywords
    # now print the results
    #print("\nAbstract:")
    #print(doc)
    #print("\nKeywords:")
    #for k in keywords:
        #print(k,keywords[k])


def limpiar_keywords(keywords_excel,stop_words):
    keywords_excel=keywords_excel[12:-4]
    keywords_excel = keywords_excel.lower()
    a,b = 'áéíóúü','aeiouu'
    trans = str.maketrans(a,b)
    #text = dataset['abstract1'][i].translate(trans)  
    keywords_excel= keywords_excel.translate(trans) 
    keywords_excel=keywords_excel.split(",") 
    ##Stemming
    ps=PorterStemmer()
    #Lemmatisation
    lem = WordNetLemmatizer()
    keywords_excel = [lem.lemmatize(word) for word in keywords_excel if not word in 
                stop_words ] 
    #print(keywords_excel)
    return keywords_excel

def integracion(keywords,top_df,top2_df,top3_df):
    keywords_algorithm=[]
    for word in keywords:
        keywords_algorithm.append(word)
    for k in range(top_df.Word.size):
        word=top_df.Word[k]
        if(word not in keywords_algorithm ):
            keywords_algorithm.append(word)
    for k in range(top2_df['Bi-gram'].size):
        word=top2_df['Bi-gram'][k]
        if(word not in keywords_algorithm ):
            keywords_algorithm.append(word)
    for k in range(top3_df['Tri-gram'].size):
        word=top3_df['Tri-gram'][k]
        if(word not in keywords_algorithm ):
            keywords_algorithm.append(word)          
    return keywords_algorithm


def comparativa_articulo(keywords_algorithm,keywords_excel):
    score= 100/8
    i=0
    num=0
    keywords_detected={}
    #keywords_excel2=keywords_excel.split()
    puntaje_mayor=0
    l_indice=''
    k_indice=''
    keywords_finales={}
    for k in keywords_algorithm :
        for l in keywords_excel:
            puntaje=SM(None, k, l).ratio()
            #print(k,l,puntaje,puntaje_mayor)
            if(puntaje>puntaje_mayor):
                puntaje_mayor=puntaje
                l_indice=l
                k_indice=k
        if (puntaje_mayor>0.635 and l_indice not in keywords_detected):
                #print('Aqui')
                keywords_detected[l_indice]=k_indice
                keywords_finales[k_indice]=puntaje_mayor
                #print('si  ....... '+k_indice+'...'+l_indice)
                i+=1
                #print(keywords_finales)
        elif(puntaje_mayor>0.635 and l_indice in keywords_detected):
                #print('Duelo')
                if(puntaje_mayor>keywords_finales[keywords_detected[l_indice]]):
                    #print(keywords_detected[l_indice])
                    del(keywords_finales[keywords_detected[l_indice]])
                    keywords_finales[k_indice]=puntaje_mayor
                    keywords_detected[l_indice]=k_indice
                    #print('terminar')
                    #print(keywords_finales)

        l_indice=''
        k_indice=''
        puntaje_mayor=0
    #print(keywords_finales)
    #print('Score = '+ str(score*i))
    return keywords_finales


def comparativa_estudiante(keywords_finales,respuesta):
    #respuesta=input('Ingrese la cadena\n')
    #respuesta= respuesta.split(';')
    score2= 100/len(keywords_finales)
    i=0
    num=0
    keywords_detected2={}
    errores=[]
    #keywords_excel2=keywords_excel.split()
    puntaje_mayor2=0
    l_indice2=''
    k_indice2=''
    keywords_finales2={}
    for k in respuesta:
        for l in keywords_finales:
            puntaje2=SM(None, k, l).ratio()
            #print(k,l,puntaje2,puntaje_mayor2)
            if(puntaje2>puntaje_mayor2):
                puntaje_mayor2=puntaje2
                l_indice2=l
                k_indice2=k
        if (puntaje_mayor2>0.635 and l_indice2 not in keywords_detected2):
                #print('Aqui')
                keywords_detected2[l_indice2]=k_indice2
                keywords_finales2[k_indice2]=puntaje_mayor2
                #print('si  ....... '+k_indice2+'...'+l_indice2)
                i+=1
                #print(keywords_finales2)
        elif(puntaje_mayor2>0.635 and l_indice2 in keywords_detected2):
                #print('Duelo')
                if(puntaje_mayor2>keywords_finales2[keywords_detected2[l_indice2]]):
                    #print(keywords_detected[l_indice])
                    del(keywords_finales2[keywords_detected2[l_indice2]])
                    keywords_finales2[k_indice2]=puntaje_mayor2
                    keywords_detected2[l_indice2]=k_indice2
                    #print('terminar')
                    #print(keywords_finales2)

        l_indice2=''
        k_indice2=''
        puntaje_mayor2=0
        
    for rpt in range(len(respuesta)):
        if respuesta[rpt] not in keywords_finales2:
            errores.append(respuesta[rpt])

    #print('Palabras sugeridas por el algoritmo: ', list(keywords_finales.keys()))
    #print('Aciertos',list(keywords_finales2.keys()))
    #print('Errores',errores )
    #print('Score = '+ str(score2*i))

    return list(keywords_finales.keys()),list(keywords_finales2.keys()),errores

#---------------------------------------------------------------------------------
def evaluar(indice):
    scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("PRUEBA-PYTHON-22fd0afc8b92.json", scope)
    client=gspread.authorize(creds)
    sheet= client.open("corpus-articulos-divididos").worksheet('DAR')
    valor=str(sheet.cell(indice,8))
    keywords_excel=str(sheet.cell(indice,9))
    stop_words=STOPWORDS()
    corpus=preprocesamiento(valor,stop_words)
    #wordcloud(stop_words,corpus)# aqui nube de palabras
    top_df=MONOGRAMA(corpus)
    top2_df=BIGRAMA(corpus)
    top3_df=TRIGRAMA(corpus)
    doc,tf_idf_vector,feature_names=VECTOR_TF_IFD(stop_words,corpus)
    keywords=keywords_extract(doc,tf_idf_vector,feature_names)
    keywords_excel=limpiar_keywords(keywords_excel,stop_words)
    keywords_algorithm=integracion(keywords,top_df,top2_df,top3_df)
    keywords_finales=comparativa_articulo(keywords_algorithm,keywords_excel)
    return keywords_finales
    #comparativa_estudiante(keywords_finales)

def buscarNombre(indice):
    scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("PRUEBA-PYTHON-22fd0afc8b92.json", scope)
    client=gspread.authorize(creds)
    sheet= client.open("corpus-articulos-divididos").worksheet('DAR')
    nombre_articulo=str(sheet.cell(indice,10))
    nombre_articulo=nombre_articulo[13:-2]
    return nombre_articulo

#def nube(stop_words,corpus):
#    wordcloud = WordCloud(
#                            background_color='white',
#                            stopwords=stop_words,
#                            max_words=100,
#                            max_font_size=50, 
#                            random_state=42
#                            ).generate(str(corpus))
#    #print(wordcloud)
#    fig = plt.figure(1)
#    plt.imshow(wordcloud)
#    plt.axis('off')
#    #plt.show()
#    fig.savefig("word1.png", dpi=900)

    

