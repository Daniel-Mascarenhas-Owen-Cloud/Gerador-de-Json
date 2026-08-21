import shutil
import os
import json
import sys

os.makedirs("saida", exist_ok=True)

tipo_Multimedidor = sys.argv[1].upper()
usina = sys.argv[2]
prefix_usina = sys.argv[3]
cabine = sys.argv[4]
IP = sys.argv[5]
slave_id = sys.argv[6]


while(tipo_Multimedidor != 'A' and tipo_Multimedidor != 'C' and tipo_Multimedidor != 'D'):
    print("Tipo inválido!")
    tipo_Multimedidor = input("Qual o tipo do Multimedidor?\n")

tipo = "Multimedidor_TIPO_" + tipo_Multimedidor

# Criar arquivo Json com inicio padrão
shutil.copy("Multimedidor/" + tipo + "/" + tipo + ".json", "saida/" )
destino = f"saida/Multimedidor{cabine}.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/" + tipo + ".json", destino)

with open(f"saida/Multimedidor{cabine}.json", "r", encoding="utf-8") as f:
    smartJson = json.load(f)

# Os PRs são adicionados a qualquer tipo de multimedidor suportado.
with open("Configuracao/JsonsConfig/PRMultimedidor.json", "r", encoding="utf-8") as f:
    template_pr_multimedidor = json.load(f)

smartJson["dataPoints"].extend(template_pr_multimedidor["dataPoints"])

if tipo_Multimedidor in ("A", "D"):
    with open("Configuracao/JsonsConfig/EnergiaDiariaMultimedidorAD.json", "r", encoding="utf-8") as f:
        template_energia_diaria_tipo_ad = json.load(f)

    smartJson["dataPoints"].extend(template_energia_diaria_tipo_ad["dataPoints"])

with open(f"saida/Multimedidor{cabine}.json", "w", encoding="utf-8") as f:
    json.dump(smartJson, f, indent=3, ensure_ascii=False)


# Ler arquivo original
with open(f"saida/Multimedidor{cabine}.json", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
conteudo = ( 
    conteudo
        .replace("USN", prefix_usina)
        .replace("Nome Usina",usina)
        .replace("000.000.000.000", IP)
        .replace("MM1","MM" + cabine)
        .replace("Cabine 1", "Cabine " + cabine)
        .replace('"slaveId":1', '"slaveId":' + slave_id)
        .replace(
            "1.7976931348623157e+308",
            "1.7976931348623157E308"
        )
        .replace("e+308", "E308")
    )

# Sobrescrever o arquivo original
with open(f"saida/Multimedidor{cabine}.json", "w", encoding="utf-8") as f:
    f.write(conteudo)

print(f"Arquivo Json gerado em saida/Multimedidor{cabine}.json!")
