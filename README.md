# Ponderada Estação Metorológica

## Objetivo:

O objetivo central é construir um sistema completo de ponta a ponta: um dispositivo físico
simulando uma estação meteorológica envia dados para um servidor web, que os armazena em
banco de dados e os disponibiliza em uma interface de visualização.

Ao concluir esta atividade, o estudante terá desenvolvido um sistema real de IoT (Internet das
Coisas), com comunicação serial, API REST, banco de dados relacional e interface web
responsiva.

## Firmware (Arduino IDE)

O sketch está em `src/firmware/firmware.ino`. Use a [Arduino IDE](https://www.arduino.cc/en/software) 2.x (recomendado) ou 1.8.x.

### 1. Abrir o projeto

- **Arquivo → Abrir…** e selecione `src/firmware/firmware.ino` neste repositório.

### 2. Instalar a biblioteca do sensor

O código usa a biblioteca **DHT sensor library** (Adafruit).

- **Ferramentas → Gerenciar bibliotecas…**
- Busque por **DHT sensor library** (autor Adafruit).
- Clique em **Instalar**. Se pedir dependência **Adafruit Unified Sensor**, instale também.

### 3. Placa e porta

- **Ferramentas → Placa** — escolha o modelo conectado (ex.: *Arduino Uno*).
- **Ferramentas → Porta** — escolha a porta USB da placa (no Linux costuma ser `/dev/ttyACM0` ou `/dev/ttyUSB0`).

Se a porta não aparecer ou der erro de permissão no Linux, adicione o usuário ao grupo `dialout`, faça logout/login e reconecte o cabo:

```bash
sudo usermod -aG dialout $USER
```

### 4. Compilar e enviar

- **Verificar** (ícone ✓) compila o sketch.
- **Carregar** (ícone →) compila e grava o firmware na placa.

### 5. Monitor serial

- **Ferramentas → Monitor Serial** (ou ícone da lupa à direita na IDE 2).
- Ajuste a taxa para **9600 baud** (canto inferior direito do monitor, na IDE 2), igual ao `Serial.begin(9600)` do sketch.

---

## Arduino CLI (opcional)

Se preferir linha de comando, instale o [arduino-cli](https://arduino.cc/cli) e use, por exemplo:

```bash
arduino-cli core update-index && arduino-cli core install arduino:avr
arduino-cli lib install "DHT sensor library"
cd src/firmware
arduino-cli compile --fqbn arduino:avr:uno .
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno .
arduino-cli monitor -p /dev/ttyACM0 -c baudrate=9600
```

Substitua `arduino:avr:uno` e a porta conforme a sua placa (`arduino-cli board list`).

1 - criação da tabela em "schema.sql"
2 - coração do banco de dados e seu funcionamento (conexão com o banco)
3 - inicialização do banco 
4 - CRUD
    4.1 - cria o comando de create (inserir novos dados)
    4.2 - cria o comando de listar
    4.3 - cria o comando de buscar
    4.4 - cria o comando update
    4.5 - cria o comando delete

5 - cria o arquivo teste_db.py para testar o comando create do CRUD e verificar o funcionamento do banco de dados com dados imaginários