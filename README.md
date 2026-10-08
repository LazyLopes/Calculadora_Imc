# 🏋️ Calculadora de IMC — Índice de Massa Corporal

Uma aplicação web para calcular o **Índice de Massa Corporal (IMC)**, desenvolvida com **Django REST Framework** no backend e **Vue.js 3 + Tailwind CSS** no frontend.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.0-06B6D4?logo=tailwindcss&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8.x-646CFF?logo=vite&logoColor=white)

<img width="1915" height="945" alt="image" src="https://github.com/user-attachments/assets/de2fadb4-0ff1-415f-a2f1-f906547709da" />

---

## 📑 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Executar](#-como-executar)
- [Endpoints da API](#-endpoints-da-api)
- [Classificações do IMC](#-classificações-do-imc)
- [Detalhamento dos Arquivos](#-detalhamento-dos-arquivos)

---

## 📖 Sobre o Projeto

O **IMC (Índice de Massa Corporal)** é uma medida utilizada para avaliar se uma pessoa está dentro do peso ideal com base na relação entre peso e altura. A fórmula é:

```
IMC = Peso (kg) ÷ Altura² (m)
```

Esta aplicação permite que o usuário:
- Insira seu peso (em kg) e altura (em metros)
- Receba o valor do IMC calculado
- Visualize a classificação segundo a OMS (Organização Mundial da Saúde)
- Consulte um histórico com os últimos 10 cálculos realizados

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| **Cálculo de IMC** | Insira peso e altura para obter o IMC |
| **Classificação automática** | O resultado é classificado de "Abaixo do peso" a "Obesidade Grau III" |
| **Barra gauge visual** | Um indicador visual mostra onde seu IMC se posiciona na escala |
| **Tabela de referência** | Todas as 6 classificações do IMC com seus respectivos intervalos |
| **Histórico de cálculos** | Os últimos 10 cálculos são salvos no banco de dados com data/hora |
| **Limpar histórico** | Opção para apagar todo o histórico de cálculos |
| **Validação de dados** | Peso (1-500 kg) e altura (0.30-3.00 m) são validados no frontend e backend |
| **Design responsivo** | Interface adaptada para desktop e dispositivos móveis |
| **Animações suaves** | Transições e micro-animações em todos os elementos interativos |
| **Dark mode premium** | Interface escura com gradientes, glassmorphism e efeitos luminosos |

---

## 🛠 Tecnologias Utilizadas

### Backend

| Tecnologia | Versão | Função |
|---|---|---|
| **Python** | 3.14 | Linguagem de programação principal do backend |
| **Django** | 6.1 | Framework web para Python. Gerencia o servidor, rotas, ORM (mapeamento objeto-relacional) e migrações do banco de dados |
| **Django REST Framework (DRF)** | 3.18 | Extensão do Django para criar APIs RESTful. Fornece serializers, validação de dados, e respostas em JSON |
| **django-cors-headers** | 4.9 | Middleware que permite requisições cross-origin (CORS), necessário para que o frontend (porta 5173) se comunique com o backend (porta 8000) |
| **SQLite** | — | Banco de dados leve embutido no Python. Armazena o histórico de cálculos sem necessidade de instalar um servidor de banco |

---

### Frontend

| Tecnologia | Versão | Função |
|---|---|---|
| **Vue.js** | 3.x | Framework JavaScript reativo para construir interfaces de usuário. Usa o sistema de componentes SFC (Single File Components) |
| **Vite** | 8.x | Ferramenta de build e servidor de desenvolvimento ultrarrápido. Substitui o webpack com HMR (Hot Module Replacement) instantâneo |
| **Tailwind CSS** | 4.0 | Framework CSS utilitário. Permite estilizar elementos diretamente no HTML usando classes como `bg-slate-900`, `rounded-2xl`, `hover:bg-indigo-500` |
| **Axios** | — | Cliente HTTP para JavaScript. Faz as requisições (GET, POST, DELETE) para a API do backend |
| **TypeScript** | — | Superset de JavaScript que adiciona tipagem estática, ajudando a prevenir erros em tempo de desenvolvimento |

---

### Fontes e Design

| Recurso | Descrição |
|---|---|
| **Inter (Google Fonts)** | Fonte sans-serif moderna, otimizada para interfaces digitais. Usada em pesos 300-800 |
| **Glassmorphism** | Efeito de vidro fosco usando `backdrop-blur` e backgrounds semi-transparentes |
| **Gradientes animados** | Backgrounds com `bg-gradient-to-br` e orbs luminosos pulsantes |
| **SVG Icons** | Ícones inline em SVG para balança (peso), setas (altura), relógio (histórico), etc. |

---

## 🏗 Arquitetura do Projeto

A aplicação segue uma arquitetura **cliente-servidor desacoplada**:

```
┌─────────────────────┐         HTTP/JSON         ┌──────────────────────┐
│                     │  ◄──────────────────────►  │                      │
│   Frontend (Vue.js) │    POST /api/imc/calcular/ │   Backend (Django)   │
│   localhost:5173     │    GET  /api/imc/historico/│   localhost:8000     │
│                     │    DELETE /api/imc/...      │                      │
│   - Interface UI    │                            │   - API REST          │
│   - Tailwind CSS    │                            │   - Lógica de cálculo │
│   - Axios (HTTP)    │                            │   - Banco de dados    │
│                     │                            │                      │
└─────────────────────┘                            └──────────────────────┘
                                                          │
                                                          ▼
                                                   ┌──────────────┐
                                                   │   SQLite     │
                                                   │  (db.sqlite3)│
                                                   └──────────────┘
```

### Fluxo de uma requisição:

1. O usuário preenche peso e altura no frontend (Vue.js)
2. Ao clicar em "Calcular IMC", o Axios envia um `POST` com JSON `{ peso, altura }` para `http://localhost:8000/api/imc/calcular/`
3. O Django recebe a requisição, valida os dados com o Serializer
4. O modelo `CalculoIMC` calcula o IMC e determina a classificação
5. O resultado é salvo no banco SQLite e retornado como JSON
6. O Vue.js recebe a resposta e atualiza a interface reativamente

---

## 📁 Estrutura de Pastas

```
Nova pasta/
│
├── backend/                    # Projeto Django (API REST)
│   ├── backend/                # Configurações do projeto Django
│   │   ├── __init__.py         # Marca o diretório como pacote Python
│   │   ├── settings.py         # Configurações gerais (apps, middleware, CORS, banco, idioma)
│   │   ├── urls.py             # Roteamento principal — inclui as URLs do app IMC
│   │   ├── wsgi.py             # Entry point para servidores WSGI (produção)
│   │   └── asgi.py             # Entry point para servidores ASGI (async)
│   │
│   ├── imc/                    # App Django dedicado ao cálculo de IMC
│   │   ├── __init__.py         # Marca como pacote Python
│   │   ├── apps.py             # Configuração do app (nome: 'imc')
│   │   ├── models.py           # Modelo CalculoIMC — define a tabela e a lógica de cálculo
│   │   ├── serializers.py      # Serializers DRF — validação e conversão JSON ↔ Python
│   │   ├── views.py            # Views da API — endpoints calcular, historico, limpar
│   │   ├── urls.py             # Rotas do app — mapeia URLs para views
│   │   ├── admin.py            # Registro de modelos no painel admin (vazio)
│   │   ├── tests.py            # Testes unitários (vazio, pronto para implementar)
│   │   └── migrations/         # Migrações do banco de dados
│   │       ├── __init__.py
│   │       └── 0001_initial.py # Migração que cria a tabela CalculoIMC
│   │
│   ├── manage.py               # CLI do Django — usado para rodar servidor, migrações, etc.
│   └── db.sqlite3              # Banco de dados SQLite (criado após o migrate)
│
├── frontend/                   # Projeto Vue.js (Interface do Usuário)
│   ├── src/
│   │   ├── assets/
│   │   │   └── main.css        # CSS global — importa Tailwind e define a fonte Inter
│   │   ├── components/
│   │   │   └── ImcCalculator.vue  # Componente principal da calculadora de IMC
│   │   ├── App.vue             # Componente raiz — layout com background animado
│   │   └── main.ts             # Entry point — monta o app Vue no DOM
│   │
│   ├── public/
│   │   └── favicon.ico         # Ícone do site
│   │
│   ├── index.html              # Template HTML — inclui fonte Inter e meta tags SEO
│   ├── vite.config.ts          # Configuração do Vite — plugins Vue e Tailwind
│   ├── package.json            # Dependências npm e scripts
│   ├── tsconfig.json           # Configuração base do TypeScript
│   ├── tsconfig.app.json       # Config TS para o código da aplicação
│   └── tsconfig.node.json      # Config TS para arquivos de configuração (vite.config)
│
└── venv/                       # Ambiente virtual Python (dependências isoladas)
```

---

## 📋 Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

| Ferramenta | Versão Mínima | Como verificar | Como instalar |
|---|---|---|---|
| **Python** | 3.10+ | `python --version` | [python.org/downloads](https://www.python.org/downloads/) |
| **Node.js** | 18+ | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | 9+ | `npm --version` | Vem junto com o Node.js |

---

## 🚀 Instalação e Configuração

### 1. Clone o projeto

### 2. Configure o Backend (Django)

```bash
# Criar ambiente virtual Python
python -m venv venv

# Ativar o ambiente virtual (Windows)
.\venv\Scripts\activate

# Instalar dependências Python
pip install django djangorestframework django-cors-headers

# Aplicar as migrações (criar tabelas no banco)
cd backend
python manage.py makemigrations imc
python manage.py migrate
```

### 3. Configure o Frontend (Vue.js)

```bash
# Voltar para a raiz do projeto
cd ..\frontend

# Instalar dependências Node.js
npm install

# Pacotes que serão instalados automaticamente:
# - vue (framework reativo)
# - vite (dev server + bundler)
# - @vitejs/plugin-vue (plugin Vite para Vue)
# - tailwindcss (framework CSS utilitário)
# - @tailwindcss/vite (integração Tailwind + Vite)
# - axios (cliente HTTP)
```

---

## ▶ Como Executar

Você precisa rodar **dois servidores simultaneamente** em terminais separados:

### Terminal 1 — Backend Django (porta 8000)

```bash
cd backend
..\venv\Scripts\activate     # Ativa o ambiente virtual
python manage.py runserver   # Inicia na porta 8000
```

### Terminal 2 — Frontend Vue.js (porta 5173)

```bash
cd frontend
npm run dev                  # Inicia na porta 5173
```

### Acessar a aplicação

Abra seu navegador e acesse: **http://localhost:5173**

---

## 🔌 Endpoints da API

A API REST está disponível em `http://localhost:8000/api/imc/`.

### `POST /api/imc/calcular/`

Calcula o IMC e salva no histórico.

**Request:**
```json
{
  "peso": 75.0,
  "altura": 1.75
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "peso": 75.0,
  "altura": 1.75,
  "imc": 24.49,
  "classificacao": "Peso normal",
  "criado_em": "2026-10-07T12:38:17.212430-03:00"
}
```

**Validações:**
| Campo | Mínimo | Máximo |
|---|---|---|
| `peso` | 1 kg | 500 kg |
| `altura` | 0.30 m | 3.00 m |

---

### `GET /api/imc/historico/`

Retorna os últimos 10 cálculos realizados, ordenados do mais recente para o mais antigo.

**Response (200 OK):**
```json
[
  {
    "id": 2,
    "peso": 100.0,
    "altura": 1.70,
    "imc": 34.6,
    "classificacao": "Obesidade Grau I",
    "criado_em": "2026-10-07T12:38:31.581264-03:00"
  },
  {
    "id": 1,
    "peso": 75.0,
    "altura": 1.75,
    "imc": 24.49,
    "classificacao": "Peso normal",
    "criado_em": "2026-10-07T12:38:17.212430-03:00"
  }
]
```

---

### `DELETE /api/imc/historico/limpar/`

Remove todos os cálculos do histórico.

**Response:** `204 No Content`

---

## 📊 Classificações do IMC

As classificações seguem os critérios da **Organização Mundial da Saúde (OMS)**:

| IMC | Classificação | Indicador Visual |
|---|---|---|
| < 18.5 | Abaixo do peso | 🔹 Azul |
| 18.5 — 24.9 | Peso normal | ✅ Verde |
| 25.0 — 29.9 | Sobrepeso | ⚠️ Amarelo |
| 30.0 — 34.9 | Obesidade Grau I | 🔶 Laranja |
| 35.0 — 39.9 | Obesidade Grau II | 🔴 Vermelho |
| ≥ 40.0 | Obesidade Grau III | 🚨 Rosa |

---

## 📄 Detalhamento dos Arquivos

### Backend

#### `backend/settings.py`
Arquivo central de configuração do Django. Contém:
- **INSTALLED_APPS**: Lista dos apps ativos — `rest_framework`, `corsheaders`, e `imc`
- **MIDDLEWARE**: Inclui `CorsMiddleware` para permitir requisições do frontend
- **CORS_ALLOWED_ORIGINS**: Permite apenas `localhost:5173` (dev server do Vue)
- **DATABASES**: Configurado para usar SQLite (arquivo `db.sqlite3`)
- **LANGUAGE_CODE**: Definido como `pt-br` para português brasileiro
- **TIME_ZONE**: Definido como `America/Sao_Paulo`

#### `imc/models.py`
Define o modelo `CalculoIMC` com os campos:
- `peso` (Float) — Peso em kg
- `altura` (Float) — Altura em metros
- `imc` (Float) — Valor calculado
- `classificacao` (CharField) — Texto da classificação
- `criado_em` (DateTimeField) — Data/hora automática

Contém o método estático `calcular_imc()` que recebe peso e altura, aplica a fórmula `peso / altura²` e retorna o valor arredondado + a classificação correspondente.

#### `imc/serializers.py`
Dois serializers:
- **CalculoIMCSerializer**: Converte o modelo para JSON (campos `id`, `peso`, `altura`, `imc`, `classificacao`, `criado_em`)
- **CalcularIMCSerializer**: Valida a entrada do usuário com limites de peso (1-500) e altura (0.3-3.0)

#### `imc/views.py`
Três endpoints:
- **`calcular_imc`** (POST): Valida dados → calcula IMC → salva no banco → retorna resultado
- **`historico_imc`** (GET): Retorna os 10 cálculos mais recentes
- **`limpar_historico`** (DELETE): Apaga todos os registros

#### `imc/urls.py`
Mapeia as rotas para as views:
- `/calcular/` → `calcular_imc`
- `/historico/` → `historico_imc`
- `/historico/limpar/` → `limpar_historico`

---

### Frontend

#### `index.html`
Template HTML com:
- Meta tag de descrição para SEO
- Fonte **Inter** do Google Fonts (pesos 300-800)
- Idioma definido como `pt-BR`
- Theme color `#0f172a` (slate-950)

#### `vite.config.ts`
Configuração do Vite com 3 plugins:
- `@vitejs/plugin-vue` — Suporte a arquivos `.vue`
- `vite-plugin-vue-devtools` — DevTools do Vue no navegador
- `@tailwindcss/vite` — Processa as classes Tailwind automaticamente

#### `src/main.ts`
Entry point que:
1. Importa o CSS global (com Tailwind)
2. Cria a instância do Vue
3. Monta o app no elemento `#app`

#### `src/assets/main.css`
CSS global que:
- Importa o Tailwind CSS via `@import "tailwindcss"`
- Define a fonte Inter como padrão via `@theme`
- Ativa `font-smoothing` para renderização suave do texto

#### `src/App.vue`
Componente raiz com:
- Background escuro com gradiente `from-slate-950 via-indigo-950 to-slate-950`
- 3 orbs luminosos animados (indigo, purple, cyan) com `animate-pulse`
- Grid pattern sutil de pontos
- Header com badge "Calculadora Online", título em gradiente, e subtítulo
- Footer com créditos

#### `src/components/ImcCalculator.vue`
Componente principal (≈400 linhas) com:

**Script (`<script setup>`):**
- `peso` e `altura` como `ref` reativos
- `classificacaoCores` — mapeamento de classificação → cores Tailwind + emoji
- `gaugePosition` — `computed` que converte IMC (10-50) para posição percentual (0-100%)
- `calcular()` — valida inputs, faz POST na API, atualiza resultado e histórico
- `carregarHistorico()` — GET na API para carregar últimos 10 cálculos
- `limparHistorico()` — DELETE na API para limpar tudo
- `formatarData()` — formata ISO date para `dd/mm/aaaa hh:mm`

**Template:**
- Card com efeito de glow (gradiente blur atrás do card)
- Inputs estilizados com ícones SVG e unidades (kg, m)
- Botão com gradiente indigo→purple e shadow
- Resultado: valor do IMC grande + emoji + classificação colorida
- Barra gauge com 6 segmentos coloridos e indicador circular
- 3 cards de detalhe (peso, altura, fórmula)
- Tabela de referência interativa (destaca a classificação atual)
- Seção de histórico expansível com cada cálculo listado

**Estilos (`<style scoped>`):**
- Animações de `fade` e `slide` para transições
- Remoção das setas nativas de `input[type="number"]`

---
