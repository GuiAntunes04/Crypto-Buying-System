# Sistema de Compra e Venda de Criptoativos

API para gerenciamento de operações de compra e venda de criptomoedas, com cálculo de lucro/prejuízo, consulta de preços em tempo real e camada de cache utilizando Redis. O sistema foi desenvolvido com foco em desempenho, escalabilidade e boas práticas de arquitetura para aplicações NoSQL.

---

## Descrição

O sistema permite que usuários registrem transações de criptoativos e acompanhem o desempenho consolidado da carteira. A aplicação fornece:

- Cálculo automático de posição média
- Apuração de lucro ou prejuízo não realizado
- Consulta de preços de mercado em tempo real
- Cache de dados com Redis
- Processamento assíncrono via Publish/Subscribe

A aplicação é exposta por meio de uma API REST construída com FastAPI e utiliza MongoDB Atlas como banco de dados principal.

---

## Funcionalidades

### 1. Gestão de Transações
- Cadastro de operações de compra e venda
- Listagem por usuário
- Atualização e exclusão de registros
- Filtros por ativo e período

### 2. Cálculo de Performance
- Preço médio por ativo
- Quantidade total em carteira
- Valor total investido
- Valor atual de mercado
- Lucro ou prejuízo estimado

### 3. Integração com API de Mercado
- Consulta de preço em tempo real via Binance US
- Tratamento de erro para restrições regionais
- Timeout configurado para evitar bloqueios

### 4. Redis (Cache e Mensageria)
- Cache de preços para reduzir chamadas externas
- Armazenamento temporário de dados de analytics
- Uso de variáveis em memória para acesso rápido
- Implementação de Publish/Subscribe para processamento assíncrono

### 5. Analytics
- Endpoint consolidado de resumo por usuário
- Processamento otimizado com aggregation pipeline do MongoDB
- Redução de carga através de cache Redis

---

## Arquitetura

Estrutura modular do projeto:

/routes/...
/services/...
/connections/...
/subscriber.py  
/main.py  

- Routes: definição dos endpoints
- Services: regras de negócio
- Connections: conexão com MongoDB e Redis
- Subscriber: consumidor de eventos Redis
- Main: inicialização da aplicação

---

## Tecnologias Utilizadas

- Python 3.11
- FastAPI
- MongoDB Atlas
- Redis
- Uvicorn
- Requests
- Python-dotenv

---

## Modelo de Dados (MongoDB)

Cada transação contém:

- usuario_id
- ticker
- tipo (compra ou venda)
- quantidade
- preco_unitario
- data
- localizacao (opcional)

A modelagem orientada a documento permite flexibilidade e expansão futura.

---

## Requisitos Atendidos

- Banco NoSQL em nuvem (MongoDB Atlas)
- API REST com FastAPI
- Uso de Aggregation Pipeline
- Indexação para otimização de busca
- Cache com Redis
- Implementação de Publish/Subscribe
- Deploy em ambiente cloud

---

## Como Executar Localmente

1. Clonar o repositório:
   git clone <url-do-repositorio>

2. Criar ambiente virtual:
   python -m venv venv

3. Ativar ambiente virtual:
   Windows:
   venv\Scripts\activate

   Linux/macOS:
   source venv/bin/activate

4. Instalar dependências:
   pip install -r requirements.txt

5. Configurar o arquivo .env:
   MONGO_URI=
   REDIS_HOST=
   REDIS_PORT=
   REDIS_USERNAME=
   REDIS_PASSWORD=

6. Executar a API:
   uvicorn main:app --reload

7. Executar o subscriber Redis (em outro terminal):
   python subscriber.py

---

## Considerações Finais

O sistema demonstra a aplicação prática de:

- Modelagem NoSQL
- Integração com APIs externas
- Cache distribuído
- Mensageria com Redis

O projeto foi estruturado visando separação de responsabilidades, clareza de código e facilidade de manutenção.
