#normalizar artigo - modelo iniciação científica
#search engine utilizando heap merge sort
#review matriz de variança e covariança - check
#analisar algoritmo quant no repo quantum lab
#comparação desempenho quant x classic


import pandas as pd
import pandas_bokeh
import yfinance as yfin
import numpy as np
from pandas_datareader import data as pdr
from tkinter import * 
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from multiprocessing import Process
import multiprocessing
 
yfin.pdr_override()

#quatro vetores globais são criados.

#stocks_registry[] serve para conter cada desvio percentual consecutivo dos históricos, ao que este se torna uma matriz ao final do processo.
#gain[] armazena as médias dos desvios percentuais de cada ação.
#volatility[] armazena o desvio padrão dos desvios percentuais de cada ação.
#risks[] se tornará a matriz de risco, após armazenar variânça e covariânça entre cada ação

stocks_registry = []
gain = []
volatility = []
risks = []

#a função setup alimenta os quatro vetores globais, a fim de preparar os principais dados necessários para alimentar a função markowitz()

def setup(n_stocks, data_inicial, data_final, codes, data_shared):

  #essas são as duas datas mencionadas no princípio deste documento.
  #data_inicial = input('insert the start data, as "yyyy-mm-dd": ')
  #data_final = input('insert the ending data, as "yyyy-mm-dd": ')

  #para cada ação, o laço repetirá, processando resultando sempre em uma média, um desvio padrão e um vetor de erros percentuais consecutivos
  #estes, por sua vez, serão adicionados em ordem nos vetores globais correspondentes 
  
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
    
    #o laço while abaixo calcula os erros percentuais consecutivos
    j=1
    while(j<len(stocks_raw)):
      stocks_gain.append(((stocks_raw[j]-stocks_raw[j-1])/stocks_raw[j-1])*100)
      j+=1
    stocks_registry.append(stocks_gain)#adiciona os erros percentuais, em porcentagem, à matriz global

    #a média é calculada em seguida
    sum = 0
    for a in stocks_gain:
      sum += a
    gain.append(sum/len(stocks_gain))
    
    #cálculo do desvio padrão. Preferiu-se fazê-lo a fim de reduzir o número de raízes calculadas, uma vez que
    #computacionalmente falando, cálculo de potências é mais performático
    sd = 0
    j=0
    while(j<len(stocks_gain)):
      sd += ((a-stocks_gain[j])*(a-stocks_gain[j]))
      j += 1
    sd = np.sqrt(sd/len(stocks_gain))  
    volatility.append(sd)

    i+=1

  print(stocks_registry)
  print("====================================================")
  print(gain)
  print("====================================================")
  print(volatility)
  print("====================================================")

  
  
  #construção da matriz de risco
  i=0
  while(i<len(volatility)):
    j=0
    row = []

    while(j<len(volatility)):
      if(i==j):
        row.append(volatility[i]*volatility[i])
        
      else:
        row.append(covar(stocks_registry[i],gain[i],stocks_registry[j],gain[j]))
      j+=1

    risks.append(row)
    i+=1

  
  print(risks)
  print()
  print("Matriz de risco:")
  print()

  plt.imshow(risks, interpolation='nearest')
  plt.colorbar()
  plt.show()

  markowitz(n_stocks,data_shared)
    
  
#função responsável por calcular a covariâça, dado os erros percentuais consecutivos e a média de duas ações
def covar(list_A, mean_A, list_B, mean_B):
  sum = 0
  i=0
  lenght=len(list_A)

  while(i<lenght):
    sum+=(list_A[i]-mean_A)*(list_B[i]-mean_B)
    i+=1
    
  return sum/lenght  

