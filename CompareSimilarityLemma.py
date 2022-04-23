import json
import spacy

nlp = spacy.load("pt_core_news_lg") # Vamos carregar os pacotes 

nome_resumo:str = ""
nome_resumo = input()



# Função responsável por abrir o arquivo .json e retornar os dados, esses são uma lista de dicionários do tipo:
# Os dados .json vem dessa forma
#[  {
#     "indice" = 0
#     "titulo" = ""
#     "autor" = ""
#     "texto" = ""
#    }...
#]
#
#
# Parâmetros:
#             nome: string do nome do arquivo inserido pelo usuário
#
#
# Retorno:
#             Retorna uma lista de dicionários
def open_arquivo(nome: str):
    
    # Lista de dicionário que vai conter os dados do .json
    resumos:list = []
    with open(nome) as file:
        resumos = json.load(file)
        file.close()

    return resumos






# Função responsável por retirar stop word dos textos, que são palavras sem muito significados como artigos, pronomes, adjetivos
# Parâmetros:
#            doc: list de objetos DOC da biblioteca spacy contendo todos os resumos
#
#
# Retorno:
#            Retorna uma string modificada somente com palavras essenciais
#
#
def remove_stop_words(doc):
    resume: str = ''
    # Cria-se uma lista de palavras que são artigos, pronomes, adjetivos, ADP, que são junções de preposição e verbo.
    # Retira-se auxiliares, que seriam verbos como "É", "Foi", e retira conjunções  como "mas".
    # Retira-se numerais, pontuações e simbolos. Então tenta realizar um tratamento para deixar as frases essenciais
    # Retira-se também advérbios
    # Cria-se uma lista de palavras proibidas, pois como queremos medir a similaridade entre dois resumos,
    # E medimos a similaridade com artigos parecidos, pronomes etc, iria criar uma similaridade falsa,
    # Então, deve-se retirar 
    #word_forbidden: list = ["DET", "PRON", "ADP", "ADJ","AUX", "CCONJ", "NUM", "PUNCT", "SYM", "ADV", "SCONJ"]


    for token in doc:
        # Se a palavra(token) estiver na lista de palavras proibidas então ela não será colocada no texto final e 
        #se ela não for uma stop_word, foi utilizado isso, porque a lista contém adjetivo e tonke.stop_word não o contém
        #logo, aumenta-se ainda mais a precisão de tratamento do texto
        if not token.is_stop and token.pos_ != 'PUNCT':
            resume += token.text + ' '
        
        
        
    

    return resume





# Função responsável por lematerizar a palavra, ou seja, deixar as palavras da frase na sua forma raiz
# Parâmetros:
#              doc: lista de objetos DOC da biblioteca spacy, contendo todos os resumos
#
#
#
# Retorno:
#               Retorna uma string contendo as frases lematerizadas
#
#
def lemmatizer_resume(doc):
    # String que vai conter o texto lemmaterizado
    resume: str = ''

    # Percorre o documento
    for token in doc:
        # Verifica se ele já existe dentro da string
        if token.lemma_ not in resume:
            # Caso não, adicione
            resume += token.lemma_ + " "
    
    return resume










# Função responsável por retornar uma lista de objetos DOCS da biblioteca spacy, o qual contém os resumos tratados de cada aluno
#
#
# Parâmetros:
#             resumos: lista de dicionários que contém os resumos
#
#
# Retorno:
#             dados_docs: Retorna uma lista contendo objetos DOCS da biblioteca spacy
#
def retorna_listaDoc(resumos:list):
    
    indice: int = 0 # Indice para regular quais dados estão sendo armazenados
    dados_docs:list = []   # Lista de objetos DOCS que será retornada
    
    #Percorre-se a lista de resumos
    for item in resumos:
        # Utiliza-se o método nlp para transformar os dados em objetos DOC
        doc = nlp(resumos[indice]["texto"].lower())
        

        # Chamada da função remove_stop_words para fazer tratamento do texto
        doc = nlp(remove_stop_words(doc))

        # Lemmatizer o documento, tornando-o somente as palavras raiz
        doc = nlp(lemmatizer_resume(doc))
        
        
        # Adiciona-se a lista de objetos
        dados_docs.append(doc)
        indice += 1
       
    
    
    return dados_docs
        

    
    
    
    
    
    
    
