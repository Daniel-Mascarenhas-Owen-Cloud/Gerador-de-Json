import shutil
import os
import math

os.makedirs("temp/saida", exist_ok=True)

os.makedirs("saida", exist_ok=True)

import shutil
import os
import math
import sys
import json

os.makedirs("temp/saida", exist_ok=True)
os.makedirs("saida", exist_ok=True)

# argumentos vindos do app.py
tipo_inversor = sys.argv[1].upper()
usina = sys.argv[2]
prefix_usina = sys.argv[3]
skid = sys.argv[4]
IP = sys.argv[5]
inv_quantidade = int(sys.argv[6])
numero_slaveid = int(sys.argv[7])



# Criar arquivo Json com inicio padrão
shutil.copy("base/inicio.json", "saida/" )
destino = f"saida/inversor{skid}.json"
if os.path.exists(destino):
    os.remove(destino)

os.rename("saida/inicio.json", destino)

while(tipo_inversor != 'B' and tipo_inversor != 'C' and tipo_inversor != 'D' and tipo_inversor != 'E' and tipo_inversor != 'G'):
    print("Tipo inválido!")
    tipo_inversor = input("Qual o tipo do inversor?\n")

# Inicio da logica
tipo = "INV_" + tipo_inversor 
endereco_DataSource = "Inversores/" + tipo + "/DataSource.json"
endereco_DataPoint = "Inversores/" + tipo + "/DataPoints.json"

data_points_genericos_tipo_e = ""

if tipo_inversor == "E":
    xids_desabilitados_tipo_e = {
        "USN_Inv_1.1_CAL_Energia Esperada (KWh)",
        "USN_Inv_1.1_CAL_PR Ajustado (%)",
        "USN_Inv_1.1_CAL_PR Simples (%)",
        "USN_Inv_1.1_CAL_Rendimento (%)"
    }

    with open("Inversores/Genericos.json", "r", encoding="utf-8") as f:
        pontos_genericos = json.loads("[" + f.read() + "]")

    pontos_tipo_e = []

    for ponto in pontos_genericos:
        if ponto.get("xid") in xids_desabilitados_tipo_e:
            ponto["enabled"] = False
            pontos_tipo_e.append(ponto)

    blocos_tipo_e = []

    for ponto in pontos_tipo_e:
        bloco = json.dumps(ponto, indent=3, ensure_ascii=False)
        bloco = "\n".join("      " + linha for linha in bloco.splitlines())
        blocos_tipo_e.append(bloco)

    data_points_genericos_tipo_e = ",\n".join(blocos_tipo_e)

if tipo_inversor == "C":
    with open(f"saida/inversor{skid}.json", "a", encoding="utf-8") as destino:
        with open("Inversores/INV_C/Sungrow.json", "r", encoding="utf-8") as origem:
            destino.write(origem.read())


if tipo_inversor == "E":
    with open(f"saida/inversor{skid}.json", "a", encoding="utf-8") as destino:
        with open("Inversores/INV_E/Fronius.json", "r", encoding="utf-8") as origem:
            destino.write(origem.read())


quantos_DataSources = math.ceil(inv_quantidade / 5 )

# Copiar para editar sem modificar anterior
for i in range(quantos_DataSources): 

    if i>0:
        with open(f"saida/inversor{skid}.json", "a", encoding="utf-8") as destino:
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


    with open(f"saida/inversor{skid}.json", "a", encoding="utf-8") as destino:
            destino.write(conteudo)



with open(f"saida/inversor{skid}.json", "a", encoding="utf-8") as destino:
    with open("base/tag_dataPoint.json", "r", encoding="utf-8") as origem:
        destino.write(origem.read())


    with open(f"saida/inversor{skid}.json", "r", encoding="utf-8") as f:
        conteudo = f.read()

    conteudo = conteudo[:-7] 

    with open(f"saida/inversor{skid}.json", "w", encoding="utf-8") as f:
        f.write(conteudo)



# Copiar para editar sem modificar anterior
for i in range(inv_quantidade): 

    i1 = i + 1  # agora começa em 1

    start = ((i1 - 1) // 5) * 5 + 1
    end = start + 4


    if i>0 and i<=inv_quantidade:
        with open(f"saida/inversor{skid}.json", "a", encoding="utf-8") as destino:
            destino.write(",")
    
    shutil.copy(endereco_DataPoint, "temp/" )


    with open("temp/DataPoints.json", "r", encoding="utf-8") as f:
        conteudo = f.read()

    if data_points_genericos_tipo_e:
        conteudo = conteudo.rstrip() + ",\n" + data_points_genericos_tipo_e

    conteudo = ( 
        conteudo
            .replace("_SMART1","_SMART" + skid)
            .replace("Smart1","Smart" + skid)
            .replace("Inv_1.1",f"Inv_{skid}.{i+1}")
            .replace("_1a5","_" + str(start) + "a" + str(end) )
            .replace("Inversor 1.1", f"Inversor {skid}.{i+1}")
            .replace('"slaveId":1,', f'"slaveId":{numero_slaveid + i},')
            .replace('Esperada 1', f'Esperada {skid}')
    )


    with open(f"saida/inversor{skid}.json", "a", encoding="utf-8") as destino:
            destino.write(conteudo)


with open(f"saida/inversor{skid}.json", "a", encoding="utf-8") as destino:
    with open("base/fim.json", "r", encoding="utf-8") as origem:
        destino.write(origem.read())



# Ler arquivo original
with open(f"saida/inversor{skid}.json", "r", encoding="utf-8") as f:
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
with open(f"saida/inversor{skid}.json", "w", encoding="utf-8") as f:
    f.write(conteudo)




# Apagar temp
shutil.rmtree("temp")

print(f"Arquivo Json gerado em saida/inversor{skid}.json!")
