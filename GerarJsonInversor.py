import shutil
import os
import math

os.makedirs("temp/saida", exist_ok=True)

os.makedirs("saida", exist_ok=True)

tipo_inversor = input("Qual o tipo do inversor? B ou C?\n")
tipo_inversor = tipo_inversor.upper()

usina = input("Qual o nome da usina?\n")

prefix_usina = input("Qual o prefixo da usina?\n")

skid = input("Qual o número do Skid?\n")

IP = input("Qual o IP do DataSource?\n")

inv_quantidade = int(input("Qual é a quantidade de inversores?\n"))

numero_slaveid = int(input("Qual é o número do primeiro slaveId?\n"))



# Criar arquivo Json com inicio padrão
shutil.copy("base/inicio.json", "saida/" )
destino = "saida/inversor.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/inicio.json", destino)

while(tipo_inversor != 'B' and tipo_inversor != 'C'):
    print("Tipo inválido!")
    tipo_inversor = input("Qual o tipo do inversor?\n")

# Inicio da logica
tipo = "INV_" + tipo_inversor 
endereco_DataSource = "Inversores/" + tipo + "/DataSource.json"
endereco_DataPoint = "Inversores/" + tipo + "/DataPoints.json"

if tipo_inversor == "C":
    with open("saida/inversor.json", "a", encoding="utf-8") as destino:
        with open("INV_C/Sungrow.json", "r", encoding="utf-8") as origem:
            destino.write(origem.read())


quantos_DataSources = math.ceil(inv_quantidade / 5 )

# Copiar para editar sem modificar anterior
for i in range(quantos_DataSources): 

    if i>0:
        with open("saida/inversor.json", "a", encoding="utf-8") as destino:
            destino.write(",")
    
    shutil.copy(endereco_DataSource, "temp/" )

    start = 1+(5*i)
    end = (i+1)*5

    with open("temp/DataSource.json", "r", encoding="utf-8") as f:
        conteudo = f.read()

    conteudo = ( 
        conteudo
        .replace("_SMART1","_SMART" + skid)
        .replace("_1a5","_" + str(start) + "a" + str(end)) 
        )


    with open("saida/inversor.json", "a", encoding="utf-8") as destino:
            destino.write(conteudo)



with open("saida/inversor.json", "a", encoding="utf-8") as destino:
    with open("base/tag_dataPoint.json", "r", encoding="utf-8") as origem:
        destino.write(origem.read())


    with open("saida/inversor.json", "r", encoding="utf-8") as f:
        conteudo = f.read()

    conteudo = conteudo[:-1] 

    with open("saida/inversor.json", "w", encoding="utf-8") as f:
        f.write(conteudo)



# Copiar para editar sem modificar anterior
for i in range(inv_quantidade): 

    i1 = i + 1  # agora começa em 1

    start = ((i1 - 1) // 5) * 5 + 1
    end = start + 4


    if i>0:
        with open("saida/inversor.json", "a", encoding="utf-8") as destino:
            destino.write(",")
    
    shutil.copy(endereco_DataPoint, "temp/" )


    with open("temp/DataPoints.json", "r", encoding="utf-8") as f:
        conteudo = f.read()

    with open("Inversores/Genericos.json", "r", encoding="utf-8") as f:
        conteudo  += f.read()

    conteudo = ( 
        conteudo
            .replace("_SMART1","_SMART" + skid)
            .replace("Smart1","Smart" + skid)
            .replace("Inv_1.1",f"Inv_{skid}.{i+1}")
            .replace("_1a5","_" + str(start) + "a" + str(end) )
            .replace("Inversor 1.1", f"Inversor {skid}.{i+1}")
            .replace('"slaveId":1,', f'"slaveId":{numero_slaveid + i},')
    )


    with open("saida/inversor.json", "a", encoding="utf-8") as destino:
            destino.write(conteudo)


with open("saida/inversor.json", "a", encoding="utf-8") as destino:
    with open("base/fim.json", "r", encoding="utf-8") as origem:
        destino.write(origem.read())



# Ler arquivo original
with open("saida/inversor.json", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
conteudo = (
    conteudo
        .replace("USN", prefix_usina)
        .replace("Nome Usina",usina)
        .replace("000.000.000.000", IP)
        .replace("Skid x", "Skid " + skid)
)

# Sobrescrever o arquivo original
with open("saida/inversor.json", "w", encoding="utf-8") as f:
    f.write(conteudo)




# Apagar temp
shutil.rmtree("temp")

print("Arquivo Json gerado em saida/inversor.json!")

# conteudo = conteudo.replace("Skid x","Skid " + skid)