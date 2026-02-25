import shutil
import os

os.makedirs("saida", exist_ok=True)


prefix_usina = input("Qual o prefixo da usina?\n")


# Criar arquivo Json com inicio padrão
shutil.copy("TimeStamps/DataSourcesTimeStamp.json", "saida/" )


# Ler arquivo original
with open("saida/DataSourcesTimeStamp.json", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Replace
    conteudo = conteudo.replace("USN", prefix_usina)

# Sobrescrever o arquivo original
with open("saida/DataSourcesTimeStamp.json", "w", encoding="utf-8") as f:
    f.write(conteudo)


print("Arquivo Json gerado em saida/DataSourcesTimeStamp.json!")