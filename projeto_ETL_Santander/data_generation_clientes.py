import random, csv, logging
import pandas as pd
from faker import Faker
from typing import List

def make_faker(locale: str = "pt_BR") -> Faker:
    return Faker(locale)

def gerar_nome(faker: Faker) -> str:
    """ Gera nome com possíveis erros forçados."""
    nome = faker.name()
    erros = [lambda n: ""]      # Nome vazio - erro forçado
    if random.random() < random.uniform(0.01, 0.1):
        return random.choice(erros)(nome)
    return nome

def gerar_email(faker: Faker) -> str:
    """Gera e-mail com possíveis erros simulados"""
    email = faker.email()
    erros = [
        lambda e: e.replace("@", ""),       # faltar @
        lambda e: e.replace(".", ""),       # faltar ponto
        lambda e: e.upper(),                # caixa alta
        lambda e: e.replace("com", "con"),  # erro de digitação
        lambda e: ""                        # email vazio - erro forçado
    ]
    if random.random() < random.uniform(0.1, 0.25):
        return random.choice(erros)(email)
    return email

def gerar_idade() -> int | str | None:
    """Gera idade com possíveis erros simulados."""
    idade = random.randint(18, 70)
    erros = [
        lambda i: -i,       # valor negativo
        lambda i: i + 100,  # valor muito alto
        lambda i: str(i),   # como string
        lambda i: "trinta", # gera texto
        lambda i: None      # valor nulo - erro forçado
    ]
    if random.random() < random.uniform(0.1, 0.25):
        return random.choice(erros)(idade)
    return idade

def gerar_cidade(cidades: List[str]) -> str:
    """GEra cidade com possíveis erros simulados."""
    cidade = random.choice(cidades)
    erros = [
        lambda c: c.lower(),            # caixa baixa
        lambda c: c[:5],                # truncada
        lambda c: c.replace("o", "0"),  # erro digitação
        lambda c: ""                    # cidade vazia - erro forçado
    ]
    if random.random() < random.uniform(0.1, 0.25):
        return random.choice(erros)(cidade)
    return cidade

def gerar_profissao(faker: Faker, lista_profissoes: List[str]) -> str | None:
    """Gera profissão com possíveis erros simulados."""
    profissao = random.choice(lista_profissoes)
    erros = [
        lambda p: p.lower(),    # tudo em minúsculo
        lambda p: p.upper(),    # tudo em maiúsculo
        lambda p: None          # profissão vazia - erro forçado
    ]
    if random.random() < random.uniform(0.05, 0.15):
        return random.choice(erros)(profissao)
    return profissao

def gerar_renda() -> float | str | None:
    """Gera renda com possíveis erros simulados."""
    renda = round(random.uniform(1500, 15000), 2)
    erros = [
        lambda r: -r,       # valor negativo
        lambda r: 9999999,  # valor muito alto
        lambda r: "dez mil",# texto
        lambda r: f"{r:,}", # separador errado
        lambda r: None      # valor vazio - erro forçado
    ]
    if random.random() < random.uniform(0.1, 0.25):
        return random.choice(erros)(renda)
    return renda

def gerar_clientes(arquivo_csv: str, quantidade_profissoes: int, num_registros: int, faker: Faker):
    """Gera dataset de clientes com inconsistências simuladas."""
    colunas = ["cliente_id", "nome", "email", "idade", "cidade", "profissao", "renda_mensal"]
    cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte",
                "Porto Alegre", "Curitiba", "Salvador",
                "Recife", "Brasília", "Manaus",
                "Belém", "Goiânia"]

    lista_profissoes = [faker.job() for _ in range(quantidade_profissoes)]

    with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(colunas)

        for i in range(1, num_registros + 1):
            writer.writerow([
                i,
                gerar_nome(),
                gerar_email(),
                gerar_idade(),
                gerar_cidade(cidades),
                gerar_profissao(lista_profissoes),
                gerar_renda()
            ])
    logging.info(f"Arquivo {arquivo_csv} gerado com {num_registros} registros!")
