import re

def formatar_tempo(tempo_segundos):
    tempo_segundos = int(tempo_segundos)

    horas = tempo_segundos // 3600
    minutos = (tempo_segundos % 3600) // 60
    segundos = tempo_segundos % 60

    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def calcular_pace(tempo_segundos, distancia_km):
    pace_segundos = round (tempo_segundos / distancia_km)
    return formatar_tempo(pace_segundos)

def transformar_tempo_em_segundos(tempo):
    if not tempo:
        raise ValueError("Informe o tempo do treino")

    partes = tempo.split(":")

    if len(partes) != 3:
        raise ValueError("Informe o tempo no formato HH:MM:SS")

    try:
        horas = int(partes[0])
        minutos = int(partes[1])
        segundos = int(partes[2])
    except ValueError:
        raise ValueError("Informe o tempo usando apenas números no formato HH:MM:SS")

    if minutos < 0 or minutos > 59:
        raise ValueError("Os minutos devem estar entre 00 e 59")

    if segundos < 0 or segundos > 59:
        raise ValueError("Os segundos devem estar entre 00 e 59")

    tempo_segundos = horas * 3600 + minutos * 60 + segundos

    if tempo_segundos <= 0:
        raise ValueError("O tempo precisa ser maior que zero")

    return tempo_segundos

def formatar_data(data):
    return data.strftime("%d/%m/%Y")

import re

def verificar_senha(senha):
    if len(senha) <= 8:
        return False, "A senha precisa ter pelo menos 8 caracteres"

    if re.search(r"[A-Z]", senha) is None:
        return False, "A senha precisa ter pelo menos uma letra maiúscula"

    if re.search(r"[a-z]", senha) is None:
        return False, "A senha precisa ter pelo menos uma letra minúscula"

    if re.search(r"[0-9]", senha) is None:
        return False, "A senha precisa ter pelo menos um número"

    return True, ""

def formatar_distancia(distancia):
    return f"{float(distancia):.2f}".replace(".", ",")


if __name__ == "__main__":
    print(calcular_pace(1800, 5))
    print(calcular_pace(1530, 5))
    print(calcular_pace(2700, 10))