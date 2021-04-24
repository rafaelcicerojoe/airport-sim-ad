# -*- coding: utf-8 -*-
import random
import simpy
from modules.relatorio import Relatorio

parametros = {
    'QTD_PISTA': 1,
    'QTD_DESEMBARQUE': 2,
    'QTD_POSTO': 1,
    'TEMPO_POUSO': 5,  # em minutos
    'TEMPO_DESEMBARQUE': 20,  # em minutos
    'TEMPO_ABASTECIMENTO': 30,  # em minutos
    'TEMPO_ENTRE_AVIOES': [60, 90]  # em minutos
}


def criar_aviao(id, env, pista, desembarque, posto):
    vai_abastecer = (random.randint(0, 1) < 0.3)
    with pista.request() as req:
        print('O avião %d iniciou o pouso' % id)

        yield req

        yield env.timeout(parametros['TEMPO_POUSO'])
        print('O avião %d pousou' % id)
        cron_ini = env.now

    with desembarque.request() as req:
        yield req

        print('O avião %d iniciou o desembarque' % id)

        yield env.timeout(parametros['TEMPO_DESEMBARQUE'])
        print('O avião %d desembarcou' % id)

    if(vai_abastecer):
        with posto.request() as req:
            yield req

            print('O avião %d iniciou o abastecimento' % id)

            yield env.timeout(parametros['TEMPO_ABASTECIMENTO'])
            print('O avião %d abasteceu' % id)
    cron_fim = env.now - cron_ini
    print('O avião %d ficou um tempo de %d minutos' % (id, cron_fim))


def aeroporto(env, pista, desembarque, posto):
    id = 1
    while True:
        env.process(criar_aviao(id, env, pista, desembarque, posto))
        yield env.timeout(random.randint(*parametros['TEMPO_ENTRE_AVIOES']))
        id += 1


def main():
    random.seed(58)
    relatorio = Relatorio(parametros)

    env = simpy.Environment()
    pista = simpy.Resource(env, parametros['QTD_PISTA'])
    desembarque = simpy.Resource(env, parametros['QTD_DESEMBARQUE'])
    posto = simpy.Resource(env, parametros['QTD_POSTO'])
    env.process(aeroporto(env, pista, desembarque, posto))
    env.run(until=1440)

    relatorio.close()


if __name__ == '__main__':
    main()
