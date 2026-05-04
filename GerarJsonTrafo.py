import shutil
import os
import sys

os.makedirs("saida", exist_ok=True)


tipo_trafo = sys.argv[1].upper()
usina = sys.argv[2]
prefix_usina = sys.argv[3].upper()
IP = sys.argv[4]
slave_id = sys.argv[5]
skid = sys.argv[6]
numero_trafo = sys.argv[7]
numeroDoGerador = int(sys.argv[8])

while(tipo_trafo != 'D'):
    print("Tipo inválido!")
    tipo_trafo = input("Qual o tipo dos relés? ").upper()

tipo = "Trafo_" + tipo_trafo

# Criar arquivo Json com inicio padrão
shutil.copy("Trafo/" + tipo + ".json", "saida/" )
destino = f"saida/Trafo{numeroDoGerador}.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/" + tipo + ".json", destino)


# Ler arquivo original
with open(destino, "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
conteudo = ( 
    conteudo
        .replace("USN", prefix_usina)
        .replace("000.000.000.000", IP)
        .replace("Usina", usina)
        .replace('"slaveId":1,', f'"slaveId":{slave_id},') # ????
        .replace("Skid 1", f"Skid {skid}")
        .replace("Trafo 1", f"Trafo {numero_trafo}")
        .replace("TRAFO1", f"TRAFO{numero_trafo}")
        .replace("TRF1", f"TRF{numero_trafo}")
    )

# Sobrescrever o arquivo original
with open(destino, "w", encoding="utf-8") as f:
    f.write(conteudo)


print(f"Arquivo Json gerado em saida/Trafo{numeroDoGerador}.json!")