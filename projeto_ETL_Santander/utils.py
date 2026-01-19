import logging
from datetime import datetime
import json
import yaml
from typing import Any, Dict
import os

def setup_logging(name: str = None):
    """
    Configura logging para console e arquivo.
    Retorna um logger nomeado.
    """
    # Cria diretório de logs se não existir
    os.makedirs("logs", exist_ok=True)

    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"etl_pipeline_{timestamp}.log"
    log_path = os.path.join('logs', log_file)

    # Formato padrão
    log_format = "%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s"

    # Configuração básica
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(),              # Console
            logging.FileHandler(log_path, mode="a", encoding="utf-8")  # Arquivo
        ]
    )

    return logging.getLogger(name)


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_json(data: Dict[str, Any], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ============================== 
# Funções principais 
# ============================== 
def gerar_datasets():
    """Gera datasets iniciais de clientes e transações.""" 
    try: 
        faker = Faker("pt_BR") 
        logger.info("Iniciando geração de datasets randômicos.") 
        gerar_clientes("001_seed_clientes.csv", num_registros=50) 
        gerar_transacoes("002_seed_transacoes.csv", num_registros=500) 
        logger.info("Datasets gerados com sucesso.") 
    except Exception as e: 
        logger.exception("Erro ao gerar datasets: %s", e) 
        raise 
    
def extrair_dados(): 
    """Extrai dados dos arquivos CSV gerados.""" 
    try: 
        logger.info("Iniciando extração dos dados.") 
        df_clientes = pd.read_csv("001_seed_clientes.csv") 
        df_transacoes = pd.read_csv("002_seed_transacoes.csv") 
        logger.info("Extração concluída com sucesso.") 
        return df_clientes, df_transacoes 
    except Exception as e: 
        logger.exception("Erro na extração dos dados: %s", e) 
        raise 
    
def validar_dados(): 
    """Valida qualidade dos dados extraídos e gera relatórios.""" 
    try: 
        logger.info("Validando qualidade dos dados de clientes.") 
        resumo_clientes = relatorio_qualidade_clientes("001_seed_clientes.csv") 
        logger.info("Resumo clientes: %s", resumo_clientes) 
        
        logger.info("Validando qualidade dos dados de transações.") 
        resumo_transacoes = relatorio_qualidade_transacoes("002_seed_transacoes.csv") 
        logger.info("Resumo transações: %s", resumo_transacoes) 
        return resumo_clientes, resumo_transacoes 
    except Exception as e: 
        logger.exception("Erro na validação dos dados: %s", e) 
        raise 
    
def transformar_dados(): 
    """Transforma datasets de clientes e transações.""" 
    try: 
        logger.info("Iniciando transformação dos dados de clientes.") 
        df_clientes, resumo_clientes = transformar_clientes(
            "001_seed_clientes.csv", 
            limites_idade=(0, 100), 
            limites_renda=(0, 20000), 
            cidades_validas=[ 
                "São Paulo", "Rio De Janeiro", "Belo Horizonte", "Porto Alegre", 
                "Curitiba", "Salvador", "Recife", "Brasília", 
                "Manaus", "Belém", "Goiânia" 
                ], 
            preencher_profissao="Não Informado" 
        ) 
        imprimir_resumo_transformacao("RESUMO TRANSFORMAÇÃO CLIENTES", resumo_clientes, salvar_resumo="resumo_clientes.txt") 
        
        logger.info("Iniciando transformação dos dados de transações.") 
        df_transacoes, resumo_transacoes = transformar_transacoes( 
            "002_seed_transacoes.csv", 
            formatos_data=("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"), 
            tipos_validos=("deposito", "saque", "transferencia"), 
            corrigir_sinal=True ) 
        imprimir_resumo_transformacao("RESUMO TRANSFORMAÇÃO TRANSAÇÕES", resumo_transacoes, salvar_resumo="resumo_transacoes.json") 
        logger.info("Transformações concluídas com sucesso.") 
        return df_clientes, df_transacoes 
    except Exception as e: 
        logger.exception("Erro na transformação dos dados: %s", e) 
        raise 
    
def carregar_dados(df_clientes, df_transacoes): 
    """Carrega dados transformados em CSV e SQL.""" 
    try: 
        logger.info("Carregando dados transformados para CSV.") 
        carregar_csv(df_clientes, "clientes_transformados.csv") 
        carregar_csv(df_transacoes, "transacoes_transformadas.csv") 
        logger.info("Carregando dados transformados para SQL.") 
        carregar_sql(df_clientes, "clientes") 
        carregar_sql(df_transacoes, "transacoes") 
        logger.info("Carregamento concluído com sucesso.") 
    except Exception as e: 
        logger.exception("Erro no carregamento dos dados: %s", e) 
        raise