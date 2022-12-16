#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import math
import networkx as nx
from rdflib.extras.external_graph_libs import rdflib_to_networkx_digraph
from rdflib import Graph, Literal, RDF, URIRef
from rdflib import Namespace
from rdflib.namespace import DC, FOAF, RDF


# In[1197]:


def get_entity_rel(df_pdf_meta, g, keyword_list_paper, keyword_list_con):
    
    n = Namespace('http://G_KG.org/')
    g.bind('n',n)


    for i in range(len(df_pdf_meta)):
        cur_authors =  df_pdf_meta['Authors'][i].split(',')
        date_cur = Literal(df_pdf_meta['Date'][i]) #aktuelles Datum
        titel = df_pdf_meta['Titles'][i].strip()
        paper_cur = Literal(titel) #aktueller Titel
        con = df_pdf_meta['Conference'][i].strip()
        con_cur = Literal(con) #aktuelle Konferenz

        g.add((n.paper, DC.title, paper_cur))
        g.add((paper_cur, DC.date, date_cur))
        g.add((con_cur, DC.title, n.conference))
        g.add((paper_cur, DC.publisher, con_cur))

        for author in cur_authors:
            author = author.strip()
            author_cur = Literal(author)
            g.add((n.Autor, FOAF.name, author_cur))
            g.add((author_cur, DC.creator, paper_cur))

        for j in range(len(keyword_list_paper['keywords'])):
            #Festlegung mindest Relevanz
            if keyword_list_paper['relevance'][j] > 0.4:
                pk_cur = Literal(keyword_list_paper['keywords'][j])
                g.add((n.ThemengebietPaper, RDF.type, pk_cur))
                if df_pdf_meta['Titles'][i] == keyword_list_paper['paper'][j]:
                    #Beziehung zwischen Titeln und keywords mit Attribut label handelt von
                    g.add((paper_cur, DC.subject, pk_cur))

        #Themen Konferenzen     
        for j in range(len(keyword_list_con['keywords'])):
            #Festlegung mindest Relevanz
            if keyword_list_con['relevance'][j] > 0.44:
                #Knotenerstellung aller keywords mit Attribut typ Thema Konferenz
                ck_cur = Literal(keyword_list_con['keywords'][j])
                g.add((n.ThemengebietKonferenz, RDF.type, ck_cur))
                if df_pdf_meta['Conference'][i] == keyword_list_con['conference'][j]:
                    #Beziehung zwischen Konferenzen und keywords mit Attribut label thematisiert
                    g.add((con_cur, DC.subject, ck_cur))
    return g


# In[3]:


#Ausgabe Graph
def show_graph(g):
    G_RDF_NX = rdflib_to_networkx_digraph(g)
    plt.figure(figsize=(25,15))
    pos = nx.spring_layout(G_RDF_NX, k=10/math.sqrt(G_RDF_NX.order())) # Layout Graph
    d = dict(G_RDF_NX.degree)
    nx.draw_networkx(G_RDF_NX, with_labels=True, pos=pos, node_size=[v * 50 for v in d.values()], edge_color= 'grey', font_family = 'Arial')
    #plt.show()
    #plt.savefig("G_KG.png", format="PNG")

