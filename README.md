# Desafio Infinity 

Neste repositório é implementado o desafio proposto em [doc/readme.md](doc/readme.md). Detalhes de entrada e padrões de imagens podem ser acessados no referido documento. Contudo, algumas informações poderão ser ressaltadas aqui para tornar o fluxo de descrição da resolução do desafio mais lógico e fluido, bem como destacar alguns pontos chave.

## Sobre o código

O código realiza a leitura de configuração que indica as imagens que serão comparadas e qual o valor limiar (*threshold*) que determina se os produtos (representados nas imagens) são os mesmos ou não.

De forma simples, o *script* principal apresenta no terminal a distância entre as imagens e se elas podem ser consideradas o mesmo produto. Além disso, o resultado das transformações utilizadas nas imagens, durante o processo de análise, são salvas em disco. Por fim, também é salvo um arquivo JPG com resultado da concatenação entre as imagens A e B em escala de cinza.



## Dependências

- opencv-python
- pydantic

Estas dependências podem ser instaladas a partir do comando abaixo:


```bash 
pip install -r requirements.txt
```

## Como utilizar o código

```bash
python solution.py examples/examples_1.yaml
```
