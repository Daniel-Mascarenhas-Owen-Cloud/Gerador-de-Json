import copy
import json
import math
import os
import sys


tipo_combiner = sys.argv[1].strip().upper()
nome_usina = sys.argv[2].strip()
prefixo = sys.argv[3].strip()
skid = sys.argv[4].strip()
ip = sys.argv[5].strip()
cbx_quantidade = int(sys.argv[6])
slave_ids = [int(slave_id.strip()) for slave_id in sys.argv[7].split(",") if slave_id.strip()]

if len(slave_ids) != cbx_quantidade:
    print("Quantidade de slaveIds diferente da quantidade de Combiner Boxes.")
    sys.exit(1)

os.makedirs("saida", exist_ok=True)

base_path = os.path.join("Combiner Box", f"CBX_{tipo_combiner}.json")
destino = f"saida/combinerbox{skid}.json"

if not os.path.exists(base_path):
    print(f"Tipo de Combiner Box invalido: {tipo_combiner}")
    sys.exit(1)

with open(base_path, "r", encoding="utf-8") as f:
    base_json = json.load(f)


def substituir_strings(valor, cbx_numero):
    if isinstance(valor, str):
        return (
            valor
            .replace("USN", prefixo)
            .replace("Nome Usina", nome_usina)
            .replace("SMART1", f"SMART{skid}")
            .replace("CBX_1.1", f"CBX_{skid}.{cbx_numero}")
            .replace("Inv_1.1", f"Inv_{skid}.{cbx_numero}")
            .replace("000.000.000.000", ip)
        )

    if isinstance(valor, list):
        return [substituir_strings(item, cbx_numero) for item in valor]

    if isinstance(valor, dict):
        return {chave: substituir_strings(item, cbx_numero) for chave, item in valor.items()}

    return valor


def datasource_por_cbx(cbx_numero):
    inicio = ((cbx_numero - 1) // 5) * 5 + 1
    fim = inicio + 4
    return f"{prefixo}_SMART{skid}_CBX_{tipo_combiner}_{inicio}a{fim}"


novo_json = {
    "dataSources": [],
    "dataPoints": [],
}

base_datasource = base_json["dataSources"][0]
quantos_datasources = math.ceil(cbx_quantidade / 5)

for i in range(quantos_datasources):
    inicio = 1 + (5 * i)
    fim = (i + 1) * 5
    datasource_xid = f"{prefixo}_SMART{skid}_CBX_{tipo_combiner}_{inicio}a{fim}"

    novo_ds = copy.deepcopy(base_datasource)
    novo_ds = substituir_strings(novo_ds, inicio)
    novo_ds["xid"] = datasource_xid
    novo_ds["name"] = datasource_xid
    novo_ds["host"] = ip

    novo_json["dataSources"].append(novo_ds)

for i in range(cbx_quantidade):
    cbx_numero = i + 1
    datasource_xid = datasource_por_cbx(cbx_numero)

    for datapoint in base_json["dataPoints"]:
        novo_dp = copy.deepcopy(datapoint)
        novo_dp = substituir_strings(novo_dp, cbx_numero)

        if novo_dp.get("dataSourceXid") != f"{prefixo}_Time Stamps":
            novo_dp["dataSourceXid"] = datasource_xid
            novo_dp["deviceName"] = datasource_xid

        point_locator = novo_dp.get("pointLocator", {})
        if "slaveId" in point_locator:
            point_locator["slaveId"] = slave_ids[i]

        novo_json["dataPoints"].append(novo_dp)

with open(destino, "w", encoding="utf-8") as f:
    json.dump(novo_json, f, indent=3, ensure_ascii=False)

with open(destino, "r", encoding="utf-8") as f:
    conteudo = f.read()

conteudo = conteudo.replace(
    "1.7976931348623157e+308",
    "1.7976931348623157E308"
)
conteudo = conteudo.replace("e+308", "E308")

with open(destino, "w", encoding="utf-8") as f:
    f.write(conteudo)

print(f"Arquivo Json gerado em {destino}!")
