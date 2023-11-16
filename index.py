import pandas as pd
import chardet
import matplotlib.pyplot as plt
import numpy as np
import mplcursors
from sklearn.preprocessing import MinMaxScaler

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
        df = df.rename(columns={f'Unnamed: {i}': f'S{semana}'})
        semana += 1
linha_sp = df.loc[df['Regiao'] == 'SÃO PAULO']
semanas_infectados = pd.DataFrame()

N = 11451245
beta = 0.375 #taxa de contágio
gama = 1/6

for i in range(1, 53):
    semanas_infectados[f'S{i}'] = linha_sp[f'S{i}']

  #número de habitantes
infectados = np.array(semanas_infectados.values.tolist()).flatten().tolist()
sucetiveis = [N-infectados[0]]
recuperados = [0]
for i in range(len(infectados)-1):
    sucetiveis.append(sucetiveis[i]*(1-beta*infectados[i]/N))
    recuperados.append(recuperados[i]+gama*infectados[i])

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
#plt.plot(semanas_infectados.columns.tolist(), sucetiveis, label="Sucetíveis", color='green', marker='.')
plt.plot(semanas_infectados.columns.tolist(), infectados, label="Infectados", color='red', marker='.')
#plt.plot(semanas_infectados.columns.tolist(), valores_recuperados_normalizados, label="Recuperados", color='blue', marker='.')
plt.xlabel('Semanas')
plt.ylabel('Pessoas')
plt.title('Gráfico de pessoas infectadas ao longo do tempo')
plt.xticks(rotation=45, ha='right')
mplcursors.cursor(hover=True)

# Adicionar uma legenda
plt.legend()

# Exibir o gráfico
plt.show()
