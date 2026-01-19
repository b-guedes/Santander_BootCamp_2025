import pandas as pd
import re, json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


def transformar_clientes(arquivo_csv,
                        limites_idade=(0, 100),
                        limites_renda=(0, 20000),
                        cidades_validas=None,
                        preencher_profissao="Não Informado"):

    """
    Transforma o dataset de clientes:
    - Limpa string, converte tipos e aplica regras de idade/renda
    - Normaliza nomes, e-mails, cidades e profissões
    - Valida limites de idade e renda, descarta valores inválidos
    - Opcionalmente restringge cidades a uma lista de válidas
    Retorna DataFrame transformado e resumo de correções.
    """

    # Carrega o CSV
    df = pd.read_csv(arquivo_csv)
    resumo = {}

    # 1) Limpeza e correção de tipos
    # Tipos corretos e correções de nome, e-mail e cidade
    df["nome"] = df["nome"].astype(str).str.strip().str.title() #remover espaço e capitalizar
    df["email"] = df["email"].astype(str).str.strip().str.lower() #remover espaços e minúsculo
    df["cidade"] = df["cidade"].astype(str).str.strip().str.title() # remover espaços e capitalizar
    df["cliente_id"] = pd.to_numeric(df["cliente_id"], errors="coerce").astype(int) #numérico
    resumo['cliente_id_inconvertivel'] = int(df["cliente_id"].isna().sum())

    # 2) Idade: converter para numérico, inválidos viram NaN
    df["idade"] = pd.to_numeric(df["idade"], errors="coerce")
    idades_invalidas = (df["idade"] < limites_idade[0]) | (df["idade"] > limites_idade[1])
    df.loc[idades_invalidas, "idade"] = None
    resumo["idades_invalidas"] = int(idades_invalidas.sum())

    # 3) Cidade válida conforme lista
    if cidades_validas:
        cidades_invalidas = ~df["cidade"].isin(cidades_validas)
        df.loc[cidades_invalidas, "cidade"] = None
        resumo["cidades_invalidas"] = int(cidades_invalidas.sum())

    # 4) Profissão: preencher nulos e outras correções
    df["profissao"] = df["profissao"].astype(str).str.strip()
    profissoes_invalidas = df['profissao'] == ""
    resumo["profissoes_preenchidas"] = int(profissoes_invalidas.sum())
    df.loc[profissoes_invalidas, "profissao"] = preencher_profissao

    # 5) Renda: converter para float, inválidos viram NaN
    df["renda_mensal"] = pd.to_numeric(df["renda_mensal"], errors="coerce")
    rendas_invalidas = (df["renda_mensal"] < limites_renda[0]) | (df["renda_mensal"] > limites_renda[1])
    df.loc[rendas_invalidas, "renda_mensal"] = None
    resumo["rendas_invalidas"] = int(rendas_invalidas.sum())

    # 6) Integridade e consistência
    # - Duplicatas por cliente_id
    id_duplicado = df["cliente_id"].duplicated(keep="first")
    resumo["cliente_id_duplicado"] = int(id_duplicado.sum())
    df = df[~id_duplicado].copy()

    # - Linhas críticas inválidas: id nulo
    linhas_invalidas = df["cliente_id"].isna()
    resumo["linhas_descartadas"] = int(linhas_invalidas.sum())
    df = df[~linhas_invalidas].copy()
    resumo["registros_finais"] = int(len(df))

    return df, resumo


