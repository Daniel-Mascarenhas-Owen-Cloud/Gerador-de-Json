import shutil
import os

os.makedirs("saida", exist_ok=True)

tipo_ETM = input("Qual o tipo da estação meteorológica?\n")
tipo_ETM = tipo_ETM.upper()

usina = input("Qual o nome da usina?\n")

prefix_usina = input("Qual o prefixo da usina?\n")

IP = input("Qual o IP do DataSource?\n")


while(tipo_ETM != 'A'):
    print("Tipo inválido!")
    tipo_ETM = input("Qual o tipo da estação meteorológica?\n")

tipo = "ETM_TIPO_" + tipo_ETM

# Criar arquivo Json com inicio padrão
shutil.copy("ETM/" + tipo + "/ETM_TIPO_A.json", "saida/" )
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
    )

# Sobrescrever o arquivo original
with open("saida/ETM.json", "w", encoding="utf-8") as f:
    f.write(conteudo)


print("Arquivo Json gerado em saida/ETM.json!")