# ANEXOS – Projeto AWS Abstergo Industries

## Documentação de Referência
- [Manual de boas práticas do Amazon RDS](https://docs.aws.amazon.com/pt_br/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html)  
- [Guia de configuração do Amazon EC2 Spot Instances](https://aws.amazon.com/pt/ec2/getting-started/)  
- Documentação das funções Lambda implementadas  

---

## Planilha de Estimativa de Custos - exemplo
| Serviço AWS              | Uso Principal                         | Custo Estimado (USD/mês) | Observações |
|---------------------------|---------------------------------------|--------------------------|-------------|
| Amazon RDS                | Banco de dados de estoque e pedidos   | 120                      | Instância db.t3.medium com backup automático |
| EC2 Spot Instances        | Análises de demanda e relatórios      | 80                       | Execução de workloads não críticos, economia de até 90% |
| AWS Lambda                | Automação de pedidos e notificações   | 40                       | Cobrança apenas por execução (eventos/pedidos) |
| Amazon CloudWatch (extra) | Monitoramento e alertas               | 20                       | Recomendado para acompanhar métricas e falhas |
| AWS S3 (extra)            | Armazenamento de documentos e históricos | 30                    | Uso de Intelligent-Tiering para reduzir custos |
| **Total Estimado**        |                                       | **290**                  | Valores aproximados para ambiente inicial |

---

## Fluxograma Detalhado dos Processos de Pedidos
```mermaid
flowchart TD
    A[Cliente realiza pedido] --> B[Pedido recebido pelo sistema AWS Lambda]
    B --> C[Dados registrados no Amazon RDS]
    C --> D[Verificação de estoque]
    D -->|Estoque disponível| E[Confirmação do pedido]
    D -->|Estoque indisponível| F[Notificação de falta enviada ao cliente]
    E --> G[Processamento de pagamento]
    G --> H[Atualização de status no RDS]
    H --> I[EC2 Spot gera relatórios de pedidos e demanda]
    I --> J[Gestores recebem relatórios para análise]
    H --> K[Notificação de pedido confirmado enviada ao cliente]
    K --> L[Preparação e envio do produto]
    L --> M[Entrega ao cliente]