# Função responsável por retornar  a matriz de similaridade entre os elementos
# 
# 
# Parâmetros:
#          docs: lista de objetos do tipo doc
# 
# Retorno:
#           Similarity: Matriz da similaridade entre os elementos
#   
def dados_similarity(docs: list, resumos: list):
    similarity: list = [] # Matriz onde ficará as comparações

    menor: float = docs[0].similarity(docs[1]) # Valor do menor inicialmente
    maior: float = docs[0].similarity(docs[1]) # valor do maior inicilmanete


    indice_primeiro = 0     # Somador do índice do primeiro valor a ser comparado
    indice_segundo = 0      # Indice do segundo elemento a ser comparado

    #Indice do primeiro e segundo após comparacao
    indice_comparacao_primeiro  = 0
    indice_comparacao_segundo  = 0


    # Indice de comparação dos maiores valores
    indice_maior_comparacao_primeiro = 0
    indice_maior_comparacao_segundo = 0

    # Para cada resumo em docs faz a similaridade entre cada elemento subsquente
    # Cria-se uma lista temporária de similaridades daquela linha  e adiciona na matriz similarity
    for resume in docs:
        similarity_temp: list = [] # Matriz temporária de similaridade

        indice_primeiro += 1   # A cada iteração soma-se o indice com 1

        for resume_pos in docs:

            indice_segundo += 1   # A cada iteração soma-se novamente o indice

            similarity_temp.append(resume.similarity(resume_pos))
            
            # Acha-se o menor valor e o indice deles
            if resume.similarity(resume_pos) < menor:
                menor = resume.similarity(resume_pos)
                indice_comparacao_primeiro = indice_primeiro
                indice_comparacao_segundo = indice_segundo

            # Acha-se o maior valor e o índice deles
            if resume.similarity(resume_pos) > maior and resume.similarity(resume_pos) != 1:
                maior = resume.similarity(resume_pos)
                indice_maior_comparacao_primeiro = indice_primeiro
                indice_maior_comparacao_segundo = indice_segundo



        indice_segundo = 0 # Reseta o valor do indice para iterar novamente na linha
            
        similarity.append(similarity_temp)
    
    
    print(f'A menor similaridade eh: {menor}')
    
    # Print os titulos dos trabalhos
    print(f'Os índices são: {indice_comparacao_primeiro} e {indice_comparacao_segundo}')
    print(f'Os títulos dos trabalhos são: : {resumos[indice_comparacao_primeiro]["titulo"]}')
    print(f'e {resumos[indice_comparacao_segundo]["titulo"]}\n')



    print(f'A maior similaridade eh: {maior}')
    print(f'Os índices são: {indice_maior_comparacao_primeiro} e {indice_maior_comparacao_segundo}')
    print(f'O título do primeiro eh: {resumos[indice_maior_comparacao_primeiro]["titulo"]}\n')
    #print(resumos[indice_maior_comparacao_primeiro])
    print(docs[indice_maior_comparacao_primeiro].text)
    

    print(f'O título do segundo eh: {resumos[indice_maior_comparacao_segundo]["titulo"]}')
    print(docs[indice_maior_comparacao_segundo].text)

    print(f'\n\n {similarity[1045][1046]}')
    return similarity
            





# Função responsável por armazenar os dados da matriz em um arquivo .json
def salva_arquivo(similarity: list):
    # Não precisa da fclose porque o open fecha automaticamente
    with open("similarity_results.json", "w") as file:
        json.dump(similarity, file, indent=2)


            


       
            
resumos:list = open_arquivo(nome_resumo) # Lista contendo todos os dados sobre os resumos

docs:list = retorna_listaDoc(resumos)    # Lista de objetos DOCS da biblioteca spacy

similarity:list = dados_similarity(docs, resumos)
salva_arquivo(similarity)
    

    
    