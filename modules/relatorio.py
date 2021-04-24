import os
from datetime import datetime


class Relatorio:
    def __init__(self, parametros):
        os.makedirs('relatorios', exist_ok=True)
        self.now = datetime.now()

        self.arquivo = open("relatorios/relatorio_%s.md" % self.now.strftime(
            "%d%m%Y%H%M%S"), "w", encoding="utf-8")
        self.parametros = parametros
        self.setHeader()

    def setHeader(self):
        print('# Relatório - Simulação - Aeroporto', file=self.arquivo)
        print('Gerado em: %s' % self.now.strftime(
            "%d/%m/%Y às %H:%M:%S"), file=self.arquivo)
        print('## Parâmetros', file=self.arquivo)
        print(' - Quantidade de pistas de pouso: %d' %
              self.parametros['QTD_PISTA'], file=self.arquivo)
        print(' - Quantidade de pistas de desembarque: %d' %
              self.parametros['QTD_DESEMBARQUE'], file=self.arquivo)
        print(' - Quantidade de pistas de abastecimento: %d' %
              self.parametros['QTD_POSTO'], file=self.arquivo)
        print(' - Tempo para pouso: %d minutos' %
              self.parametros['TEMPO_POUSO'], file=self.arquivo)
        print(' - Tempo para desembarque: %d minutos' %
              self.parametros['TEMPO_DESEMBARQUE'], file=self.arquivo)
        print(' - Tempo para abastecimento: %d minutos' %
              self.parametros['TEMPO_ABASTECIMENTO'], file=self.arquivo)
        print(' - Tempo entre aviões: entre %d a %d minutos' %
              (self.parametros['TEMPO_ENTRE_AVIOES'][0], self.parametros['TEMPO_ENTRE_AVIOES'][1]), file=self.arquivo)
        print('------', file=self.arquivo)

    def close(self):
        self.arquivo.close()
