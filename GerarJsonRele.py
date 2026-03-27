import shutil
import os
import sys

os.makedirs("saida", exist_ok=True)


tipo_rele = sys.argv[1].upper()
usina = sys.argv[2].upper()
prefix_usina = sys.argv[3]
IP = sys.argv[4]
slave_id = sys.argv[5]
numero_rele = sys.argv[6]
cabine = sys.argv[7]
numeroDoGerador = int(sys.argv[8])

while(tipo_rele != 'A'):
    print("Tipo inválido!")
    tipo_rele = input("Qual o tipo dos relés? ").upper()

tipo = "Rele_TIPO_" + tipo_rele

# Criar arquivo Json com inicio padrão
shutil.copy("Rele/" + tipo + ".json", "saida/" )
destino = f"saida/Rele{numeroDoGerador}.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/Rele_TIPO_A.json", destino)


# Ler arquivo original
with open(destino, "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
conteudo = ( 
    conteudo
        .replace("USN", prefix_usina)
        .replace("000.000.000.000", IP)
        .replace("Usina", usina)
        .replace('"slaveId":1,', f'"slaveId":{slave_id},')
        .replace("RELE1", f"RELE{numero_rele}")
        .replace("Cabine 1", f"Cabine {cabine}")
    )

# Sobrescrever o arquivo original
with open(destino, "w", encoding="utf-8") as f:
    f.write(conteudo)


print(f"Arquivo Json gerado em saida/Rele{numeroDoGerador}.json!")