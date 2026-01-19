# Projeto de ETL com Datasets Simulados

## 📌 Descrição
Este projeto demonstra, de forma prática, o processo de **ETL (Extract, Transform, Load)** aplicado a dados simulados.  
São criados dois datasets distintos:
- **Transações bancárias** (dados randômicos que emulam movimentações financeiras)  
- **Base de clientes** (informações fictícias de usuários)  

Ambos são gerados utilizando ferramentas do **Python**, garantindo diversidade e realismo nos dados iniciais.

---

## 🚀 Fluxo do Projeto

### 1. Extração e Carga Inicial
- Geração dos datasets em formato **CSV**.  
- Carregamento dos arquivos e análise preliminar.  
- Relatório inicial com **erros e inconsistências** (valores ausentes, duplicados, formatos incorretos).

### 2. Transformação e Limpeza
- Correção dos erros identificados.  
- Sinalização das alterações realizadas para manter transparência.  
- Geração de relatórios com resumo das correções.  
- Preparação dos datasets para uso **sem falhas**.

### 3. Carga Final
- Exportação dos dados tratados em **CSV** e **SQL**.  
- Disponibilização para usos posteriores, como análises exploratórias, dashboards ou integração em sistemas.

---

## 🛠️ Tecnologias Utilizadas
- **Python** (pandas, numpy, etc.)  
- **CSV** para armazenamento simples.  
- **SQL** para integração com bancos de dados relacionais.  

---

## 🎯 Objetivo
O projeto oferece uma visão prática e estruturada do ciclo completo de ETL, reforçando conceitos de **qualidade e integridade dos dados** e demonstrando como ferramentas de Python podem automatizar e documentar cada etapa do processo.

---

## 📂 Estrutura do Projeto
```bash
projeto_ETL_Santander/
├── ETL_Python_ProjetoDIO.ipynb  # Notebook principal com demonstração do processo ETL
├── config.yaml
├── data_cleaning.py
├── data_generation_clientes.py
├── data_generation_transacoes.py
├── data_load.py
├── data_validations.py
├── main.py
├── requirements.txt
├── utils.py
└── LICENSE


