import matplotlib.pyplot as plt
import numpy as np

N = 5000
I0 = 1
R0 = 0
S0 = N-I0-R0
beta = 0.2
gama = 1/10
dias = 90

def sequencia(N, S0, I0,R0,beta, gama, dias):
    listas = [S0]
    listai = [I0]
    listar = [R0]
    for i in range(dias):
        listas.append(listas[i]*(1-beta*listai[i]/N))
        listai.append(listai[i]*(1+beta*listas[i]/N-gama))
        listar.append(listar[i]+gama*listai[i])
    for i in range(dias):
        listas[i] = round(listas[i],2)
        listai[i] = round(listai[i],2)
        listar[i] = round(listar[i],2)
    return [listas, listai, listar]

dias = [1, 2, 3, 4, 5]
suscetiveis = [1000, 800, 600, 400, 200]
infectados = [50, 150, 300, 500, 700]
recuperados = [0, 10, 50, 200, 400]

# Criar um gráfico de linhas
plt.plot(dias, suscetiveis, label='Suscetíveis', color='green')
plt.plot(dias, infectados, label='Infectados', color='red')
plt.plot(dias, recuperados, label='Recuperados', color='blue')

# Adicionar rótulos e título
plt.xlabel('Dias')
plt.ylabel('Número de Pessoas')
plt.title('Modelo Epidemiológico - Suscetíveis, Infectados e Recuperados')

# Adicionar uma legenda
plt.legend()

# Exibir o gráfico
plt.show()
