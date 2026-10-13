#!/usr/bin/env python3
"""
Extrator de Markdown em Lotes a partir de PDFs (Livros, Artigos, Teses e Relatórios)
Utiliza PyMuPDF para indexação de páginas e Docling para conversão com IA.
Otimizado para execução em CPU e GPU, compatível com Windows 11 e Linux.

Estrutura de pastas:
- Entrada: 'entrada/' (ou arquivo informado na linha de comando)
- Saída: 'saida/<nome_do_pdf>/<nome_do_pdf>_paginas_X_a_Y.md'
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
        # pyrefly: ignore [missing-import]
        import fitz
    except ImportError:
        fitz = None

try:
    # pyrefly: ignore [missing-import]
    from docling.document_converter import DocumentConverter
except ImportError:
    DocumentConverter = None


def criar_conversor(forcar_cpu: bool = False, forcar_gpu: bool = False, num_threads: int | None = None):
    """
    Inicializa o DocumentConverter configurando opções de aceleração (CPU / GPU / Threads).
    Fallback automático para inicialização padrão caso haja variação de versão do Docling.
    """
    gpu_disponivel = False
    nome_gpu = None
    try:
        # pyrefly: ignore [missing-import]
        import torch
        if torch.cuda.is_available():
            gpu_disponivel = True
            nome_gpu = torch.cuda.get_device_name(0)
    except Exception:
        pass

    if forcar_cpu:
        print("[⚙️] Modo forçado: Executando exclusivamente em CPU (--cpu).")
    elif gpu_disponivel:
        print(f"[🚀] Aceleração por GPU ativada: {nome_gpu}")
    elif forcar_gpu:
        print("[!] Aviso: '--gpu' foi solicitada, mas nenhuma GPU CUDA foi encontrada pelo PyTorch.")
        print("    Para ativar sua GPU NVIDIA, instale o PyTorch com suporte a CUDA:")
        print("    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124\n")
    else:
        print("[ℹ️] Nenhuma GPU CUDA detectada pelo PyTorch. Executando em CPU.")

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

        if forcar_cpu:
            dispositivo = AcceleratorDevice.CPU
        elif gpu_disponivel or forcar_gpu:
            dispositivo = AcceleratorDevice.CUDA
        else:
            dispositivo = AcceleratorDevice.AUTO

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
        if forcar_cpu or forcar_gpu or num_threads:
            print(f"[i] Aviso ao configurar acelerador ({e}). Utilizando inicialização padrão...")
        # pyrefly: ignore [missing-import]
        from docling.document_converter import DocumentConverter
        return DocumentConverter()


def processar_pdf(pdf_path: str, converter, tamanho_lote: int):
    """
    Processa um único arquivo PDF em lotes, salvando os resultados em:
    saida/<nome_do_pdf>/<nome_do_pdf>_paginas_X_a_Y.md
    """
    nome_base = os.path.splitext(os.path.basename(pdf_path))[0]
    pasta_saida = os.path.join("saida", nome_base)
    os.makedirs(pasta_saida, exist_ok=True)

    print("\n" + "=" * 60)
    print(f"📄 DOCUMENTO: {os.path.basename(pdf_path)}")
    print(f"📁 DESTINO: {os.path.abspath(pasta_saida)}")
    print("=" * 60)

    # 1. Leitura do total de páginas com PyMuPDF
    print("Lendo a quantidade total de páginas...")
    try:
        doc = fitz.open(pdf_path)
        total_paginas = doc.page_count
        doc.close()
    except Exception as e:
        print(f"[!] Erro ao abrir o PDF '{pdf_path}' com PyMuPDF: {e}")
        return False

    print(f"Total de páginas detectadas: {total_paginas}")

    total_lotes = (total_paginas + tamanho_lote - 1) // tamanho_lote
    print(f"Tamanho do lote: {tamanho_lote} páginas por arquivo")
    print(f"Total de lotes calculados: {total_lotes}")

    # 2. Loop de processamento em lotes
    lote_num = 1
    lotes_sucesso = 0
    lotes_falha = 0
    tempo_inicio_doc = time.time()

    for pagina_inicial in range(1, total_paginas + 1, tamanho_lote):
        pagina_final = min(pagina_inicial + tamanho_lote - 1, total_paginas)

        nome_arquivo = f"{nome_base}_paginas_{pagina_inicial}_a_{pagina_final}.md"
        caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)

        pct = (pagina_final / total_paginas) * 100
        print(f"\n[+] [Lote {lote_num}/{total_lotes}] Páginas {pagina_inicial} até {pagina_final} ({pct:.1f}%)...")
        tempo_inicio_lote = time.time()

        try:
            # Extrai o lote atual de páginas com Docling
            conv_res = converter.convert(pdf_path, page_range=(pagina_inicial, pagina_final))

            # Salva o arquivo Markdown gerado
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write(conv_res.document.export_to_markdown())

            tempo_lote = time.time() - tempo_inicio_lote
            tamanho_kb = os.path.getsize(caminho_arquivo) / 1024
            print(f"[-] Lote concluído em {tempo_lote:.1f}s ({tamanho_kb:.1f} KB)")
            print(f"    Salvo como: {caminho_arquivo}")
            lotes_sucesso += 1

        except Exception as e:
            print(f"[!] Erro ao processar o lote {pagina_inicial}-{pagina_final}: {e}")
            lotes_falha += 1
            continue
        finally:
            lote_num += 1

    tempo_doc = time.time() - tempo_inicio_doc
    print(f"\n[✓] Concluído '{nome_base}' em {tempo_doc:.1f}s ({lotes_sucesso}/{total_lotes} lotes salvos)")
    if lotes_falha > 0:
        print(f"[!] Lotes com falha: {lotes_falha}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Extrator de Markdown em lotes a partir de PDFs usando Docling e PyMuPDF."
    )
    parser.add_argument(
        "pdf",
        nargs="?",
        default=None,
        help="Caminho do PDF a ser processado (opcional se houver PDF em 'entrada/')"
    )
    parser.add_argument(
        "--todos",
        "-a",
        action="store_true",
        help="Processa todos os PDFs encontrados na pasta 'entrada/' sequencialmente"
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
        "--gpu",
        action="store_true",
        help="Prioriza ou valida a execução com aceleração em GPU (CUDA)"
    )
    parser.add_argument(
        "--threads",
        "-t",
        type=int,
        default=None,
        help="Número de threads de CPU a serem utilizadas (ex: 4)"
    )

    args = parser.parse_args()

    # Validação das bibliotecas instaladas
    if fitz is None:
        print("\n[!] O pacote 'PyMuPDF' não está instalado no ambiente virtual.")
        print("    Instale executando: pip install PyMuPDF\n")
        sys.exit(1)

    if DocumentConverter is None:
        print("\n[!] O pacote 'docling' não está instalado no ambiente virtual.")
        print("    Instale executando: pip install -r requirements.txt\n")
        sys.exit(1)

    # Identificação da lista de arquivos a processar
    arquivos_para_processar = []
    pasta_entrada = "entrada"

    if args.todos:
        # Modo: Processar todos os PDFs de entrada/
        if os.path.isdir(pasta_entrada):
            arquivos_para_processar = [
                os.path.join(pasta_entrada, f)
                for f in sorted(os.listdir(pasta_entrada))
                if f.lower().endswith(".pdf") and os.path.isfile(os.path.join(pasta_entrada, f))
            ]
        if not arquivos_para_processar:
            print(f"\n[!] Erro: A flag '--todos' foi informada, mas nenhum PDF foi encontrado na pasta '{pasta_entrada}/'.\n")
            sys.exit(1)
        print(f"\n[i] Modo em lote ativado: {len(arquivos_para_processar)} arquivo(s) encontrado(s) na pasta '{pasta_entrada}/'.")

    elif args.pdf:
        # Modo: Arquivo específico informado pelo usuário
        caminho_direto = args.pdf
        caminho_em_entrada = os.path.join(pasta_entrada, args.pdf)

        if os.path.isfile(caminho_direto):
            arquivos_para_processar = [caminho_direto]
        elif os.path.isfile(caminho_em_entrada):
            arquivos_para_processar = [caminho_em_entrada]
        else:
            print(f"\n[!] Erro: O arquivo '{args.pdf}' não foi encontrado no diretório nem na pasta '{pasta_entrada}/'.")
            print("    Verifique o nome do arquivo e tente novamente.\n")
            sys.exit(1)

    else:
        # Nenhum arquivo e nenhuma flag informados: verifica a pasta entrada/
        pdfs_entrada = []
        if os.path.isdir(pasta_entrada):
            pdfs_entrada = [
                os.path.join(pasta_entrada, f)
                for f in sorted(os.listdir(pasta_entrada))
                if f.lower().endswith(".pdf") and os.path.isfile(os.path.join(pasta_entrada, f))
            ]

        if len(pdfs_entrada) == 1:
            arquivos_para_processar = [pdfs_entrada[0]]
            print(f"[i] Nenhum argumento informado. Processando o único PDF em '{pasta_entrada}/':")
            print(f"    -> {pdfs_entrada[0]}")
        elif len(pdfs_entrada) > 1:
            print(f"\n[i] Foram encontrados {len(pdfs_entrada)} arquivos PDF na pasta '{pasta_entrada}/':")
            for idx, p in enumerate(pdfs_entrada, 1):
                print(f"    {idx}. {os.path.basename(p)}")
            print("\nComo você deseja processar?")
            print(f"  • Um por um:    python extrator_lotes.py \"{pdfs_entrada[0]}\"")
            print(f"  • Todos na fila: python extrator_lotes.py --todos\n")
            sys.exit(0)
        else:
            print("\n[!] Erro: Nenhum arquivo PDF foi informado e nenhum PDF foi encontrado na pasta 'entrada/'.")
            print("    Coloque seu arquivo .pdf na pasta 'entrada/' ou passe o caminho:")
            print("    python extrator_lotes.py caminho/do/arquivo.pdf\n")
            sys.exit(1)

    # Inicializa o modelo Docling uma única vez para todos os documentos
    print("\nIniciando o modelo de IA (Docling)...")
    converter = criar_conversor(forcar_cpu=args.cpu, forcar_gpu=args.gpu, num_threads=args.threads)

    tamanho_lote = max(1, args.lote)
    tempo_inicio_geral = time.time()

    for idx, pdf_file in enumerate(arquivos_para_processar, 1):
        print(f"\n>>> Processando documento [{idx}/{len(arquivos_para_processar)}]: {os.path.basename(pdf_file)}")
        processar_pdf(pdf_file, converter, tamanho_lote)

    tempo_total_geral = time.time() - tempo_inicio_geral
    print("\n" + "=" * 60)
    print("TODOS OS DOCUMENTOS FORAM PROCESSADOS COM SUCESSO!")
    print(f"Total de documentos: {len(arquivos_para_processar)}")
    print(f"Tempo total de execução: {tempo_total_geral:.1f}s")
    print(f"Pastas geradas dentro de: {os.path.abspath('saida')}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()