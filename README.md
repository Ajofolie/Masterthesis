# Masterthesis

Die endgültig genutzte Sammlung besteht aus 83 wissenschaftlichen papern und 16 zugehörigen Konferenzen.

Dateien:
- Ordner keywords: Enthält die generierten keywords aus Publikationen und Konferenzen

- Ordner PDF: Enthält die verwendeten Publikationen

- Ordner AimsAndScope: Enthält die verwendeten Konferenzbeschreibungen

- metadata_list: Hilfs-Excel-Datei zur Befüllung sowie Korrektur der Metadaten von wissenschaftlichen Veröffentlichungen

- Energy efficiency_Test: Test PDF-Datei zur Erweiterung der Hilfsdatei metadata_list.xlsx

- G_KG.ttl: Resultierende turtle Datei. Enthält alle Triple des RDF Graphen

- G_KG_Update.ttl: Test turtle Datei zur Erweiterung der Wissensbasis durch weitere Triple

- G_KG_Networkx: Resultierender Graph nur durch Networkx erstellt.

- G_KG_RDF_ohne_lab: Bild des RDF-Graphen ohne Label

- PreProcessMetadata: Programmteil 1

- PreProcess_NLP: Programmteil 2

- KG: Programmteil 3

- main: Ausführung der Programmteile, SPARQL Abfragen, Update des Graphen

- KG_old: Altes Programm zur Erstellung des Graphen mittels Networkx

In den Folgenden Abschnitten wird auf die einzelnen Programmteile eingegangen und die Rolle der Metadaten Datei näher erläutert.

PreProcessMetadata
Das Skript umfasst drei folgende Funktionen:

     read_paper_meta

Die erste Funktion  hat die Aufgabe, die Metadaten der wissenschaftlichen paper einzulesen und diese in die Hilfsdatei metadata_list.xlsx zu schreiben. Dabei ist es wichtig, dass eine solche Datei bereits existiert. Das Lesen und auslesen dieser Datei wird durch das Paket pandas ermöglicht.


In einem ersten Schritt wird über die Ordnerstruktur iteriert, wobei geprüft wird, ob der Name einer PDF Datei bereits in der Excel Datei existiert. Die Iteration geschieht durch das Modul pathlib, da zum Einen die Struktur des Pfades verändert wird, und zum Anderen die Funktion glob eine Liste mit allen in diesem Pfad befindlichen Dateien erstellt (die mit .pdf enden).
Falls der Name der PDF Datei bereits existiert, wird geprüft, ob die Spalte Check zu dieser PDF Datei befüllt ist oder nicht. Diese Spalte dient der manuellen Überprüfung auf Korrektheit der Metadaten durch den Nutzer selbst. Ist die Spalte nicht befüllt, wird eine Flag auf False gesetzt, welche im späteren Verlauf der Funktion eine Rolle spielt.
Ist der Name der Datei noch nicht in der Metadaten Liste vorhanden, so wird der Dateiname in die Metadaten Liste unter PDF eingetragen, die Metadaten der PDF ausgelesen und in die jeweiligen Spalten eingetragen. 
Das Einlesen und Bearbeiten der Metadaten wird durch die Module
fitz(PyMuPDF) und PyMuPDF2 (PDFFileReader und PDFFileWriter) realisiert.
Da es möglich ist, dass abgefragte Metadateninformationen nicht vorhanden sind, erfolgt vor jedem holen der jeweiligen Metadateninformation eine Abfrage, ob diese auch vorhanden ist. Ist dies der Fall, wird die Information in einer Variable in Form einer Liste gespeichert. Ansonsten wird die Metadateninformation für das jeweilige paper leer angelegt und gespeichert. Dies muss im Fall der ConferenceName Information geschehen, da es sich hierbei um eine benutzerdefinierte Information handelt. Die einzelnen Informationen werden in Listen zwischengespeichert, die dann zur Befüllung der Spalten in der Excel Datei dienen. Am Ende werden eventuell bereits vorhandene Informationen mit neuen Informationen zusammengebracht, um ein Überschreiben von bereits existierenden Informationen in der Excel Datei zu verhindern und eine Fortschreibung zu ermöglichen. 
Am Ende der Funktion spielt die gesetzte Flag eine Rolle. Denn falls diese Flag auf False steht, soll das Programm abbrechen und die metadata_list.xlsx Datei öffnen. Das Öffnen wird über das build-in Paket os realisiert. Somit wird eine manuelle Überprüfung durch den Nutzer vorausgesetzt und eine sichere Weiterverarbeitung garantiert. Die Flag wird auf False gesetzt wenn eine Datei noch nicht in der Liste vorhanden war oder die Spalte Check nicht befüllt ist.
Die Funktion erhält den Dateipfad wo sich die PDF Dateien befinden als Übergabeparameter und gibt die Liste der gesammelten Metadaten als Rückgabewert zurück.

     write_paper_meta

