# NDVI Finder
Este projeto visa produzir um produto NDVI composto por várias cenas que podem ser separados em regiões com seus períodos de estudo considerando o semi-árido brasileiro.

Observação: É possível fazer modificações para que você possa gerar o NDVI para áreas fora do território semi-árido.

*Leia isto em outros idiomas: [Inglês](README.md), [Português](README.pt.md)*

# Construindo projeto
Para construir este projeto, execute o script *build* usando o seguinte código.

```
    sh build
```

# Configurando projeto
Para configurar o projeto, você precisa editar os arquivos `samples/semi-arid/time_range.csv` e `samples/semi-arid/path_row.txt`. Em `time_range.csv`, alterando para cada região seu respectivo ano e dia juliano do início e fim do estudo (período chuvoso + pós chuva) e o início do pós-chuva (para o algoritmo priorizar os melhores pixels do índice de vegetação). Por exemplo, temos a seguinte configuração:

```
REGION_NAME, START_DATE, END_DATE, START_POST_RAIN
MYREGION, 2018 001,2018 091, 2018 070
```

Em `path_row.txt`, você precisa ter as mesmas regiões adicionadas em `time_range.csv`, mas agora descrevendo o path/row de cada cena do landsat que compõe a região. Por exemplo, temos a seguinte configuração:

```
MYREGION PATH01 ROW01 PATH02 ROW02 PATH03 ROW03 ...
```

Observação: As configurações presentes no código estão corretas para calcular o NDVI do ano de 1986 do semi-árido brasileiro.

# Executando projeto
Para executar o projeto, use o seguinte comando:

```
    python main.py run
```

# Informação adicional
### Baixar imagens do landsat

```
    python downloader.py download samples/semi-arid/path_row.txt samples/semi-arid/time_range.csv output/
```
