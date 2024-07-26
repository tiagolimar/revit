# TLMarcenaria

Este é um plugin para Revit desenvolvido utilizando PyRevit. O plugin importa dados de um arquivo CSV e cria instâncias de uma família específica de acordo com as especificações fornecidas.

## script.py
O script.py é o principal arquivo do plugin. Ele executa as seguintes funções:

- Importa um arquivo CSV.
- Cria instâncias de uma família específica no Revit com base nos dados do CSV.

## Uso
1. Importação de Dados CSV:

> - O arquivo CSV deve conter os seguintes campos: `Comprimento`, `Largura`, `Espessura`, `Cod`, `Quantidade`.
> - Os valores devem estar separados por ponto e vírgula (;).

1. Execução do Script:

> - O script solicitará que você selecione um arquivo CSV.
> - Em seguida, ele processará o arquivo e criará instâncias da família no Revit.

## Dependências
- Revit com PyRevit instalado.

## Exemplo de Arquivo CSV

```csv
"Comprimento";"Largura";"Espessura";"Cod";"Quantidade"
100;50;2;A001;2
200;50;2;A002;3
```

## Instruções de Instalação
- Clone este repositório no seu diretório de plugins do PyRevit.
- Certifique-se de que o arquivo Painel.rfa está no mesmo diretório que o script.py.
- No Revit, acesse a guia do TLMarcenaria e execute o plugin "Importar CSV".