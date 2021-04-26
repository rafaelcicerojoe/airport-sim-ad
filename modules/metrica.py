

class Metricas:
    
  def avioes_por_hora():
          return (tempo_dif[0]+ tempo_dif[1])/2

  def get_iterable(iter):
          j = 0
          for i in iter:
            j+=1
          return j
  def tempo_medio(t_max,t_min,n_fuel,n_avioes):
          n_non_fuel = n_avioes - n_fuel
          return round(((n_fuel*t_max)+(n_non_fuel*t_min))/n_avioes,2)
  def avioes_por_hora(tempo):
          return round((60/tempo),2)