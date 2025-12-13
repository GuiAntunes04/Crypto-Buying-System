# Sistema de Compra de Criptomoedas

Sistema desenvolvido para permitir que usuários comprem criptomoedas através da integração com a API da Binance. Cada usuário pode conectar sua própria chave secreta da Binance para realizar transações.

## 📋 Descrição

Este sistema permite que usuários cadastrem suas chaves de API da Binance e realizem compras de criptomoedas de forma segura. Além disso, os usuários podem programar ordens de compra/venda que serão executadas automaticamente quando o preço da criptomoeda atingir um valor determinado. O sistema utiliza banco de dados NoSQL (MongoDB) para armazenar os dados dos usuários, chaves de API, ordens programadas e histórico de transações.

## 🎯 Funcionalidades Principais

- **Compra de Criptomoedas**: Realização de compras e vendas de criptomoedas através da API da Binance
- **Ordens Programadas**: Programação de ordens de compra/venda que são executadas automaticamente quando o preço atinge um valor determinado (stop orders)
- **Monitoramento de Preços**: Acompanhamento em tempo real das cotações para execução automática das ordens programadas
- **Segurança**: Criptografia das chaves secretas armazenadas no banco de dados

## 🛠 Tecnologias

- **Backend**: Python
- **Banco de Dados**: MongoDB (NoSQL)
- **Integração**: API da Binance
- **Autenticação**: JWT
- **Criptografia**: Para proteção das chaves secretas

## 🔒 Segurança

- Chaves secretas são criptografadas antes de serem armazenadas
- Autenticação via JWT para acesso às funcionalidades
- Cada usuário gerencia apenas suas próprias chaves e transações

## 📝 Estrutura de Dados

O sistema armazena:
- **Usuários**: Informações de cadastro e autenticação
- **Chaves Binance**: API Key e Secret Key (criptografadas) vinculadas a cada usuário
- **Ordens Programadas**: Ordens de compra/venda com preço-alvo que serão executadas automaticamente
- **Transações**: Histórico de compras e vendas realizadas com detalhes de cada operação

## ⚠️ Importante

- Cada usuário deve fornecer suas próprias chaves de API da Binance
- As chaves secretas são armazenadas de forma criptografada
- Recomenda-se o uso da Binance Testnet para testes
- Criptomoedas são investimentos de alto risco

