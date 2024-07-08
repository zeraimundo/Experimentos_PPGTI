import pandas as pd
import matplotlib.pyplot as plt

# Caminhos dos arquivos de log
file_paths = [
    '/mnt/data/r5720.log',
    '/mnt/data/c5720.log',
    '/mnt/data/b5720.log',
    '/mnt/data/d5720.log'
]

# Inicializar um DataFrame para combinar os dados
combined_data = pd.DataFrame()

# Ler e combinar os dados dos arquivos de log
for file_path in file_paths:
    log_data = pd.read_csv(file_path, delimiter=',', header=0)
    combined_data = pd.concat([combined_data, log_data[['timestamp', 'framesDisplayedCalc']]], axis=0)

# Criar o gráfico de linhas
plt.figure(figsize=(10, 6))
for file_path in file_paths:
    log_data = pd.read_csv(file_path, delimiter=',', header=0)
    plt.plot(log_data['timestamp'], log_data['framesDisplayedCalc'], label=file_path.split('/')[-1])

plt.xlabel('Timestamp')
plt.ylabel('Frames Displayed Calc')
plt.title('Frames Displayed Calc vs Timestamp')
plt.legend()
plt.grid(True)
plt.show()

