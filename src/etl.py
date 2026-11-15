
from pathlib import Path
import pandas as pd


# Caminhos do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO_ORIGINAL = (
    PASTA_PROJETO
    / "data"
    / "raw"
    / "tabela9514_grupo_idade_BR_GR_UF.xlsx"
)

PASTA_SAIDA = PASTA_PROJETO / "data" / "processed"


def transformar_aba(arquivo, nome_aba):
    """
    Lê uma aba da tabela do IBGE e transforma os dados
    para o formato organizado: localidade, sexo e faixa etária.
    """

    dados = pd.read_excel(
        arquivo,
        sheet_name=nome_aba,
        header=None
    )

    # Os dados começam na linha 7 (índice 6).
    # A última linha contém a fonte, não dados populacionais.
    linhas_dados = dados[
        dados.iloc[:, 1].astype(str).str.strip().eq("Total")
    ].copy()

    # Blocos de colunas correspondentes a cada sexo.
    blocos = {
        "Total": (2, 24),
        "Homens": (24, 46),
        "Mulheres": (46, 68)
    }

    registros = []

    for _, linha in linhas_dados.iterrows():

        localidade = str(linha.iloc[0]).strip()

        for sexo, (inicio, fim) in blocos.items():

            # Os nomes das faixas etárias estão na linha de cabeçalho.
            faixas_etarias = dados.iloc[5, inicio:fim].tolist()

            valores = linha.iloc[inicio:fim].tolist()

            for faixa_etaria, valor in zip(faixas_etarias, valores):

                valor_numerico = pd.to_numeric(
                    valor,
                    errors="coerce"
                )

                if pd.isna(valor_numerico):
                    continue

                registros.append({
                    "localidade": localidade,
                    "forma_declaracao_idade": str(linha.iloc[1]).strip(),
                    "ano": 2022,
                    "sexo": sexo,
                    "faixa_etaria": str(faixa_etaria).strip(),
                    "valor": valor_numerico
                })

    resultado = pd.DataFrame(registros)

    return resultado


def executar_etl():

    print("Iniciando o processamento dos dados do IBGE...")

    # Verifica se o arquivo original existe.
    if not ARQUIVO_ORIGINAL.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_ORIGINAL}"
        )

    # Cria a pasta de saída, caso ainda não exista.
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

    # Identifica as abas da planilha.
    excel = pd.ExcelFile(ARQUIVO_ORIGINAL)

    aba_populacao = next(
        (aba for aba in excel.sheet_names if "Pessoas" in aba),
        None
    )

    aba_percentual = next(
        (aba for aba in excel.sheet_names if "percen" in aba.lower()),
        None
    )

    if aba_populacao is None or aba_percentual is None:
        raise ValueError(
            "Não foi possível localizar as abas de população e percentual."
        )

    # Processa os dados absolutos.
    populacao = transformar_aba(
        ARQUIVO_ORIGINAL,
        aba_populacao
    )

    # Processa os dados percentuais.
    percentual = transformar_aba(
        ARQUIVO_ORIGINAL,
        aba_percentual
    )

    # Salva os arquivos em formato CSV compactado.
    populacao.to_csv(
        PASTA_SAIDA / "populacao_2022.csv.gz",
        index=False,
        encoding="utf-8",
        compression="gzip"
    )

    percentual.to_csv(
        PASTA_SAIDA / "percentual_populacao_2022.csv.gz",
        index=False,
        encoding="utf-8",
        compression="gzip"
    )

    print("\nProcessamento concluído!")

    print(f"Registros de população: {len(populacao)}")
    print(f"Registros percentuais: {len(percentual)}")

    print("\nTotal da população brasileira:")
    print(
        populacao[
            (populacao["localidade"] == "Brasil")
            & (populacao["sexo"] == "Total")
            & (populacao["faixa_etaria"] == "Total")
        ]["valor"].iloc[0]
    )

    print(f"\nArquivos salvos em: {PASTA_SAIDA}")


if __name__ == "__main__":
    executar_etl()
