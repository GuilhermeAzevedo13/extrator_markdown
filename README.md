# 📚 Extrator de Markdown em Lotes para PDFs

> **Transforme livros, apostilas, artigos científicos e relatórios em PDF em arquivos Markdown (`.md`) formatados e estruturados com Inteligência Artificial, com aceleração por GPU (NVIDIA CUDA) ou CPU no Windows 11 e Linux.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Motor IA](https://img.shields.io/badge/Motor_IA-Docling-orange.svg)](https://github.com/docling-project/docling)
[![Leitor PDF](https://img.shields.io/badge/Leitor_PDF-PyMuPDF-green.svg)](https://github.com/pymupdf/PyMuPDF)
[![Sistemas](https://img.shields.io/badge/Sistemas-Windows%2011%20%7C%20Linux-lightgrey.svg)]()
[![Hardware](https://img.shields.io/badge/Hardware-GPU_(CUDA)_%7C_CPU-blueviolet.svg)]()
[![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-yellow.svg)](LICENSE)

---

## 🎯 Resumo em 3 Passos (Como Funciona)

Para quem quer rapidez, o fluxo deste projeto se resume a:

1. **Colocar o PDF:** Você arrasta o arquivo PDF para dentro da pasta `entrada/`.
2. **Executar o comando:** Você abre o terminal e digita `python extrator_lotes.py`.
3. **Pegar o resultado:** O programa cria uma pasta exclusiva dentro de `saida/` contendo o livro/artigo fatiado em arquivos `.md` perfeitamente legíveis.

---

## 📑 Sumário

- [O que este projeto faz?](#-o-que-este-projeto-faz)
- [Por que o processamento em lotes (fatias)?](#-por-que-o-processamento-em-lotes-fatias)
- [Estrutura de Pastas do Projeto](#-estrutura-de-pastas-do-projeto)
- [🪟 Guia Passo a Passo: Windows 11](#-guia-passo-a-passo-windows-11)
- [🐧 Guia Passo a Passo: Linux (Ubuntu, Debian, Fedora, Arch)](#-guia-passo-a-passo-linux-ubuntu-debian-fedora-arch)
- [💻 Todas as Formas de Usar](#-todas-as-formas-de-usar)
  - [1. Processar automaticamente o PDF que está na entrada](#1-o-jeito-mais-fácil-1-único-pdf-na-pasta-entrada)
  - [2. Processar VÁRIOS PDFs em fila de uma só vez (`--todos`)](#2-processar-vários-pdfs-em-fila-de-uma-vez-só---todos)
  - [3. Processar um PDF específico pelo nome](#3-processar-um-arquivo-específico)
  - [4. Economizar memória RAM em livros muito grandes (`--lote 50`)](#4-economizar-memória-ram-em-computadores-mais-modestos---lote-50)
  - [5. Limitar o uso do processador (`--threads 4`)](#5-controlar-o-uso-do-processador---threads)
- [Tabela de Parâmetros e Opções](#-tabela-de-parâmetros-e-opções)
- [O que é um arquivo Markdown (.md) e como usar?](#-o-que-é-um-arquivo-markdown-md-e-como-usar)
- [🛠️ Dúvidas e Problemas Frequentes (FAQ)](#️-dúvidas-e-problemas-frequentes-faq)

---

## 💡 O que este projeto faz?

Quando tentamos copiar o texto de um PDF de livro ou artigo, quase sempre o resultado vem bagunçado: quebras de linha estranhas, tabelas desconfiguradas e fórmulas ilegíveis.

Este extrator utiliza o **[Docling](https://github.com/docling-project/docling)** (uma tecnologia avançada de IA desenvolvida pela IBM Research) para analisar visualmente o PDF e transformá-lo em texto puro formatado em **Markdown (`.md`)**.

### O que ele preserva com precisão:
- 📖 **Hierarquia de Títulos:** Capítulos, seções e subtítulos (`# Título`, `## Subtítulo`).
- 📊 **Tabelas Complexas:** Convertidas em tabelas Markdown legíveis.
- 🧮 **Equações Matemáticas:** Transformadas em código LaTeX (`$E = mc^2$`).
- 💻 **Blocos de Código:** Formatados com destaque de sintaxe.
- 💬 **Citações e Notas de Rodapé:** Preservadas no fluxo de leitura.

---

## ⚡ Por que o processamento em lotes (fatias)?

Processar um livro inteiro de 300, 500 ou 1000 páginas de uma vez só na memória do computador pode sobrecarregar a memória RAM, travando o sistema com o erro `OutOfMemoryError`.

Para resolver isso, o script divide o documento em **fatias de páginas configuráveis** (por padrão, 100 páginas por lote):

1. **Memória sempre leve:** A cada lote finalizado (ex: páginas 1 a 100), o arquivo `.md` é gravado no disco e a memória RAM é liberada para o próximo lote.
2. **Segurança total:** Se faltar energia ou o computador desligar, você **não perde** o que já foi convertido! Os lotes anteriores já estão salvos e você pode continuar de onde parou.
3. **Uso imediato:** Você já pode começar a ler ou usar os primeiros capítulos enquanto o restante ainda está sendo processado.

---

## 📁 Estrutura de Pastas do Projeto

O repositório é organizado de forma simples e intuitiva:

```text
extrator_markdown/
│
├── entrada/                  ⬅️ COLOQUE SEUS PDFs AQUI!
│   └── .gitkeep
│
├── saida/                    ⬅️ SEUS MARKDOWNS GERADOS VÃO APARECER AQUI!
│   └── .gitkeep
│
├── extrator_lotes.py         ⬅️ O script que faz a mágica acontecer
├── requirements.txt          ⬅️ Lista de programas que o Python precisa instalar
├── .gitignore                ⬅️ Garante que seus PDFs e Markdowns não subam para o GitHub
└── README.md                 ⬅️ Este manual de instruções
```

---

## 🪟 Guia Passo a Passo: Windows 11

Siga este passo a passo caso você esteja usando o Windows 11:

### Passo 1: Verificar se você tem o Python instalado
1. Pressione a tecla `Windows` no teclado, digite `cmd` ou `Terminal` e aperte `Enter`.
2. Digite:
   ```cmd
   python --version
   ```
3. Se aparecer `Python 3.10.x`, `3.11.x` ou `3.12.x`, está tudo certo!
4. *(Se não tiver instalado, baixe no site oficial [python.org](https://www.python.org/downloads/) e **MUITO IMPORTANTE: marque a caixinha "Add Python to PATH"** durante a instalação).*

---

### Passo 2: Abrir o terminal dentro da pasta do projeto
O jeito mais fácil no Windows 11:
1. Abra o **Explorador de Arquivos** e entre na pasta `extrator_markdown`.
2. Clique com o **botão direito** em um espaço vazio da pasta e selecione **"Abrir no Terminal"** (ou aperte `Shift` + botão direito $\rightarrow$ "Abrir janela do PowerShell aqui").

---

### Passo 3: Criar o Ambiente Virtual (venv)
O ambiente virtual é uma "caixa isolada" para instalar as ferramentas sem bagunçar o restante do seu Windows. Digite no terminal:

```powershell
python -m venv venv
```
*(Aguarde alguns segundos até o terminal liberar a linha novamente).*

---

### Passo 4: Ativar o Ambiente Virtual
No terminal PowerShell, digite:

```powershell
.\venv\Scripts\Activate.ps1
```

> ⚠️ **Apareceu uma mensagem em vermelho dizendo que a execução de scripts foi desabilitada?**  
> Isso é uma proteção padrão do Windows. Para liberar, basta digitar o comando abaixo e apertar `Enter`:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> ```
> Em seguida, execute novamente:
> ```powershell
> .\venv\Scripts\Activate.ps1
> ```

**Como saber que deu certo?**  
Você verá `(venv)` aparecer no início da linha do terminal, assim:
`((venv) PS C:\...\extrator_markdown>`

---

### Passo 5: Instalar as ferramentas necessárias
Com a `(venv)` ativada, digite:

```powershell
pip install -r requirements.txt
```
*(O Python baixará e configurará o Docling, o PyMuPDF e o PyTorch automaticamente. Isso pode levar alguns minutos dependendo da sua internet).*

**Pronto! A instalação no Windows 11 está 100% concluída.**

---

## 🐧 Guia Passo a Passo: Linux (Ubuntu, Debian, Fedora, Arch)

Siga este passo a passo caso você esteja usando Linux:

### Passo 1: Abrir o Terminal e instalar os pacotes básicos
Abra o terminal com o atalho `Ctrl + Alt + T` e instale os pacotes básicos do Python:

No **Ubuntu / Debian / Mint / Pop!_OS**:
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

No **Fedora**:
```bash
sudo dnf install -y python3 python3-pip
```

No **Arch Linux**:
```bash
sudo pacman -S python python-pip
```

---

### Passo 2: Navegar até a pasta do projeto
```bash
cd /caminho/para/extrator_markdown
```

---

### Passo 3: Criar o Ambiente Virtual (venv)
```bash
python3 -m venv venv
```

---

### Passo 4: Ativar o Ambiente Virtual
```bash
source venv/bin/activate
```
*(Você verá `(venv)` aparecer no início da linha do terminal)*.

---

### Passo 5: Instalar as dependências

Se você possui placa de vídeo **NVIDIA (GeForce RTX/GTX)** e quer acelerar a conversão com **GPU (CUDA)**:
```bash
pip install --upgrade pip
# 1. Instala o PyTorch compilado com suporte a CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
# 2. Instala o extrator e as demais bibliotecas
pip install -r requirements.txt
```

Caso queira usar apenas **CPU** (sem placa dedicada):
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

*(Aguarde o download e configuração automática de todos os pacotes).*

**Pronto! A instalação no Linux está 100% concluída.**

---

## 💻 Todas as Formas de Usar

Com o terminal aberto e a `(venv)` ativada, veja como extrair seus documentos:

### 1. O jeito mais fácil (1 único PDF na pasta `entrada/`)
1. Coloque o seu arquivo PDF dentro da pasta `entrada/`.
2. No terminal, execute apenas:
   ```bash
   python extrator_lotes.py
   ```
3. O script detecta o PDF sozinho, calcula a quantidade de páginas e inicia a extração em lotes de 100 páginas!

---

### 2. Processar VÁRIOS PDFs em fila de uma vez só (`--todos`)
Se você colocou 2, 5 ou 10 PDFs dentro da pasta `entrada/` e quer deixar o computador processando tudo sozinho:

```bash
python extrator_lotes.py --todos
```

**Como fica a organização na pasta `saida/`?**  
O programa cria uma pasta separada para cada arquivo:
```text
saida/
├── Livro_1_Introducao_IA/
│   ├── Livro_1_Introducao_IA_paginas_1_a_100.md
│   └── Livro_1_Introducao_IA_paginas_101_a_200.md
│
├── Livro_2_Deep_Learning/
│   ├── Livro_2_Deep_Learning_paginas_1_a_100.md
│   └── Livro_2_Deep_Learning_paginas_101_a_180.md
│
└── Artigo_Cientifico/
    └── Artigo_Cientifico_paginas_1_a_35.md
```
Nenhum arquivo se mistura ou substitui o outro!

---

### 3. Processar um arquivo específico
Você pode apontar diretamente para qualquer arquivo informando o caminho:

```bash
python extrator_lotes.py "entrada/meu_livro.pdf"
```
*(Dica: Se o nome do arquivo tiver espaços, coloque entre aspas duplas `" "` como no exemplo acima).*

---

### 4. Economizar memória RAM em computadores mais modestos (`--lote 50`)
Em computadores com 8 GB de RAM ou ao processar livros com centenas de ilustrações e tabelas pesadas, reduza o tamanho do lote de 100 para **50** ou **25** páginas:

```bash
python extrator_lotes.py "entrada/meu_livro.pdf" --lote 50
```

---

### 5. Controlar o uso do processador (`--threads`)
Se você quiser deixar a extração rodando em segundo plano enquanto assiste vídeos, navega ou trabalha sem o computador engasgar, limite a quantidade de núcleos de CPU:

```bash
# Limita o uso a 4 núcleos de CPU
python extrator_lotes.py --todos --threads 4
```

---

## ⚙️ Tabela de Parâmetros e Opções

Você pode combinar as opções conforme a sua necessidade:

| Parâmetro / Flag | Para que serve? | Exemplo de Uso |
| :--- | :--- | :--- |
| `pdf` | Nome ou caminho do PDF que você quer extrair | `python extrator_lotes.py "entrada/livro.pdf"` |
| `-a`, `--todos` | Converte **todos** os PDFs da pasta `entrada/` em fila | `python extrator_lotes.py --todos` |
| `-l`, `--lote <N>` | Altera a quantidade de páginas por arquivo (padrão: 100) | `python extrator_lotes.py --lote 50` |
| `--gpu` | Prioriza e valida a execução acelerada por GPU (CUDA) | `python extrator_lotes.py --gpu` |
| `--cpu` | Força a execução exclusivamente em CPU | `python extrator_lotes.py --cpu` |
| `-t`, `--threads <N>` | Define quantas threads/núcleos o processador usará | `python extrator_lotes.py --threads 4` |
| `-h`, `--help` | Mostra o menu de ajuda com todas as opções na tela | `python extrator_lotes.py --help` |

---

## 📖 O que é um arquivo Markdown (.md) e como usar?

Os arquivos gerados terminam em `.md`. Markdown é o padrão universal da web para texto estruturado.

### Onde você pode usar esses arquivos:
- 📱 **Obsidian e Notion:** Aplicativos de anotações e gestão de conhecimento (basta arrastar o arquivo `.md` para dentro deles).
- 🤖 **ChatGPT, Claude e NotebookLM:** Envie os arquivos `.md` diretamente para IAs como base de conhecimento ou contexto (arquivos Markdown gastam muito menos tokens que PDFs e não perdem formatação).
- 💻 **Editores de Texto:** Podem ser abertos com o VS Code, Bloco de Notas ou qualquer leitor de texto comum.

---

## 🛠️ Dúvidas e Problemas Frequentes (FAQ)

### 1. "O script parece ter travado no Lote 1 e não sai do lugar"
**Não se preocupe!** Na primeiríssima vez que você roda o programa, o Docling precisa baixar os modelos de visão computacional e layout da internet (cerca de 1.5 GB). Dependendo da sua velocidade de internet, isso pode levar alguns minutos. Nas próximas vezes, o início será imediato pois os modelos já ficam salvos no seu computador.

### 2. "Erro: O arquivo não foi encontrado no diretório"
Se o seu arquivo PDF tiver espaços ou caracteres especiais no nome, você **deve** colocá-lo entre aspas duplas no terminal:
- ❌ Incorreto: `python extrator_lotes.py entrada/Meu Livro Grande.pdf`
- ✅ Correto: `python extrator_lotes.py "entrada/Meu Livro Grande.pdf"`

### 3. "No Windows: A execução de scripts foi desabilitada neste sistema"
Esse é o erro mais comum do Windows PowerShell. Para resolver para sempre nesta sessão:
1. Digite no terminal: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`
2. Pressione `Enter`.
3. Tente ativar a venv novamente: `.\venv\Scripts\Activate.ps1`.

### 4. "No Linux: No module named venv"
Algumas distribuições Linux (como Ubuntu e Debian) vêm sem o pacote de ambientes virtuais instalado por padrão. Basta rodar:
```bash
sudo apt install -y python3-venv
```

### 5. "Se eu fechar o terminal no meio do livro, perco o que foi feito?"
**Não!** Como o processamento é feito em lotes, cada lote que você viu a mensagem `[-] Lote concluído e salvo` já está 100% gravado no disco dentro da pasta `saida/`.

---

## 🤝 Créditos

- **[Docling](https://github.com/docling-project/docling)**: Biblioteca de entendimento documental mantida pela equipe de IA do IBM Research Zurich.
- **[PyMuPDF](https://github.com/pymupdf/PyMuPDF)**: Leitor ultrarrápido de documentos e PDFs.

---

Distribuído sob a licença MIT. Sinta-se livre para usar, estudar e compartilhar!
