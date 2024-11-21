#########################################################################################################
# Classe para controle da estufa
#########################################################################################################
import time # Biblioteca para contagem de tempo
from controllers.arduino import ArduinoController # Importando a classe ArduinoController

#########################################################################################################
# Lista de canais de sensores e atuadores
#########################################################################################################
# Temperatura: Multiplexador 0, canal 0
# Umidade do ar: Multiplexador 0, canal 1
# Umidade do solo: Multiplexador 0, canal 2
# Chamas: Multiplexador 0, canal 0
# Buzzer: Multiplexador 1, canal 1
# Umidificação: Multiplexador 1, canal 2
# Irrigação: Multiplexador 1, canal 3
# Display: Multiplexador 2, canal 0, 1, 2, 3, 4
# Cooler: Multiplexador 2, canal 3
# Luz: Multiplexador 2, canal 4
# Porta: Multiplexador 2, canal 5
#
#########################################################################################################
# Classe para EstufaController
#########################################################################################################
class EstufaController:
    # Inicialização da classe
    def __init__(self, arduino_controller=None):
        """
        Inicializa a estufa com um controlador Arduino.
        """
        self.arduino_controller = ArduinoController("COM3") # Inicializa o controlador Arduino com a porta serial "/dev/ttyUSB0"

#########################################################################################################
    # Função para verificar sensor de temperatura
#########################################################################################################
    def temperatura(self):
        # Verificar sensor de temperatura
        return self.arduino_controller.get(multiplexador=1, canal=0)

#########################################################################################################
    # Função para verificar sensor de umidade do ar
#########################################################################################################
    def umidade_ar(self):
        return self.arduino_controller.get(multiplexador=1, canal=1)

#########################################################################################################
    # Função para verificar sensor de umidade do solo
#########################################################################################################
    def umidade_solo(self):
        return self.arduino_controller.get(multiplexador=1, canal=2)

#########################################################################################################
    # Função para verificar sensor de chamas
#########################################################################################################
    def chamas(self):
        # Verificar sensor de chamas através do arduino_controller
        flame_status = self.arduino_controller.get(multiplexador=1, canal=0)
        
        if flame_status == "1":  # Aqui você ajusta conforme o valor retornado pelo sensor
            self.arduino_controller.set(multiplexador=3, canal=0, comando="ON")
            time.sleep(3)
            self.arduino_controller.set(multiplexador=3, canal=0, comando="OFF")
            # Repita a sequência conforme necessário ou ajuste conforme o que deseja
        return flame_status


#########################################################################################################
    # Função para exibir dados no display OLED
#########################################################################################################
    def exibir(self):
        """
        Exibe as leituras dos sensores no display OLED.
        """
        temp = self.temperatura()
        umid_ar = self.umidade_ar()
        umid_solo = self.umidade_solo()
        flame = self.chamas()
        print(f"Temperatura: {temp}°C | Umidade Ar: {umid_ar}% | Umidade Solo: {umid_solo}% | Chamas: {flame}")

#########################################################################################################
    # Função para acionar o ventilador
#########################################################################################################
    def ventilador(self, comando="ON"):
        self.arduino_controller.set(multiplexador=2, canal=0, comando=comando)

#########################################################################################################
    # Função para acionar o sistema de irrigação
#########################################################################################################
    def bomba(self, comando="ON"):
        self.arduino_controller.set(multiplexador=2, canal=1, comando=comando)

#########################################################################################################
    # Função para acionar umudificador
#########################################################################################################
    def umidificador(self,  comando="ON"):
        self.arduino_controller.set(multiplexador=2, canal=2, comando=comando)

#########################################################################################################
    # Função para acionar a buzzer
#########################################################################################################
    def buzzer(self):
        self.arduino_controller.set(multiplexador=3, canal=0, comando="ON")
        time.sleep(3)
        self.arduino_controller.set(multiplexador=3, canal=0, comando="OFF")

#########################################################################################################
    # Função para verificar sensor de reserva de água
#########################################################################################################
    def reserva_agua(self):
        return self.arduino_controller.get(multiplexador=1, canal=3)

#########################################################################################################
    # Sensor de luz
#########################################################################################################
    def luz(self):
        return self.arduino_controller.get(multiplexador=2, canal=3)

#########################################################################################################
    # Função responsável por monitorar e controlar todos os sensores e atuadores
#########################################################################################################
    ### precisa ser inicializado no main loop
    ### Os dados precisam ser buscados do banco
    ### Implementar a capacidade ascincrona e comunicação com o Arduino
    def monitor(self):
        """
        Monitora e controla todos os sensores e atuadores da estufa.
        """
        while True:
            # Leitura dos sensores
            temperatura = self.temperatura()
            umidade_ar = self.umidade_ar()
            umidade_solo = self.umidade_solo()
            reserva_agua = self.reserva_agua()
            chamas = self.chamas()
            luz = self.luz()

            # Verificar se há chamas
            if chamas == True:
                # Ligar o buzzer
                self.buzzer()
                # Ligar o buzzer por 3 segundos
                time.sleep(3)
                # Ligar o buzzer
                self.buzzer()
                # Ligar o buzzer por 3 segundos
                time.sleep(3)
                # Ligar o buzzer
                self.buzzer()
                # Ligar o buzzer por 3 segundos
                time.sleep(3)

            # Exibir dados no display
            self.exibir()

            # Enviar dados para o dashboard
            ### necessita implementar para enviar os dados pelo model do home
            # Enviar dados para o dashboard

            # Aguardar 1 segundo
            time.sleep(1)

            # Verificar se a temperatura está abaixo do limite
            ### necessita implementar para buscar os dados pelo model da pant
            if temperatura < 25:
                # Ligar o ventilador
                self.ventilador()
            else:
                # Desligar o ventilador
                self.ventilador("OFF")

            # Verificar se a umidade do ar está acima do limite
            if umidade_ar > 70:
                # Ligar o sistema do umidificador
                self.umidificador()
            else:
                # Desligar o sistema do umidificador
                self.umidificador("OFF")

            # Verificar se a umidade do solo está acima do limite
            if umidade_solo > 60:
                # Ligar o irrigador
                self.irrigador()
            else:
                # Desligar o irrigador
                self.irrigador("OFF")

            # Verifica a reserva de água
            if reserva_agua == False:
                # Ligar a bomba
                self.bomba()

            # Verifica a luz
            if luz == True:
                # verifica a data e hora do sistema e com a ultima verificação da planta
                # atualiza o o contador de minuto do banco
                # verifica no banco se a planta nessecita de luz e aciona a luz se necessário
                # Zera o contador de minuto do banco
                print('ignore esse print, ja estava aqui, ignore!!')
#########################################################################################################