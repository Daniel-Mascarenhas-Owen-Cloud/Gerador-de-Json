import shutil
import os
import json
import sys

os.makedirs("saida", exist_ok=True)


tipo_smartlogger = sys.argv[1].upper()
usina = sys.argv[2]
prefix_usina = sys.argv[3]
skid = sys.argv[4]
IP = sys.argv[5]
slaveID = sys.argv[6]
quantidade_inversores = (
    int(sys.argv[7])
    if len(sys.argv) > 7
    else int(input("Quantos inversores existem neste SmartLogger? "))
)
quantidade_smartloggers = (
    int(sys.argv[8])
    if len(sys.argv) > 8
    else int(input("Quantos SmartLoggers existem? "))
)


while((tipo_smartlogger != 'A') and (tipo_smartlogger != 'C') and (tipo_smartlogger != 'E')):
    print("Tipo inválido!")
    tipo_smartlogger = input("Qual o tipo do smartlogger?\n")

tipo = "Smart_TIPO_" + tipo_smartlogger

# Criar arquivo Json com inicio padrão
shutil.copy("Smarts/" + tipo + "/" + tipo + ".json", "saida/" )
destino = f"saida/smartlogger{skid}.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/" + tipo + ".json", destino)

with open(f"saida/smartlogger{skid}.json", "r", encoding="utf-8") as f:
    smartJson = json.load(f)

with open("Smarts/Genericos.json", "r", encoding="utf-8") as f:
    smartJson_generico = json.load(f)

    smartJson["dataPoints"].extend(smartJson_generico["dataPoints"])

    with open("Smarts/EstadosInversoresSmart.json", "r", encoding="utf-8") as f:
        pontos_inversores = json.load(f)

    estados = {
        "Produzindo": "Produzindo",
        "Disponíveis": "Disponivel",
        "Sem Comunicação": "Sem Comunicação",
        "Parados": "Parado"
    }

    for ponto in pontos_inversores["dataPoints"]:
        estado_total = ponto["xid"].split("Inversores ", 1)[1]
        estado_inversor = estados[estado_total]
        contexto = []

        for inversor in range(1, quantidade_inversores + 1):
            contexto.append({
                "varName": f"inv{inversor}",
                "dataPointXid": (
                    f"USN_Inv_1.{inversor}_STA_{estado_inversor}"
                )
            })

        ponto["pointLocator"]["context"] = contexto

        soma = " + ".join(
            f"inv{inversor}.value"
            for inversor in range(1, quantidade_inversores + 1)
        )
        ponto["pointLocator"]["script"] = f"return {soma};"

    smartJson["dataPoints"].extend(pontos_inversores["dataPoints"])

    if tipo_smartlogger == "E":
        xid_fator_mensal = "USN_CAL_Fator de Capacidade Mensal 1"
        xid_fator_anual = "USN_CAL_Fator de Capacidade Anual 1"

        for ponto in smartJson["dataPoints"]:
            if ponto.get("xid") == xid_fator_mensal:
                ponto["enabled"] = False

            if ponto.get("xid") == xid_fator_anual:
                ponto["loggingType"] = "ON_CHANGE"
                ponto["intervalLoggingPeriod"] = 15

with open(f"saida/smartlogger{skid}.json", "w", encoding="utf-8") as f:
    json.dump(smartJson, f, indent=3, ensure_ascii=False)


# Ler arquivo original
with open(f"saida/smartlogger{skid}.json", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
conteudo = ( 
    conteudo
        .replace("USN", prefix_usina)
        .replace("Nome Usina",usina)
        .replace("000.000.000.000", IP)
        .replace("Skid x", "Skid " + skid)
        .replace("_SMART1","_SMART" + skid)
        .replace("Smart1","Smart" + skid)
        .replace("VIR_Capacidade Instalada 1","VIR_Capacidade Instalada " + skid)
        .replace("Diário 1","Diário " + skid)
        .replace("Mensal 1","Mensal " + skid)
        .replace("Anual 1","Anual " + skid)
        .replace('"slaveId": 1', f'"slaveId": {slaveID}')
        .replace("Sistema 1","Sistema " + skid)
    )

# Sobrescrever o arquivo original
with open(f"saida/smartlogger{skid}.json", "w", encoding="utf-8") as f:
    f.write(conteudo)


# Gerar os totais de estados de todos os SmartLoggers da usina
with open("Smarts/EstadoDosInversores.json", "r", encoding="utf-8") as f:
    estado_inversores = json.load(f)

for ponto in estado_inversores["dataPoints"]:
    estado = ponto["xid"].split("Inversores ", 1)[1]
    contexto = []

    for smart in range(1, quantidade_smartloggers + 1):
        contexto.append({
            "varName": f"smart{smart}",
            "dataPointXid": (
                f"{prefix_usina}_Smart{smart}_STA_Inversores {estado}"
            )
        })

    ponto["pointLocator"]["context"] = contexto
    soma = " + ".join(
        f"smart{smart}.value"
        for smart in range(1, quantidade_smartloggers + 1)
    )
    ponto["pointLocator"]["script"] = f"return {soma};"

texto_estados = json.dumps(
    estado_inversores,
    indent=3,
    ensure_ascii=False
).replace("USN", prefix_usina)
texto_estados = texto_estados.replace(
    "1.7976931348623157e+308",
    "1.7976931348623157E308"
)

with open("saida/EstadoDosInversores.json", "w", encoding="utf-8") as f:
    f.write(texto_estados)

print(f"Arquivo Json gerado em saida/smartlogger{skid}.json!")
print("Estado dos inversores gerado em saida/EstadoDosInversores.json!")
