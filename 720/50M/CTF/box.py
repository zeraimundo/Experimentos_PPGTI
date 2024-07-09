import pandas as pd
import matplotlib.pyplot as plt

# Configurações para lidar com grandes conjuntos de dados
plt.rcParams['agg.path.chunksize'] = 10000  # Ajuste este valor conforme necessário
plt.rcParams['path.simplify_threshold'] = 1.0  # Ajuste este valor conforme necessário

# Load the CSV files
def load_and_adjust_data(send_file, recv_file):
    send_data = pd.read_csv(send_file)
    recv_data = pd.read_csv(recv_file)
    timezero = send_data['time'][0]
    send_data['time'] = send_data['time'] - timezero
    recv_data['time'] = recv_data['time'] - timezero
    return send_data, recv_data

send_b_1080_5M, r_b_1080_5M = load_and_adjust_data('enviados_tratado_b51080.csv', 'recebidos_tratado_b51080.csv')
send_c_1080_5M, r_c_1080_5M = load_and_adjust_data('enviados_tratado_c51080.csv', 'recebidos_tratado_c51080.csv')
send_d_1080_5M, r_d_1080_5M = load_and_adjust_data('enviados_tratado_d51080.csv', 'recebidos_tratado_d51080.csv')
send_r_1080_5M, r_r_1080_5M = load_and_adjust_data('enviados_tratado_r51080.csv', 'recebidos_tratado_r51080.csv')

def merge_and_calculate_delay(send_data, recv_data):
    result = pd.merge(send_data, recv_data, on='id', how='left', suffixes=('_s', '_r'))
    result['time_d'] = result['time_r'] - result['time_s']
    result = result.dropna(how='any')
    return result['time_d']

time_d_b_1080_5M = merge_and_calculate_delay(send_b_1080_5M, r_b_1080_5M)
time_d_c_1080_5M = merge_and_calculate_delay(send_c_1080_5M, r_c_1080_5M)
time_d_d_1080_5M = merge_and_calculate_delay(send_d_1080_5M, r_d_1080_5M)
time_d_r_1080_5M = merge_and_calculate_delay(send_r_1080_5M, r_r_1080_5M)

# Prepare data for boxplot
data = [time_d_b_1080_5M, time_d_c_1080_5M, time_d_d_1080_5M, time_d_r_1080_5M]

# Plot the boxplot
plt.figure(figsize=(12, 6))
plt.boxplot(data, labels=['BBR', 'Cubic', 'DCTCP', 'Reno'], showfliers=False)
plt.xlabel('Protocol')
plt.ylabel('Delay (seconds)')
plt.title('Boxplot of Delays for Different Protocols')
plt.grid(True)
plt.show()