Nachdem die Metadaten Liste korrekt befüllt und gepflegt wurde, wird die nächste Funktion aufgerufen. Dieser Schritt dient einer konsistenten Datenhaltung. Denn hier werden die korrigierten Metadaten in die eigentlichen Metadaten der Dateien geschrieben. Somit ist auch eine Löschung der Metadaten Liste unproblematisch, denn bei einer weiteren Ausführung der Funktion read_paper_meta würden die korrigierten Metadaten erneut in die Liste eingetragen werden. Die Funktion erhält ebenfalls den Dateipfad als Übergabeparamter, in dem sich die PDF Dateien befinden. In diesem Schritt werden mittels der erstellten und korrigierten Excel Liste alle Metadaten eingelesen und in den jeweiligen PDF Dateien eingepflegt. Diese Funktion besitzt keinen Rückgabeparameter.
Analog dazu existiert eine weitere Funktion.

     write_conference_meta

Hier wird der Titel einer Konferenz ermittelt und in den Metadaten einer Konferenzbeschreibung hinterlegt. Auch hier wird wieder der Dateipfad übergeben und das Objekt mit den Metadateninformationen. Hier muss jedoch auch über alle Konferenzbeschreibungen iteriert werden, da noch keine Verbindung zwischen den Konferenztiteln und den tatsächlichen Konferenz Dateien besteht. Da aber in jeder Konferenzbeschreibung auch der Titel der Konferenz enthalten ist, kann durch eine Prüfung, ob der ConferenceName aus der Metadatenliste in einer Konferenz Datei vorhanden ist, auch der Titel in die Metadaten der Konferenz Datei geschrieben werden. Auch diese Funktion gibt keinen Wert zurück.

Nachdem diese Funktionen ausgeführt wurden, ergibt sich eine Datenhaltung mit korrekten und gepflegten Metadaten. Diese Metadaten können dazu genutzt werden, die ersten Knoten in der Wissensbasis zu befüllen und bilden den ersten Pflicht Übergabeparameter für die Funktion, die später die Knoten und Kanten des Graphen bilden.

     PreProcess_NLP
Das Skript besteht aus folgenden Funktionen:

     build_corpus: liest Texte aus den PDF Dateien und bildet den Text Korpus zu wissenschafltichen Publikationen
     build_conference: liest Texte aus den Konferenz Beschreibungen und bildet den Text Korpus zu Konferenzen
     preprocess_corpus: Vorverarbeitung der Texte
     get_stopwords: Definition der Stopwords
     generate_keywords: Erstellung der keywords aus den PDF Dateien

     build_corpus und build_conference

Bei dieser Funktion wird ein Dictionary erstellt, welches die Titel und Texte der PDF Dateien enthält. Der Übergabeparameter ist der Dateipfad, in dem sich die Dateien befinden. Erneut wird mithilfe von fitz über die Dateien iteriert um die Metadaten, genauer den hinterlegten Titel, auszulesen. Darauf folgt eine weitere Schleife, die Seite für Seite in einem PDF Dokument nach einem abstract sucht. Die Suche wird durch string matching realisiert. Falls die Seite gefunden wird auf dem sich das abstract befindet, wird ausschließlich der Text von dieser Seite in dem erstellten dictionary gespeichert. Falls das Dokument kein abstract enthält, wird der gesamte Text des Dokuments gespeichert. Das gefüllte dictionary wird am Ende der Funktion zurückgegeben.
In build_conference werden analog zu build_corpus die Beschreibung von Konferenzen ausgelesen. Auch hier wird der Dateipfad als Parameter übergeben und ein identisches dictionary zurückgegeben. Hier wird jedoch immer der gesamte Text gespeichert.

     preprocess_corpus

