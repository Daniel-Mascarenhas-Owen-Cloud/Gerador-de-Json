import shutil
import os
import sys
import json

# argumentos vindos do app.py
prefix_usina = sys.argv[1]
tipo_inversor = sys.argv[2].upper() if len(sys.argv) > 2 else ""


os.makedirs("saida", exist_ok=True)

# Criar arquivo Json com inicio padrão
shutil.copy("Configuracao/DadosConfig.json", "saida/")

# Ler arquivo copiado
with open("saida/DadosConfig.json", "r", encoding="utf-8") as f:
    dados_config = json.load(f)

if tipo_inversor == "E":
    xid_fator_mensal_total = "USN_CAL_Fator de Capacidade Mensal Total"

    for ponto in dados_config["dataPoints"]:
        if ponto.get("xid") == xid_fator_mensal_total:
            ponto["enabled"] = False
            break

conteudo = json.dumps(dados_config, indent=3, ensure_ascii=False)
conteudo = conteudo.replace("USN", prefix_usina)
conteudo = conteudo.replace("1.7976931348623157e+308", "1.7976931348623157E308")

# Sobrescrever o arquivo original
with open("saida/DadosConfig.json", "w", encoding="utf-8") as f:
    f.write(conteudo)

print("Arquivo Json gerado em saida/DadosConfig.json!")
