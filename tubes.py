import random
import math

jumlahPopulasi = 100
panjangKromosom = 20
pc = 0.70
pm = 0.4
generasi = 50

def fungsi(x,y):
  return ((math.cos(x) + math.sin(y))**2)/(x**2+y**2)

def generatePopulasi(jumlahPopulasi):
  populasi = []
  for _ in range(jumlahPopulasi):
    populasi.append(generateKromosom(panjangKromosom))
  return populasi

def generateKromosom(panjangKromosom):
  result = []
  for _ in range(panjangKromosom):
    result.append(random.randint(0,1))
  return result

def decodeKromosom(kromosom):
  xmin = -5
  xmax = 5
  ymin = -5
  ymax = 5

  x = 0
  y = 0
  z = 0
  n =  len(kromosom)//2
  for i in range(0, n):
    z += 2**(-(i+1))
  for i in range(0, n):
    x += kromosom[i]*2**-(i+1)
    y += kromosom[n + 1]*2**-(i+1)

  x = xmin + ((xmax - xmin)/z)*x
  y = ymin + ((ymax - ymin)/z)*y
  return [x,y]
  
def fitness(populasi):
  total = []
  for i in populasi:
    x, y = decodeKromosom(i)
    total.append(fungsi(x,y))
  return total


def rouletteWheel(populasi, jumlahPopulasi, fitness):
  index = 0
  total = sum(fitness)
  # mengambil angka random dari 0 sampai 1
  bilrandom = random.uniform(0,1)
  for i in range(jumlahPopulasi):
    if(fitness[i]/total) > bilrandom:
      index = i
      break
    i += 1
  return populasi[index]

def crossover(pc, panjangKromosom, x, y):
  bilrandom = random.uniform(0, panjangKromosom-1)
  if bilrandom < pc:
    mv = random.randint(0,3)
    for i in range(mv):
      temp = x[i]
      x[i] = y[i]
      y[i] = temp
  return [x, y]

def mutasi(panjangKromosom, pr, keturunan):
  bilrandom = random.uniform(0,1)
  for i in range(panjangKromosom):
    if bilrandom < pr:
      keturunan[0][i] = 1 - keturunan[0][i]
      keturunan[1][i] = 1 - keturunan[1][i]
  return keturunan

def elitisme(fitness):
  min1 = 0
  min2 = 0
  for i in range(1, len(fitness)):
    if fitness[i] < fitness[min1]:
      min2 = min1
      min1 = i
  return min1, min2

populasi = generatePopulasi(jumlahPopulasi)
kromosom = generateKromosom(panjangKromosom)

for _ in range(generasi):
  newPopulasi = []
  fit = fitness(populasi)
  parent1, parent2 = elitisme(fit)
  newPopulasi.append(populasi[parent1])
  newPopulasi.append(populasi[parent2])
  
  for _ in range((jumlahPopulasi-2)//2):
    parent1 = rouletteWheel(populasi, jumlahPopulasi, fit)
    parent2 = rouletteWheel(populasi, jumlahPopulasi, fit)
    while(parent1 == parent2):
      parent2 = rouletteWheel(populasi, jumlahPopulasi, fit)

  keturunan = crossover(pc,panjangKromosom,parent1[:], parent2[:])
  keturunan = mutasi(panjangKromosom, pm, keturunan)
  newPopulasi.append(keturunan[0])
  newPopulasi.append(keturunan[1])

populasi = newPopulasi

fit = fitness(populasi)
index = fit.index(min(fit))
print(populasi[index])
print(fit[index])
print(decodeKromosom(populasi[index]))
