#Funções para leitura dos dados, de acordo com formato

import pandas as pd

def read_csv(caminho_arquivo, separador_arquivo, encoding='utf-8'):
    print("Lendo o arquivo", caminho_arquivo)
    return pd.read_csv(caminho_arquivo, sep=separador_arquivo, encoding=encoding)


def read_sql():
    return 1

def read_json():
    return 1
