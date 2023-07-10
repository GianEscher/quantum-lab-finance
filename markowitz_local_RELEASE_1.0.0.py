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

global n_stocks,data_inicial,data_final, data, codes


#a função setup alimenta os quatro vetores globais, a fim de preparar os principais
# dados necessários para alimentar a função markowitz()
def setup(n_stocks, data_inicial, data_final, codes):

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
  
  #construção da matriz de risco
  risks = []
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

  plt.imshow(risks, interpolation='nearest')
  plt.colorbar()
  plt.show()

  return markowitz(n_stocks, codes, gain, volatility, risks)
    
#função responsável por calcular a covariâça, dado os erros percentuais consecutivos e a média de duas ações
def covar(list_A, mean_A, list_B, mean_B):
  sum = 0
  i=0
  lenght=len(list_A)

  while(i<lenght):
    sum+=(list_A[i]-mean_A)*(list_B[i]-mean_B)
    i+=1
    
  return sum/lenght  


def markowitz(n_stocks, codes, gain, volatility, risks):

  #número de portfolios a ser calculado; definido arbitrariamente
  iterations = 300000

  #vetor contendo retorno total de cada portfolio calculado
  return_total = []

  #vetor contendo risco total de cada portfolio calculado
  global risk_total
  risk_total = []

  weight_matrix = []

  #define um dicionário contendo todos os dados
  global data
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

    data[str(codes[i])] = weight_column

    i += 1
  
  #Insere o dicionario local contendo riscos, ganhos e pesos 
  #no dicionario da memoria compartilhada

  #portfolios = pd.DataFrame(data)
  #print(data)
  return data


def optimize_search(data, arr, min_element, max_element):

  #arr = merge_sort(arr, 0, len(arr)-1)

  min_index = binary_search(arr[0], min_element)
  max_index = binary_search(arr[0], max_element)

  print("min index")
  print(min_index)
  print("max index")
  print(max_index)

  print("risco minimo")
  print(arr[0][min_index])
  print("risco maximo")
  print(arr[0][max_index])
  
  i = min_index
  selected_gain = 0
  selected_index = 0
  #returns = data["Retorno"]
  
  while(i<=max_index):
    current_gain = data["Retorno"][arr[1][i]]
    if current_gain > selected_gain:
      selected_gain = current_gain
      selected_index = arr[1][i]
    i += 1
    
  return [arr, selected_gain, selected_index]
    

def plot_markowitz(data):

  portfolios = pd.DataFrame(data) 
  portfolios.plot.scatter(x='Risco', y='Retorno', c='green', marker='o', s=10, alpha=0.15)
  
  data = pd.DataFrame(data)
  print(data)
  
  plt.show()


def merge_sort(arr, left, right):
  #right é o último índice do vetor a ser dividido/sortido; left é o primeiro
  
  if(left<right) :

    mid = (left+right)//2
    #o meio é arredondado para baixo

    n1 = []#em linguagens estáticas, o tamanho desse vetor temporário será dado por mid - left + 1
    n2 = []#no mesmo caso, o tamanho seria definido por right - mid
    idx1 = []
    idx2 = []

    size_l = mid - left + 1
    size_r = right - mid
    
    #low = arr[mid:]
    i = 0
    while(i<size_l):
      n1.append(arr[0][i])
      idx1.append(arr[1][i])
      i += 1

    i = 0
    while(i<size_r):
      n2.append(arr[0][i+mid+1-left])
      idx2.append(arr[1][i+mid+1-left])
      i += 1

    m1 = []
    m2 = []

    m1.append(n1)
    m1.append(idx1)

    m2.append(n2)
    m2.append(idx2)

    merge_sort(m1, left, mid)
    merge_sort(m2, mid+1, right)

    i = j = k = 0

    while i < size_l and j < size_r:
      if n1[i] <= n2[j]:
        arr[0][k] = n1[i]
        arr[1][k] = idx1[i]
        i += 1
      else:
        arr[0][k] = n2[j]
        arr[1][k] = idx2[j]
        j += 1
      k += 1

    while i < size_l:
      arr[0][k] = n1[i]
      arr[1][k] = idx1[i]
      i += 1
      k += 1
    
    while j < size_r:
      arr[0][k] = n2[j]
      arr[1][k] = idx2[j]
      j += 1
      k += 1

  return(arr)


