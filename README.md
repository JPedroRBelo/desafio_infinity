# Desafio Infinity 

Neste repositório é implementado o desafio proposto em [doc/readme.md](doc/readme.md). Detalhes de entrada e padrões de imagens podem ser acessados no referido documento. Contudo, algumas informações poderão ser ressaltadas aqui para tornar o fluxo de descrição da resolução do desafio mais lógico e fluido, bem como destacar alguns pontos chave.

## Sobre o código

O código realiza a leitura de parâmetros de configuração, os quais indicam as imagens que serão comparadas e qual o valor limiar (*threshold*) para indicar se os produtos (representados nas imagens) são os mesmos ou não.

De forma resumida, o *script* principal apresenta no terminal a distância entre as imagens e se elas podem ser consideradas o mesmo produto. Além disso, é salvo em disco, um arquivo JPG com resultado da concatenação entre as imagens A e B em escala de cinza.

De forma detalhada, o código segue a seguinte estrutura:

1. Abre YAML
2. Valida e carrega dados do YAML
3. Abre imagens com os produtos a serem comparados
4. Pré-processa imagens:
    - Converte para escala de cinza
    - Redimensiona para 256x256 pixels 
5. Calcula histogramas das imagens
6. Calcula distância angular (cosseno) dos histogramas gerados
7. Verifica se distância é menor que o limiar (*threshold*) informado no YAML e apresenta informações:
    - distância;
    - informação se são o mesmo produto, dado o limiar
8. Concatena imagens pré-processadas e salva em disco.

Para verificar se as imagens representam o mesmo produto ou não é utilizada a seguinte lógica: 
- Se a distância é menor que o limiar, então os produtos são iguais;
- Caso contrário, os produtos são diferentes.


## Dependências

Para o projeto, foi utilizado o Python 3.12.4, com auxílio de ambiente virtual para instalação de dependências. As principais dependências são:

- numpy
- opencv-python
- scipy
- pydantic

Estas dependências podem ser instaladas a partir do comando abaixo:

```bash 
pip install -r requirements.txt
```

## Como utilizar o código

O repositório conta com arquivos YAML de exemplos de configuração para execução do *script* principal ([solution.py](solution.py)). Nestes arquivos são indicados as imagens a serem comparadas, o limiar de segregação e o caminho para salvar imagens concatenadas. Estes exemplos estão na pasta [examples](examples/).

Na pasta [products](products/) há também diversos exemplos de imagens que podem ser instanciadas no arquivo YAML de configuração. Para executar o *script* principal basta, por exemplo, executar o seguinte comando:

```bash
python solution.py examples/examples_1.yaml
```

Se, por algum acaso, os parâmetros (tanto de execução, quanto do arquivo YAML) estiverem incorretos, o *script* identifica tais inconsistências. Há também verificações em caso de algum arquivo não possa ser carregado.


