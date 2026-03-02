import shutil
import os
import json

os.makedirs("saida", exist_ok=True)

tipo_Multimedidor = input("Qual o tipo do Multimedidor?\n")
tipo_Multimedidor = tipo_Multimedidor.upper()

usina = input("Qual o nome da usina?\n")

prefix_usina = input("Qual o prefixo da usina?\n")

cabine = input("Qual o número da Cabine?\n")

IP = input("Qual o IP do DataSource?\n")

slave_id = input("Qual o Slave Address?\n")


while(tipo_Multimedidor != 'A'):
    print("Tipo inválido!")
    tipo_Multimedidor = input("Qual o tipo do Multimedidor?\n")

tipo = "Multimedidor_TIPO_" + tipo_Multimedidor

# Criar arquivo Json com inicio padrão
shutil.copy("Multimedidor/" + tipo + "/" + tipo + ".json", "saida/" )
destino = "saida/Multimedidor.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/" + tipo + ".json", destino)

with open("saida/Multimedidor.json", "r", encoding="utf-8") as f:
    smartJson = json.load(f)


# Ler arquivo original
with open("saida/Multimedidor.json", "r", encoding="utf-8") as f:
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
with open("saida/Multimedidor.json", "w", encoding="utf-8") as f:
    f.write(conteudo)

print("Arquivo Json gerado em saida/Multimedidor.json!")