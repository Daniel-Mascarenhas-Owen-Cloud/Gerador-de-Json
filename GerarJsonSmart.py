import shutil
import os
import json

os.makedirs("saida", exist_ok=True)

tipo_smartlogger = input("Qual o tipo do smartlogger?\n")
tipo_smartlogger = tipo_smartlogger.upper()

usina = input("Qual o nome da usina?\n")

prefix_usina = input("Qual o prefixo da usina?\n")

skid = input("Qual o número do Skid?\n")

IP = input("Qual o IP do DataSource?\n")


while(tipo_smartlogger != 'A'):
    print("Tipo inválido!")
    tipo_smartlogger = input("Qual o tipo do smartlogger?\n")

tipo = "Smart_TIPO_" + tipo_smartlogger

# Criar arquivo Json com inicio padrão
shutil.copy("Smarts/" + tipo + "/" + tipo + ".json", "saida/" )
destino = "saida/smartlogger.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/" + tipo + ".json", destino)

with open("saida/smartlogger.json", "r", encoding="utf-8") as f:
    smartJson = json.load(f)

with open("Smarts/Genericos.json", "r", encoding="utf-8") as f:
    smartJson_generico = json.load(f)

    smartJson["dataPoints"].extend(smartJson_generico["dataPoints"])

with open("saida/smartlogger.json", "w", encoding="utf-8") as f:
    json.dump(smartJson, f, indent=3, ensure_ascii=False)


# Ler arquivo original
with open("saida/smartlogger.json", "r", encoding="utf-8") as f:
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
    )

# Sobrescrever o arquivo original
with open("saida/smartlogger.json", "w", encoding="utf-8") as f:
    f.write(conteudo)

print("Arquivo Json gerado em saida/smartlogger.json!")