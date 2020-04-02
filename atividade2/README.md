# Exercício 1

### 1. Adicione outro Peixe e um Hamster com nome Frodo

```javascript
db.pets.insert({name: "Frodo", species: "Peixe"})
```

```javascript
db.pets.insert({name: "Frodo", species: "Hamster"})
```

### 2. Faça uma contagem dos pets na coleção

```javascript
db.pets.find().count()
```

### 3. Retorne apenas um elemento o método prático possível

```javascript
db.findOne()
```

### 4. Identifique o ID para o Gato Kilha.

```javascript
db.pets.findOne({name: 'Kilha', {_id: 1}})
```

### 5. Faça uma busca pelo ID e traga o Hamster Mike

```javascript
db.pets.findOne({_id: ObjectId('<id hamster mike>'))
```

### 6. Use o find para trazer todos os Hamsters

```javascript
db.pets.find({species: "Hamster"})
```


### 7. Use o find para listar todos os pets com nome Mike

```javascript
db.pets.find({name: "Mike"})
```

### 8. Liste apenas o documento que é um Cachorro chamado Mike

```javascript
db.pets.find({name: "Mike", species: "Cachorro"})
```

# Exercício 2

### 1.Liste/Conte todas as pessoas que tem exatamente 99 anos. Você pode usar um count para indicar a quantidade.

```javascript
db.italians.find({age: 99}).count()
```

### 2. Identifique quantas pessoas são elegíveis atendimento prioritário (pessoas com mais de 65 anos)

```javascript
db.italians.find({age: {$gt: 65}})
``` 

### 3. Identifique todos os jovens (pessoas entre 12 a 18 anos).

```javascript
db.italians.find({age: {$gte: 12, $lte: 18}})
```

### 4. Identifique quantas pessoas tem gatos, quantas tem cachorro e quantas não tem nenhum dos dois

```javascript
db.italians.find({cat: {$exists: 1}}).count()
```

```javascript
db.italians.find({dog: {$exists: 1}}).count()
```

```javascript
db.italians.find({dog: {$exists: 0}, cat: {$exists: 0}}).count()
```

### 5. Liste/Conte todas as pessoas acima de 60 anos que tenham gato

```javascript
db.italians.find({cat: {$exists: 1}, age: {$gt: 65}}).count()
```

### 6. Liste/Conte todos os jovens com cachorro

```javascript
db.italians.find({dog: {$exists: 1}, age: {$lte: 18}}).count()
```

### 7. Utilizando o $where, liste todas as pessoas que tem gato e cachorro

```javascript
db.italians.find({
    $where: function() {
        return (typeof this.cat !== 'undefined') || (typeof this.dog !== 'undefined')
    }
})
```

### 8. Liste todas as pessoas mais novas que seus respectivos gatos.

```javascript
db.italians.find({cat: {$exists: 1}, age: {$lt: 18}}, {_id: 0, firstname: 1, cat: 1})
```

### 9. Liste as pessoas que tem o mesmo nome que seu bichano (gatou ou cachorro)

```javascript
db.italians.find({
    dog: {$exists: 1},
    cat: {$exists: 1},
    $where: function() {
        return this.dog ? this.dog.name === this.firstname || this.cat.name === this.firstname
        }
    }).count()
```

### 10. Projete apenas o nome e sobrenome das pessoas com tipo de sangue de fator RH negativo

```javascript
db.italians.find({$where: function {
    return this.bloodType.endsWith('-')
}, {firstname: 1, surname: 1, _id: 0}})
```

### 11. Projete apenas os animais dos italianos. Devem ser listados os animais com nome e idade. Não mostre o identificado do mongo (ObjectId)

```javascript
db.italians.find({$or: [{cat: {$exists: 1}}, {dog: {$exists: 1}}]}, {cat: 1, dog: 1, _id: 0})
```

### 12. Quais são as 5 pessoas mais velhas com sobrenome Rossi?

```javascript
db.italians.find({surname: 'Rossi'}).sort({age: -1}).limit(5)
```

### 13. Crie um italiano que tenha um leão como animal de estimação. Associe um nome e idade ao bichano

```javascript
db.italians.insert({name: "Mario", lion: {name: "yoshi", age: 5}})
```

### 14. Infelizmente o Leão comeu o italiano. Remova essa pessoa usando o Id.

```javascript
db.italians.findOne({name: "Mario", lion: {$exists: 1}})

db.italians.remove({_id: ObjectId(<id do mario>)})
```

