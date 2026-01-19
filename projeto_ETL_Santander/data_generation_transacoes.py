import csv, random, logging
from faker import Faker
from datetime import datetime, timedelta

def gerar_transacoes(arquivo_csv="002_seed_transacoes.csv", num_registros=500):
    """
    Gera um dataset de transações bancárias com possíveis inconsistências.

    - Saques devem ser negativos, mas podem ter erro forçado.
    - Depósitos e transferências devem ser positivos, mas podem ter erro forçado.
    - Datas podem vir em formatos diferentes.
    """
    colunas = ["transacao_id", "cliente_id", "tipo", "valor", "data", "agencia"]
    tipos = ["deposito", "saque", "transferencia"]
    formatos_data = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]

    with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(colunas)

        for i in range(1, num_registros + 1):
            transacao_id = i
            cliente_id = f"C{str(random.randint(1, 50)).zfill(3)}"
            tipo = random.choice(tipos)

            # Valor correto
            if tipo == "saque":
                valor = -random.randint(100, 2000)
            else:
                valor = random.randint(100, 5000)

            # Forçar erro com probabilidade de 10% a 20%
            if random.random() < random.uniform(0.1, 0.2):
                erros_valor = [
                    lambda v: abs(v),         # sinal invertido (saque positivo, depósito negativo)
                    lambda v: 0,              # valor zerado
                    lambda v: "mil reais",    # valor como texto
                    lambda v: 9999999         # valor absurdamente alto
                ]
                valor = random.choice(erros_valor)(valor)

            # Data aleatória nos últimos 180 dias, com formato inconsistente
            data_base = datetime.today() - timedelta(days=random.randint(0, 180))
            formato_escolhido = random.choice(formatos_data)
            data = data_base.strftime(formato_escolhido)

            # Agência
            agencia = f"AG{str(random.randint(1, 20)).zfill(2)}"

            writer.writerow([transacao_id, cliente_id, tipo, valor, data, agencia])

    logging.info(f"Arquivo {arquivo_csv} gerado com {num_registros} registros!")