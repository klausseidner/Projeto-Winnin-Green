############################################################################################################
############################################################################################################
# Ardudeck - Biblioteca para controlar o Arduino, seus sensores e atuadores
############################################################################################################
############################################################################################################
# Instalar as bibliotecas necessárias:
# pip install smbus2 adafruit-circuitpython-ssd1306 pillow
############################################################################################################

############################################################################################################
# Importando as bibliotecas necessárias
############################################################################################################
from threading import Thread # Biblioteca para trabalhar com threads
import serial  # Biblioteca para comunicação serial com o Arduino
import time    # Biblioteca para manipulação de tempo
import smbus2 # Biblioteca para comunicação I2C com o Arduino
import board # Biblioteca para detectar o dispositivo board
import busio # Biblioteca para comunicação I2C com o Arduino
from PIL import Image, ImageDraw, ImageFont # Biblioteca para manipulação de fontes
import adafruit_ssd1306 # Biblioteca para comunicação I2C com o display OLED
from config import map, arduino_port, speedrate, reconnect_interval # Configurações do Arduino

############################################################################################################
############################################################################################################
# Classe responsável por controlar o Arduino
############################################################################################################
############################################################################################################
class ArduinoController:
    def __init__(self):
        self.arduino = None # Serial connection object
        self.connected = False # Indica se a conexão com o Arduino está ativa
        self._connect() # Iniciar o processo de conexão inicial
        self.reconnect_thread = Thread(target=self.check_connection, daemon=True) # Thread para verificar a conexão periódicamente
        self.reconnect_thread.start() # Inicia a thread de reconexão

############################################################################################################
    # Função para conectar ao Arduino
############################################################################################################
    def _connect(self):
        """Tenta estabelecer conexão com o Arduino."""
        try:
            self.arduino = serial.Serial(port=arduino_port, baudrate=speedrate, timeout=1) # Tenta conectar ao Arduino
            time.sleep(2)  # Espera a inicialização do Arduino
            self.connected = True # Conexão com o Arduino estabelecida
            print("Conexão com o Arduino estabelecida.") # Informa que a conexão foi estabelecida
        except serial.SerialException as e: # Exceção caso a conexão falhe
            print(f"Erro ao conectar ao Arduino: {e}") # Informa o erro ao conectar ao Arduino
            self.connected = False # Conexão com o Arduino não estabelecida

############################################################################################################
    # Função para checkar a conexão com o Arduino
############################################################################################################
    def check_connection(self):
        """Verifica periodicamente se o Arduino está conectado e tenta reconectar."""
        while True:
            if not self.connected: # Se a conexão com o Arduino não está ativa
                print("Tentando reconectar ao Arduino...") # Informa que a conexão está sendo tentada
                self._connect() # Tenta reconectar ao Arduino
            time.sleep(reconnect_interval) # Espera o intervalo de reconexão

############################################################################################################
    # Função para ler um sensor do Arduino
############################################################################################################
    def get(self, multiplexador, canal):
        """Lê um valor de um sensor do Arduino.
        :param multiplexador: Número do multiplexador (1 ou 2).
        :param canal: Número do canal (0 a 15). """
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

############################################################################################################
    # Função para escrever um valor no Arduino
############################################################################################################
    def set(self, multiplexador, canal, comando="ON"):
        """Escreve um valor no Arduino.
        :param multiplexador: Número do multiplexador (1 ou 2).
        :param canal: Número do canal (0 a 15).
        :param comando: Comando a ser enviado ao atuador (ex.: 'ON' ou 'OFF'). """
        if self.connected and self.arduino:  # Se a conexão com o Arduino está ativa
            canal_global = canal + (multiplexador - 1) * 16 # Calcula o canal global
            comando_codificado = f"SET,{canal_global},{comando}\n".encode() # Codifica o comando para envio ao Arduino
            self.arduino.write(comando_codificado) # Envia o comando ao Arduino
            time.sleep(0.1) # Espera a resposta do Arduino
        else: # Caso o Arduino não está conectado
            print(f"Arduino não conectado. Simulando comando: SET {multiplexador}, {canal}, {comando}") # Informa o comando simulado

############################################################################################################
    # Função para fechar a conexão serial com o Arduino
