import shutil
import os
import sys

os.makedirs("saida", exist_ok=True)

tipo_equipamento = sys.argv[1].upper()
usina = sys.argv[2]
prefix_usina = sys.argv[3]
IP = sys.argv[4]


while(tipo_equipamento != 'A'):
    print("Tipo inválido!")
    tipo_equipamento = input("Qual o tipo do Nobreak?\n")

tipo = "Nobreak_TIPO_" + tipo_equipamento

# Criar arquivo Json com inicio padrão
shutil.copy("Nobreak/" + tipo + "/" + tipo + ".json", "saida/" )
destino = "saida/Nobreak.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/" + tipo + ".json", destino)


# Ler arquivo original
with open("saida/Nobreak.json", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
conteudo = ( 
    conteudo
        .replace("USN", prefix_usina)
        .replace("Nome Usina",usina)
        .replace("000.000.000.000", IP)
    )

# Sobrescrever o arquivo original
with open("saida/Nobreak.json", "w", encoding="utf-8") as f:
    f.write(conteudo)
    

print("Arquivo Json gerado em saida/Nobreak.json!")