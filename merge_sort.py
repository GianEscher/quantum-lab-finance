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

    print(arr)


arr = [12, 11, 11, 11, 11, 11, 13, 5, 6, 7, 7]
merge_sort(arr, 0, len(arr)-1)
print("\nSorted array is ")
print(arr)