# Exercício 1

## 1. Crie a tabela com 2 famílias de colunas:
```
create 'italians', 'personal-data', 'professional-data'
```

```
hbase shell /tmp/italians.txt
```

## 2. Importe o arquivo via linha de comando, e agora execute as seguintes operações:

### 1. Adicione mais 2 italianos mantendo adicionando informações como data de nascimento nas informações pessoais e um atributo de anos de experiência nas informações profissionais;

```
put 'italians', '9999', 'personal-data:name',  'Rosana Madonati'
put 'italians', '9999', 'personal-data:city',  'Palermo'
put 'italians', '9999', 'personal-data:birthdate',  '10-01-1970'
put 'italians', '9999', 'professional-data:role',  'Programadora'
put 'italians', '9999', 'professional-data:salary',  '5200'
put 'italians', '9999', 'professional-data:experience',  '30'


put 'italians', '9998', 'personal-data:name',  'Marco Popopatati'
put 'italians', '9998', 'personal-data:city',  'Palermo'
put 'italians', '9998', 'personal-data:birthdate',  '10-01-1974'
put 'italians', '9998', 'professional-data:role',  'Programador'
put 'italians', '9998', 'professional-data:salary',  '5200'
put 'italians', '9998', 'professional-data:experience',  '28'
```


### 2. Adicione o controle de 5 versões na tabela de dados pessoais.

```
    alter 'italians', NAME => 'personal-data', VERSIONS => 5
```


### 3. Faça 5 alterações em um dos italianos;

```
put 'italians', '9999', 'personal-data:city', 'cidade1'                                                             
put 'italians', '9999', 'personal-data:city', 'cidade2'      
put 'italians', '9999', 'personal-data:city', 'cidade3'      
put 'italians', '9999', 'personal-data:city', 'cidade4'                                                             
put 'italians', '9999', 'personal-data:city', 'cidade5'

```

### 4. Com o operador get, verifique como o HBase armazenou o histórico.

```
hbase(main):017:0> get 'italians', '9999'
COLUMN                CELL                                                      
 personal-data:birthd timestamp=1585929874106, value=10-01-1970                 
 ate                                                                            
 personal-data:city   timestamp=1585930910187, value=cidade5                    
 personal-data:name   timestamp=1585929849452, value=Rosana Madonati            
 professional-data:ex timestamp=1585929896007, value=30                         
 perience                                                                       
 professional-data:ro timestamp=1585929880677, value=Programadora               
 le                                                                             
 professional-data:sa timestamp=1585929885845, value=5200                       
 lary                                                                           
1 row(s)
Took 0.0207 seconds 
```

### 5. Utilize o scan para mostrar apenas o nome e profissão dos italianos.

```
scan 'italians', {COLUMNS => ['personal-data:name', 'professional-data:role']}
```

### 6. Apague um italiano com row id ímpar
```
delete 'italians', '1'
```

### 7. Crie um contador de idade 55 para o italiano de row id 5

```
incr 'italians', '5', 'personal-data:age', 55
```

### 8. Incremente a idade do italiano em 1
```
incr 'italians', '5', 'personal-data:age', 1
```