# 📚 Extrator de Markdown em Lotes para PDFs

> **Pipeline de alta precisão para converter livros, teses, artigos e relatórios em Markdown estruturado via IA, otimizado para execução em CPU tanto no Windows 11 quanto no Linux.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Docling](https://img.shields.io/badge/Engine-Docling-orange.svg)](https://github.com/docling-project/docling)
[![PyMuPDF](https://img.shields.io/badge/PDF_Index-PyMuPDF-green.svg)](https://github.com/pymupdf/PyMuPDF)
[![OS](https://img.shields.io/badge/OS-Windows%2011%20%7C%20Linux-lightgrey.svg)]()
[![Hardware](https://img.shields.io/badge/Hardware-CPU%20Optimized-blueviolet.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📑 Sumário

- [Visão Geral](#-visão-geral)
- [Por que o Processamento em Lotes?](#-por-que-o-processamento-em-lotes)
- [Pré-requisitos](#-pré-requisitos)
- [🚀 Instalação Passo a Passo](#-instalação-passo-a-passo)
  - [Opção A: Linux (Ubuntu, Debian, Fedora, Arch)](#opcao-a-linux-ubuntudebianfedoraarch)
  - [Opção B: Windows 11 (PowerShell / CMD)](#opcao-b-windows-11-powershell--cmd)
- [💻 Como Executar](#-como-executar)
  - [Uso Básico](#uso-básico)
  - [Exemplos Práticos](#exemplos-práticos)
  - [Opções e Parâmetros da CLI](#opções-e-parâmetros-da-cli)
- [⚙️ Otimização de Performance em CPU](#️-otimização-de-performance-em-cpu)
  - [Tabela de Dimensionamento de Lotes por RAM](#tabela-de-dimensionamento-de-lotes-por-ram)
  - [Controle de Threads](#controle-de-threads)
- [📁 Estrutura do Repositório](#-estrutura-do-repositório)
- [🛠️ Solução de Problemas Comuns (Troubleshooting)](#️-solução-de-problemas-comuns-troubleshooting)
- [Créditos e Referências](#créditos-e-referências)

---

## 💡 Visão Geral

Este projeto foi desenvolvido para resolver um problema comum ao processar documentos extensos com modelos de Inteligência Artificial: **a perda de dados ou estouro de memória ao tentar processar arquivos gigantes de uma só vez em processadores convencionais (CPU)**.

Utilizando o motor [Docling](https://github.com/docling-project/docling) (desenvolvido pela equipe do IBM Research) em conjunto com a velocidade de indexação do [PyMuPDF](https://github.com/pymupdf/PyMuPDF), o extrator divide o PDF dinamicamente em blocos de páginas configuráveis e gera arquivos Markdown ricos, preservando:

- 📖 Títulos, subtítulos e hierarquia estrutural de leitura
- 📊 Tabelas complexas convertidas com precisão
- 🧮 Equações e fórmulas matemáticas (LaTeX)
- 📝 Blocos de código e citações
- 🖼️ Descrições e referências de imagens

---

## ⚡ Por que o Processamento em Lotes?

Converter um livro ou manual de 300 a 1000 páginas em CPU de uma só vez exige gigabytes de memória RAM para carregar o grafo de documento completo, gerando lentidão extrema ou o infame erro `OutOfMemoryError`.

Com o processamento em fatias (`page_range`):

1. **Baixo Consumo de RAM:** A cada lote (ex: 50 ou 100 páginas), a memória é liberada após a gravação do arquivo `.md`.
2. **Resiliência a Falhas:** Se uma página isolada estiver corrompida, o script captura o erro daquele lote e continua os próximos sem perder o trabalho anterior.
3. **Modularidade:** Você já pode começar a ler ou injetar em sua base RAG/Obsidian os primeiros capítulos enquanto os restantes ainda estão sendo gerados.

---

## 📋 Pré-requisitos

- **Python 3.10, 3.11 ou 3.12** instalado na sua máquina (*Docling descontinuou suporte ao Python 3.9 a partir da v2.70*).
- **RAM Recomendada:** Mínimo de 8 GB (16 GB recomendado para lotes maiores).
- **Conexão com a Internet** na primeira execução para download automático dos modelos do Hugging Face.

---

## 🚀 Instalação Passo a Passo

O PyTorch convencional baixa dependências pesadas de aceleração NVIDIA CUDA (~2.8 GB). Para rodar com eficiência em **CPU**, criamos uma instalação limpa que baixa apenas as rodas de CPU (~200 MB), economizando gigabytes de armazenamento e tempo de download.

### Opção A: Linux (Ubuntu/Debian/Fedora/Arch)

#### 1. Instale o pacote de ambiente virtual do Python (se ainda não tiver)

No Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip
```

#### 2. Clone ou acerte o diretório do repositório

```bash
cd /caminho/para/extrator_markdown
```

#### 3. Crie e ative a venv

```bash
python3 -m venv venv
source venv/bin/activate
```

*(Você verá `(venv)` no início da linha do terminal)*.

#### 4. Atualize o pip

```bash
pip install --upgrade pip
```

#### 5. Instale as dependências otimizadas para CPU

Utilize o arquivo `requirements-cpu.txt` que já inclui o repositório oficial CPU do PyTorch:

```bash
pip install -r requirements-cpu.txt
```

---

### Opção B: Windows 11 (PowerShell / CMD)

#### 1. Abra o Terminal ou PowerShell

Certifique-se de que o Python está instalado e marcado a opção **"Add Python to PATH"**.

#### 2. Navegue até a pasta do projeto

```powershell
cd C:\caminho\para\extrator_markdown
```

#### 3. Crie a venv

```powershell
python -m venv venv
```

#### 4. Ative a venv

No **PowerShell**:

```powershell
.\venv\Scripts\Activate.ps1
```

> ⚠️ **Aviso de Política de Execução do PowerShell:**
> Se aparecer o erro `A execução de scripts foi desabilitada neste sistema`, libere temporariamente executando no PowerShell:
>
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> ```
>
> E em seguida execute novamente `.\venv\Scripts\Activate.ps1`.

No **Prompt de Comando (CMD)** clássico:

```cmd
venv\Scripts\activate.bat
```

#### 5. Atualize o pip

```powershell
python -m pip install --upgrade pip
```

#### 6. Instale as dependências otimizadas para CPU

```powershell
pip install -r requirements-cpu.txt
```

---

## 💻 Como Executar

### Uso Básico

Para iniciar a extração, basta informar o caminho ou nome do arquivo PDF pelo terminal:

```bash
# Com a venv ativada:
python extrator_lotes.py meu_documento.pdf
```

> ⚠️ **Validação Imediata:**  
> O script exige o caminho do arquivo PDF. Se o arquivo não for informado ou se **não for encontrado no diretório**, um erro explicativo é retornado imediatamente no terminal, interrompendo a execução de forma rápida e segura.

---

### Exemplos Práticos

#### 1. Processando um arquivo no diretório atual

```bash
python extrator_lotes.py artigo.pdf
```

#### 2. Processando com caminho relativo ou subpasta

```bash
python extrator_lotes.py documentos/livro_completo.pdf
```

#### 3. Ajustando o tamanho do lote para máquinas com menos memória RAM (ex: 50 páginas)

```bash
python extrator_lotes.py meu_artigo.pdf --lote 50
```

#### 4. Forçando execução estrita em CPU e controlando número de núcleos/threads

```bash
python extrator_lotes.py livro_denso.pdf --cpu --threads 4
```

---

### Opções e Parâmetros da CLI

| Argumento / Flag | Descrição | Obrigatório? | Padrão |
| :--- | :--- | :--- | :--- |
| `pdf` | Caminho do arquivo PDF a ser processado | **Sim** | — |
| `-l`, `--lote` | Quantidade de páginas processadas por lote/arquivo `.md` | Não | `100` |
| `--cpu` | Força estritamente a execução em CPU | Não | `False` (Auto) |
| `-t`, `--threads` | Define o número de threads paralelas utilizadas pela CPU | Não | `None` (Auto) |

Para ver o menu de ajuda completo a qualquer momento:

```bash
python extrator_lotes.py --help
```

---

## ⚙️ Otimização de Performance em CPU

Processar documentos ricos via IA em CPU envolve análise de layout visual e reconhecimento óptico de caracteres (OCR). As seguintes práticas garantem o melhor equilíbrio entre velocidade e estabilidade:

### Tabela de Dimensionamento de Lotes por RAM

| Memória RAM Disponível | Tamanho de Lote Recomendado (`--lote`) | Cenário de Uso |
| :--- | :--- | :--- |
| **8 GB** | `25` a `50` | Livros com muitas imagens e tabelas |
| **16 GB** | `50` a `100` | Equilíbrio ideal entre tempo e organização |
| **32 GB ou mais** | `100` a `200` | Artigos volumosos ou compêndios |

### Controle de Threads

Se você estiver executando o script em segundo plano enquanto utiliza o computador para outras tarefas, restrinja o consumo de núcleos:

```bash
# Limita o Docling a utilizar apenas 4 threads
python extrator_lotes.py meu_livro.pdf --cpu --threads 4
```

Também é possível definir variáveis de ambiente no sistema:

- **Linux:** `export OMP_NUM_THREADS=4`
- **Windows (PowerShell):** `$env:OMP_NUM_THREADS="4"`

---

## 📁 Estrutura do Repositório

```text
extrator_markdown/
├── entrada/                     # Coloque seus PDFs aqui (ignorado pelo git)
│   └── .gitkeep
├── saida/                       # Onde os arquivos .md serão gerados (ignorado pelo git)
│   └── .gitkeep
├── extrator_lotes.py            # Script principal com CLI e resolução automática
├── requirements.txt             # Dependências padrão
├── requirements-cpu.txt         # Dependências otimizadas para CPU (PyTorch leve)
├── .gitignore                   # Exclusões de ambiente, cache e PDFs pesados
└── README.md                    # Documentação completa do projeto
```

---

## 🛠️ Solução de Problemas Comuns (Troubleshooting)

### 1. `RuntimeError: operator torchvision::nms does not exist`

- **Causa:** Ocorre quando foram misturadas versões do `torch` e `torchvision` com e sem suporte a CUDA.
- **Solução:** Remova as versões antigas e reinstale do repositório CPU:

  ```bash
  pip uninstall torch torchvision torchaudio -y
  pip install -r requirements-cpu.txt
  ```

### 2. No Windows: `File ... Activate.ps1 cannot be loaded because running scripts is disabled`

- **Causa:** Política de restrição de execução padrão do PowerShell no Windows.
- **Solução:** Execute uma vez no terminal:

  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  .\venv\Scripts\Activate.ps1
  ```

### 3. No Linux: `No module named venv`

- **Causa:** Distribuições Debian/Ubuntu separam o módulo `venv` do pacote Python principal.
- **Solução:**

  ```bash
  sudo apt install -y python3-venv
  ```

### 4. O script parece ter travado no primeiro lote

- **Causa:** Na primeiríssima execução, o Docling faz o download dos pesos dos modelos de visão e layout (cerca de 1 a 2 GB no diretório de cache do usuário).
- **Solução:** Aguarde alguns minutos dependendo da sua velocidade de internet. As execuções seguintes iniciarão instantaneamente.

### 5. Erro de caminhos longos no Windows (`PathTooLongException` ou `FileNotFoundError`)

- **Causa:** O Windows possui um limite histórico de 260 caracteres para nomes de pastas e arquivos.
- **Solução:** Mantenha o repositório em um caminho curto (ex: `C:\projetos\extrator_markdown`) ou ative a opção "Long Paths Enabled" no Registro do Windows.

---

## 🤝 Créditos e Referências

- **[Docling](https://github.com/docling-project/docling)**: Biblioteca de entendimento e conversão documental por IA mantida pelo time de IA do IBM Research Zurich.
- **[PyMuPDF (fitz)](https://github.com/pymupdf/PyMuPDF)**: Motor ultrarrápido para renderização, inspeção e manipulação de arquivos PDF.

---

Distribuído sob a licença MIT. Sinta-se livre para usar, contribuir e integrar em suas aplicações de RAG e Processamento de Linguagem Natural!
