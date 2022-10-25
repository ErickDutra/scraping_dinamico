from urllib import request
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

def buscar(formatar):
    url = f'https://www.kabum.com.br/busca/{formatar}'

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}


    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    qtd_itens = soup.find('div', id='listingCount').get_text().strip()

    index = qtd_itens.find(' ')
    qtd = qtd_itens[:index]

    ultima_pagina = math.ceil(int(qtd)/20)

    dic_produtos = {'marca': [], 'preco': []}

    for i in range(1, ultima_pagina+1):
        url_pag = f'https://www.kabum.com.br/busca/{formatar}?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
        site = requests.get(url_pag, headers=headers)
        soup = BeautifulSoup(site.content, 'html.parser')
        produtos = soup.find_all('div', class_=re.compile('productCard'))

        for produto in produtos:
            marca = produto.find('span', class_=re.compile(
                'nameCard')).get_text().strip()
            preco = produto.find('span', class_=re.compile(
                'priceCard')).get_text().strip()
            print(marca, preco)

            dic_produtos['marca'].append(marca)
            dic_produtos['preco'].append(preco)
        print(url_pag)

    df = pd.DataFrame(dic_produtos)
    df.to_csv(r"C:\Users\erick\OneDrive\Área de Trabalho\scraping_dinamico\scraping_site_dinamico\placa_mae" , encoding='UTF-8', sep=';')

while True:
    escolha = int(input("Escolha uma opção: [1]Fazer pesquisa [0]Sair."))

    if escolha == 1:
        nome_nao_formatado = str(input("Oque deseja buscar?")).lower()
        nome_find = nome_nao_formatado.find(' ')
        if nome_find <= 0:
            formatar = nome_nao_formatado.replace(' ', '-')
            buscar(formatar)
        else:
            formatar = nome_nao_formatado
            buscar(formatar)
    elif escolha == 0:
        break
    

'''algumas buscas não funcionam por serem feitas as alterações somente na url de busca, assim sendo essas alteraçoes acabam não encontrando o site de busca, tente não incluir os "de", "da" exemplo: placa video. '''