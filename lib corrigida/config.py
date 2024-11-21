# Configurações do Arduino
arduino_port = "/dev/ttyUSB0"
speedrate = 9600
reconnect_interval = 5

# Mapa de canais
map = {
        "aht10": {"i2c": True},  # Comunicação I2C padrão (SDA e SCL) - Sensores de temperatura e umidade
        # Multiplexador 1 para sensores
        "ground": {"multiplexador": 1, "channel": 0},  # Sensor de umidade do solo
        "light": {"multiplexador": 1, "channel": 1},  # Sensor de luz
        "fire": {"multiplexador": 1, "channel": 2},  # Sensor de chama
        "magnetic": {"multiplexador": 1, "channel": 3},  # Sensor de magnetismo
        # Multiplexador 2 para atuadores
        "buzzer": {"multiplexador": 2,"channel": 0}, # Buzzer passivo
        "irrigation": {"multiplexador": 2, "channel": 1},  # Irrigação
        "fan": {"multiplexador": 2, "channel": 2},  # Ventilador
        "humidifier": {"multiplexador": 2, "channel": 3},  # Humidificador
        "lamp": {"multiplexador": 2, "channel": 4},  # Lâmpada
        "rgb_red": {"multiplexador": 2, "channel": 5},  # Cor vermelha
        "rgb_green": {"multiplexador": 2, "channel": 6},  # Cor verde
        "rgb_blue": {"multiplexador": 2, "channel": 7},  # Cor azul
    }