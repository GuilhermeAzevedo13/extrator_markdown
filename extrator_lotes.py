#!/usr/bin/env python3
"""
Extrator de Markdown em Lotes a partir de PDFs (Livros, Artigos, Teses e Relatórios)
Utiliza PyMuPDF (fitz) para indexação de páginas e Docling para conversão com IA.
Otimizado para execução em CPU e GPU, compatível com Windows 11 e Linux.
"""

import os
import sys
import time
import argparse

# Tentativa de importação com mensagens educativas (usa pymupdf preferencialmente)
try:
    # pyrefly: ignore [missing-import]
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None

try:
    # pyrefly: ignore [missing-import]
    from docling.document_converter import DocumentConverter
except ImportError:
    DocumentConverter = None


def criar_conversor(forcar_cpu: bool = False, num_threads: int | None = None):
    """
    Inicializa o DocumentConverter configurando opções de aceleração (CPU / Threads).
    Fallback automático para inicialização padrão caso haja variação de versão do Docling.
    """
    try:
        # pyrefly: ignore [missing-import]
        from docling.document_converter import DocumentConverter, PdfFormatOption
        # pyrefly: ignore [missing-import]
        from docling.datamodel.base_models import InputFormat
        # pyrefly: ignore [missing-import]
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        # pyrefly: ignore [missing-import]
        from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions

        pipeline_options = PdfPipelineOptions()

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
            print(f"[i] Aviso ao configurar acelerador ({e}). Utilizando inicialização padrão...")
        # pyrefly: ignore [missing-import]
        from docling.document_converter import DocumentConverter
        return DocumentConverter()


def main():
    parser = argparse.ArgumentParser(
        description="Extrator de Markdown em lotes a partir de PDFs usando Docling e PyMuPDF."
    )
    parser.add_argument(
        "pdf",
        nargs="?",
        default=None,
        help="Caminho do arquivo PDF a ser processado (obrigatório)"
    )
    parser.add_argument(
        "--lote",
        "-l",
        type=int,
        default=100,
        help="Quantidade de páginas por lote (padrão: 100). Em máquinas com pouca RAM em CPU, use 25 a 50."
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
        help="Número de threads de CPU a serem utilizadas (ex: 4)"
    )

    args = parser.parse_args()

    # 1. Validação do parâmetro do PDF
    if not args.pdf:
        print("\n[!] Erro: Nenhum arquivo PDF foi informado.")
        print("    Uso: python extrator_lotes.py <caminho_do_arquivo.pdf> [opcoes]")
        print("    Exemplo: python extrator_lotes.py meu_livro.pdf")
        print("    Exemplo CPU: python extrator_lotes.py meu_livro.pdf --cpu --lote 50\n")
        sys.exit(1)

    pdf_path = args.pdf

    # 2. Validação da existência do PDF no diretório
    if not os.path.isfile(pdf_path):
        print(f"\n[!] Erro: O arquivo '{pdf_path}' não foi encontrado no diretório.")
        print("    Verifique se o nome e o caminho do arquivo estão corretos e tente novamente.\n")
        sys.exit(1)

    # 3. Validação das bibliotecas instaladas
    if fitz is None:
        print("\n[!] O pacote 'PyMuPDF' não está instalado no ambiente virtual.")
        print("    Instale executando: pip install PyMuPDF\n")
        sys.exit(1)

    if DocumentConverter is None:
        print("\n[!] O pacote 'docling' não está instalado no ambiente virtual.")
        print("    Instale executando: pip install -r requirements-cpu.txt\n")
        sys.exit(1)

    # 4. Configuração das pastas de saída
    pasta_saida = os.path.splitext(os.path.basename(pdf_path))[0]
    os.makedirs(pasta_saida, exist_ok=True)

    # 5. Leitura do total de páginas com PyMuPDF
    print(f"\nLendo a quantidade total de páginas de '{pdf_path}'...")
    try:
        doc = fitz.open(pdf_path)
        total_paginas = doc.page_count
        doc.close()
    except Exception as e:
        print(f"[!] Erro ao abrir o PDF com PyMuPDF: {e}")
        sys.exit(1)

    print(f"Total de páginas detectadas: {total_paginas}")

    tamanho_lote = max(1, args.lote)
    total_lotes = (total_paginas + tamanho_lote - 1) // tamanho_lote
    print(f"Tamanho do lote: {tamanho_lote} páginas por arquivo")
    print(f"Total de lotes calculados: {total_lotes}")
    print(f"Pasta de saída: {os.path.abspath(pasta_saida)}")

    # 6. Inicialização do modelo Docling
    print("\nIniciando a inicialização do modelo de IA (Docling)...")
    converter = criar_conversor(forcar_cpu=args.cpu, num_threads=args.threads)
    print("Documento:", pdf_path)

    # 7. Loop de processamento em lotes
    lote_num = 1
    lotes_sucesso = 0
    lotes_falha = 0
    tempo_inicio_total = time.time()

    for pagina_inicial in range(1, total_paginas + 1, tamanho_lote):
        pagina_final = min(pagina_inicial + tamanho_lote - 1, total_paginas)

        nome_arquivo = f"{pasta_saida}_paginas_{pagina_inicial}_a_{pagina_final}.md"
        caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)

        print(f"\n[+] [Lote {lote_num}/{total_lotes}] Processando páginas {pagina_inicial} até {pagina_final}...")
        tempo_inicio_lote = time.time()

        try:
            # Extrai o lote atual de páginas
            conv_res = converter.convert(pdf_path, page_range=(pagina_inicial, pagina_final))

            # Salva o arquivo Markdown gerado
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write(conv_res.document.export_to_markdown())

            tempo_lote = time.time() - tempo_inicio_lote
            print(f"[-] Lote concluído em {tempo_lote:.1f}s e salvo como: {caminho_arquivo}")
            lotes_sucesso += 1

        except Exception as e:
            print(f"[!] Erro ao processar o lote {pagina_inicial}-{pagina_final}: {e}")
            lotes_falha += 1
            # Continua para o próximo lote mesmo se o atual der erro
            continue
        finally:
            lote_num += 1

    tempo_total = time.time() - tempo_inicio_total
    print("\n" + "=" * 50)
    print("Processamento completo!")
    print(f"Tempo total: {tempo_total:.1f}s")
    print(f"Lotes finalizados com sucesso: {lotes_sucesso}/{total_lotes}")
    if lotes_falha > 0:
        print(f"Lotes com erro: {lotes_falha}")
    print(f"Arquivos salvos na pasta: {os.path.abspath(pasta_saida)}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()