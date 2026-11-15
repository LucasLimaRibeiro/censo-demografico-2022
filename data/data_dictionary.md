# Dicionário de Dados — Censo Demográfico 2022

## 1. Identificação da fonte

- **Instituição responsável:** Instituto Brasileiro de Geografia e Estatística (IBGE).
- **Pesquisa:** Censo Demográfico 2022.
- **Tabela:** 9514.
- **Título:** População residente, por sexo, idade e forma de declaração da idade.
- **Abrangência geográfica:** Brasil, Grandes Regiões e Unidades da Federação.
- **Tipo de dado:** Dados do Universo.
- **Arquivo original:** `tabela9514_grupo_idade_BR_GR_UF.xlsx`.
- **Formato original:** XLSX (Excel).
- **Fonte oficial:** [IBGE — Censo Demográfico 2022](https://www.ibge.gov.br/estatisticas/sociais/trabalho/22827-censo-demografico-2022.html)

## 2. Descrição da base

A tabela apresenta informações sobre a população residente no Brasil em 2022, organizadas por localização geográfica, sexo e grupos de idade.

O arquivo original possui três abas:

1. **População residente - Pessoas:** apresenta os valores absolutos da população.
2. **População residente - percentual:** apresenta a distribuição percentual da população.
3. **Notas:** contém observações metodológicas e explicações sobre os símbolos utilizados na tabela.

A planilha original apresenta cabeçalhos agrupados e múltiplos níveis de informação. Durante o processo ETL, essas informações foram reorganizadas em uma estrutura tabular adequada para análise computacional.

Foram selecionadas as informações correspondentes à categoria total da forma de declaração da idade, considerando as localidades disponíveis na tabela: Brasil, cinco Grandes Regiões e 27 Unidades da Federação.

## 3. Dicionário de variáveis

Os arquivos processados possuem as seguintes variáveis:

| Variável | Descrição | Tipo |
|---|---|---|
| `localidade` | Nome do território ao qual os dados populacionais se referem | Texto (string) |
| `forma_declaracao_idade` | Forma de declaração da idade. Nesta extração, foi utilizada a categoria Total | Texto (string) |
| `ano` | Ano de referência dos dados (2022) | Inteiro (int) |
| `sexo` | Categoria de sexo: Total, Homens ou Mulheres | Texto (string) |
| `faixa_etaria` | Grupo de idade da população, incluindo o total geral | Texto (string) |
| `valor` | Quantidade de pessoas ou percentual, conforme o arquivo processado | Numérico |

**Observação:** a variável `valor` representa quantidades absolutas no arquivo `populacao_2022.csv.gz` e valores percentuais no arquivo `percentual_populacao_2022.csv.gz`.

## 4. Unidades e formatos

- **População residente:** quantidade de pessoas.
- **Percentual da população:** valores percentuais apresentados pelo IBGE.
- **Ano:** 2022.
- **Grupos de idade:** faixas etárias, como 0 a 4 anos, 5 a 9 anos e demais intervalos disponíveis na tabela.
- **Localidade:** Brasil, Grandes Regiões e Unidades da Federação.
- **Sexo:** Total, Homens e Mulheres.

Os arquivos processados foram armazenados em formato CSV compactado com compressão GZIP e codificação UTF-8.

## 5. Observações metodológicas

A tabela apresenta dados do Universo do Censo Demográfico 2022.

O IBGE informa que os dados referentes aos municípios Abel Figueiredo (PA) e São Pedro da Água Branca (MA) foram corrigidos em 22/12/2023, com impacto nos totais estaduais e regionais.

A planilha original também apresenta símbolos para representar situações como zero absoluto, zero decorrente de arredondamento, valor não aplicável e valor não disponível.

Essas situações devem ser observadas durante o tratamento dos dados, evitando interpretações incorretas.

## 6. Tratamento e rastreabilidade

O arquivo original foi preservado na pasta `data/raw/`.

As etapas de leitura, limpeza, transformação e organização foram implementadas por meio do script Python `src/etl.py`, utilizando a biblioteca Pandas.

O processo realizado incluiu:

- Leitura das abas de população absoluta e percentual.
- Identificação das linhas correspondentes às localidades.
- Separação das informações por sexo e faixa etária.
- Reorganização dos cabeçalhos agrupados em colunas individuais.
- Conversão dos valores para formato numérico.
- Armazenamento dos resultados na pasta `data/processed/`.

Os arquivos gerados foram:

- `populacao_2022.csv.gz`
- `percentual_populacao_2022.csv.gz`

O processamento gerou 2.178 registros para cada arquivo, totalizando 4.356 registros.

Como validação inicial, foi verificado que a população total do Brasil corresponde a 203.080.756 habitantes, sendo 98.532.431 homens e 104.548.325 mulheres. Também foi realizada uma verificação de duplicidade, que não identificou registros duplicados considerando localidade, sexo e faixa etária.

O script pode ser executado novamente a partir da pasta principal do projeto utilizando:

```bash
python -m src.etl
```

## 7. Licenciamento e reutilização

A fonte dos dados é o Instituto Brasileiro de Geografia e Estatística (IBGE).

A reutilização e redistribuição dos dados devem respeitar as condições de uso e atribuição estabelecidas pelo IBGE e pela fonte original.

A licença do código desenvolvido para o projeto será MIT. Os materiais produzidos no projeto terão sua licença documentada separadamente, respeitando os direitos e as condições aplicáveis aos dados originais.

## 8. Princípios FAIR

A organização dos dados considera os princípios FAIR:

- **Findable (Localizáveis):** identificação da fonte, documentação das variáveis e organização dos arquivos.
- **Accessible (Acessíveis):** disponibilização dos arquivos e scripts em repositório público.
- **Interoperable (Interoperáveis):** utilização de formatos abertos, como CSV compactado, e padronização das variáveis.
- **Reusable (Reutilizáveis):** documentação da origem, metodologia de tratamento, estrutura dos dados e condições de reutilização.