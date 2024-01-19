import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mplcursors
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression

scaler = MinMaxScaler()
caminho_arquivo = './data/data.xlsx'
df = pd.read_excel(caminho_arquivo)
df = df.rename(columns={'Unnamed: 1': 'DRS', 'Unnamed: 3': 'GVE', 'Unnamed: 4': 'Codigo_regiao', 'Unnamed: 5': 'Regiao', 'Unnamed: 6': 'Municipio'})
df = df.dropna()
df['Municipio'] = df['Municipio'].replace(to_replace=r'\d', value='', regex=True)
semana = 1
for i in range(7, 60):
    if i == 59:
        df = df.rename(columns={f'Unnamed: {i}': 'Total'})
    else:
        df = df.rename(columns={f'Unnamed: {i}': semana})
        semana += 1
linha_sp = df.loc[df['Regiao'] == 'SÃO PAULO']
semanas_infectados = pd.DataFrame()

N = 11451245
gama = 1/6

for i in range(1, 53):
    semanas_infectados[i] = linha_sp[i]


semanas = semanas_infectados.columns.tolist()
infectados = np.array(semanas_infectados.values.tolist()).flatten().tolist()
sucetiveis = [N-infectados[0]]
recuperados = [0]
count = 0
elements_count = 10
beta_array = []
while count < 5:
    y = []
    X = []
    for i in range(elements_count - 10, elements_count):
        y.append(semanas[i])
        X.append(infectados[i])
    X = np.array(X).reshape(-1,1)
    y = np.array(y)
    modelo = LinearRegression()
    modelo.fit(X, y)
    b = modelo.coef_[0]
    beta = b +  gama
    beta_array.append(beta)
    print(beta)
    for i in range(elements_count - 10, elements_count):
        sucetiveis.append(sucetiveis[i]*(1-beta*infectados[i]/N))
        recuperados.append(recuperados[i]+gama*infectados[i])
    elements_count = elements_count + 10
    count += 1
sucetiveis.append(sucetiveis[50]*(1-beta*infectados[50]/N))
recuperados.append(recuperados[50]+gama*infectados[50])

valores_sucetiveis_normalizados = scaler.fit_transform([[v] for v in sucetiveis])
valores_infectados_normalizados = scaler.fit_transform([[v] for v in infectados])
valores_recuperados_normalizados = scaler.fit_transform([[v] for v in recuperados])

#Gráfico separado
'''
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(8, 12))

ax1.plot(semanas_infectados.columns.tolist(), sucetiveis, label="Sucetíveis", color='green', marker='.')
ax1.set_ylabel('Suscetíveis')
ax1.legend()

ax2.plot(semanas_infectados.columns.tolist(), infectados, label="Infectados", color='red', marker='.')
ax2.set_ylabel('Infectados')
ax2.legend()

ax3.plot(semanas_infectados.columns.tolist(), recuperados, label="Recuperados", color='blue', marker='.')
ax3.set_xlabel('Semanas')
ax3.set_ylabel('Recuperados')
ax3.legend()

fig.suptitle('Modelo Epidemiológico - Sucetíveis, Infectados e Recuperados')
'''

#Gráfico com todas as linhas juntas
plt.plot(semanas, valores_sucetiveis_normalizados, label="Sucetíveis", color='green', marker='.')
plt.plot(semanas, valores_infectados_normalizados, label="Infectados", color='red', marker='.')
plt.plot(semanas, valores_recuperados_normalizados, label="Recuperados", color='blue', marker='.')
#plt.plot(['S10', 'S20', 'S30', 'S40', 'S50'], beta_array, label="beta", color='blue', marker='.')

plt.xlabel('Semanas')
plt.ylabel('Beta')
plt.title('Modelo Epidemiológico - beta')
plt.xticks(rotation=45, ha='right')
mplcursors.cursor(hover=True)

# Adicionar uma legenda
plt.legend()

# Exibir o gráfico
plt.show()
