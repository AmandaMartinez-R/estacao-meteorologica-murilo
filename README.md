# Ponderada Estação Metorológica 🌦️

## Autores
- Amanda Cristina Martinez da Rosa
- Carlos Icaro Kauã Coelho Paiva


## Objetivo:

O objetivo central é construir um sistema completo de ponta a ponta: um dispositivo físico
simulando uma **estação meteorológica** envia dados para um servidor web, que os armazena em
banco de dados e os disponibiliza em uma interface de visualização.

Ao concluir esta atividade, o estudante terá desenvolvido um sistema real de IoT (Internet das
Coisas), com comunicação serial, API REST, banco de dados relacional e interface web
responsiva.

## Firmware (Arduino IDE) -  Como executar

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

## Arduino CLI (opcional) - Como executar

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

---

## Dependências Python e leitura serial (Arduino → API) - Como executar

O script `src/serial_reader.py` lê a porta serial onde o Arduino envia JSON (uma linha por leitura, como no firmware) e repassa os dados para a API com `POST` em `http://localhost:5000/leituras`. Para isso funcionar, é preciso instalar as bibliotecas listadas em `src/requirements.txt`.

### 1. Instalar o `requirements.txt`

Recomenda-se um ambiente virtual; na raiz do repositório:

```bash
python3 -m venv venv
source venv/bin/activate          # Linux/macOS
# ou, no Windows: venv\Scripts\activate

pip install -r src/requirements.txt
```

Isso instala **Flask**, **pyserial** e **requests**, usados pelo servidor e pelo leitor serial.

### 2. Subir o servidor antes do leitor serial

O `serial_reader.py` envia dados para o Flask. Em um terminal, dentro de `src/`:

```bash
cd src
python3 app.py
```

### 3. Rodar o leitor serial

Com a placa conectada e o firmware gravado, em **outro** terminal:

```bash
cd src
python3 serial_reader.py
```

Ajuste a constante `PORTA` em `serial_reader.py` conforme o sistema: no Linux costuma ser `/dev/ttyACM0` ou `/dev/ttyUSB0`; no Windows, algo como `COM3`. A taxa (`BAUD`) deve ser **9600**, igual ao sketch.

---

## Passo a passo realizado no projeto

O trabalho foi organizado em camadas: primeiro o modelo de dados e o acesso ao SQLite, depois testes locais do banco, em seguida a API Flask e, por fim, a ponte serial entre o Arduino e o servidor.

### Banco de dados (SQLite)

Foi definido o esquema relacional em `schema.sql`, com a tabela de leituras (temperatura, umidade, metadados e carimbo de tempo). Em `database.py` ficou o núcleo da persistência: função de conexão com o banco, `init_db()` para aplicar o script SQL na inicialização e as operações de **CRUD** — inserir leitura, listar (com limite), buscar por identificador, atualizar e excluir. O script `teste_db.py` valida o fluxo com dados fictícios, exercitando pelo menos a criação e a listagem.

### API REST (Flask)

Sobre essa base foi montada a API em `app.py`: estrutura Flask com templates para o painel, rota **GET /** como painel principal (e opção de resposta JSON), **GET /leituras** para listar todas as leituras, **POST /leituras** para receber novos registros (rota usada pelo Arduino, via `serial_reader.py` ou integração equivalente), `GET /leituras/<id>`, `PUT /leituras/<id>` e `DELETE /leituras/<id>` para consultar e alterar registros pontuais, além de **GET /api/estatisticas** para agregados. O servidor é executado com `python3 app.py` a partir da pasta `src/`, conforme a seção anterior.

### Firmware e integração física

O sketch em `src/firmware/firmware.ino` lê o sensor DHT e envia JSON pela serial; o `serial_reader.py` lê essa porta e encaminha as leituras para o **POST /leituras**, fechando o circuito entre hardware, backend e interface.