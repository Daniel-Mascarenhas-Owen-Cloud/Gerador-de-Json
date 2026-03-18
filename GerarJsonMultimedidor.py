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


while(tipo_Multimedidor != 'A'):
    print("Tipo inválido!")
    tipo_Multimedidor = input("Qual o tipo do Multimedidor?\n")

tipo = "Multimedidor_TIPO_" + tipo_Multimedidor

# Criar arquivo Json com inicio padrão
shutil.copy("Multimedidor/" + tipo + "/" + tipo + ".json", "saida/" )
destino = "saida/Multimedidor{cabine}.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/" + tipo + ".json", destino)

with open(f"saida/Multimedidor{cabine}.json", "r", encoding="utf-8") as f:
    smartJson = json.load(f)


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
        .replace('"slaveId":1', '"slaveId":' + slave_id)
    )

# Sobrescrever o arquivo original
with open(f"saida/Multimedidor{cabine}.json", "w", encoding="utf-8") as f:
    f.write(conteudo)

print(f"Arquivo Json gerado em saida/Multimedidor{cabine}.json!")