### 15. Passou um ano. Atualize a idade de todos os italianos e dos bichanos em 1.

```javascript
    db.italians.update({age: {$exists: 1}}, {$inc: {age: 1}}, {multi: 1})
    db.italians.update({dog: {$exists: 1}}, {$inc: {"dog.age": 1}}, {multi: 1})
    db.italians.update({cat: {$exists: 1}}, {$inc: {"cat.age": 1}}, {multi: 1})
```


### 16. O Corona Vírus chegou na Itália e misteriosamente atingiu pessoas somente com gatos e de 66 anos. Remova esses italianos.


```javascript
    db.italians.remove({age: {$eq: 66}, cat: {$exists: 1}})
```

### 17. Utilizando o framework agregate, liste apenas as pessoas com nomes iguais a sua respectiva mãe e que tenha gato ou cachorro.

```javasrcript
db.italians.aggregate([
    {'$match':
        {father: {$exists: 1}, $or: [{cat: {$exists:1}}, {dog: {$exists: 1}}]}]
    },
    {$project:
        {firstname: 1, mother: 1, isEqual: {$cmp: ["$firstname", "$mother.firstname"]}}
    },
    {$match: {isEqual: 0}}])
```

### 18. Utilizando aggregate framework, faça uma lista de nomes única de nomes. Faça isso usando apenas o primeiro nome

```javascript
 db.italians.distinct('firstname')

 db.italians.aggregate([{$group: {_id:0, ItalianFirstName: {$addToSet: "$firstname"}}}])
 ```


### 19. Agora faça a mesma lista do item acima, considerando nome completo.

```javascript
 db.italians.aggregate([
     { $project: { fullName: { $concat: [ "$firstname", " ", "$surname" ] } } },
     {$group: {_id:0, ItalianFullName: {$addToSet: "$fullName"}}}])
```

### 20. Procure pessoas que gosta de Banana ou Maçã, tenham cachorro ou gato, mais de 20 e menos de 60 anos.
 
 ```javascript
 db.italians.find({favFruits: {$elemMatch: {$in: ["Banana", "Maçã"]}}, $or: [{dog: {$exists: 1}}, {cat: {$exists: 1}}], age: {$gt: 20, $lt: 60}})

 ```

# Exercício 3


### 1. Liste as ações com profit acima de 0.5 (limite a 10 o resultado)

```javascript
db.stocks.find({"Profit Margin": {$gt: 0.5}}).limit(10)
```

### 2. Liste as ações com perdas (limite a 10 novamente)
```javascript
db.stocks.find({"Performance (Year)": {$lt: 0}}).sort({"Performance (Month)": -1}).limit(10)
```

### 3. Liste as 10 ações mais rentáveis

```javascript
db.stocks.find().sort({"Profit Margin": 1).limit(10)
```

### 4. Qual foi o setor mais rentável?
```javascript
db.stocks.aggregate([{$group: { _id: {"Sector": "$Sector"}, totalAmount: {$sum: "$Profit Margin"}}}])
```

### 5. Ordene as ações pelo profit e usando um cursor, liste as ações.
´´´javascript
var cursor = db.stocks.find()
var array = cursor.toArray().sort(function(a, b) {return a['Profit Margin'] - b['Profit Margin']})
´´´

### 6. Renomeie o campo “Profit Margin” para apenas “profit”.

```javascript
db.stocks.updateMany({}, {$rename: {"Profit Margin": "profit"}})
```

### 7. Agora liste apenas a empresa e seu respectivo resultado

```javascript
db.stocks.find({}, {'Company': 1, 'Price': 1, _id: 0})
```

### 8. Analise as ações. É uma bola de cristal na sua mão... Quais as três ações você investiria?

```javascript
db.stocks.aggregate([{ $sample: { size: 3 } }])
```

### 9. Liste as ações agrupadas por setor

```javascript
db.stocks.aggregate([{$group: { _id: {"Sector": "$Sector"}}}])
```

# Exercício 4

### 1. Liste as pessoas que enviaram e-mails (de forma distinta, ou seja, sem repetir). Quantas pessoas são?

```javascript
db.stocks.distinct('sender').length
```

### 2. Contabilize quantos e-mails tem a palavra “fraud”

``` javascript
db.stocks.createIndex( { "text": "text" } )
db.stocks.find( { $text: { $search: "fraud" } } ).count()
```