def merge_sort(arr, left, right):
  #right é o último índice do vetor a ser dividido/sortido; left é o primeiro
  
  print("array")
  print(arr)
  print("right:")
  print(right)
  print("left:")
  print(left)
  if(left<right) :

    print("tested")
    mid = (left+right)//2
    print("mid")
    print(mid)
    #o meio é arredondado para baixo

    n1 = []#em linguagens estáticas, o tamanho desse vetor temporário será dado por mid - left + 1
    n2 = []#no mesmo caso, o tamanho seria definido por right - mid

    size_l = mid - left + 1
    size_r = right - mid
    
    #low = arr[mid:]
    i = 0
    while(i<size_l):
      n1.append(arr[i])
      i += 1

    i = 0
    while(i<size_r):
      n2.append(arr[i+mid+1-left])
      i += 1

    print("called left")
    merge_sort(n1, left, mid)
    print("called right")
    merge_sort(n2, mid+1, right)

    i = j = k = 0
    
    print(n1)
    print(n2)
    print(mid+1)
    print(right+1)

    while i < size_l and j < size_r:
      print(i)
      print(j)
      if n1[i] <= n2[j]:
        arr[k] = n1[i]
        print("n1 menor n2")
        print(n1[i])
        print(n2[j])
        i += 1
      else:
        arr[k] = n2[j]
        print("n2 menor n1")
        print(n1[i])
        print(n2[j])
        j += 1
      print(k)
      k += 1

    print(arr)

    while i < size_l:
      arr[k] = n1[i]
      i += 1
      k += 1
    
    while j < size_r:
      arr[k] = n2[j]
      j += 1
      k += 1 

  #right é o último índice do vetor a ser dividido/sortido; left é o primeiro
  
  if((right+1)<1) :

    mid = (right-left+1)//2
    #o meio é arredondado para baixo

    n1 = []#em linguagens estáticas, o tamanho desse vetor temporário será dado por mid - left + 1
    n2 = []#no mesmo caso, o tamanho seria definido por right - mid

    #low = arr[mid:]
    i = 0
    while(i<=mid):
      n1[i] = arr[i]
      i += 1

    i = mid+1
    while(i<=right):
      n2[i] = arr[i]
      i += 1
    
    merge_sort(n1, left, mid)
    merge_sort(n2, mid+1, right)

    i = j = k = 0

    while i < mid+1 and j < right + 1:
      if n1[i] <= n2[j]:
        arr[k] = n1[i]
        i += 1
      else:
        arr[k] = n2[k]
        j += 1

    while i < mid+1:
      arr[k] = n1[i]
      i += 1
      k += 1
    
    while j < right+1:
      arr[k] = n2[i]
      i += 1
      k += 1

def markowitz(n_stocks,data_shared):

  #número de portfolios a ser calculado; definido arbitrariamente
  iterations = 30000

  #vetor contendo retorno total de cada portfolio calculado
  return_total = []

  #vetor contendo risco total de cada portfolio calculado
  global risk_total
  risk_total = []

  weight_matrix = []

  #define um dicionário contendo todos os dados
  data = {'Retorno': return_total, 'Risco': risk_total}

  iter = 0
  while(iter<iterations):
    #vetor para conter os pesos gerados
    weights = []

    #primeiro peso é gerado em um conjunto x e ]0,1]
    weights.append(np.random.uniform(low=0.01, high=1.0, size=(1,))[0])
    
    #subtrai o valor do primeiro peso da pool restante
    percentage_aux = 1.0

    #gera cada peso entre 1 e n_stocks-1
    i=1
    while(i<(n_stocks-1)):
      percentage_aux -= weights[i-1]
      weights.append(np.random.uniform(low=0.01, high=(percentage_aux), size=(1,))[0])
      
      i += 1

    #o último peso não deve ser gerado, bastando calcular o restante da porcentagem (a carteira do portfolio sempre gera com 100%)
    weights.append(percentage_aux-weights[i-1])

    #soma todos os termos que consistem de variança*peso^2
    i = 0
    sum_a = 0
    while(i<n_stocks):
      sum_a += weights[i]*weights[i]*volatility[i]*volatility[i]
      i += 1

    #produtorio dos pesos para facilitar na iteração seguinte
    productory_weights = 1
    for a in weights:
      productory_weights *= a
    
    #soma todos os termos que consistem de 2*produtorio(peso)*covar
    i = 0
    sum_b = 0
    while(i<n_stocks):
      #o iterador j é feito dessa forma a fim de retirar somente as covarianças da matriz de risco, sem percorrer o mesmo valor novamente
      j=i+1
      while(j<n_stocks):
        sum_b += 2*productory_weights*risks[i][j]
        j += 1
      i += 1

    risk_total.append(sum_a + sum_b)

    i = 0
    sum = 0
    while(i<n_stocks):
      sum += gain[i]*weights[i]
      i += 1

    return_total.append(sum)

    weight_matrix.append(weights)

    iter += 1

  i = 0
  while (i<n_stocks):
    j=0
    weight_column = []

    while(j<iterations):
      weight_column.append(weight_matrix[j][i])
      j += 1

    data["peso: " + str(i+1)] = weight_column

    i += 1
  
  #Insere o dicionario local contendo riscos, ganhos e pesos 
  #no dicionario da memoria compartilhada
  for key in data:
    data_shared[key] = data[key]

  portfolios = pd.DataFrame(data)
  print(data)


  
def plot_markowitz(data_shared):
  print(data_shared)

  data = {}
  for key in data_shared:
    data[key] = data_shared[key]

  portfolios = pd.DataFrame(data) 
  print(portfolios)
  portfolios.plot.scatter(x='Risco', y='Retorno', c='green', marker='o', s=10, alpha=0.15)
  plt.show()

