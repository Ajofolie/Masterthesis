#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import math
import re
import networkx as nx
from rdflib.extras.external_graph_libs import rdflib_to_networkx_digraph
from rdflib import Graph, Literal, RDF, URIRef
from rdflib import Namespace
from rdflib.namespace import DC, FOAF, RDF, XSD



# In[1197]:

def get_entity_rel(df_pdf_meta, g, keyword_list_paper, keyword_list_con, G_KG_ns):


    for i in range(len(df_pdf_meta)):
        authors =  df_pdf_meta['Authors'][i].split(',')
        date = df_pdf_meta['Date'][i] #aktuelles Datum
        date_cur = Literal(date, datatype=XSD.date)
        titel = re.sub("[/\W]", "_",df_pdf_meta['Titles'][i])
        title_cur = G_KG_ns._+titel #aktueller Titel
        con = re.sub("[/\W]", "_",df_pdf_meta['Conference'][i])
        con_cur = G_KG_ns._+con #aktuelle Konferenz

        g.add((G_KG_ns.paper, DC.title, title_cur))
        g.add((title_cur, DC.date, date_cur))
        g.add((G_KG_ns.conference, DC.title, con_cur))
        g.add((title_cur, DC.publisher, con_cur))

        for author in authors:
            author =  re.sub("[/\W]", "_",author)
            author_cur = G_KG_ns._+author
            g.add((G_KG_ns.Autor, FOAF.name, author_cur))
            g.add((title_cur, DC.creator, author_cur))

        for j in range(len(keyword_list_paper['keywords'])):
            #Festlegung mindest Relevanz
            if keyword_list_paper['relevance'][j] > 0.4:
                pk = re.sub("[/\W]", "_",keyword_list_paper['keywords'][j])
                pk_cur = G_KG_ns._+pk
                g.add((G_KG_ns.ThemengebietPaper, RDF.type, pk_cur))
                if df_pdf_meta['Titles'][i] == keyword_list_paper['paper'][j]:
                    #Beziehung zwischen Titeln und keywords mit Attribut label handelt von
                    g.add((title_cur, DC.subject, pk_cur))

        #Themen Konferenzen     
        for j in range(len(keyword_list_con['keywords'])):
            #Festlegung mindest Relevanz
            if keyword_list_con['relevance'][j] > 0.44:
                #Knotenerstellung aller keywords mit Attribut typ Thema Konferenz
                ck = re.sub("[/\W]", "_",keyword_list_con['keywords'][j])
                ck_cur = G_KG_ns._+ck
                g.add((G_KG_ns.ThemengebietKonferenz, RDF.type, ck_cur))
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
    plt.savefig("G_KG_RDF.png", format="PNG")

