import shutil
import os

os.makedirs("temp/saida", exist_ok=True)

tipo_smartlogger = input("Qual o tipo do smartlogger?\n")
tipo_smartlogger = tipo_smartlogger.upper()

usina = input("Qual o nome da usina?\n")

prefix_usina = input("Qual o prefixo da usina?\n")

skid = input("Qual o número do Skid?\n")

IP = input("Qual o IP do DataSource?\n")


while(tipo_smartlogger != 'A'):
    print("Tipo inválido!")
    tipo_smartlogger = input("Qual o tipo do smartlogger?\n")

tipo = "Smart_TIPO_" + tipo_smartlogger

# Criar arquivo Json com inicio padrão
shutil.copy("Smarts/" + tipo + "/" + tipo + ".json", "saida/" )
destino = "saida/smartlogger.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/" + tipo + ".json", destino)




# Ler arquivo original
with open("saida/smartlogger.json", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
conteudo = ( 
    conteudo
        .replace("USN", prefix_usina)
        .replace("Nome Usina",usina)
        .replace("000.000.000.000", IP)
        .replace("Skid x", "Skid " + skid)
        .replace("_SMART1","_SMART" + skid)
        .replace("Smart1","Smart" + skid)
        .replace("VIR_Capacidade Instalada 1","VIR_Capacidade Instalada " + skid)
        .replace("Capacidade Diário 1","Capacidade Diário " + skid)
        .replace("Capacidade Mensal 1","Capacidade Mensal " + skid)
        .replace("Capacidade Anual 1","Capacidade Anual " + skid)
    )

# Sobrescrever o arquivo original
with open("saida/smartlogger.json", "w", encoding="utf-8") as f:
    f.write(conteudo)

# Apagar temp
shutil.rmtree("temp")

print("Arquivo Json gerado em saida/smartlogger.json!")