Nachdem die Texte extrahiert wurden, soll der Text vorverarbeitet werden. Dazu wird die Variable mit allen Texten übergeben und tokenisiert. 
Nach diesen Transformationen werden die Texte zurückgegeben und können weitervearbeitet werden.

     get_stopwords

Diese Funktion dient zur Zusammenstellung der stopwords. Diese Wörter sollen aus den Texten herausgefiltert werden und bei der Generierung von keywords nicht berücksichtigt werden. Neben einer feststehenden Liste an Wörtern, können auch benutzerdefinierte Begriffe hinzugefügt werden. Neben der englischen stopword Liste wurden in autorefanhang:stopwords aufgeführte Wörter festgesetzt.

     generate_keywords

Die Kernfunktion dieses Skripts erzeugt die keywords aus den wissenschaftlichen papern und Konferenzbeschreibungen. Die Funktion erhält als Parameter die aufbereiteten Texte und zum Anderen die Texte aus den Konferenzen. Es werden zwei dictionaries deklariert, für die Texte der paper und der Texte aus den Konferenzbeschreibungen. Sie beinhalten außerdem die keys keywords, relevance und paper bzw. conference. Außerdem wird das Modell zur keyword Extraktion definiert. In diesem Fall wird KeyBERT verwendet, welches auch aus der gleichnamigen Bibliothek stammt. 

Das verwendete vortrainierte Modell ist all-mpnet-base-v2. Dieses Modell bildet Sätze und Paragraphen auf einen 768 dimensionalen dichten Vektorraum ab und kann für Aufgaben wie Clustering oder semantische Suche verwendet werdencitehuggingFaceModell.
Zusätzlich wird ein vectorr eingesetzt. Es wird der KeyphraseCountVectorr mit dem Parameter stop_words versehen, der die in generate_keywords definierten stopwords berücksichtigt.

Der KeyphraseCountVectorr wandelt die keyphrases und keywords mittels POS in eine Matrix. Diese Matrix beschreibt die Häufigkeit der keyphrases, die in dem jeweiligen Textdokument vorkommen. Das Paket nutzt zusätzlich spaCy, um das POS-Tagging durchzuführen. Diese Tags werden dann mit dem definierten regulären Ausdrucks abgeglichen. Vordefiniert ist hierbei eine Abfolge von keinen oder mehreren Adjektiven, auf die eines oder mehreren Nomen folgen citekeyphrasevecSchopf. In dieser Implementierung wurde diese Abfolge übernommen, da dies die besten Resultate in diesem Anwendungsfall liefern kann. Aus den Ergebnissen wird anschließend die Matrix gebildet. Durch die Verwendung von POS-Tagging durch spaCy, sind die entstandenen keywords- und phrases grammatikalisch korrekt.

Für jeden Text, aus wissenschaftlichen papern und Konferenzbeschreibungen werden keywords durch das gewählte Modell generiert. KeyBERT bildet zum Einen mithilfe des gewählten vectorrs mögliche keyphrase und keyword Kandidaten und zum Anderen die dazu gehörigen embeddings, also die Umformung in numerische Daten. Die numerischen Daten werden für jeden keyword Kandidaten, sowie für jedes einzelne Textdokument gebildet. Am Ende werden diese Werte abgeglichen, um die keywords- und phrases zu wählen, die das Dokument am besten widerspiegeln. Diese Methoden und weitere Parameter können der Funktion extract_keywords, die zur KeyBert Implementierung gehört, wie folgt angepasst werden:


     doc=corpus['text'][x]
     vectorr=vectorr
     top_n=20 (für Konferenzen 10)
     use_mmr=True
     diversity=0.6 (für Konferenzen 0.6)


