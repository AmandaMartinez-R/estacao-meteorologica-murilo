import json
import os
import time

import requests
import serial
import serial.tools.list_ports

from serial_config import PORTA_FALLBACK, BAUD, URL

def escolher_porta():
    env = os.environ.get('SERIAL_PORT', '').strip()
    if env:
        return env
    for p in serial.tools.list_ports.comports():
        dev = p.device
        if 'ttyACM' in dev or 'ttyUSB' in dev:
            return dev
    return PORTA_FALLBACK


def listar_portas():
    portas = list(serial.tools.list_ports.comports())
    if not portas:
        print('Nenhuma porta serial encontrada.')
        return
    print('Portas disponíveis:')
    for p in portas:
        print(f"  {p.device} — {p.description}")


def ler_serial():
    porta = escolher_porta()
    print(f"Abrindo {porta} a {BAUD} baud → POST {URL}")
    print('(Ctrl+C para sair)\n')

    try:
        ser = serial.Serial(porta, BAUD, timeout=2)
    except serial.SerialException as e:
        print(f'Erro ao abrir a porta: {e}\n')
        listar_portas()
        print('\nDica: export SERIAL_PORT=/dev/ttyACM0  # ou a porta do seu Arduino')
        raise SystemExit(1) from e

    ultimo_aviso = time.monotonic()
    with ser:
        while True:
            try:
                raw = ser.readline()
            except serial.SerialException as e:
                print(f'Erro de leitura serial: {e}')
                time.sleep(1)
                continue

            linha = raw.decode('utf-8', errors='replace').strip()
            agora = time.monotonic()

            if linha:
                ultimo_aviso = agora
                try:
                    dados = json.loads(linha)
                    response = requests.post(URL, json=dados, timeout=5)
                    print(f'Enviado: {dados} | HTTP {response.status_code}')
                except json.JSONDecodeError:
                    print(f'Linha inválida (não é JSON): {linha}')
                except requests.RequestException as e:
                    print(f'Falha ao enviar para a API: {e}')
            elif agora - ultimo_aviso >= 15:
                print('(aguardando linha na serial — verifique cabo, porta e se o sketch está enviando JSON)')
                ultimo_aviso = agora

            time.sleep(0.05)


if __name__ == '__main__':
    try:
        ler_serial()
    except KeyboardInterrupt:
        print('\nEncerrado.')
