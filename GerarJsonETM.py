import shutil
import os
import sys

os.makedirs("saida", exist_ok=True)


tipo_ETM = sys.argv[1].upper()
prefix_usina = sys.argv[2]
IP = sys.argv[3]
slaveId = sys.argv[4]
nomeUsina = sys.argv[5]


while(tipo_ETM != 'A'):
    print("Tipo inválido!")
    tipo_ETM = input("Qual o tipo da estação meteorológica?\n")

tipo = "ETM_TIPO_" + tipo_ETM

# Criar arquivo Json com inicio padrão
shutil.copy("ETM/" + tipo + "/" + tipo + ".json", "saida/" )
destino = "saida/ETM.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/ETM_TIPO_A.json", destino)


# Ler arquivo original
with open("saida/ETM.json", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
conteudo = ( 
    conteudo
        .replace("USN", prefix_usina)
        .replace("000.000.000.000", IP)
        .replace('"slaveId":1,', f'"slaveId":{slaveId},')
        .replace("UFV Usina", f"UFV {nomeUsina}")

# Sobrescrever o arquivo original
with open("saida/ETM.json", "w", encoding="utf-8") as f:
    f.write(conteudo)


print("Arquivo Json gerado em saida/ETM.json!")