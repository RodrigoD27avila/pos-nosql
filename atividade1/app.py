import redis

cli = redis.StrictRedis(host='localhost', port=6379, db=0)


# 0- cria a cartela para retirarmos um número randômico para adicionar das cartelas dos usuários
for x in range(99):
    cli.sadd('cartela:master', x)

# 1 - aqui vamos cirar 50 participantes concatenando a string user + número = userXX
for x in range(50):
    # cria o nome, cartela e score id
    username = 'user:{0:02}'.format(x)
    cartela  = 'cartela:{0:02}'.format(x)
    score    = 'score:{0:02}'.format(x)
    cli.hset(username, 'name',     'user{0:02}'.format(x))
    cli.hset(username, 'bcartela', cartela)
    cli.hset(username, 'bscore',   score)

    # 2 - cria a cartela do usuário, retirando um elemento randômico da cartel master
    while True:
        cli.sadd(cartela, int(cli.srandmember('cartela:master')))
        size = cli.scard(cartela)

        # se a cartela estiver formada com os 15 números
        if size >= 15:
            break

    # 3 - cria o score do usuário  
    cli.set(score, 0)

print('HORA do BINGO!!!!')

# 4 hora do bingo
temGanhadores = False
while not temGanhadores:
   # tira um número randômico 
   numero = int(cli.srandmember('cartela:master'))

   #percorre todos os usuarios, checa se se tem o número, atualiza o score e chaca para ver se ganhou
   for x in range(50):
        username = 'user:{0:02}'.format(x)
        name     = cli.hget(username, 'name')
        cartela  = cli.hget(username, 'bcartela')
        score    = cli.hget(username, 'bscore')

        if (cli.sismember(cartela, numero)):
           cli.incr(score)

        if (int(cli.get(score)) >= 15):
            print('BINGO!!!!!! {0} GANHOU!!'.format(name.decode('utf-8')))
            temGanhadores = True


# limpa o redis
cli.flushdb()


