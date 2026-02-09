# Sistema de Compra e Venda de Criptoativos

Sistema desenvolvido para permitir que usuários gerenciem suas carteiras de criptomoedas, acompanhem transações em tempo real e visualizem análises de desempenho através de uma interface intuitiva.

## 📋 Descrição

Este sistema centraliza a gestão de ativos digitais, permitindo que o usuário registre suas operações de compra e venda e obtenha insights automáticos sobre seu patrimônio. Através da integração com o MongoDB, o sistema oferece uma busca rápida e análises detalhadas da distribuição geográfica e financeira dos investimentos.

## 🎯 Funcionalidades Principais

- **Gestão de Portfólio**: O usuário pode cadastrar, visualizar, editar e excluir suas transações de compra e venda de criptomoedas.
- **Importação de Histórico**: Possibilidade de carregar grandes volumes de transações passadas de uma só vez para atualizar a carteira rapidamente.
- **Painel de Analytics**: Visualização de indicadores de desempenho, como o valor total investido, lucro/prejuízo estimado e volume por ativo.
- **Filtros Inteligentes**: Busca avançada de transações por nome do ativo, períodos de tempo ou localização geográfica da operação.
- **Monitoramento em Tempo Real**: Consulta de preços atuais de mercado via integração com a API da Binance.

## 🛠 Tecnologias

- **Linguagem Principal**: Python
- **Framework API**: FastAPI
- **Banco de Dados**: MongoDB Atlas (NoSQL)
- **Visualização**: Streamlit
- **Integração**: API da Binance

## 📊 Estrutura de Dados (Modelo de Documento)

O sistema organiza as informações em documentos NoSQL, permitindo flexibilidade e rapidez na consulta de:
- **Dados do Ativo**: Ticker, nome e valor de mercado.
- **Detalhes da Ordem**: Quantidade negociada e preço de execução.
- **Dados Geográficos**: Localização de registro da transação para auditoria e segurança.

## 🔧 Como Rodar o Projeto

1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Configure suas credenciais no arquivo `.env`.
5. Inicie a API e o Dashboard conforme as instruções na pasta `docs`.

## 📝 Observações Técnicas (Requisitos Atendidos)

- Persistência em nuvem via **MongoDB Atlas**.
- Endpoints de alta performance com **FastAPI**.
- Uso de **Aggregation Pipelines** para processamento de dados.
- Indexação avançada (**Text e Geosphere2d**) para otimização de buscas.
