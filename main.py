# -*- coding: utf-8 -*-
import random
import simpy
import math
from modules.relatorio import Relatorio
from modules.metrica import Metricas as metrica

parametros = {
    'QTD_PISTA': 6,
    'QTD_DESEMBARQUE': 6,
    'QTD_POSTO': 2, 
    'TEMPO_POUSO': 5,  # em minutos
    'TEMPO_DESEMBARQUE': 20,  # em minutos
    'TEMPO_ABASTECIMENTO': 20,  # em minutos
    'TEMPO_ENTRE_AVIOES': [2, 5],  # em minutos
}
abastecidos = []
total_avioes = []
tempo_por_aviao = []

def criar_aviao(id, env, pista, desembarque, posto, abastecidos,relatorio,tempo_por_aviao):
    vai_abastecer = (random.randint(0, 1) < 0.3)
    with pista.request() as req:
        relatorio.addLog('O avião %d iniciou o pouso' % id)
        yield req

        yield env.timeout(parametros['TEMPO_POUSO'])
        relatorio.addLog('O avião %d pousou' % id)
        cron_ini = env.now

    with desembarque.request() as req:
        yield req

        relatorio.addLog('O avião %d iniciou o desembarque' % id)

        yield env.timeout(parametros['TEMPO_DESEMBARQUE'])
        relatorio.addLog('O avião %d desembarcou' % id)

    if(vai_abastecer):
        with posto.request() as req:
            yield req

            relatorio.addLog('O avião %d iniciou o abastecimento' % id)

            yield env.timeout(parametros['TEMPO_ABASTECIMENTO'])
            abastecidos.append(1)
            relatorio.addLog('O avião %d abasteceu' % id)
    cron_fim = env.now - cron_ini
    tempo_por_aviao.append(cron_fim)
    relatorio.addLog('O avião %d ficou um tempo de %d minutos' % (id,cron_fim))

def aeroporto(env, pista, desembarque, posto, abastecidos,relatorio,total_avioes,tempo_por_aviao):
    id = 1
    total_avioes.append(id)    
    while True:
        yield env.process(criar_aviao(id, env, pista, desembarque, posto, abastecidos,relatorio,tempo_por_aviao))
        yield env.timeout(random.randint(*parametros['TEMPO_ENTRE_AVIOES']))
        id += 1
        total_avioes.append(id)

def main():
    random.seed(58)
    relatorio = Relatorio(parametros)
    env = simpy.Environment()
    pista = simpy.Resource(env, parametros['QTD_PISTA'])
    desembarque = simpy.Resource(env, parametros['QTD_DESEMBARQUE'])
    posto = simpy.Resource(env, parametros['QTD_POSTO'])
    env.process(aeroporto(env, pista, desembarque, posto,abastecidos,relatorio,total_avioes,tempo_por_aviao))
    env.run(until=1440)
    
    n_abastecidos = metrica.get_iterable(abastecidos)
    n_avioes = max(total_avioes)
    tempo_max = max(tempo_por_aviao)
    tempo_min = min(tempo_por_aviao)
    tempo_med = int(metrica.tempo_medio(tempo_max,tempo_min,n_abastecidos,n_avioes))
    per_hora = metrica.avioes_por_hora(tempo_med)
    
    relatorio.addMetrica('Quantidade de aviões atendidos',n_avioes)
    relatorio.addMetrica('Tempo Máximo(em minutos)',tempo_max)
    relatorio.addMetrica('Tempo Mínimo(em minutos)',tempo_min)
    relatorio.addMetrica('Tempo Médio(em minutos)', tempo_med)
    relatorio.addMetrica('Voos por Hora', per_hora)
    relatorio.close()


if __name__ == '__main__':
    main()
