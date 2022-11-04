#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import fitz
import spacy
import requests
import IPython
import pathlib
import nltk
import pandas as pd
import numpy as np
#nltk.download('wordnet')
#nltk.download('stopwords')
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer, word_tokenize
from keyphrase_vectorizers import KeyphraseCountVectorizer
from keybert import KeyBERT
#nltk.download('wordnet') 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer


# In[4]:


def build_corpus(files_path):
    text_dict = {'title': [],
                 'text': []}

    #Iteration über PDF's und in text speichern. Alle PDF's liegen in text_list Es werden nur die ersten beiden Seiten eingelesen
    for file in files_path:
        has_abstract = False
        cur_reader = fitz.open(file)
        text = ''
        text_tmp = ''
        cur_title = cur_reader.metadata['title']

        for i in range(len(cur_reader)):  
            page = cur_reader.load_page(i)

            abstract = page.search_for("abstract")
            if abstract:
                text +=  cur_reader.get_page_text(i)
                has_abstract = True
                break;
            else:
                text_tmp +=  cur_reader.get_page_text(i)

        if not has_abstract:
            text = text_tmp

        text_dict['title'].append(cur_title)
        text_dict['text'].append(text)
        

        cur_reader.close()
        
    return text_dict


# In[15]:


def build_conference(files_path):
    con_dict = {'title': [],
                 'text': []}
    
    for file in files_path:
        cur_reader = fitz.open(file)
        text = ''
        cur_title = cur_reader.metadata['title']
        
        for i in range(len(cur_reader)):  
            page = cur_reader.load_page(i)
            text +=  cur_reader.get_page_text(i)
            
        con_dict['title'].append(cur_title)
        con_dict['text'].append(text)
        
    return con_dict


# In[5]:


def get_stopwords():
#Englische Stop Words
    stop_words = set(stopwords.words("english"))
#Hinzufügen eigener Stopwords
    new_words = ["the", "as", "was", "that", "open", "access", "thought", "sees", "agreement", "term", "initially", "people", "eu", "citiations", "de", "authors",
                "com", "citations", "table", "et", "al", "conference", "th", "ieee", "fig", "aaai", "www", "org", "yet", "http" ]
    my_stop_words = stop_words.union(new_words)
    return my_stop_words


# In[2]:


def preprocess_corpus(corpus):
    for i in range(len(corpus['title'])):
        detokenize = []
        all_tokens = []
        
        text = corpus['text'][i] 
        tokens = word_tokenize(text) #tokens auf Wortebene

    for i in range(len(tokens)):
        tokens[i] = re.sub("(\\d)+","", tokens[i])   #entfernt Zahlen
        all_tokens.append(tokens[i])
        
    detokenize = TreebankWordDetokenizer().detokenize(all_tokens)
    corpus['text'].append(detokenize)
    return corpus


# In[25]:


def generate_keywords(corpus, conference_corpus):
    
    corpus = preprocess_corpus(corpus)
    
    paper_keys = {'keywords': [], 
                'relevance':[],
                'paper': [] }
    
    conference_keys = {'keywords': [], 
                        'relevance':[],
                        'conference': [] }
    
    kw_model = KeyBERT()
    vectorizer = CountVectorizer(ngram_range=(1,3), stop_words=get_stopwords())

    
    #Erstellt mir ngrams vom Text, sind auch keywords aus n-grammen. Das vielleicht als Attribut an die paper? bläht Graph nicht auf und danach kann dann gesucht werden? 
    #ToDo: Funktion weiter untersuchen und vielleicht an Parametern basteln
    #iteration über alle PDF's
    


    for x in range(len(corpus['title'])): 
        keywords_dist_paper = kw_model.extract_keywords(corpus['text'][x], vectorizer=vectorizer, top_n=20, use_maxsum=True, nr_candidates=10, use_mmr=True, diversity=0.5)
       
        for i in range(len(keywords_dist_paper)):
            keyword =  keywords_dist_paper[i][0]
            paper_keys['keywords'].append(keyword)
            relevance = keywords_dist_paper[i][1]
            paper_keys['relevance'].append(relevance)
            paper_keys['paper'].append(corpus["title"][x])
            
    for x in range(len(conference_corpus['title'])): 
        keywords_dist_conference = kw_model.extract_keywords(conference_corpus['text'][x], vectorizer=vectorizer, top_n=20, use_maxsum=True, nr_candidates=10, use_mmr=True, diversity=0.5)
        
        for i in range(len(keywords_dist_conference)):
            keyword =  keywords_dist_conference[i][0]
            conference_keys['keywords'].append(keyword)
            relevance = keywords_dist_conference[i][1]
            conference_keys['relevance'].append(relevance)
            conference_keys['conference'].append(conference_corpus["title"][x])
        #Umwandlung in Dataframe

    df_paper = pd.DataFrame(paper_keys)
    filepath_paper = 'keywords/paper_Keywords.csv'
    df_paper = df_paper.sort_values('relevance',ascending=False)
    df_paper.to_csv(filepath_paper)

    df_conference = pd.DataFrame(conference_keys)
    filepath_conference = 'keywords/conference_Keywords.csv'
    df_conference = df_conference.sort_values('relevance',ascending=False)
    df_conference.to_csv(filepath_conference)

    return paper_keys, conference_keys


