import json, requests

r = requests.get('https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_get')
data = r.text

lista = json.loads(data)
posts = lista['posts']

#Exercicio A: IDs dos produtos que contém "promoção" no título e seus respectivos preços para todas as mídias.
listaPromocao = []

for i in posts:
    #preenchendo lista do exercicio A
    if "promocao" in i['title']:
        listaPromocao.append(i)

#ordena lista
def myFunc(e):
    return e['price']

listaPromocao.sort(key=myFunc)

#elimina repeticoes
listaPromocaoSemRep = []
chave = ''
for i in listaPromocao:
    if i['product_id'] != chave:
        listaPromocaoSemRep.append(i)
        chave = i['product_id']

#cria dicionario
response_a = []
auxdict = {}

for i in listaPromocaoSemRep:
    auxdict.update({'product_id':i['product_id'], 'price':i['price']})
    response_a.append(auxdict)
    auxdict = {}
    
#print(response_a)
    
#Exercicio B: IDs dos posts e preços dos produtos para as postagens com mais de 700 likes na mídia instagram_cpc.
    
postsInsta = []
cnt = 0
for i in posts:
    #preenchendo lista do exercicio B
    if "instagram" in i['media']:
        if i['likes']>=700:
            postsInsta.append(i)
         
#ordena lista
def myFunc(e):
    return e['price']

postsInsta.sort(key=myFunc)

#elimina repeticoes
response_b = []
auxdict = {}
chave = ''
for i in postsInsta:
    if i['product_id'] != chave:
#        postsInstaSemRep.append(i)
        auxdict.update({'product_id':i['product_id'], 'price':i['price']})
        response_b.append(auxdict)
        auxdict = {}
        chave = i['product_id']

#print(response_b)
    
#Exercicio C: Somatório de likes no mês de maio de 2019 para todas as mídias pagas (google_cpc, facebook_cpc,instagram_cpc).
#optei por calcular separado os likes de cada midia social caso seja de interesse futuro ter cada conjunto separadamente

likesInsta = 0
likesFace = 0
likesGoogle = 0
    
for i in posts:
    if "/05/2019" in i['date']:
        if "google_cpc" in i['media']:
            likesGoogle+=i['likes']
        if "facebook_cpc" in i['media']:
            likesFace+=i['likes']
        if "instagram_cpc" in i['media']:
            likesInsta+=i['likes']

response_c = likesInsta+likesFace+likesGoogle

#print(response_c)

#Exercicio D: lista de produtos com erro no preço

er = requests.get('https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_get_error')
postsVerify = er.text

listaCheck = json.loads(postsVerify)
postsCheck = listaCheck['posts']

#ordena lista pelo id do produto
def myFunc(e):
    return e['product_id']

postsCheck.sort(key=myFunc)

#procura erros
response_d = []
id_ = ''
preco = ''

for i in postsCheck:
    if i['product_id'] != id_:
        id_ = i['product_id']
        preco = i['price']
    if i['price'] != preco:
        response_d.append(i['product_id'])

#dicionario com as respostas finais
response = {
        "full_name": "Betariz Campos de Almeida de Castro Monteiro",
        "email": "beatriz.campos.monteiro@usp.br",
        "code_link'": "www.github.com/name/psel-raccoon",
        "response_a": response_a,
        "response_b": response_b,
        "response_c": response_c,
        "response_d": response_d
        }

response = json.dumps(response)

url = 'https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_post'
confirma = requests.post(url, data = response, timeout=2.50)
print(confirma)
