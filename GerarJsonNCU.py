import shutil
import os
import sys
import json
import copy
import math

os.makedirs("temp/saida", exist_ok=True)
os.makedirs("saida", exist_ok=True)

tipo_NCU = sys.argv[1].upper()
usina = sys.argv[2]
prefix_usina = sys.argv[3]
NCU = sys.argv[4]
IP = sys.argv[5]


while(tipo_NCU != 'A' and tipo_NCU != 'B' and tipo_NCU != 'C'):
    print("Tipo inválido!")
    tipo_NCU = input("Qual o tipo do NCU?\n")

tipo = "NCU_TIPO_" + tipo_NCU

# Criar arquivo Json com inicio padrão
shutil.copy("NCU/" + tipo + f"/{tipo}.json", "saida/" )
destino = f"saida/NCU{NCU}.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/" + tipo + ".json", destino)


if tipo_NCU == "C":
    quantidade_trackers = int(sys.argv[6])
    motores_por_tracker = [int(valor) for valor in sys.argv[7:]]

    if len(motores_por_tracker) != quantidade_trackers:
        raise ValueError(
            "Informe a quantidade de motores de cada tracker da NCU tipo C."
        )

    with open(destino, "r", encoding="utf-8") as f:
        json_ncu = json.load(f)

    with open(
        "NCU/NCU_TIPO_C/Trackers.json",
        "r",
        encoding="utf-8"
    ) as f:
        trackers = json.loads("[" + f.read() + "]")

    with open(
        "NCU/NCU_TIPO_C/Motores.json",
        "r",
        encoding="utf-8"
    ) as f:
        motores_base = json.load(f)

    datapoints_auxiliares_skc = [
        ponto
        for ponto in trackers
        if ponto["xid"].startswith("USN_TRK_1.1_STA_Monitor")
        or ponto["xid"].startswith("USN_TRK_1.1_VIR_")
    ]

    # O arquivo contém os trackers expandidos da referência original.
    # Os quatro primeiros datapoints formam o modelo do Tracker 1.
    trackers_base = trackers[:4]

    datasource_ncu = json_ncu["dataSources"][0]
    for indice_grupo in range(math.ceil(quantidade_trackers / 10)):
        inicio_grupo = indice_grupo * 10 + 1
        fim_grupo = inicio_grupo + 9
        datasource_motores = copy.deepcopy(datasource_ncu)
        xid_datasource_motores = (
            f"USN_NCU1_C_{inicio_grupo}a{fim_grupo}"
        )
        datasource_motores["xid"] = xid_datasource_motores
        datasource_motores["name"] = xid_datasource_motores
        datasource_motores["port"] = 505 + indice_grupo
        datasource_motores["timeout"] = 5000
        json_ncu["dataSources"].append(datasource_motores)

    for numero_tracker in range(1, quantidade_trackers + 1):
        for tracker_base in trackers_base:
            tracker = copy.deepcopy(tracker_base)

            tracker["xid"] = tracker["xid"].replace(
                "TRK_1.1", f"TRK_1.{numero_tracker}"
            )
            tracker["name"] = tracker["name"].replace(
                "TRK_1.1", f"TRK_1.{numero_tracker}"
            )

            incremento_offset = 15 if "Velocidade do Vento" in tracker["xid"] else 23
            tracker["pointLocator"]["offset"] += (
                numero_tracker - 1
            ) * incremento_offset
            tracker["pointLocator"]["slaveId"] = numero_tracker

            for detector in tracker.get("eventDetectors", []):
                detector["xid"] = detector["xid"].replace(
                    "TRK_1.1", f"TRK_1.{numero_tracker}"
                )
                detector["alias"] = detector["alias"].replace(
                    "SKC 1", f"SKC {numero_tracker}"
                )

            json_ncu["dataPoints"].append(tracker)

        for auxiliar_base in datapoints_auxiliares_skc:
            auxiliar = copy.deepcopy(auxiliar_base)
            texto_auxiliar = json.dumps(auxiliar, ensure_ascii=False)
            texto_auxiliar = (
                texto_auxiliar
                .replace("TRK_1.1", f"TRK_1.{numero_tracker}")
                .replace("SKC 1", f"SKC {numero_tracker}")
            )
            auxiliar = json.loads(texto_auxiliar)

            if "slaveId" in auxiliar.get("pointLocator", {}):
                auxiliar["pointLocator"]["slaveId"] = numero_tracker

            json_ncu["dataPoints"].append(auxiliar)

        for numero_motor in range(1, motores_por_tracker[numero_tracker - 1] + 1):
            for motor_base in motores_base:
                motor = copy.deepcopy(motor_base)
                identificador_base = "TRK_1.1.1"
                identificador_motor = (
                    f"TRK_1.{numero_tracker}.{numero_motor}"
                )
                motor["xid"] = motor["xid"].replace(
                    identificador_base, identificador_motor
                )
                motor["name"] = motor["name"].replace(
                    identificador_base, identificador_motor
                )

                if "Posição Atual" in motor["xid"]:
                    motor["pointLocator"]["offset"] += (
                        (numero_tracker - 1) * 15 + numero_motor - 1
                    )
                else:
                    motor["pointLocator"]["offset"] += (
                        (numero_tracker - 1) * 23 + (numero_motor - 1) * 2
                    )

                inicio_grupo = ((numero_tracker - 1) // 10) * 10 + 1
                fim_grupo = inicio_grupo + 9
                datasource_motores = (
                    f"USN_NCU1_C_{inicio_grupo}a{fim_grupo}"
                )
                motor["dataSourceXid"] = datasource_motores
                motor["deviceName"] = datasource_motores
                motor["pointLocator"]["slaveId"] = numero_tracker

                for detector in motor.get("eventDetectors", []):
                    detector["xid"] = detector["xid"].replace(
                        identificador_base, identificador_motor
                    )
                    detector["alias"] = (
                        detector["alias"]
                        .replace("SKC 1", f"SKC {numero_tracker}")
                        .replace("Motor 1", f"Motor {numero_motor}")
                    )

                json_ncu["dataPoints"].append(motor)

    with open(destino, "w", encoding="utf-8") as f:
        json.dump(json_ncu, f, indent=3, ensure_ascii=False)




# Ler arquivo original
with open(f"saida/NCU{NCU}.json", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
conteudo = ( 
    conteudo
        .replace("USN", prefix_usina)
        .replace("Nome Usina", usina)
        .replace("000.000.000.000", IP)
        .replace("NCU1", f"NCU{NCU}")
        .replace("NCU x", f"NCU {NCU}")
        .replace("NCU 1", f"NCU {NCU}")
        .replace("TRK_1.", f"TRK_{NCU}.")
        .replace("Nome da Usina", usina)
        .replace("e+308", "E308")
    )

# Sobrescrever o arquivo original
with open(f"saida/NCU{NCU}.json", "w", encoding="utf-8") as f:
    f.write(conteudo)

# Apagar temp
shutil.rmtree("temp")

print(f"Arquivo Json gerado em saida/NCU{NCU}.json!")
