import pandas as pd
import yfinance as yfin
import numpy as np
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

from dwave.system import DWaveSampler, EmbeddingComposite

yfin.pdr_override()


def covar(list_A, mean_A, list_B, mean_B):
  sum = 0
  i=0
  lenght=len(list_A)

  while(i<lenght):
    sum+=(list_A[i]-mean_A)*(list_B[i]-mean_B)
    i+=1

  return sum/lenght

def setup(n_stocks, data_inicial, data_final, codes, maxiter):

  #essas são as duas datas mencionadas no princípio deste documento.
  #data_inicial = input('insert the start data, as "yyyy-mm-dd": ')
  #data_final = input('insert the ending data, as "yyyy-mm-dd": ')

  #para cada ação, o laço repetirá, processando resultando sempre em uma média, um desvio padrão e um vetor de erros percentuais consecutivos
  #estes, por sua vez, serão adicionados em ordem nos vetores globais correspondentes

  gain = []
  volatility = []
  stocks_registry = []

  i=0
  while(i<n_stocks):

    #o primeiro dos vetores abaixo recebe os dados de fechamento brutos da ação.
    #o vetor stocks-_gain[], por sua vez, armazena temporariamente os erros percentuais consecutivos calculados, para então
    #adicioná-los à matriz stocks_registry[] e ainda facilitr os cálculos de média e desvio padrão

    stocks_raw = []
    stocks_gain = []

    #Observation: apparently, if i append a global list inside another global list, any alterations made to the former will be DINAMICALLY
    #updated in the latter too search for that later. seems like quite the phantasmagorical behaviour

    #stocks = input('insert the stock code: ')
    stocks = codes[i]
    history = pdr.DataReader(stocks, data_inicial, data_final)#recupera os dados do banco de dados do Yahoo Finance

    stocks_raw = history['Close'].tolist()#retira somente a coluna de dados de fechamento do dataframe recebido
    print(codes[i])
    print(len(stocks_raw))



    #o laço while abaixo calcula os erros percentuais consecutivos
    j=1
    while(j<len(stocks_raw)):
      stocks_gain.append(((stocks_raw[j]-stocks_raw[j-1])/stocks_raw[j-1]))
      j+=1
    stocks_registry.append(stocks_gain)#adiciona os erros percentuais, em porcentagem, à matriz global

    #a média é calculada em seguida
    sum = 0
    for a in stocks_gain:
      sum += a
    mean = sum/len(stocks_gain)

    #ALTERACAO PARA TORNAR MEDIA MENSAL!!!
    mean_monthly = 0
    if mean>0:
      mean_monthly = np.power(mean+1,21)-1
    elif mean < 0:
      mean_monthly = np.power(mean-1,21)+1#o exp eh impar, portanto n ha problema no sinal da potencia - permanece negativo
    gain.append(mean_monthly)

    #cálculo do desvio padrão. Preferiu-se fazê-lo a fim de reduzir o número de raízes calculadas, uma vez que
    #computacionalmente falando, cálculo de potências é mais performático
    sd = 0
    j=0
    while(j<len(stocks_gain)):
      sd += ((mean-stocks_gain[j])*(mean-stocks_gain[j]))
      j += 1
    #ALTERACAO PARA TORNAR VOLATILIDADE MENSAL!!!
    sd = np.sqrt(sd*21/len(stocks_gain))
    volatility.append(sd)

    i+=1


  risks = []
  i=0
  while(i<len(volatility)):
    j=0
    row = []

    while(j<len(volatility)):
      if(i==j):
        variat = volatility[i]*volatility[i]
        row.append(variat)

      else:
        covariat = covar(stocks_registry[i],gain[i],stocks_registry[j],gain[j])
        row.append(covariat)

      j+=1


    risks.append(row)
    i+=1

  return [n_stocks, codes, gain, volatility, risks]

  #start = time.time()
  #call =  markowitz(n_stocks, codes, gain, volatility, risks)
  #end = time.time()
  #print("Markowitz def average consumed time")
  #print(end-start)

def input_data():
  #stocks = ['petr4.sa', 'vale3.sa', 'brkm5.sa','posi3.sa', 'anim3.sa','lren3.sa','klbn4.sa','sanb11.sa','itub4.sa','mglu3.sa','csna3.sa']
  stocks = ['petr4.sa', 'vale3.sa', 'brkm5.sa']

  n_stocks = len(stocks)

  maxiter = 1000
  #0 to n
  #priority_init = [10,9,8,7,6,5,4,3,2,1,0]


  #proportions among weights
  #proportions = [1]*n_stocks
  print(n_stocks)


  data_final  = "2023-07-28"
  data_inicial = "2023-07-01"


  data_aux_arr = setup(n_stocks, data_inicial, data_final, stocks, maxiter)
  return data_aux_arr

def solve_QUBO(linear_vars, quadratic_vars):
  sampler = EmbeddingComposite(DWaveSampler())

  Q = {**linear_vars, **quadratic_vars} 
  #note to myself: here we use **kwargs to pass all keywords into new dictio Q
  sampleset = sampler.sample_qubo(Q, num_reads = 200)

  print(sampleset)
  print(sampleset.lowest())

def build_QUBO(data_aux_arr):

  n_stocks = data_aux_arr[0]
  gain = data_aux_arr[2]
  volatility = data_aux_arr[3]
  risks = data_aux_arr[4]

  #print("risks ")
  #print(risks)

  linear_vars = {}
  quadratic_vars = {}

  column = 0
  while column < n_stocks:
    row = column
    while row < n_stocks:
      if row == column:
        dic_key = "x" + str(row)
        linear_vars[(dic_key, dic_key)] = risks[column][row]
      else:
        quadratic_vars[("x" + str(row), "x" + str(column))] = 2*risks[column][row]
      #print(f"[{i},{j}]")
      row += 1
    column += 1
  
  #print("linear_vars")
  #print(linear_vars)
  #print("quadratic_vars")
  #print(quadratic_vars)

  solve_QUBO(linear_vars, quadratic_vars)


build_QUBO(input_data())

