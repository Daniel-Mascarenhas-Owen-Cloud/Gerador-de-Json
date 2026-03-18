import shutil
import os
import sys

os.makedirs("temp/saida", exist_ok=True)
os.makedirs("saida", exist_ok=True)

tipo_NCU = sys.argv[1].upper()
usina = sys.argv[2]
prefix_usina = sys.argv[3]
NCU = sys.argv[4]
IP = sys.argv[5]


while(tipo_NCU != 'A'):
    print("Tipo inválido!")
    tipo_NCU = input("Qual o tipo do NCU?\n")

tipo = "NCU_TIPO_" + tipo_NCU

# Criar arquivo Json com inicio padrão
shutil.copy("NCU/" + tipo + f"/{tipo}.json", "saida/" )
destino = f"saida/NCU{NCU}.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/" + tipo + ".json", destino)




# Ler arquivo original
with open(f"saida/NCU{NCU}.json", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
conteudo = ( 
    conteudo
        .replace("USN", prefix_usina)
        .replace("Nome Usina",usina)
        .replace("000.000.000.000", IP)
        .replace("NCU1", f"NCU{NCU}")
        .replace("NCU x", f"NCU {NCU}")
    )

# Sobrescrever o arquivo original
with open(f"saida/NCU{NCU}.json", "w", encoding="utf-8") as f:
    f.write(conteudo)

# Apagar temp
shutil.rmtree("temp")

print(f"Arquivo Json gerado em saida/NCU{NCU}.json!")