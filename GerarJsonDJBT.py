import shutil
import os
import sys

os.makedirs("saida", exist_ok=True)


tipo_DJBT = sys.argv[1].upper()
prefix_usina = sys.argv[2]
usina = sys.argv[3]
IP = sys.argv[4]
skid = sys.argv[5]
numero = sys.argv[6]

while(tipo_DJBT != 'A'):
    print("Tipo inválido!")
    tipo_DJBT = input("Qual o tipo da estação meteorológica?\n")

tipo = "DJBT_TIPO_" + tipo_DJBT

# Criar arquivo Json com inicio padrão
shutil.copy("DJBT/" + tipo + "/" + tipo + ".json", "saida/" )
destino = f"saida/DJBT{numero}.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/DJBT_TIPO_A.json", destino)


# Ler arquivo original
with open(destino, "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
conteudo = ( 
    conteudo
        .replace("USN", prefix_usina)
        .replace("000.000.000.000", IP)
        .replace("Nome da Usina", usina)
        .replace("Skid 1", f"Skid {skid}")
        .replace("DJBT1", f"DJBT{numero}")
)

# Sobrescrever o arquivo original
with open(destino, "w", encoding="utf-8") as f:
    f.write(conteudo)


print(f"Arquivo Json gerado em {destino}!")