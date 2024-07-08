import pandas as pd
import matplotlib.pyplot as plt

# Configurações para lidar com grandes conjuntos de dados
plt.rcParams['agg.path.chunksize'] = 10000  # Ajuste este valor conforme necessário
plt.rcParams['path.simplify_threshold'] = 1.0  # Ajuste este valor conforme necessário

# Load the CSV files
# BBR
send_b_1080_5M = pd.read_csv('enviados_tratado_b51080.csv')
r_b_1080_5M = pd.read_csv('recebidos_tratado_b51080.csv')
timezero = send_b_1080_5M['time'][0]
send_b_1080_5M['time'] = (send_b_1080_5M['time'] - timezero)
r_b_1080_5M['time'] = (r_b_1080_5M['time'] - timezero)
# Cubic
send_c_1080_5M = pd.read_csv('enviados_tratado_c51080.csv')
r_c_1080_5M = pd.read_csv('recebidos_tratado_c51080.csv')
timezero = send_c_1080_5M['time'][0]
send_c_1080_5M['time'] = (send_c_1080_5M['time'] - timezero)
r_c_1080_5M['time'] = (r_c_1080_5M['time'] - timezero)
# DCTCP
send_d_1080_5M = pd.read_csv('enviados_tratado_d51080.csv')
r_d_1080_5M = pd.read_csv('recebidos_tratado_d51080.csv')
timezero = send_d_1080_5M['time'][0]
send_d_1080_5M['time'] = (send_d_1080_5M['time'] - timezero)
r_d_1080_5M['time'] = (r_d_1080_5M['time'] - timezero)
# Reno
send_r_1080_5M = pd.read_csv('enviados_tratado_r51080.csv')
r_r_1080_5M = pd.read_csv('recebidos_tratado_r51080.csv')
timezero = send_r_1080_5M['time'][0]
send_r_1080_5M['time'] = (send_r_1080_5M['time'] - timezero)
r_r_1080_5M['time'] = (r_r_1080_5M['time'] - timezero)

# Merge the dataframes on 'id'
# Using 'how=left' ensures that we keep all packets from the send dataframe even if they are not in the receive dataframe
resultados_b_1080_5M = pd.merge(send_b_1080_5M, r_b_1080_5M, on='id', how='left', suffixes=('_s', '_r'))
resultados_c_1080_5M = pd.merge(send_c_1080_5M, r_c_1080_5M, on='id', how='left', suffixes=('_s', '_r'))
resultados_d_1080_5M = pd.merge(send_d_1080_5M, r_d_1080_5M, on='id', how='left', suffixes=('_s', '_r'))
resultados_r_1080_5M = pd.merge(send_r_1080_5M, r_r_1080_5M, on='id', how='left', suffixes=('_s', '_r'))

# Calculate the time difference in seconds
resultados_b_1080_5M['time_d'] = (resultados_b_1080_5M['time_r'] - resultados_b_1080_5M['time_s'])
resultados_b_1080_5M = resultados_b_1080_5M.dropna(how='any')
resultados_b_1080_5M['rolling_avg'] = resultados_b_1080_5M['time_d'].rolling(window=100).mean()

resultados_c_1080_5M['time_d'] = (resultados_c_1080_5M['time_r'] - resultados_c_1080_5M['time_s'])
resultados_c_1080_5M = resultados_c_1080_5M.dropna(how='any')
resultados_c_1080_5M['rolling_avg'] = resultados_c_1080_5M['time_d'].rolling(window=100).mean()

resultados_d_1080_5M['time_d'] = (resultados_d_1080_5M['time_r'] - resultados_d_1080_5M['time_s'])
resultados_d_1080_5M = resultados_d_1080_5M.dropna(how='any')
resultados_d_1080_5M['rolling_avg'] = resultados_d_1080_5M['time_d'].rolling(window=100).mean()

resultados_r_1080_5M['time_d'] = (resultados_r_1080_5M['time_r'] - resultados_r_1080_5M['time_s'])
resultados_r_1080_5M = resultados_r_1080_5M.dropna(how='any')
resultados_r_1080_5M['rolling_avg'] = resultados_r_1080_5M['time_d'].rolling(window=100).mean()

# Plot the time differences over send time
plt.figure(figsize=(12, 6))
plt.plot(resultados_b_1080_5M['time_r'], resultados_b_1080_5M['rolling_avg'], linestyle='-', label='BBR')
plt.plot(resultados_c_1080_5M['time_r'], resultados_c_1080_5M['rolling_avg'], linestyle='-', label='Cubic')
plt.plot(resultados_d_1080_5M['time_r'], resultados_d_1080_5M['rolling_avg'], linestyle='-', label='DCTCP')
plt.plot(resultados_r_1080_5M['time_r'], resultados_r_1080_5M['rolling_avg'], linestyle='-', label='Reno')

plt.xlabel('Time (seconds)')
plt.ylabel('Rolling average of delay')
plt.legend()
plt.grid(True)
plt.show()
