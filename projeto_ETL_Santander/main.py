import logging, csv, random, re, json, sqlite3
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import setup_logging, timestamp, gerar_datasets, extrair_dados, validar_dados, transformar_dados, carregar_dados
from data_generation_clientes import *
from data_generation_transacoes import *
from data_cleaning import *
from data_validations import *
from data_load import *


# ============================== 
# Configuração de Logging 
# ============================== 
logger = setup_logging('main')


# ============================== 
# Funções principais 
# ============================== 
def main():
    logger.info(f"Pipeline ETL iniciado. Timestamp: {timestamp()}")
    try:
        gerar_datasets()
        df_clientes, df_transacoes = extrair_dados()
        validar_dados()
        df_clientes, df_transacoes = transformar_dados()
        carregar_dados(df_clientes, df_transacoes)
        logger.info("Pipeline ETL concluído com sucesso.")
    except Exception as e:
        logger.error(f"Pipeline ETL falhou: {e}")
    finally:
        logger.info(f"Execução finalizada. Timestamp: {timestamp()}")

if __name__ == "__main__":
    main()