def transformar_transacoes(arquivo_csv,
                        formatos_data=("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"),
                        tipos_validos=("deposito", "saque", "transferencia"),
                        corrigir_sinal=True):
    """
    Transforma o dataset de transações:
    - Sanitiza strings, converte tipos, aplica regras de valor por tipo.
    - Converte datas para datetime com múltiplos formatos.
    - Deduplica transações e valida IDs.
    Retorna DataFrame transformado e resumo de correções.
    """
    df = pd.read_csv(arquivo_csv)
    resumo = {}

    # 1) Sanitização
    df["cliente_id"] = df["cliente_id"].astype(str).str.strip().str.upper()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.lower()
    df["agencia"] = df["agencia"].astype(str).str.strip().str.upper()

    # 2) Coerção de tipos
    df["transacao_id"] = pd.to_numeric(df["transacao_id"], errors="coerce").astype("Int64")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

    resumo["transacao_id_inconvertivel"] = int(df["transacao_id"].isna().sum())
    resumo["valor_inconvertivel"] = int(df["valor"].isna().sum())

    # 3) Regras de negócio (sinais e limites)
    if corrigir_sinal:
        saque_pos = (df["tipo"] == "saque") & (df["valor"] > 0)
        dep_neg = (df["tipo"].isin(["deposito", "transferencia"])) & (df["valor"] < 0)

        resumo["saques_corrigidos_sinal"] = int(saque_pos.sum())
        resumo["dep_transf_corrigidos_sinal"] = int(dep_neg.sum())

        df.loc[saque_pos, "valor"] = -df.loc[saque_pos, "valor"]
        df.loc[dep_neg, "valor"] = df.loc[dep_neg, "valor"].abs()

    # 4) Conversão de datas (múltiplos formatos)
    def parse_data(x):
        s = str(x).strip()
        for f in formatos_data:
            try:
                return pd.to_datetime(s, format=f)
            except:
                continue
        return pd.NaT

    df["data"] = df["data"].apply(parse_data)
    resumo["datas_invalidas"] = int(df["data"].isna().sum())

    # 5) Normalização de categorias
    # - Tipos inválidos
    tipo_invalido = ~df["tipo"].isin(tipos_validos)
    resumo["tipo_transacao_invalido"] = int(tipo_invalido.sum())
    # Estratégia: manter para revisão ou descartar
    # df = df[~tipo_invalido].copy()

    # 6) Integridade e consistência
    # - Duplicatas por transacao_id
    dup_tx = df["transacao_id"].duplicated(keep="first")
    resumo["transacao_id_duplicado"] = int(dup_tx.sum())
    df = df[~dup_tx].copy()

    # - Linhas críticas inválidas: id nulo, valor NaN, tipo inválido
    linhas_invalidas = df["transacao_id"].isna() | df["valor"].isna() | tipo_invalido.reindex(df.index, fill_value=False)
    resumo["linhas_descartadas"] = int(linhas_invalidas.sum())
    df = df[~linhas_invalidas].copy()

    resumo["registros_finais"] = int(len(df))
    return df, resumo


# Relatórios de transformação
def imprimir_resumo_transformacao(titulo, resumo, salvar_resumo=None):
    """
    Imprime e opcionalmente salva o resumo de transormação

    Parâmetros:
    - título: título do relatório
    - resumo: dicionário com resumo de transformação
    - salvar: caminho do arquivo para salvar o relatório em JSON ou TXT (opcional)

    """
    # Impressão no console de saída
    print("\n" + "="*60)
    print(titulo)
    print("="*60)
    for k, v in resumo.items():
        print(f"- {k}: {v}")

    # Salvamento em arquivo
    if salvar_resumo:
        registro = { "titulo": titulo, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "resumo": resumo }
        # Se for JSON
        if salvar_resumo.endswith(".json"):
            with open(salvar_resumo, "a", encoding="utf-8") as arquivo:
                arquivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
            # Se for TXT
        elif salvar_resumo.endswith(".txt"):
            with open(salvar_resumo, "a", encoding="utf-8") as arquivo:
                arquivo.write("\n" + "="*60 + "\n")
                arquivo.write(titulo + "\n")
                arquivo.write("="*60 + "\n")
                arquivo.write("Timestamp: " + registro["timestamp"] + "\n")
            for k, v in resumo.items():
                arquivo.write(f"- {k}: {v}\n")
        else:
            raise ValueError("Formato de arquivo não suportado. Use .json ou .txt")