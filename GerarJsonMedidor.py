import shutil
import os
import sys

os.makedirs("saida", exist_ok=True)


tipo_medidor = sys.argv[1].upper()
usina = sys.argv[2].upper()
prefix_usina = sys.argv[3]
IP = sys.argv[4]
numero_medidor = sys.argv[5]

numero_medidor = int(numero_medidor)

while(tipo_medidor != 'A'):
    print("Tipo inválido!")
    tipo_medidor = input("Qual o tipo do Medidor? ").upper()

tipo = "Medidor_TIPO_" + tipo_medidor

# Criar arquivo Json com inicio padrão
shutil.copy("Medidor/" + tipo + ".json", "saida/" )
destino = f"saida/Medidor{numero_medidor}.json"
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
        .replace("MEDIDOR1", f"MEDIDOR{numero_medidor}")
        .replace("Cabine 1", f"Cabine {numero_medidor}")
    )

# Sobrescrever o arquivo original
with open(destino, "w", encoding="utf-8") as f:
    f.write(conteudo)


print(f"Arquivo Json gerado em saida/Medidor{numero_medidor}.json!")