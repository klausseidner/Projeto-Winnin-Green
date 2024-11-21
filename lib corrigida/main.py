############################################################################################################
# Arquivo principal do projeto
############################################################################################################
############################################################################################################
# Importando as bibliotecas necessárias
############################################################################################################
from ardudeck import OLEDDisplay # Bibliotecas para controlar o Arduino, o sensor AHT10, e o display OLED
from rotinas import Estufa # Biblioteca com as rotinas para a estufa
import time # Biblioteca para gerenciar o tempo

############################################################################################################
# Configurações
############################################################################################################
display = OLEDDisplay() # Inicializa o display OLED
rgb_red = "ON" # Define a cor vermelha do RGB
rgb_green = "OFF" # Define a cor verde do RGB
rgb_blue = "OFF" # Define a cor azul do RGB

############################################################################################################
# Inicia a rotina de monitoramento e controle
############################################################################################################
def main():
    try:
        while True: # Entrando no loop infinito
            estufa = Estufa() # Inicializa a rotina de monitoramento e controle da estufa
            solo = estufa.solo() # Obtém umidade do solo
            temperatura = estufa.temperatura() # Obtém temperatura ambiente
            ar = estufa.ar() # Obtém a concentração de ar
            iluminacao = estufa.iluminacao() # Obtém a intensidade da luz solar
            chamas = estufa.chamas() # Obtém a presença de chamas
            porta = estufa.porta() # Obtém a presença de péssima condição
            
            # Mostra os dados no display OLED
            display.clear() # Limpa o display OLED
            display.show_text("Umidade do solo: {:.2f}%".format(solo), 0, 0) # Mostra a umidade do solo
            display.show_text("Temperatura: {:.2f}°C".format(temperatura), 0, 16) # Mostra a temperatura ambiente
            display.show_text("Concentração de ar: {:.2f}%".format(ar), 0, 32) # Mostra a concentração de ar
            time.sleep(2) # Pausa para mostrar os dados
            display.clear() # Limpa o display OLED
            display.show_text("Iluminacao: {:.2f} Lux".format(iluminacao), 0, 48) # Mostra a intensidade da luz solar
            display.show_text("Chamas: {}".format("Sim" if chamas else "Não"), 0, 64) # Mostra a presença de chamas
            display.show_text("Porta: {}".format("Aberto" if porta else "Fechado"), 0, 80) # Mostra a presença de péssima condição
            display.show_text("Cor RGB: R: {}, G: {}, B: {}".format(rgb_red, rgb_green, rgb_blue), 0, 96) # Mostra a cor
            time.sleep(2) # Pausa para mostrar os dados
            estufa.rgb(rgb_red, rgb_green, rgb_blue) # Liga ou desliga a cor RGB

    except KeyboardInterrupt: # Captura a interrupção do teclado (Ctrl+C)
        print("Encerrado pelo usuário.") # Exibe uma mensagem de encerramento
    finally:
        display.clear() # Limpa o display OLED
        # Fechamos a conexão com o Arduino
        estufa.arduino.close() # Fecha a conexão serial com o Arduino
        print("Rotina de monitoramento e controle encerrada.") # Exibe uma mensagem de encerramento


############################################################################################################
# Executa a rotina de monitoramento e controle
############################################################################################################
if __name__ == "__main__": # Executa o código apenas se este arquivo for o principal
    main() # Executa a rotina de monitoramento e controle

############################################################################################################