############################################################################################################
    def close(self):
        """Fecha a conexão serial com o Arduino, se estiver conectada."""
        if self.connected and self.arduino: # Se a conexão com o Arduino está ativa
            self.arduino.close() # Fecha a conexão serial com o Arduino
            self.connected = False # Conexão com o Arduino fechada

############################################################################################################
############################################################################################################
# Classe responsável pelos dispositivos conectados ao Arduino.
############################################################################################################
############################################################################################################
class Devices:
    def __init__(self, arduino_controller):
        """
        Inicializa a classe com o controlador do Arduino.
        :param arduino_controller: Instância de ArduinoController para comunicação com o Arduino.
        """
        self.arduino = arduino_controller # Controlador do Arduino

############################################################################################################
    # Função de leitura de sensores
############################################################################################################
    def get(self, device):
        """
        Lê o valor de um sensor conectado a um multiplexador.
        :param device: Nome do dispositivo a ser lido.
        """
        try:
            config = map[device] # Configurações do dispositivo
            value = self.arduino.get(config["multiplexador"], config["channel"]) # Lê o valor do sensor
            return value # Retorna o valor do sensor
        except Exception as e:
            print(f"Erro ao ler o sensor {device}: {str(e)}")
            return None

############################################################################################################
    # Função de leitura do sensor de temperatura e umidade do AHT10
############################################################################################################
    def aht10(self):
        """
        Lê temperatura e umidade do sensor AHT10.
        """
        # Inicializa o sensor e o display
        aht10 = AHT10(bus_number=1)

        try:
            sensor_data = aht10.read_data() # Lê os dados do AHT10
            return sensor_data
        except Exception as e:
            print(f"Erro ao ler o sensor AHT10: {str(e)}")
            return None

############################################################################################################
    # Função de alerta sonoro
############################################################################################################
    def alert(self, duracao=1):
        """
        Ativa o buzzer passivo por um tempo específico.
        """
        channel = map["buzzer"]["channel"] # Pino digital para buzzer passivo
        self.arduino.set(0, channel, "ON") # Ativa o buzzer passivo
        time.sleep(duracao) # Pausa o tempo especificado
        self.arduino.set(0, channel, "OFF") # Desativa o buzzer passivo

############################################################################################################
    # Função para ativar ou desativar atuador
############################################################################################################
    def set(self, state, channel):
        """
        Ativa ou desativa um atuador.
        :param state: Estado a ser ativado (True) ou desativado (False).
        :param channel: Canal do atuador.
        """
        if state == "ON":
            self.arduino.set(0, channel, "ON") # Ativa o atuador
            return True
        else:
            self.arduino.set(0, channel, "OFF") # Desativa o atuador
            return False

############################################################################################################
############################################################################################################
# Clase para sensor de temperatura e umidade do ar (AHT10)
############################################################################################################
############################################################################################################
class AHT10:
    AHT10_ADDRESS = 0x38 # Endereço do sensor AHT10
    AHT10_CMD_CALIBRATE = [0xE1, 0x08, 0x00] # Comando para calibrar o sensor
    AHT10_CMD_MEASURE = [0xAC, 0x33, 0x00] # Comando para realizar a leitura dos dados do sensor
    AHT10_CMD_RESET = 0xBA # Comando para resetar o sensor

############################################################################################################
    # Método construtor
############################################################################################################
    def __init__(self, bus_number=1):
        """
        Inicializa o sensor AHT10.
        :param bus_number: Número do barramento I²C (padrão: 1)
        """
        self.bus = smbus2.SMBus(bus_number) # Inicializa o barramento I²C
        self.calibrated = False # Variável para armazenar se o sensor está calibrado
        self._initialize_sensor() # Inicializa o sensor

############################################################################################################
    # Função para inicializar o sensor AHT10
############################################################################################################
    def _initialize_sensor(self):
        """Inicializa o sensor e calibra-o."""
        self.bus.write_i2c_block_data(self.AHT10_ADDRESS, 0x00, self.AHT10_CMD_RESET) # Reseta o sensor
        time.sleep(0.02) # Aguarda o reset
        self.bus.write_i2c_block_data(self.AHT10_ADDRESS, 0x00, self.AHT10_CMD_CALIBRATE) # Calibra o sensor
        time.sleep(0.1) # Aguarda a calibração
        self.calibrated = True # Marca o sensor como calibrado

############################################################################################################
    # Função para ler os dados do sensor AHT10
############################################################################################################
    def read_data(self):
        """
        Lê os valores de temperatura e umidade do sensor.
        :return: Um dicionário com 'temperature' e 'humidity'.
        """
        if not self.calibrated: # Verifica se o sensor está calibrado
            raise RuntimeError("Sensor não calibrado. Recalibre antes de ler os dados.")
        self.bus.write_i2c_block_data(self.AHT10_ADDRESS, 0x00, self.AHT10_CMD_MEASURE) # Realiza a leitura dos dados
        time.sleep(0.1) # Aguarda a leitura dos dados
        data = self.bus.read_i2c_block_data(self.AHT10_ADDRESS, 0x00, 6) # Lê os dados da leitura
        status = data[0] # Leitura do status
        if status & 0x80:  # Verifica se o sensor está ocupado
            raise RuntimeError("Sensor ocupado. Tente novamente.") # Erro caso o sensor esteja ocupado
        raw_humidity = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4 # Extrai os dados da leitura
        raw_temperature = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5] # Extrai os dados da leitura
        humidity = (raw_humidity / 1048576.0) * 100 # Calcula a umidade
        temperature = ((raw_temperature / 1048576.0) * 200) - 50  # Calcula a temperatura
        humidity = round(humidity, 2) # Arredonda a umidade
        temperature = round(temperature, 2) # Arredonda a temperatura
        return humidity, temperature  # Retorna a umidade e a temperatura

############################################################################################################
############################################################################################################
# Classe para o Display
############################################################################################################
############################################################################################################
class OLEDDisplay:
############################################################################################################
    # Método construtor
############################################################################################################
    def __init__(self, width=128, height=64, i2c_bus=None):
        """
        Inicializa o display OLED.
        :param width: Largura do display (padrão: 128)
        :param height: Altura do display (padrão: 64)
        :param i2c_bus: Barramento I²C (se None, inicializa automaticamente)
        """
        if i2c_bus is None: # Inicializa automaticamente o barramento I²C
            i2c_bus = busio.I2C(board.SCL, board.SDA) # Inicializa o barramento I²C
        self.display = adafruit_ssd1306.SSD1306_I2C(width, height, i2c_bus) # Inicializa o display OLED
        self.width = width # Largura do display
        self.height = height # Altura do display
        self.display.fill(0) # Preenche o display com branco
        self.display.show() # Mostra o display
        self.image = Image.new("1", (self.width, self.height)) # Cria uma imagem do display
        self.draw = ImageDraw.Draw(self.image) # Cria um desenho do display

############################################################################################################
    # Funções limpar o display
############################################################################################################
    def clear(self):
        """Limpa o display."""
        self.display.fill(0) # Preenche o display com branco
        self.display.show() # Mostra o display

############################################################################################################
    # Funções para mostrar texto no display
############################################################################################################
    def show_text(self, text, x=0, y=0, font_size=12):
        """
        Exibe texto no display.
        :param text: Texto a ser exibido.
        :param x: Coordenada X para o texto.
        :param y: Coordenada Y para o texto.
        :param font_size: Tamanho da fonte.
        """
        self.clear() # Limpa o display
        font = ImageFont.truetype("arial.ttf", font_size) # Define a fonte
        self.draw.text((x, y), text, font=font, fill=255) # Exibe o texto no display
        self.display.image(self.image) # Mostra o display
        self.display.show() # Mostra o display

############################################################################################################
    # Função para mostrar dados dos sensores no display
############################################################################################################
    def show_sensor_data(self, data):
        """
        Exibe os dados dos sensores no display.
        :param data: Dicionário com os valores dos sensores.
        """
        self.clear() # Limpa o display
        y_offset = 0 # Offset vertical para posicionar os dados
        for key, value in data.items(): # Exibe os dados dos sensores
            self.draw.text((0, y_offset), f"{key}: {value}", fill=255) # Exibe o texto no display
            y_offset += 12 # Ajusta o offset vertical para mostrar os dados dos sensores
        self.display.image(self.image) # Mostra o display
        self.display.show() # Mostra o display

############################################################################################################