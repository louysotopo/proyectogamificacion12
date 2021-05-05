from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
import pandas as pd
import random
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
# nltk.donwload('stopwords')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
set(stopwords.words('spanish'))
from nltk import word_tokenize
from nltk.stem import SnowballStemmer

#extrae datos
def gettingData():
    _route = 'https://docs.google.com/spreadsheets/d/'
    _sheet_id='1w6Lr3cO7rQ8G-D9DpIgIzf4DC28eDbtuy8c_y-zgyRU'
    _sheet_name='Parte_Piero'

    url=f'https://docs.google.com/spreadsheet/ccc?key={_sheet_id}&output=xlsx'
    df = pd.read_excel(url,sheet_name=_sheet_name)

    _titles = df.titulo
    _summary = df.resumen_limpio
    _keywords = df.palabras_clave
    _full_article = df.articulo_completo_limpio

    return _titles, _summary, _keywords, _full_article, len(_titles)

def getRandom(limit):
  return random.randint(2,limit) 


# arrays con las palabras a comparar y devuelve un array 
# con las palabras que se determinan igual
def getMatching (arr_original, arr_prediccion):

  stemmer = SnowballStemmer('spanish')

  arr_matching = []
  matching = False

  for elem_orig in arr_original:
    matching = False
    for elem_pred in arr_prediccion:
      if matching == True:
        break
      for word_orig in elem_orig.split():
        word_orig = word_orig.lower()
        word_orig = word_orig.replace("ñ","n").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
        
        if matching == True:
          break
        for word_pred in elem_pred.split():
          word_pred = word_pred.lower()
          word_pred = word_pred.replace("ñ","n").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
          if stemmer.stem(word_pred) == stemmer.stem(word_orig):
            arr_matching.append([elem_orig, elem_pred])
            matching = True

  return arr_matching


#setting stop_words
def setting_stop_words():

  stop_words = set(stopwords.words('spanish'))  

  #Añadir stopwords
  extra_stop_words = ['https','doi']
  for item in extra_stop_words:
    stop_words.add(item)

  return stop_words

#removing stop_words
def removing_stop_words(_text, _separe_by):
    #setting stop_words
  stop_words = setting_stop_words()
  word_tokens = word_tokenize(_text.lower())
  filtered_sentence = [] 
  
  for w in word_tokens: 
    if w not in stop_words:
      w.replace(":"," ")
      filtered_sentence.append(w)
  
  return _separe_by.join(filtered_sentence)   

#clean array
def clean_array(arr_key1):
  
  for i in range(len(arr_key1)):
    arr_key1[i] = arr_key1[i].strip()
 
  return arr_key1


def nivel_1_resultados(_titles, _summary, arr_usuario):

  #removing stop_words summary
  cleaned_summary = removing_stop_words(_summary, ", ")

  #removing stop_words title
  cleaned_title = removing_stop_words(_titles, " ")  

  #limpiado en el resumen como palabras clave
  _aux_keywords = cleaned_summary

  #volver arrays   #volver array titulo
  arr_key1 = " ".join(_titles.split()).split()
  arr_key2 = " ".join(_aux_keywords.split()).split(",")
  
  #clean array
  arr_key1 = clean_array(arr_key1) #original
  arr_key2 = clean_array(arr_key2) #prediction
  arr_key3 = clean_array(arr_usuario) #user

  #v1
  # matching_user_original = getMatching(arr_key3, arr_key1)
  # matching_user_prediction = getMatching(arr_key3, arr_key2)
  # matching_original_prediction = getMatching(arr_key1, arr_key2)

  #v2
  matching_user_original = getMatching(arr_key1, arr_key3)
  matching_original_prediction = getMatching(arr_key1, arr_key2)
  
  aux_arr = []
  for item in matching_original_prediction:
    aux_arr.append(item[0].strip())
  
  matching_user_prediction = getMatching(aux_arr, arr_key3)


  return matching_user_original, matching_user_prediction, matching_original_prediction

def nivel_2_resultados(_keywords, _full_article, arr_usuario):
  #setting stop_words
  stop_words = setting_stop_words()

  #removing stop_words summary
  cleaned_article = removing_stop_words(_full_article, " ")
  
  #extración palabras clave
  _aux_keywords = keywords(cleaned_article, lemmatize=True, words=20).replace('\n',', ')

  #volver arrays   #volver array titulo
  arr_key1 = " ".join(_keywords.split()).split(",")
  arr_key2 = " ".join(_aux_keywords.split()).split(",")

  #clean array
  arr_key1 = clean_array(arr_key1) #original
  arr_key2 = clean_array(arr_key2) #prediction
  arr_key3 = clean_array(arr_usuario) #user

  #v2
  matching_user_original = getMatching(arr_key1, arr_key3)
  matching_original_prediction = getMatching(arr_key1, arr_key2)
  
  aux_arr = []
  for item in matching_original_prediction:
    aux_arr.append(item[0].strip())
  
  matching_user_prediction = getMatching(aux_arr, arr_key3)

  return matching_user_original, matching_user_prediction, matching_original_prediction

def divideArrays(double_array):
    arr_1 = []
    arr_2 = []
    for item in double_array:
        arr_1.append(item[0])
        arr_2.append(item[1])

    return arr_1, arr_2

def getDiference(arr1, arr2):

    arr1 = clean_array(arr1) #original
    arr2 = clean_array(arr2) 
    
    to_erase = []

    for item in arr1:
        for item2 in arr2:
            if item == item2:
                to_erase.append(item)
                break
                
    for item in to_erase:
      arr1.remove(item)

    return arr1

def equal_string(str1, str2):
    str1 = str1.lower().strip().replace("ñ","n").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    str2 = str2.lower().strip().replace("ñ","n").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    if str1 == str2:
        return True
    return False