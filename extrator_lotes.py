#!/usr/bin/env python3
"""
Extrator de Markdown em Lotes para PDFs (Livros, Artigos, Teses e Relatórios)
Utiliza PyMuPDF (fitz) para indexação de páginas e Docling para conversão com IA.
Otimizado para execução em CPU e GPU, compatível com Windows 11 e Linux.
"""

import os
import sys
import time
import argparse
from pathlib import Path

# Tentativa de importação com mensagens amigáveis caso o usuário ainda não tenha ativado a venv
try:
    import fitz
except ImportError:
    fitz = None

try:
    from docling.document_converter import DocumentConverter
except ImportError:
    DocumentConverter = None


def criar_conversor(forcar_cpu: bool = False, num_threads: int | None = None):
    """
    Inicializa o DocumentConverter configurando opções de aceleração (CPU / Threads).
    Possui fallback automático para a inicialização padrão caso ocorra qualquer variação de API.
    """
    try:
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions

        pipeline_options = PdfPipelineOptions()
        
        # Define o dispositivo de aceleração (CPU vs Automático)
        dispositivo = AcceleratorDevice.CPU if forcar_cpu else AcceleratorDevice.AUTO
        acc_kwargs = {"device": dispositivo}
        if num_threads and num_threads > 0:
            acc_kwargs["num_threads"] = num_threads
            
        pipeline_options.accelerator_options = AcceleratorOptions(**acc_kwargs)
        
        return DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
    except Exception as e:
        if forcar_cpu or num_threads:
            print(f"[i] Aviso ao configurar acelerador ({e}). Utilizando inicialização padrão do Docling...")
        from docling.document_converter import DocumentConverter
        return DocumentConverter()


