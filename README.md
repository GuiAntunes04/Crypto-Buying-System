# Sistema de Compra de Criptomoedas

Sistema desenvolvido para permitir que usuários comprem criptomoedas através da integração com a API da Binance. Cada usuário pode conectar sua própria chave secreta da Binance para realizar transações.

## 📋 Descrição

Este sistema permite que usuários cadastrem suas chaves de API da Binance e realizem compras de criptomoedas de forma segura. O sistema utiliza banco de dados NoSQL (MongoDB) para armazenar os dados dos usuários, chaves de API e histórico de transações.

## 🎯 Funcionalidades Principais

- **CRUD de Usuários**: Cadastro, consulta, atualização e remoção de usuários
- **CRUD de Chaves Binance**: Gerenciamento seguro das chaves de API da Binance de cada usuário
- **CRUD de Transações**: Registro e consulta de todas as transações de compra realizadas
- **Integração com Binance API**: Consulta de cotações em tempo real e execução de ordens de compra
- **Segurança**: Criptografia das chaves secretas armazenadas no banco de dados

## 🛠 Tecnologias

- **Backend**: Node.js com Express
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
- **Transações**: Histórico de compras realizadas com detalhes de cada operação

## ⚠️ Importante

- Cada usuário deve fornecer suas próprias chaves de API da Binance
- As chaves secretas são armazenadas de forma criptografada
- Recomenda-se o uso da Binance Testnet para testes
- Criptomoedas são investimentos de alto risco

