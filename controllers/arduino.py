############################################################################################################
# Classe responsável por manipular o Arduino
############################################################################################################

############################################################################################################
# Importações necessárias
############################################################################################################
from threading import Thread
import serial  # Biblioteca para comunicação serial com o Arduino
import time    # Biblioteca para manipulação de tempo

#########################################################################################################
# Classe Principal
#########################################################################################################
class ArduinoController:
    def __init__(self, port, speedrate=9600, reconnect_interval=5):
        self.port = port
        self.speedrate = speedrate
        self.reconnect_interval = reconnect_interval
        self.arduino = None
        self.connected = False
        
        # Iniciar o processo de conexão inicial
        self._connect()

        # Iniciar a thread para verificar a conexão periodicamente
        self.reconnect_thread = Thread(target=self.check_connection, daemon=True)
        self.reconnect_thread.start()

    def _connect(self):
        """Tenta estabelecer conexão com o Arduino."""
        try:
            self.arduino = serial.Serial(port=self.port, baudrate=self.speedrate, timeout=1)
            time.sleep(2)  # Espera a inicialização do Arduino
            self.connected = True
            print("Conexão com o Arduino estabelecida.")
        except serial.SerialException as e:
            print(f"Erro ao conectar ao Arduino: {e}")
            self.connected = False

    def check_connection(self):
        """Verifica periodicamente se o Arduino está conectado e tenta reconectar."""
        while True:
            if not self.connected:
                print("Tentando reconectar ao Arduino...")
                self._connect()
            time.sleep(self.reconnect_interval)

    def get(self, multiplexador, canal):
        if self.connected and self.arduino:
            canal_global = canal + (multiplexador - 1) * 16
            comando = f"GET,{canal_global}\n".encode()
            self.arduino.write(comando)
            time.sleep(0.1)
            if self.arduino.in_waiting > 0:
                return self.arduino.readline().decode().strip()
            return "Sem resposta"
        else:
            # Valor simulado para visualização quando o Arduino não está conectado
            print("Arduino não conectado, retornando valor simulado.")
            return 0

    def set(self, multiplexador, canal, comando="ON"):
        if self.connected and self.arduino:
            canal_global = canal + (multiplexador - 1) * 16
            comando_codificado = f"SET,{canal_global},{comando}\n".encode()
            self.arduino.write(comando_codificado)
            time.sleep(0.1)
        else:
            # Log de simulação quando o Arduino não está conectado
            print(f"Arduino não conectado. Simulando comando: SET {multiplexador}, {canal}, {comando}")

    def close(self):
        """Fecha a conexão serial com o Arduino, se estiver conectada."""
        if self.connected and self.arduino:
            self.arduino.close()
            self.connected = False

# class ArduinoController:
#     # Inicialização da classe
#     def __init__(self, port, speedrate=9600):
#         """
#         Inicializa a conexão serial com o Arduino.
#         """
#         self.arduino = serial.Serial(port=port, baudrate=speedrate, timeout=1)
#         time.sleep(2)  # Espera a inicialização do Arduino

#     # Função para leitura de dados de um canal específico
#     def get(self, multiplexador, canal):
#         """
#         Lê o valor de um sensor conectado a um canal específico do multiplexador.
        
#         :param multiplexador: Número do multiplexador (1 ou 2).
#         :param canal: Número do canal (0 a 15).
#         :return: Valor lido do sensor ou uma mensagem de erro.
#         """
#         if multiplexador not in [1, 2] or not (0 <= canal <= 15):
#             return "Multiplexador ou canal inválido."
        
#         # Envia o comando para o Arduino (canal global para distinção entre multiplexadores)
#         canal_global = canal + (multiplexador - 1) * 16
#         comando = f"GET,{canal_global}\n".encode()
#         self.arduino.write(comando)
#         time.sleep(0.1)
        
#         if self.arduino.in_waiting > 0:
#             return self.arduino.readline().decode().strip()
#         return "Sem resposta"

#     # Função para acionar um atuador em um canal específico
#     def set(self, multiplexador, canal, comando="ON"):
#         """
#         Envia um comando para acionar um atuador em um canal específico do multiplexador.
        
#         :param multiplexador: Número do multiplexador (1 ou 2).
#         :param canal: Número do canal (0 a 15).
#         :param comando: Comando a ser enviado ao atuador (ex.: 'ON' ou 'OFF').
#         """
#         canal_global = canal + (multiplexador - 1) * 16
#         comando_codificado = f"SET,{canal_global},{comando}\n".encode()
#         self.arduino.write(comando_codificado)
#         time.sleep(0.1)

#     # Função para fechar a conexão
#     def close(self):
#         """Fecha a conexão serial com o Arduino."""
#         self.arduino.close()