import shutil
import os
import sys
import json

# argumentos vindos do app.py
usina = sys.argv[1]
prefix_usina = sys.argv[2]
ip = sys.argv[3]
offset = sys.argv[4]
qtd_cameras = sys.argv[5]

offset = int(offset)
qtd_cameras = int(qtd_cameras)

os.makedirs("saida", exist_ok=True)

# Criar arquivo Json com inicio padrão
shutil.copy("Cameras/DataSource.json", "saida/")

if os.path.exists("saida/Cameras.json"):
    os.remove("saida/Cameras.json")

os.rename("saida/DataSource.json", "saida/Cameras.json")


# Lista acumuladora
todos_dataPoints = []

for i in range(qtd_cameras):

    with open("Cameras/DataPoints.json", "r", encoding="utf-8") as f:
        conteudo = f.read()

    conteudo = ( conteudo
                .replace("Monitor de Conexão Câmera 1", f"Monitor de Conexão Câmera {i+1}")
                .replace('"offset": 0,', f'"offset": {offset+i},')
                )

    dados = json.loads(conteudo)

    # Junta todos
    todos_dataPoints.extend(dados["dataPoints"])


# Agora lê o DataSource UMA VEZ
with open("Cameras/DataSource.json", "r", encoding="utf-8") as f:
    conteudo = json.load(f)

# Adiciona tudo de uma vez
conteudo["dataPoints"].extend(todos_dataPoints)

# Salva UMA VEZ
with open("saida/Cameras.json", "w", encoding="utf-8") as f:
    json.dump(conteudo, f, ensure_ascii=False, indent=4)


with open("saida/Cameras.json", "r", encoding="utf-8") as f:
    conteudo = f.read()

conteudo = ( conteudo
            .replace("Usina I", usina)
            .replace("USN", prefix_usina)
            .replace("000.000.000.000", ip)
            )

# Sobrescrever o arquivo original
with open("saida/Cameras.json", "w", encoding="utf-8") as f:
    f.write(conteudo)

print("Arquivo Json gerado em saida/Cameras.json!")