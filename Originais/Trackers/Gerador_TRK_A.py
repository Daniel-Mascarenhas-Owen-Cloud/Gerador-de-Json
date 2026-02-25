import json
import copy
import math

# ====== CONFIGURAÇÃO DO ARQUIVO BASE ======
ARQUIVO_BASE = r"C:\Users\benny\OneDrive\Documentos\OWEN\COG\PADRONIZACAO\Trackers_Tipo_A.json"
ARQUIVO_SAIDA = r"C:\Users\benny\OneDrive\Documentos\OWEN\COG\PADRONIZACAO\Trackers_Tipo_A_GERADO.json"

# ====== INPUTS DO USUÁRIO ======
nome_usina = input("Qual o nome da usina? ").strip()
prefixo = input("Qual o prefixo? (ex: USN) ").strip()
ncu_num = input("Qual o número da NCU? ").strip()
qtd_trackers = int(input("Qual a quantidade de Trackers? "))

# ====== LEITURA DO JSON BASE ======
with open(ARQUIVO_BASE, "r", encoding="utf-8") as f:
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
                .replace("UFV Nome", nome_usina)
                .replace("NCU 1", f"NCU {ncu_num}")
                .replace("Tracker 1", f"Tracker {tracker}")
            )

        novo_json["dataPoints"].append(novo_dp)

# ====== GRAVAÇÃO DO ARQUIVO ======
with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(novo_json, f, indent=3, ensure_ascii=False)

print("\n✅ JSON gerado com sucesso!")
print(f"📄 Arquivo: {ARQUIVO_SAIDA}")
