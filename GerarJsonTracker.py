import json
import copy
import math
import os
import shutil
import sys

tipo_tracker = sys.argv[1].strip().upper()
nome_usina = sys.argv[2].strip()
prefixo = sys.argv[3].strip()
ncu_num = sys.argv[4].strip()
IP = sys.argv[5].strip()
qtd_trackers = int(sys.argv[6])


destino = "saida/tracker.json"
if os.path.exists(destino):
    os.remove(destino)
# Criar arquivo Json com inicio padrão
os.makedirs("saida", exist_ok=True)
os.makedirs("temp", exist_ok=True)

shutil.copy("base/inicio.json", "saida/" )

os.rename("saida/inicio.json", destino)

tipo = "Trackers_Tipo_" + tipo_tracker 
endereco_DataSource = "Trackers/" + tipo + "/DataSource.json"

quantos_DataSources = math.ceil(qtd_trackers / 20 )

for i in range(quantos_DataSources): 

    if i>0:
        with open("saida/tracker.json", "a", encoding="utf-8") as destino:
            destino.write(",")
    
    shutil.copy(endereco_DataSource, "temp/" )

    start = 1+(20*i)
    end = (i+1)*20

    with open("temp/DataSource.json", "r", encoding="utf-8") as f:
        conteudo = f.read()

    conteudo = ( 
        conteudo
        .replace("_NCU1","_NCU" + ncu_num)
        .replace("_1a20","_" + str(start) + "a" + str(end)) 
        .replace("000.000.000.000", IP)
        .replace("USN", prefixo)
        )


    with open("saida/tracker.json", "a", encoding="utf-8") as destino:
            destino.write(conteudo)

            
with open("saida/tracker.json", "a", encoding="utf-8") as destino:
    with open("Base/fim.json", "r", encoding="utf-8") as origem:
        destino.write(origem.read())



# ====== LEITURA DO JSON BASE ======
with open(f"Trackers/Trackers_Tipo_{tipo_tracker}/Trackers_Tipo_{tipo_tracker}.json", "r", encoding="utf-8") as f:
    base_json = json.load(f)

base_datapoints = base_json["dataPoints"]

novo_json = {"dataPoints": []}

# ====== FUNÇÕES AUXILIARES ======
def datasource_por_tracker(tracker):
    inicio = ((tracker - 1) // 20) * 20 + 1
    fim = inicio + 19
    return f"{prefixo}_NCU{ncu_num}_A_{inicio}a{fim}"

# ====== PROCESSAMENTO ======
for tracker in range(1, qtd_trackers + 1):
    for dp in base_datapoints:
        novo_dp = copy.deepcopy(dp)
        novo_dp["discardHighLimit"] = 1.7976931348623157E308
        novo_dp["discardLowLimit"] = -1.7976931348623157E308

        # ====== XID / NAME ======
        novo_dp["xid"] = (
            novo_dp["xid"]
            .replace("USN", prefixo)
            .replace("TRK_1.1", f"TRK_{ncu_num}.{tracker}")
        )

        novo_dp["name"] = (
            novo_dp["name"]
            .replace("USN", prefixo)
            .replace("TRK_1.1", f"TRK_{ncu_num}.{tracker}")
        )

        # ====== DATASOURCE ======
        novo_dp["dataSourceXid"] = datasource_por_tracker(tracker)
        novo_dp["deviceName"] = datasource_por_tracker(tracker)

        # ====== OFFSET ======
        novo_dp["pointLocator"]["offset"] += (tracker - 1) * 22

        # ====== EVENT DETECTORS ======
        for ed in novo_dp.get("eventDetectors", []):
            ed["xid"] = (
                ed["xid"]
                .replace("USN", prefixo)
                .replace("TRK_1.1", f"TRK_{ncu_num}.{tracker}")
            )

            ed["alias"] = (
                ed["alias"]
                .replace("Nome", nome_usina)
                .replace("NCU 1", f"NCU {ncu_num}")
                .replace("Tracker 1", f"Tracker {tracker}")
            )

        novo_json["dataPoints"].append(novo_dp)

# ====== GRAVAÇÃO DO ARQUIVO ======
# with open("Trackers_Tipo_A_GERADO.json", "w", encoding="utf-8") as f:
#     json.dump(novo_json, f, indent=3, ensure_ascii=False)



with open("saida/tracker.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

dados["dataPoints"] = []
dados["dataPoints"] = novo_json["dataPoints"]

with open(f"saida/tracker{ncu_num}.json", "w", encoding="utf-8") as f:
     json.dump(dados, f, indent=3, ensure_ascii=False)


shutil.rmtree("temp")

print("\n✅ JSON gerado com sucesso!")
