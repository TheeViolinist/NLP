import spacy



nlp = spacy.load("pt_core_news_lg") # Vamos carregar os pacotes 
doc1 = nlp("tesntaod")
print(doc1.text)