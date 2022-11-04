#!/usr/bin/env python
# coding: utf-8

# In[71]:


import PreProcessMetadata
import PreProcess_NLP
import math
import pandas as pd
import networkx as nx
from matplotlib import cm
import pathlib
import matplotlib.pyplot as plt
import matplotlib.colors as pltcol
pd.set_option('display.max_colwidth', 200)
get_ipython().run_line_magic('matplotlib', 'inline')


# In[65]:


#Erzeuge Knoten, Kanten aus Datei mit Metadaten
def get_meta_entity(meta, KG_entities):
    cur_authors =  meta["Authors"].split(",")
    
    #Nodes ggf Edges mit Typen belegen (zB Author, Paper whatever), Typen im Nachgang zur einer Kategorialen Variable/Spalte in einem gesonderten Dataframe bauen
    #Colormap mit (anzahl Types) möglichen Farben. bei Draw, node_color = categorial, cmap=colormap
    #siehe https://towardsdatascience.com/customizing-networkx-graphs-f80b4e69bedf
    
    #Kantenerstellung zwischen allen Titeln und Erstellungsdatum als Attribut
    KG_entities.add_node(meta["Titles"], date=meta["Date"], color=0.8) #Attribute können auch die Keywords sein, die üner NLP generiert wurden
    KG_entities.add_node(meta["Conference"], color=3.2)
    #Kantenerstellung zwischen Überklasse paper und allen Titeln 
    KG_entities.add_edge("Paper", meta["Titles"], label="ist")
    #Beziehung zwischen Überklasse Konferenz und allen Konferenztiteln
    KG_entities.add_edge("Konferenz", meta["Conference"], label="ist")
    

    
    KG_entities.add_edge(meta["Titles"], meta["Conference"], label="ist Teil von")
    
    for author in cur_authors:
        KG_entities.add_node(author, color=2)
        KG_entities.add_edge(author, meta["Titles"], label="hat verfasst")
        KG_entities.add_edge("Autor", author, label="ist")
    #Themen 
   # for file in files_keys_path:
       # print(file)
       # cur_reader = pd.read_csv(file)
        #cur_csv = pathlib.Path(file).name
       # print(cur_reader)
       # KG_entities.add_node(cur_reader['keywords'], color=4.2)
        #KG_entities.add_edge(meta["paper"], keys["PaperKeys"], label="thematisiert")
        #KG_entities.add_edge(meta["conference"], keys["ConKeys"], label="thematisiert")
        
    return KG_entities


# In[66]:


#Farbschema des Graphen
def kg_colors(graph, vmin=0, vmax=7):
    cnorm = pltcol.Normalize(vmin=vmin, vmax=vmax)
    cpick = cm.ScalarMappable(norm=cnorm, cmap='turbo')
    cpick.set_array([])
    val_map = {}
    for k, v in nx.get_node_attributes(graph, 'color').items():
        val_map[k] = cpick.to_rgba(v)
    colors = []
    for node in graph.nodes():
        colors.append(val_map[node])
    return colors


# In[73]:


# Einlesen der PDF's
pdf_path = ('C:/Users/Jana/LabCode/PDF')
p = pathlib.Path(pdf_path)
files_path = list(p.glob('*.pdf'))
path = 'C:/Users/Jana/LabCode/'

df_pdf_meta = read_paper_meta(path)
write_paper_meta(path)
write_conference_meta(path, df_pdf_meta)
corpus = build_corpus(files_path)
keyword_list = generate_keywords(corpus)
#muss ich hier die Excel lesen? Die meta_control wird doch returned. Das noch umstellen


#keyword_path = ('C:/Users/Jana/LabCode/keywords/')
#p = pathlib.Path(keyword_path)
#files_path = list(p.glob('*.csv'))
#Initialerstellung Graph
G_Meta= nx.MultiDiGraph()

#Erstellung initial fester Knoten
G_Meta.add_node("Paper", color=0.9)
G_Meta.add_node("Autor", color=2)
G_Meta.add_node("Konferenz", color=3)
G_Meta.add_node("Themengebiet", color=4)
#Idee: statt hier metadata_csv zu nehmen, die meta_control nehmen
for i in range(len(df_pdf_meta)):
    G_Meta = get_meta_entity(df_pdf_meta.iloc[i], G_Meta)

colors = kg_colors(G_Meta)


# In[62]:


#Ausgabe Graph
plt.figure(figsize=(25,15))
pos = nx.spring_layout(G_Meta, k=10/math.sqrt(G_Meta.order())) # richtiges Layout noch finden
d = dict(G_Meta.degree)
nx.draw_networkx(G_Meta, with_labels=True, pos=pos, node_size=[v * 100 for v in d.values()], node_color=colors, edge_color= 'grey', font_family = 'Arial') 
plt.show()


# In[ ]:




