import shutil
import os

os.makedirs("temp/saida", exist_ok=True)
os.makedirs("saida", exist_ok=True)

tipo_NCU = input("Qual o tipo do NCU? (Ex: A)\n")
tipo_NCU = tipo_NCU.upper()

usina = input("Qual o nome da usina?\n")

prefix_usina = input("Qual o prefixo da usina?\n")

NCU = input("Qual o número da NCU?\n")

IP = input("Qual o IP do DataSource?\n")


while(tipo_NCU != 'A'):
    print("Tipo inválido!")
    tipo_NCU = input("Qual o tipo do NCU?\n")

tipo = "NCU_TIPO_" + tipo_NCU

# Criar arquivo Json com inicio padrão
shutil.copy("NCU/" + tipo + f"/{tipo}.json", "saida/" )
destino = "saida/NCU.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/" + tipo + ".json", destino)




# Ler arquivo original
with open("saida/NCU.json", "r", encoding="utf-8") as f:
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
with open("saida/NCU.json", "w", encoding="utf-8") as f:
    f.write(conteudo)

# Apagar temp
shutil.rmtree("temp")

print("Arquivo Json gerado em saida/NCU.json!")