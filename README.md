# 📨 NP2 - Middleware Orientado a Mensagens (MOM)

Repositório da NP2 da disciplina **Programação Paralela e Distribuída (PPD)**.  
Este projeto implementa um **Middleware Orientado a Mensagens (MOM)** utilizando **ActiveMQ**, **STOMP** e **Python** com interface gráfica.

---

## 🧩 Objetivo

Desenvolver um sistema de **gerenciamento e utilização de mensagens** baseado em filas e tópicos, simulando um middleware para comunicação assíncrona entre aplicações distribuídas.

---

## 🖼️ Visão Geral

O sistema é composto por:

- **Gerenciador MOM (`momManagerGui.py`)**: Interface gráfica para criar e remover filas, tópicos e usuários.
- **Aplicativo do Usuário (`userAppGui.py`)**: Interface gráfica para envio/recebimento de mensagens entre usuários e tópicos.
- **Módulo MOM (`momManager.py`)**: Classe responsável por gerenciar filas, tópicos e usuários no broker.
- **Broker**: ActiveMQ (Java), acessado via protocolo STOMP.

---

## 🚀 Como Executar

### 1. Suba o ActiveMQ localmente

Baixe e execute o [ActiveMQ](https://activemq.apache.org/components/classic/download/):

```bash
./bin/activemq start
```

Acesse o painel web: [http://localhost:8161/admin](http://localhost:8161/admin)  
Usuário/senha padrão: `admin` / `admin`

---

### 2. Instale as dependências Python

```bash
pip install stomp.py
```

---

### 3. Execute o Aplicativo de Usuário

```bash
python userAppGui.py
```

Funcionalidades disponíveis:
- Envio de mensagens entre usuários (1:1, offline)
- Envio de mensagens para tópicos (broadcast)
- Assinatura de tópicos
- Recepção assíncrona de mensagens (via STOMP listener)

---

## 📂 Estrutura do Projeto

```
NP2-PPD-Message-Oriented-Middleware/
│
├── momManager.py         # Classe gerenciadora MOM
├── momManagerGui.py      # Interface gráfica do gerenciador
├── userAppGui.py         # Aplicação gráfica do usuário
└── README.md             # Documentação do projeto
```

---

## 🎓 Desenvolvido para

Disciplina **Programação Paralela e Distribuída (PPD)**  
Curso de **Engenharia de Computação** — [IFCE](https://ifce.edu.br)

---

## 📌 Requisitos

- Python 3.8+
- ActiveMQ (clássico) executando em `localhost:61613`
- Biblioteca `stomp.py`

---

## 📄 Licença

Distribuído apenas para fins acadêmicos. Sem garantia de estabilidade ou suporte.

---