def resolver_caminho_pdf(caminho_informado: str | None) -> Path:
    """
    Localiza o PDF a ser processado:
    1. Argumento passado na linha de comando
    2. Arquivo padrão histórico (1-s2.0-S1877050925016655-main.pdf)
    3. Arquivo(s) dentro da pasta 'entrada/'
    4. Arquivo(s) no diretório raiz do repositório
    """
    if caminho_informado:
        p = Path(caminho_informado)
        if not p.is_file():
            print(f"[!] Erro: Arquivo informado não encontrado: {caminho_informado}")
            sys.exit(1)
        return p

    # Arquivo padrão original
    padrao = Path("1-s2.0-S1877050925016655-main.pdf")
    if padrao.is_file():
        return padrao

    # Busca na pasta entrada/
    pasta_entrada = Path("entrada")
    if pasta_entrada.is_dir():
        pdfs_entrada = [f for f in pasta_entrada.glob("*.pdf") if f.is_file()]
        if len(pdfs_entrada) == 1:
            print(f"[i] PDF selecionado automaticamente em entrada/: {pdfs_entrada[0].name}")
            return pdfs_entrada[0]
        elif len(pdfs_entrada) > 1:
            print(f"[i] Encontrados {len(pdfs_entrada)} PDFs na pasta entrada/.")
            print(f"[i] Processando o primeiro: {pdfs_entrada[0].name}")
            print(f"[i] Para escolher outro, informe o caminho: python extrator_lotes.py \"{pdfs_entrada[1]}\"")
            return pdfs_entrada[0]

    # Busca no diretório atual
    pdfs_raiz = [f for f in Path(".").glob("*.pdf") if f.is_file()]
    if len(pdfs_raiz) == 1:
        print(f"[i] PDF selecionado automaticamente no diretório atual: {pdfs_raiz[0].name}")
        return pdfs_raiz[0]
    elif len(pdfs_raiz) > 1:
        print(f"[i] Encontrados {len(pdfs_raiz)} PDFs no diretório. Processando: {pdfs_raiz[0].name}")
        return pdfs_raiz[0]

    # Nenhum PDF localizado
    print("\n" + "=" * 60)
    print("[!] Nenhum arquivo PDF foi encontrado para processamento!")
    print("=" * 60)
    print("\nComo executar:")
    print("  1. Coloque seu arquivo PDF na pasta 'entrada/' ou nesta pasta.")
    print("  2. Ou passe o caminho do arquivo diretamente pelo terminal:")
    print("     python extrator_lotes.py caminho/para/seu_livro.pdf")
    print("  3. Exemplos adicionais:")
    print("     python extrator_lotes.py artigo.pdf --lote 50")
    print("     python extrator_lotes.py livro.pdf --cpu --threads 4")
    print("=" * 60 + "\n")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Extrator de Markdown em lotes a partir de PDFs usando Docling e PyMuPDF."
    )
    parser.add_argument(
        "pdf",
        nargs="?",
        default=None,
        help="Caminho do arquivo PDF a ser processado (opcional se houver PDF na pasta entrada/ ou raiz)"
    )
    parser.add_argument(
        "--lote",
        "-l",
        type=int,
        default=100,
        help="Quantidade de páginas por lote (padrão: 100). Em máquinas com menos RAM em CPU, use 25 a 50."
    )
    parser.add_argument(
        "--saida",
        "-s",
        type=str,
        default=None,
        help="Pasta de saída para os arquivos Markdown gerados (padrão: pasta com nome do PDF dentro de saida/)"
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Força a execução exclusivamente em CPU"
    )
    parser.add_argument(
        "--threads",
        "-t",
        type=int,
        default=None,
        help="Número de threads de CPU a serem utilizadas pelo acelerador (ex: 4)"
    )

    args = parser.parse_args()

    # Verificação de dependências instaladas
    if fitz is None:
        print("\n[!] O pacote 'PyMuPDF' não está instalado no ambiente atual.")
        print("    Para instalar, execute: pip install PyMuPDF")
        print("    Ou instale todos os requisitos: pip install -r requirements-cpu.txt\n")
        sys.exit(1)

    if DocumentConverter is None:
        print("\n[!] O pacote 'docling' não está instalado no ambiente atual.")
        print("    Para instalar no modo otimizado para CPU, execute:")
        print("    pip install -r requirements-cpu.txt\n")
        sys.exit(1)

    # 1. Resolver arquivo PDF
    pdf_path = resolver_caminho_pdf(args.pdf)

    # 2. Configurar diretório de saída
    nome_base = pdf_path.stem
    if args.saida:
        pasta_saida = Path(args.saida)
    else:
        # Cria subpasta organizada em saida/<nome_do_arquivo>
        pasta_saida = Path("saida") / nome_base

    pasta_saida.mkdir(parents=True, exist_ok=True)

    # 3. Detectar total de páginas com PyMuPDF (rápido e seguro)
    print(f"\n[+] Lendo quantidade total de páginas de '{pdf_path.name}'...")
    try:
        doc = fitz.open(str(pdf_path))
        total_paginas = doc.page_count
        doc.close()
    except Exception as e:
        print(f"[!] Erro ao abrir o PDF com PyMuPDF: {e}")
        sys.exit(1)

    print(f"[✓] Total de páginas detectadas: {total_paginas}")

    tamanho_lote = max(1, args.lote)
    total_lotes = (total_paginas + tamanho_lote - 1) // tamanho_lote
    print(f"[✓] Tamanho do lote: {tamanho_lote} páginas por arquivo")
    print(f"[✓] Total de lotes calculados: {total_lotes}")
    print(f"[✓] Pasta de destino: {pasta_saida.resolve()}")

    # 4. Inicializar modelo Docling
    print("\n[+] Inicializando o motor de IA do Docling...")
    modo = "CPU" if args.cpu else "Auto (GPU se disponível, senão CPU)"
    print(f"[i] Modo de hardware: {modo}" + (f" ({args.threads} threads)" if args.threads else ""))
    converter = criar_conversor(forcar_cpu=args.cpu, num_threads=args.threads)

    # 5. Processamento dos lotes
    lote_num = 1
    lotes_sucesso = 0
    lotes_falha = 0
    tempo_inicio_total = time.time()

    print("\n" + "=" * 60)
    print("INICIANDO PROCESSAMENTO EM LOTES")
    print("=" * 60)

    for pagina_inicial in range(1, total_paginas + 1, tamanho_lote):
        pagina_final = min(pagina_inicial + tamanho_lote - 1, total_paginas)
        nome_arquivo = f"{nome_base}_paginas_{pagina_inicial}_a_{pagina_final}.md"
        caminho_arquivo = pasta_saida / nome_arquivo

        pct = (pagina_final / total_paginas) * 100
        print(f"\n[+] [Lote {lote_num}/{total_lotes}] Processando páginas {pagina_inicial} até {pagina_final} ({pct:.1f}% do PDF)...")

        tempo_inicio_lote = time.time()
        try:
            # Converte a fatia de páginas especificada
            conv_res = converter.convert(str(pdf_path), page_range=(pagina_inicial, pagina_final))

            # Exporta para Markdown estruturado
            conteudo_markdown = conv_res.document.export_to_markdown()

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo_markdown)

            tempo_lote = time.time() - tempo_inicio_lote
            tamanho_kb = caminho_arquivo.stat().st_size / 1024
            print(f"[-] Lote {lote_num} concluído em {tempo_lote:.1f}s ({tamanho_kb:.1f} KB)")
            print(f"    Arquivo: {caminho_arquivo}")
            lotes_sucesso += 1

        except Exception as e:
            print(f"[!] Erro ao processar o lote {pagina_inicial}-{pagina_final}: {e}")
            lotes_falha += 1
            # Continua para o próximo lote para não perder o restante do trabalho
            continue
        finally:
            lote_num += 1

    tempo_total = time.time() - tempo_inicio_total
    print("\n" + "=" * 60)
    print("RESUMO DO PROCESSAMENTO")
    print("=" * 60)
    print(f"Status: Concluído em {tempo_total:.1f}s")
    print(f"Lotes finalizados com sucesso: {lotes_sucesso}/{total_lotes}")
    if lotes_falha > 0:
        print(f"Lotes que apresentaram falha: {lotes_falha}")
    print(f"Arquivos salvos em: {pasta_saida.resolve()}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()