Der mitgegebene corpus stellt die Sammlung an extrahierten Texten aus den PDF Dokumenten dar. Der vectorr beschreibt den übergebenen KeyphraseCountVectorr. Der Parameter top_n bezeichnet die Anzahl der Wörter und Phrasen, die ausgewählt werden sollen. Darüber hinaus werden die Berechnungen zur Auswahl dieser gesetzt. Es wurde die Berechnung mittels maximal marginal relevance gewählt. Die Wahl ist eine Diversität von 0.5, da hier die besten Ergebnisse erzielt werden können.

Nach der Generierung werden die keywords für wissenschaftliche paper und Konferenzbeschreibungen in .csv-Dateien geschrieben und gespeichert. Diese sind in dargestellt.

Die Tabelle für die paper beinhaltet neben den keywords und der zugehörigen Relevanz (wie gut passt das keyword zu dem Text) den Titel des zugehörigen papers. Selbiges gilt für Konferenzen, wo der Konferenztitel mit abgebildet wird. Diese beiden Datenstrukturen werden auch von der Funktion zurückgegeben.

     KG_old
Das dritte Skript besteht aus mehreren Funktionen. Eine sorgt für die Befüllung des Graphen und die Andere für eine Farbpalette, die die Knoten in Abhängigkeit ihres Überknotens (Label) einfärbt. Alle Weiteren dienen der Abfrage des Graphen.

     kg_colors

Durch die Erstellung einer colormap werden alle Konferenzen in einer Farbe dargestellt und beispielsweise Autoren in einer anderen. Die gewählte Farbpalette ist turbofootnoteurlhttps://matplotlib.org/stable/tutorials/colors/colormaps.html aus dem imporierten Paket matplotlib.

     get_entity_rel

Neben der Farbgebung sorgt diese Funktion für die Erstellung der Kanten und Knoten. Übergeben werden hierbei folgende Parameter:

     Das Dataframe, welches die PDF Dateien enthält (analog zu metadata_list.xlsx)
     den mittels networkx erstellten Graphen
     die durch KeyBert erstellten keywords- und phrases von wissenschaftlichen papern
     die durch KeyBert erstellten keywords- und phrases von Konferenzbeschreibungen


Die Funktion erstellt zuerst die Überknoten mittels:

     KG_entities.add_node("Paper", color=0.9, typ='class')

beziehungsweise Instanzknoten:

     KG_entities.add_node(author, color=2, typ='Autor')

 Im Anschluss folgt eine Iteration über jeden Eintrag des Dataframes und generiert dabei Knoten für jeden Titel, zugehörige Autoren und Konferenzen. 

     KG_entities.add_node(meta['Titles'][i], date=meta['Date'][i],
         color=0.8, typ='Titel')

An jeder Stelle, an der Knoten erstellt werden, wird auch ein Farbe über das Attribut color definiert, die die Knoten erhalten sollen.
Zusätzlich werden die Kanten erstellt:

     KG_entities.add_edge(meta['Conference'][i], 'Konferenz',
         label='ist') #Überknoten
     KG_entities.add_edge(meta['Titles'][i], meta['Conference'][i], 
         label='ist Teil von') #Instanzknoten

Die Themen, also generierte keywords- und phrases werden auch in dieser Funktion als Knoten gebildet. Es wird ein Knoten mit seiner Farbe erstellt und die zugehörige Kante zum zugehörigen Titel oder Konferenz über thematisiert gebildet. Die richtige Zuordnung der Kanten wird zum Einen darüber garantiert, dass es durch den Aufbau des Dataframes möglich ist über einzelne Zeilen zu iterieren. Zum Anderen wird bei Themengebieten zusätzlich geprüft, ob der Titel, bzw. die Konferenz gleich dem Titel oder der Konferenz in den keyword Auflistungen ist. Zurückgegeben wird der entstandene Graph.
Die Abfrage des Graphen mittels Suchbegriffen wird in weiteren Funktionen realisiert. Je nach Abfrage werden unterschiedliche Ergebnisse geliefert.
Außerhalb der Funktion wird der gesuchte Begriff definiert und gegebenenfalls die Suchergebnisse nach einer Überklasse spezifiziert.
Dieser Begriff wird zuerst über eine Schleife in den Knoten des Graphen gesucht. Falls der Begriff gefunden wird, wird die Funktion query_graph mit dem Knoten, in dem sich der Begriff befindet, aufgerufen.
