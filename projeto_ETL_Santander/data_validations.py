# Validação de dados dos clientes
def validar_idade(valor, min_idade=0, max_idade=100):
    """
    Valida idade: deve ser numérica e dentro dos limites.
    """
    try:
        v = int(valor)
        return not (min_idade <= v <= max_idade)
    except:
        return True  # inválido se não for número

def validar_renda(valor, min_renda=0, max_renda=20000):
    """Valida renda: deve ser numérica e dentro dos limites."""
    try:
        v = float(valor)
        return not (min_renda <= v <= max_renda)
    except:
        return True

def validar_email(valor):
    """Valida email: deve conter '@' e '.'."""
    return "@" not in str(valor) or "." not in str(valor)

def relatorio_qualidade_clientes(arquivo_csv):
    """
    Gera um relatório de qualidade dos dados para auditoria em ETL.
    """
    df = pd.read_csv(arquivo_csv)

    relatorio = {
        "valores_nulos": df.isnull().sum().to_dict(),
        "duplicados": int(df.duplicated().sum()),
        "id_duplicado": int(df["cliente_id"].duplicated().sum()),
        "cidades_unicas": df["cidade"].value_counts().to_dict(),
        "profissoes_unicas": df["profissao"].value_counts().to_dict(),
        "idades_invalidas": df["idade"].apply(validar_idade).sum(),
        "rendas_invalidas": df["renda_mensal"].apply(validar_renda).sum(),
        "emails_invalidos": df["email"].apply(validar_email).sum()
    }

    return relatorio


# Validação dos dados das transações
def validar_valor(valor, tipo):
    """Valida valor da transação: saques devem ser negativos, depósitos/transferências positivos."""
    try:
        v = float(valor)
        if tipo == "saque":
            return v >= 0  # erro se saque não for negativo
        else:
            return v <= 0  # erro se depósito/transferência não for positivo
    except:
        return True  # inválido se não for número

def validar_data(valor):
    """Valida se a data pode ser convertida para datetime em algum dos formatos esperados."""
    formatos = ["%d/%m/%Y"]
    for f in formatos:
        try:
            datetime.strptime(str(valor), f)
            return False  # válido
        except:
            continue
    return True  # inválido

def relatorio_qualidade_transacoes(arquivo_csv):
    """
    Gera relatório de qualidade para dataset de transações.
    """
    df = pd.read_csv(arquivo_csv)

    relatorio = {
        "valores_nulos": df.isnull().sum().to_dict(),
        "duplicados": int(df.duplicated().sum()),
        "transacao_id_duplicado": int(df["transacao_id"].duplicated().sum()),
        "tipos_transacao": df["tipo"].value_counts().to_dict(),
        "valores_invalidos": df.apply(lambda row: validar_valor(row["valor"], row["tipo"]), axis=1).sum(),
        "datas_invalidas": df["data"].apply(validar_data).sum(),
        "agencias_unicas": df["agencia"].value_counts().to_dict()
    }

    return relatorio