def merge_sort(arr, left, right):
  #right é o último índice do vetor a ser dividido/sortido; left é o primeiro
  
  if(left<right) :

    mid = (left+right)//2
    #o meio é arredondado para baixo

    n1 = []#em linguagens estáticas, o tamanho desse vetor temporário será dado por mid - left + 1
    n2 = []#no mesmo caso, o tamanho seria definido por right - mid

    size_l = mid - left + 1
    size_r = right - mid
    
    #low = arr[mid:]
    i = 0
    while(i<size_l):
      n1.append(arr[i])
      i += 1

    i = 0
    while(i<size_r):
      n2.append(arr[i+mid+1-left])
      i += 1

    merge_sort(n1, left, mid)
    merge_sort(n2, mid+1, right)

    i = j = k = 0

    while i < size_l and j < size_r:
      if n1[i] <= n2[j]:
        arr[k] = n1[i]
        i += 1
      else:
        arr[k] = n2[j]
        j += 1
      print(k)
      k += 1

    while i < size_l:
      arr[k] = n1[i]
      i += 1
      k += 1
    
    while j < size_r:
      arr[k] = n2[j]
      j += 1
      k += 1

def binary_search(arr, left, right, element):

  #a condicao abaixo permitira a execucao da busca, a menos que as entradas sejam invalidas
  #desde a invocacao deste metodo
  print(left)
  print(right)
  print("===================")
  
  while(left<=right):

    #note que os indices sao referentes ao array original, e nao relativos aos segmentos
    #analisados na busca
    mid = left + (right-left)//2

    print(left)
    print(mid)
    print(right)
    print("===================")


    if(arr[mid]==element):
      print("the element is at index:" + str(mid))
      return 0

    elif(arr[mid]<element):
      left = mid+1
      
    else:
      right = mid-1

  print("there is no such element")

def search_gui(data_shared):

  root = Tk()
  frm = ttk.Frame(root, padding=10)
  frm.grid()

  risk_min = Entry(frm,width=30)
  risk_min.grid(row = 0, column = 1)

  risk_max = Entry(frm,width=30)
  risk_max.grid(row = 1, column = 1)


  stocks_label = Label(frm, text="Risco mínimo: ")
  stocks_label.grid(row=0,column=0)

  stocks_label = Label(frm, text="Risco máximo: ")
  stocks_label.grid(row=0,column=0)

  root.mainloop()


def setup_gui(data_shared):
  root = Tk()
  frm = ttk.Frame(root, padding=10)
  frm.grid()

  string_variable = tk.StringVar(frm, "0")
  
  stocks_entry = Entry(frm,width=30,textvariable=string_variable)
  stocks_entry.grid(row=0,column=1)

  start_entry = Entry(frm,width=30)
  start_entry.grid(row=1,column=1)

  end_entry = Entry(frm,width=30)
  end_entry.grid(row=2,column=1)



  stocks_label = Label(frm, text="Numero de ações: ")
  stocks_label.grid(row=0,column=0)

  stocks_label = Label(frm, text="Data de início (formato yyyy-mm-dd): ")
  stocks_label.grid(row=1,column=0)

  stocks_label = Label(frm, text="Data de fechamento (formato yyyy-mm-dd): ")
  stocks_label.grid(row=2,column=0)
  
  def retrieve():
    
    n_stocks = int(stocks_entry.get())
    
    data_inicial = str(start_entry.get())
    data_final = str(end_entry.get())
    root.destroy()
    stocks_gui(n_stocks,data_inicial,data_final,data_shared)
    

  do_it = Button(frm, text="Próximo", command=retrieve)
  do_it.grid(row=3,column=1)

  root.mainloop()

def stocks_gui(n_stocks,data_inicial,data_final,data_shared):

  root = Tk()
  frm = ttk.Frame(root,padding=10)
  frm.grid()

  arr = []

  stocks_label = Label(frm, text="Insira os códigos abaixo")
  stocks_label.grid(row=0,column=0)

  i=0
  while(i<n_stocks):
    stock_code = Entry(frm,width=30)
    stock_code.grid(row=(i+1),column=0)
    arr.append(stock_code)
    i += 1

  def setup_follow():
    codes = []
    i = 0
    while(i<n_stocks):
      codes.append(arr[i].get())
      i += 1
    root.destroy()
    setup(n_stocks,data_inicial,data_final,codes,data_shared) 

  do_it = Button(frm, text="Próximo", command=setup_follow)
  do_it.grid(row=i+1,column=0)

  root.mainloop()

if __name__ == '__main__':

  #data_shared = multiprocessing.Array('d',0)
  manager = multiprocessing.Manager()
  data_shared = manager.dict()

  p0 = Process(target=setup_gui, args=([data_shared]))
  p0.start()  
  p0.join()

  #p_plot = Process(target=plot_markowitz, args=[data_shared])
  #p_plot.start()
  

  p_search = Process(target=search_gui, args=([data_shared]))
  p_search.start()

  plot_markowitz(data_shared)

  #p_plot.join()
  p_search.join()

  #print(data_shared)

  


  #print("{}".format(data_shared[:]))
  
#setup_gui()