def binary_search(arr, element):

  left = 0
  right = len(arr)-1

  arr_altered = []
  for num in arr:
    arr_altered.append(num)
  arr_altered.append(element+1)


  #a condicao abaixo permitira a execucao da busca, a menos que as entradas sejam invalidas
  #desde a invocacao deste metodo

  while(left<=right):

      #note que os indices sao referentes ao array original, e nao relativos aos segmentos
      #analisados na busca
    mid = left + (right-left)//2


    if arr[mid-1]<element and arr_altered[mid+1]>element: #arr[mid] == element
      #[1.9,2,2,2,2,2,2,2,2.1]
      print("the element is at index:" + str(mid))
      return mid

    elif(arr[mid]<element):
      left = mid+1
          
    else:
      right = mid-1

  print("there is no such element")
  return 0


def search_gui(data_shared, sorted_risk):

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
  stocks_label.grid(row=1,column=0)


  i = 2
  label_arr = []
  list_of_keys = list(data_shared.keys())
  
  gain_label = Label(frm, text="Melhor ganho:")
  gain_label.grid(row = i + 1, column = 0)

  gain = Label(frm, text = "")
  gain.grid(row = i+1, column= 1)

  risk_label = Label(frm, text="Risco:")
  risk_label.grid(row = i + 2, column = 0)

  risk = Label(frm, text = "")
  risk.grid(row = i+2, column= 1)

  label_arr.append(gain)
  label_arr.append(risk)

  while i < len(data_shared):
    current_key = list_of_keys[i]
    result_label = Label(frm, text=str(current_key))
    result_label.grid(row = i+3, column = 0)

    result = Label(frm, text="")
    result.grid(row = i+3, column = 1)

    label_arr.append(result)

    i += 1


  def search(data_shared, sorted_risk, label_arr):
    
    aux_array = optimize_search(data_shared, sorted_risk, float(risk_min.get()), float(risk_max.get()))
    
    sorted_risk = aux_array[0]
    selected_gain = aux_array[1]
    selected_index = aux_array[2]

    #print(sorted_risk)
    print("selected gain")
    print(selected_gain)
    print("selected index")
    print(selected_index)

    show_results(selected_gain, selected_index, label_arr)

  def show_results(selected_gain, selected_index, label_arr):
 
    i = 2
    list_of_keys = list(data_shared.keys())

    label_arr[0].config(text=str(selected_gain))
    print(data_shared["Risco"][selected_index])
    label_arr[1].config(text = str(data_shared["Risco"][selected_index]))

    while i < len(list_of_keys):
      result = data_shared[list_of_keys[i]][selected_index]*100 
      print(result)
      print(f"{result:.4f}")
      label_arr[i].config(text=f"{result:.4f} %")
      i += 1

    #do the dict search

  find_weights = Button(frm, text="Otimizar", command = lambda: search(data_shared, sorted_risk, label_arr))
  find_weights.grid(row=2, column=1)

  root.mainloop()


def setup_gui():
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

    global n_stocks, data_inicial, data_final
    
    n_stocks = int(stocks_entry.get())
    
    data_inicial = str(start_entry.get())
    data_final = str(end_entry.get())
    root.destroy()
    stocks_gui()
    

  do_it = Button(frm, text="Próximo", command=retrieve)
  do_it.grid(row=3,column=1)

  root.mainloop()


def stocks_gui():

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
    global codes

    codes = []
    i = 0
    while(i<n_stocks):
      codes.append(arr[i].get())
      i += 1
    root.destroy() 

  do_it = Button(frm, text="Próximo", command= lambda: setup_follow())
  do_it.grid(row=i+1,column=0)

  root.mainloop()

if __name__ == '__main__':

  #data_shared = multiprocessing.Array('d',0)
  
  #manager = multiprocessing.Manager()
  #data_shared = manager.dict()

  #p0 = Process(target=setup_gui, args=([data_shared]))
  #p0.start()  
  #p0.join()
  setup_gui()
  data = setup(n_stocks, data_inicial, data_final, codes)

  p_plot = Process(target=plot_markowitz, args=[data])
  p_plot.start()

  print("tamanho riscos")
  print(len(data["Risco"]))


  iter = 0
  unsorted_risk = data["Risco"]
  lenght = len(unsorted_risk)
  matrix = []
  #matrix.append(unsorted_risk)
  copy_unsorted_risk = [0]*lenght
  indexes = []
  while iter < lenght:
    #print([arr_raw[i], i])
    copy_unsorted_risk[iter] = unsorted_risk[iter]
    indexes.append(iter)
    iter += 1
  matrix.append(copy_unsorted_risk)
  matrix.append(indexes)
  
  sorted_risk = merge_sort(matrix, 0, len(unsorted_risk)-1)
  print("sorted matrix")
  print(sorted_risk)

  search_gui(data, sorted_risk)
  

  #p_search = Process(target=search_gui, args=([data_shared]))
  #p_search.start()

  #plot_markowitz(data)

  #p_plot.join()
  #p_search.join()

  #print(data_shared)

  


  #print("{}".format(data_shared[:]))
  
#setup_gui()
