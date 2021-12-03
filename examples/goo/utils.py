import random
import numpy
import b2d 
import networkx
# from abc import ABC,abstractmethod

def xor(a,b):
    return (a and not b) or (not a and b)




def pairwise_distance(data, f, distance):
    n = len(data)
    results = []
    for i in range(n-1):    
        da = f(data[i])
        for j in range(i+1, n):
            db= f(data[j])

            d = distance(da, db)
            results.append((i,j,d))
    return results

def best_pairwise_distance(data, f, distance):
    n = len(data)
    best = (None,None,float('inf'))
    for i in range(n-1):    
        da = f(data[i])
        for j in range(i+1, n):
            db= f(data[j])

            d = distance(da, db)
            if d < best[2]:
                best = (i,j,d)
    return best