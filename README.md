___
**<h1>Modulo JsonManager</h1>**  
___  

**OBS:** Esse módulo **NÃO** é indicado para armazenar uma grande quantidade
de dados, ele foi criado com a intenção de facilitar a utilização
de arquivos JSON

**<h2>Criando objetos `JsonArq`:</h2>**

Ao criar um objeto do tipo `JsonArq`, deve-se passar uma string
com o caminho de um arquivo json **existente ou não**.

- Caso o caminho seja inválido, será gerado um erro
- Caso o arquivo não exista, ele será criado ao criar
o objeto

O parametro `overwrite_if_exists` por padrão tem seu valor
como `False`. Desse modo o objeto importa os dados salvos
no arquivo json para ele, caso seja definido como `True`
se o arquivo json já existir ele será sobrescrito.

<br/>

<h3>**exemplo:**</h3>

> **pessoas.json**
> ``` json
> {"nome": "Gabriel Paschoal"}
> ```
---
> ``` python
> j_arq = JsonArq('.\\Pessoas.json')
> print(j_arq)
> ```
>     > {'nome': 'Gabriel Paschoal'}

> ``` python
> j_arq = JsonArq('.\\Pessoas.json', overwrite_if_exists=True)
> print(j_arq)
> ```
>     > {}
<br/>
Após a criação do objeto, ele pode ser tratado como um dicionário e possui suas principais funções.
<br/>

<h3>**exemplo:**</h3>
> ``` python
> j_arq = JsonArq('.\\Pessoas.json', overwrite_if_exists=True)
---
> ``` python
> j_arq['nome'] = 'Gabriel Paschoal'
> print(j_arq)
> ```
>     > {'nome': 'Gabriel Paschoal'}

> ``` python
> j_arq.update({
>   'idade': 21,
>   'cpf': '12323434551',
>   'nacionalidade': 'brasileiro'
> })
> 
> print(j_arq)
> ```
>     > {'nome': 'Gabriel Paschoal', 'idade': 21, 'cpf': '12323434551', 'nacionalidade': 'brasileiro'}

> ``` python
> del j_arq['cpf']
> print(j_arq)
> ```
>     > {'nome': 'Gabriel Paschoal', 'idade': 21, 'nacionalidade': 'brasileiro'}

> ``` python
> value = j_arq['idade']
> print(value)
> ```
>     > 21
<br/>

**<h2>Função `save`:</h2>**  

Essa função salva todas as alterações feitas no arquivo json.


> **Exemplo:** 
> ``` python
> j_arq = JsonArq('.\\pessoas.json', overwrite_if_exists=True)
> j_arq.update({
>   'nome': 'Gabriel Paschoal',
>   'idade': 21
> })
> j_arq.save()
> ```
---
> **pessoas.json**
> ``` json
> {"nome": "Gabriel Paschoal", "idade": 21}
> ```

**<h2>Atributo `auto_save`:</h2>**  

Esse atributo por padrão possui o valor `False`,
caso seja alterado para `True` todas as alterações
realizadas serão salvas instantaneamente.

- Essa função tende a ser pouco custosa, podendo
deixar o programa mais lento
> **Exemplo:** 
> ``` python
> j_arq = JsonArq('.\\pessoas.json', overwrite_if_exists=True)
> j_arq.auto_save = True
> j_arq.update({
>   'nome': 'Gabriel Paschoal',
>   'idade': 21
> })
> ```
---
> **pessoas.json**
> ``` json
> {"nome": "Gabriel Paschoal", "idade": 21}
> ```

**<h3>OBS:</h3>**
o `auto_save` pode ser passado como parametro na criação
do objeto

> **Exemplo:** 
> ``` python
> j_arq = JsonArq('.\\pessoas.json', overwrite_if_exists=True, auto_save=True)
> j_arq.update({
>   'nome': 'Gabriel Paschoal',
>   'idade': 21
> })
> ```
---
> **pessoas.json**
> ``` json
> {"nome": "Gabriel Paschoal", "idade": 21}
> ```

