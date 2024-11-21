<p align="center">
  <img src="https://github.com/klausseidner/Projeto-Winnin-Green/blob/main/logo.png" width="10%" alt="
  logo">
</p>

<p align="center">
    <h1 align="center">
        WinninGreen (Estufas IoT)
    </h1>
</p>

<p align="center">
    <h3 align="center">
        ❯ O projeto de Estufa automatizada com Arduino é voltado para pequenos cultivadores que desejam cultivar plantas em casa, mas não dispõem de tempo suficiente para os cuidados necessários. ❮
    </h3>
</p>


## 🫵 Capturas de tela

![App Screenshot](https://github.com/klausseidner/Projeto-Winnin-Green/blob/main/capturas%20de%20tela/1.jpg)
![App Screenshot](https://github.com/klausseidner/Projeto-Winnin-Green/blob/main/capturas%20de%20tela/2.jpg)
![App Screenshot](https://github.com/klausseidner/Projeto-Winnin-Green/blob/main/capturas%20de%20tela/3.jpg)
![App Screenshot](https://github.com/klausseidner/Projeto-Winnin-Green/blob/main/capturas%20de%20tela/4.jpg)
![App Screenshot](https://github.com/klausseidner/Projeto-Winnin-Green/blob/main/capturas%20de%20tela/5.jpg)
![App Screenshot](https://github.com/klausseidner/Projeto-Winnin-Green/blob/main/capturas%20de%20tela/6.jpg)


## ⭐ Funcionalidades

- Controle de umidade do ar
- Controle de temperatura
- Controle de umidade do solo
- Volume de água no reservatório de irrigação
- Alerta de chamas
- Alarme de porta da estufa aberta
- Alarme sonoro
- Controle de luminosidade
- Iluminação para eventos (RGB)
- Gestão remota
- Multiplataforma

## 🧩 Tecnologias Utilizadas

- **Frontend**: HTML e javascript
- **Backend**: Python (Flask)
- **Banco de Dados**: SQLite
- **Hardware**: Arduino, modulo rele (8 canais), sensor de umidade de solo, sensor de umidade do ar, sensor de temperatura, sensor de chamas, sensor magnetico, bomba de agua, sensor de nivel de agua (boia para acionar um botão), sensor de iluminação, buzzer passivo, lampada, cooler, fonte 5v, fonte 12v, 2 multiplexadores e fita de led RGB.


## 📂 Estrutura do Projeto

```sh
└── PROJETO-WINNIN-GREEN
    ├── controllers
    │   ├── arduino.py
    │   ├── auth_controller.py
    │   ├── estufa.py
    │   ├── light_shedule.py
    │   └── plant.py
    ├── lib corrigida
    │   ├── ardudeck.py
    │   ├── config.py
    │   ├── main.py
    │   └── rotinas.py
    ├── models
    │   ├── auth_model.py
    │   ├── home.py
    │   ├── light_shedule.py
    │   ├── plants.py
    │   ├── sensors_data.py
    │   └── system_config.py
    ├── routes
    │   ├── auth.py
    │   ├── home.py
    │   └── plants.py
    ├── static
    │   ├── assets
    │   │   ├── css
    │   │   ├── fonts
    │   │   ├── img
    │   │   ├── js
    │   │   ├── scss
    │   │   ├── gulpfile.js
    │   │   └── package.json
    │   └── uploads
    ├── views
    │   ├── accounts
    │   ├── home
    │   ├── includes
    │   ├── layouts
    │   └── plant
    ├── .env
    ├── config.py
    ├── db.sqlite3
    ├── deployer.json
    ├── env.sample
    ├── extensions.py
    ├── log.json
    ├── logo.png
    ├── main.py
    ├── package.json
    ├── readme.MD
    ├── requeriments.txt
    └── utils.py
```


## 🚀 Instalação

Instale os requirimentos (requirements.txt)

```bash
  pip install -r requirements.txt
```

Inicie a aplicação (main.py)
```bash
python3 ./main.py
```


## 📦 Instruções de uso

Acesse do seu navegador de preferência http://127.0.0.1:5000/

Faça o registro do seu usuário (recomendamos deletar a rota de registro após a instalação)

Efetue o login!

E desfrute do melhor da sua estufa Iot!


## 📚 Referência

 - [Flávio Guimarães (Expert em Programação em Arduino)](https://brincandocomideias.com.br/)
 - [Automatização e monitoramento de uma estufa de alface](https://ric.cps.sp.gov.br/handle/123456789/7434)
 - [Internet das coisas (IoT) aplicada para resolução de desafios](https://www.escolavirtual.gov.br/curso/534)
 - [Ardudeck](https://github.com/klausseidner/ardudeck/)


## 🤝 Autores

- [@klausseidner](https://www.github.com/klausseidner)
- [@Pedrohbar](https://github.com/Pedrohbar)

**Orientador**: Prof. Andre Przewodowski Filho

**Instituição de ensino**: Universidade Estácio de Sá, Campus Niterói


## 📌 Documentação

[O código está todo comentado para facilitar o uso.](#)


## 🎗 Licença

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)