# In[26]:


#pdf_path = ('C:/Users/Jana/LabCode/PDF')
#con_path = ('C:/Users/Jana/LabCode/AimsAndScope')
#p_con = pathlib.Path(con_path)
#files_path_con = list(p_con.glob('*.pdf'))

#p = pathlib.Path(pdf_path)
#files_path = list(p.glob('*.pdf'))
#print(range(len(corpus['title'])))
#corpus = build_corpus(files_path)
#corpus_con = build_conference(files_path_con)


#keyword_list = generate_keywords(corpus, corpus_con)


# In[ ]:


# Eventuell Pos_tagging, Dependency, n-Gram Bildung ect zur Verbesserung der Ergebnisse

def preprocess():
    corpus = []
    keywords = []
    #Herauszufilternde Satzzeichen
    punctuations = ['(','.',')',',','[',']',';',':','_','*','']
    #Lemma und Stemma
    lem = WordNetLemmatizer()
    ps= PorterStemmer() ##Stemming

    #iteration über alle PDF's
    for i in range(len(text_list)):
        text = text_list[i] 
        text = text.lower() #alles kleinschreiben
        tokens = word_tokenize(text) #tokens auf Wortebene
       #Iteration über alle tokens pro PDF
        for i in range(len(tokens)):
            tokens[i] = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ", tokens[i]) #entfernt tags
            tokens[i] = re.sub("(\\d|\\W)+","", tokens[i])   #entfernt Zahlen und spezielle Satzzeichen, toDo: Bindestrich hinbekommen
            #Entfernen einzelner und 2 Buchstaben
            if(len(tokens[i]) <= 2):
               tokens[i] = ''

        #tokens = [lem.lemmatize(word) for word in tokens if not word in stop_words] #Lemmatisation ist das eine gute Idee?
        tokens = [ps.stem(word) for word in tokens if not word in stop_words] #Lemmatisation ist das eine gute Idee?

        keywords.append([word for word in tokens if not word in stop_words and not word in punctuations]) #Erstellen keywords (preprocessed) ohne Satzzeichen und Stop Words ect.
        corpus.append(text) # pre Processed Corpus -> gesamter Text in kleinbuchstaben


# In[ ]:


#brauch ich das noch?
def word_count(text):
    counts = dict()
    words = text.split(" ")

    #print(words)
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return words, counts


# In[ ]:


def weightage(word,text,number_of_documents=1):
    
    number_of_times_word_appeared = len(word_list)

    tf = number_of_times_word_appeared/float(len(text))

    idf = np.log((number_of_documents)/float(number_of_times_word_appeared))
    
    tf_idf = tf*idf
    
    return number_of_times_word_appeared, tf, idf, tf_idf 


# In[ ]:


def word_appearance():

    #def x(corpus, keywords): #wenn ich es als Funtkion mache bekomme ich andere Ausgabe. Aber wieso ?!
    #Iteration über Texte
    for i in range(len(corpus)):
        df_keys = {'keywords': [], #Erstellung Dictionary für nachher DataFrame
                  'number_of_times_word_appeared': [],
                  'idf': [],
                  'tf': [],
                  'tf_idf': []}
        for keyword in keywords[i]: #Iteration über keywords pro Text
            word_list = re.findall(keyword,corpus[i]) #Finde die keywords wieder im Text
            if len(word_list) >= 1: #Falls keyword gefunden
                curArray = []
                curArray = weightage(keyword, corpus[i])    

                #if keyword not in df_keys.get('keywords') : #funktioniert so nicht
                #Füllung des Dictionary anhand der Funktion weightage
                df_keys['keywords'].append([keyword])
                df_keys['number_of_times_word_appeared'].append(curArray[0])
                df_keys['tf'].append(curArray[1])
                df_keys['idf'].append(curArray[2])
                df_keys['tf_idf'].append(curArray[3])
    #Umwandlung in Dataframe
        df = pd.DataFrame(df_keys)

        df=df.loc[df.astype(str).drop_duplicates(subset='keywords').index]
        df = df.sort_values('tf_idf',ascending=True)
        df.head(25).to_csv(str(i)+'_Keywords.csv') #Erstellung csv pro Text
    


        
     


# In[ ]:


def better_vectorizer():
    cv=CountVectorizer(max_df=3, min_df=0, stop_words=stop_words, max_features=10000, ngram_range=(1,3))
    fittedStopwords = ["dummy" for dummy in range(len(corpus))]
    for i in range(len(corpus)):
        corpus[i] = [corpus[i]]
        fittedStopwords[i] = cv.fit_transform(corpus[i])
    print(fittedStopwords)


# In[ ]:




