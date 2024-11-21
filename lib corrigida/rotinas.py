############################################################################################################
# Arquivo responsável pelas rotinas de leitura dos sensores e controlador do Arduino
############################################################################################################
############################################################################################################
# Importando bibliotecas necessárias
############################################################################################################
import time # Biblioteca para contagem de tempo
from ardudeck import ArduinoController, Devices, AHT10 # Biblioteca para comunicação com o Arduino e os sensores

############################################################################################################
# Inicializando o controlador do Arduino e os sensores
############################################################################################################
arduino = ArduinoController() # Inicializa o controlador do Arduino
device = Devices(arduino) # Inicializa os dispositivos do Arduino
air = AHT10(bus_number=1) # Inicializa o sensor AHT10

############################################################################################################
# Classe Estufa que encapsula as rotinas de leitura dos sensores e controlador do Arduino
############################################################################################################
class Estufa:
############################################################################################################
    # Função para leitura da umidade do solo
############################################################################################################
    def solo():
        try: # Tenta ler a umidade do solo
            value = device.get('ground') # Lê a umidade do solo
            if value < 50: # Se a umidade do solo for inferior a 50%
                device.set('irrigation', 'ON')  # Ativa a irrigação
            else: # Se a umidade do solo não for inferior a 50%
                device.set('irrigation', 'OFF')  # Desativa a irrigação
            return value # Retorna a umidade do solo
        except Exception as e: # Caso ocorra algum erro durante a leitura
            print(f"Erro na leitura do solo: {e}") # Exibe a mensagem de erro
            return None # Retorna vazio

############################################################################################################
    # Função para leitura da temperatura
############################################################################################################
    def temperatura():
        try: # Tenta ler a temperatura
            temperature, humidity = device.aht10() # Lê a temperatura e a umidade
            if temperature > 30: # Se a temperatura for superior a 30°C
                device.set('fan', 'ON')  # Ativa o calor
            else: # Se a temperatura não for superior a 30°C
                device.set('fan', 'OFF')  # Desativa o calor
            return temperature # Retorna a temperatura
        except Exception as e: # Caso ocorra algum erro durante a leitura
            print(f"Erro na leitura da temperatura: {e}") # Exibe a mensagem de erro
            return None # Retorna vazio

############################################################################################################
    # Função para leitura da umidade do ar
############################################################################################################
    def ar():
        try: # Tenta ler a umidade do ar
            temperature, humidity = device.aht10() # Lê a temperatura e a umidade
            if humidity < 50: # Se a umidade do ar for inferior a 50% 
                device.set('humidifier', 'ON')  # Ativa a lâmpada
            else: # Se a umidade do ar não for inferior a 50%
                device.set('humidifier', 'OFF')  # Desativa a lâmpada
            return humidity # Retorna a umidade do ar
        except Exception as e: # Caso ocorra algum erro durante a leitura
            print(f"Erro na leitura do ar: {e}") # Exibe a mensagem de erro
            return None # Retorna vazio

############################################################################################################
    # Função para leitura da luminosidade
############################################################################################################
    def iluminacao():
        try:
            value = device.get('light')
################## TEM QUE IMPLEMENTAR COMO NECESSÁRIO A LEITURA DA LUMINOSIDADE ############
            # Verificar o tempo de iluminação para ativar a lâmpada
            device.set('lamp', 'ON' if value < 50 else 'OFF')  # Ativa a lâmpada
            return value
        except Exception as e:
            print(f"Erro na leitura da luminosidade: {e}")
            return None

############################################################################################################
    # Função para leitura de chamas
############################################################################################################
    def chamas():
        try: # Tenta ler a presença de chamas
            value = device.get('fire') # Lê a presença de chamas
            if value == 1: # Se detectar chamas
                device.alert(5) # Ativa o alerta com tempo de 5 segundos
            return value # Retorna a presença de chamas
        except Exception as e: # Caso ocorra algum erro durante a leitura
            print(f"Erro na leitura da chamas: {e}") # Exibe a mensagem de erro
            return None # Retorna a presença de chamas

############################################################################################################
    # Função para leitura da porta aberta
############################################################################################################
    def porta():
        try: # Tenta ler a presença de porta aberta
            value = device.get('door') # Lê a presença de porta aberta
            if value == 1: # Se detectar a porta aberta
                device.alert(2) # Ativa o alerta com tempo de 10 segundos
            return value # Retorna a presença de porta aberta
        except Exception as e: # Caso ocorra algum erro durante a leitura
            print(f"Erro na leitura da porta: {e}") # Exibe a mensagem de erro
            return None # Retorna a presença de porta aberta

############################################################################################################
# Função para ativar cor RGB usando match-case
############################################################################################################
    def rgb(data):
        try:
            # Verifica qual cor foi ativada
            match data:
                case {"red": "ON"}:
                    device.set('rgb_red', 'ON' if device.get('rgb_red') == 0 else 'OFF')
                case {"green": "ON"}:
                    device.set('rgb_green', 'ON' if device.get('rgb_green') == 0 else 'OFF')
                case {"blue": "ON"}:
                    device.set('rgb_blue', 'ON' if device.get('rgb_blue') == 0 else 'OFF')
                case {"red": "OFF"}:
                    device.set('rgb_red', 'OFF')
                case {"green": "OFF"}:
                    device.set('rgb_green', 'OFF')
                case {"blue": "OFF"}:
                    device.set('rgb_blue', 'OFF')
                case _:
                    print("Nenhuma cor válida foi ativada.")
        except Exception as e:
            print(f"Erro ao ativar cor RGB: {e}")

############################################################################################################