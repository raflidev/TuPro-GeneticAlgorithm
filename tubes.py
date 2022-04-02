import random
import math

# ukuran populasi
jumlahPopulasi = 6
# ukuran kromosom
panjangKromosom = 25
# probabilitas crossover
pc = 0.7
# probabilitas mutasi
pm = 0.4
# generasi
generasi = 50

def fungsi(x,y):
  # fungsi matematika yang digunakan pada kasus ini
  return ((math.cos(x) + math.sin(y))**2)/(x**2+y**2)

def fungsiFitness(x,y):
  return 1 / (0.01+(fungsi(x,y)))


def generateKromosom(panjangKromosom):
  # membuat kromosom (mengambil 0 dan 1 secara acak)
  result = []
  for _ in range(panjangKromosom):
    result.append(random.randint(0,1))
  return result

def generatePopulasi(jumlahPopulasi):
  # membentuk populasi dari kromosom
  populasi = []
  for _ in range(jumlahPopulasi):
    populasi.append(generateKromosom(panjangKromosom))
  return populasi

def decodeKromosom(kromosom):
  # menconvert kromosom menjadi angka/nilai
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
  # mengitung total fitness setiap populasi
  total = []
  for i in populasi:
    x, y = decodeKromosom(i)
    total.append(fungsiFitness(x,y))
  return total


def rouletteWheel(populasi, jumlahPopulasi, fitness):
  # seleksi pemilihan orang tua dengan metode roulettewhell
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
  # melakukan crossover dengan perbandingan bilangan random
  bilrandom = random.uniform(0, panjangKromosom-1)
  if bilrandom < pc:
    mv = random.randint(0, panjangKromosom-1)
    for i in range(mv):
      temp = x[i]
      x[i] = y[i]
      y[i] = temp
  return [x, y]

def mutasi(panjangKromosom, pr, keturunan):
  # melakukan mutasi keturunan
  bilrandom = random.uniform(0,1)
  for i in range(panjangKromosom):
    if bilrandom < pr:
      keturunan[0][i] = 1 - keturunan[0][i]
      keturunan[1][i] = 1 - keturunan[1][i]
  return keturunan

def elitisme(fitness):
  # mencari 2 nilai terbaik pada fitness
  index1 = 0
  index2 = 0
  for i in range(1, len(fitness)):
    if fitness[i] > fitness[index1]:
      index2 = index1
      index1 = i
  return [index1, index2]

# inisialisai populasi dan kromosom
populasi = generatePopulasi(jumlahPopulasi)
kromosom = generateKromosom(panjangKromosom)

print("Populasi Awal: ", populasi)

# perpindahan generasi untuk melakukan proses seleksi populasi
for _ in range(generasi):
  newPopulasi = []
  # mencari fitness terbaik untuk dibandingkan dengan generasi selanjutnya
  fit = fitness(populasi)
  parent1, parent2 = elitisme(fit)
  # menambahkan populasi untuk melakukan seleksi generasi
  newPopulasi.append(populasi[parent1])
  newPopulasi.append(populasi[parent2])
  
  for _ in range((jumlahPopulasi-2)//2):
    # mencari parent dengan metode roulettewhell
    parent1 = rouletteWheel(populasi, jumlahPopulasi, fit)
    parent2 = rouletteWheel(populasi, jumlahPopulasi, fit)

    # jika parent bernilai sama, akan diacak ulang
    if(parent1 == parent2):
      parent2 = rouletteWheel(populasi, jumlahPopulasi, fit)

    # melakukan crossover dan mutasi
    keturunan = crossover(pc,panjangKromosom,parent1[:], parent2[:])
    keturunan = mutasi(panjangKromosom, pm, keturunan)
    
    # menambahkan keturunan pada populasi
    newPopulasi.append(keturunan[0])
    newPopulasi.append(keturunan[1])


# assign populasi baru ke populasi
populasi = newPopulasi
# menghitung ulang fitness
fit = fitness(populasi)
# mencari index minimum pada fitness
index = fit.index(max(fit))

# hasil kromosom terbaik
print("Kromosom Terbaik: ", populasi[index])
# hasil fitness terbaik
print("Fitness Terbaik: ", fit[index])
# ngambil nilai kromosom pada populasi index minimum
print("Nilai Kromosom: ", decodeKromosom(populasi[index]))
