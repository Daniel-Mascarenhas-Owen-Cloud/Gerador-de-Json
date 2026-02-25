import json
import os

pasta = "saida"  # pasta onde estão os jsons
saida = "saida_final.json"

resultado = {
    "dataSources": [],
    "dataPoints": []
}

# percorre todos os arquivos da pasta
for arquivo in os.listdir(pasta):
    if arquivo.endswith(".json"):
        caminho = os.path.join(pasta, arquivo)

        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

            # junta as listas se existirem
            if "dataSources" in dados:
                resultado["dataSources"].extend(dados["dataSources"])

            if "dataPoints" in dados:
                resultado["dataPoints"].extend(dados["dataPoints"])

# salva o json final
with open(saida, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=3, ensure_ascii=False)

with open(saida, "r", encoding="utf-8") as f:
    conteudo = f.read()

conteudo = conteudo.replace("1.7976931348623157e+308", "1.7976931348623157E308")

with open(saida, "w", encoding="utf-8") as f:
    f.write(conteudo)

print("JSONs unidos com sucesso!")