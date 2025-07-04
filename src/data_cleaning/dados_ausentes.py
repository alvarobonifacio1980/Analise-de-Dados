#Funções para analise dos dados, verificando registros ausentes
import pandas as pd

def analisa_dados_ausentes(dataframe: pd.DataFrame):
    dados_ausentes = dataframe.isna().sum()
    total_registros = len(dataframe)
    df_ausentes = dados_ausentes.reset_index()
    df_ausentes.columns = ["Coluna", "Qtde_ausentes"]
    df_ausentes["Percentual"] = df_ausentes["Qtde_ausentes"] / total_registros * 100
    df_ausentes["Percentual"] = df_ausentes["Percentual"].apply(lambda x: f"{x:.2f}%")
    filtro = df_ausentes['Qtde_ausentes'] > 0
    return df_ausentes[filtro]

