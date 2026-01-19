def carregar_csv(df, destino="clientes_transformados.csv"):
    """
    Carrega DataFrame transformado em um CSV final.
    """
    df.to_csv(destino, index=False, encoding="utf-8")
    logging.info(f"Dados carregados em {destino} com {len(df)} registros.")


def carregar_sql(df, tabela, banco="etl.db"):
    """
    Carrega DataFrame transformado em uma tabela SQL.
    """
    conn = sqlite3.connect(banco)
    df.to_sql(tabela, conn, if_exists="replace", index=False)
    conn.close()
    logging.info(f"Dados carregados na tabela '{tabela}' do banco {banco}.")