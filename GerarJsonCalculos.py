import json
import os
import sys

os.makedirs("saida", exist_ok=True)


letras = "abcdefghijklmnopqrstuvwxyz"


prefixo = sys.argv[1]
num_skids = int(sys.argv[2])
inversores_por_skid = sys.argv[3].split(",")
inversores_por_skid = [int(x) for x in inversores_por_skid]



json_final = {"dataPoints":[]}


def gerar_contexto_inversor(prefixo, skid, qtd, tipo):

    context = []
    vars_script = []

    for i in range(qtd):

        var = letras[i]

        context.append({
            "varName": var,
            "dataPointXid": f"{prefixo}_Inv_{skid}.{i+1}_MED_Energia {tipo} (KWh)"
        })

        vars_script.append(f"{var}.value")

    if tipo == "Mensal":
        divisor = "/1000"
        unidade = "(KWh)"
    else:
        divisor = "/1000000"
        unidade = "(GWh)"

    script = "return (" + " + ".join(vars_script) + ")" + divisor + ";"

    return context, script, unidade


for skid, qtd in enumerate(inversores_por_skid, start=1):

    context, script, unidade = gerar_contexto_inversor(prefixo, skid, qtd, "Mensal")

    ponto = {
        "xid": f"{prefixo}_CAL_Energia Mensal {skid} (KWh)",
        "loggingType": "INTERVAL",
        "intervalLoggingPeriodType": "MINUTES",
        "intervalLoggingType": "INSTANT",
        "purgeType": "YEARS",
        "pointLocator": {
            "dataType": "NUMERIC",
            "updateEvent": "CONTEXT_UPDATE",
            "context": context,
            "executionDelayPeriodType": "SECONDS",
            "executionDelaySeconds": 0,
            "script": script,
            "settable": False,
            "updateCronPattern": ""
        },
        "eventDetectors": [],
        "engineeringUnits": "",
        "purgeStrategy": "PERIOD",
        "chartColour": None,
        "chartRenderer": None,
        "dataSourceXid": f"{prefixo}_Dados Calculados",
        "defaultCacheSize": 1,
        "description": "",
        "deviceName": f"{prefixo}_Dados Calculados",
        "discardExtremeValues": False,
        "discardHighLimit": 1.7976931348623157E308,
        "discardLowLimit": -1.7976931348623157E308,
        "enabled": True,
        "eventTextRenderer": {
            "type": "EVENT_NONE"
        },
        "intervalLoggingPeriod": 5,
        "name": f"{prefixo}_CAL_Energia Mensal {skid} (KWh)",
        "purgePeriod": 1,
        "purgeValuesLimit": 100,
        "textRenderer": {
            "type": "ANALOG",
            "format": "0.0",
            "suffix": ""
        },
        "tolerance": 0.0
    }

    json_final["dataPoints"].append(ponto)


for skid, qtd in enumerate(inversores_por_skid, start=1):

    context, script, unidade = gerar_contexto_inversor(prefixo, skid, qtd, "Anual")

    ponto = {
        "xid": f"{prefixo}_CAL_Energia Anual {skid} (GWh)",
        "loggingType": "INTERVAL",
        "intervalLoggingPeriodType": "MINUTES",
        "intervalLoggingType": "INSTANT",
        "purgeType": "YEARS",
        "pointLocator": {
            "dataType": "NUMERIC",
            "updateEvent": "CONTEXT_UPDATE",
            "context": context,
            "executionDelayPeriodType": "SECONDS",
            "executionDelaySeconds": 0,
            "script": script,
            "settable": False,
            "updateCronPattern": ""
        },
        "eventDetectors": [],
        "engineeringUnits": "",
        "purgeStrategy": "PERIOD",
        "chartColour": None,
        "chartRenderer": None,
        "dataSourceXid": f"{prefixo}_Dados Calculados",
        "defaultCacheSize": 1,
        "description": "",
        "deviceName": f"{prefixo}_Dados Calculados",
        "discardExtremeValues": False,
        "discardHighLimit": 1.7976931348623157E308,
        "discardLowLimit": -1.7976931348623157E308,
        "enabled": True,
        "eventTextRenderer": {
            "type": "EVENT_NONE"
        },
        "intervalLoggingPeriod": 5,
        "name": f"{prefixo}_CAL_Energia Anual {skid} (GWh)",
        "purgePeriod": 1,
        "purgeValuesLimit": 100,
        "textRenderer": {
            "type": "ANALOG",
            "format": "0.0",
            "suffix": ""
        },
        "tolerance": 0.0
    }

    json_final["dataPoints"].append(ponto)


context_smart = []
vars_smart = []

for i in range(num_skids):

    var = letras[i]

    context_smart.append({
        "varName": var,
        "dataPointXid": f"{prefixo}_Smart{i+1}_MED_Energia Diaria Total (KWh)"
    })

    vars_smart.append(f"{var}.value")

script_smart = "energy = " + " + ".join(vars_smart) + ";\nreturn energy;"


smart_total = {
    "xid": f"{prefixo}_CAL_Energia Diária Total (KWh)",
    "loggingType": "INTERVAL",
    "intervalLoggingPeriodType": "MINUTES",
    "intervalLoggingType": "INSTANT",
    "purgeType": "YEARS",
    "pointLocator": {
        "dataType": "NUMERIC",
        "updateEvent": "CONTEXT_UPDATE",
        "context": context_smart,
        "executionDelayPeriodType": "SECONDS",
        "executionDelaySeconds": 0,
        "script": script_smart,
        "settable": False,
        "updateCronPattern": ""
    },
    "eventDetectors": [],
    "engineeringUnits": "",
    "purgeStrategy": "PERIOD",
    "chartColour": None,
    "chartRenderer": None,
    "dataSourceXid": f"{prefixo}_Dados Calculados",
    "defaultCacheSize": 1,
    "description": "",
    "deviceName": f"{prefixo}_Dados Calculados",
    "discardExtremeValues": False,
    "discardHighLimit": 1.7976931348623157E308,
    "discardLowLimit": -1.7976931348623157E308,
    "enabled": True,
    "eventTextRenderer": {
        "type": "EVENT_NONE"
    },
    "intervalLoggingPeriod": 5,
    "name": f"{prefixo}_CAL_Energia Diária Total (KWh)",
    "purgePeriod": 1,
    "purgeValuesLimit": 100,
    "textRenderer": {
        "type": "ANALOG",
        "format": "0.0",
        "suffix": ""
    },
    "tolerance": 0.0
}

json_final["dataPoints"].append(smart_total)

# MENSAL

context_mensal = []
vars_mensal = []

for i in range(num_skids):
    var = letras[i]

    context_mensal.append({
        "varName": var,
        "dataPointXid": f"{prefixo}_CAL_Energia Mensal {i+1} (KWh)"
    })

    vars_mensal.append(f"{var}.value")

script_mensal = "energy = " + " + ".join(vars_mensal) + ";\nreturn energy;"

mensal_total = {
    "xid": f"{prefixo}_CAL_Energia Mensal Total (KWh)",
    "loggingType": "INTERVAL",
    "intervalLoggingPeriodType": "MINUTES",
    "intervalLoggingType": "INSTANT",
    "purgeType": "YEARS",
    "pointLocator": {
        "dataType": "NUMERIC",
        "updateEvent": "CONTEXT_UPDATE",
        "context": context_mensal,
        "executionDelayPeriodType": "SECONDS",
        "executionDelaySeconds": 0,
        "script": script_mensal,
        "settable": False,
        "updateCronPattern": ""
    },
    "eventDetectors": [],
    "engineeringUnits": "",
    "purgeStrategy": "PERIOD",
    "chartColour": None,
    "chartRenderer": None,
    "dataSourceXid": f"{prefixo}_Dados Calculados",
    "defaultCacheSize": 1,
    "description": "",
    "deviceName": f"{prefixo}_Dados Calculados",
    "discardExtremeValues": False,
    "discardHighLimit": 1.7976931348623157E308,
    "discardLowLimit": -1.7976931348623157E308,
    "enabled": True,
    "eventTextRenderer": {
        "type": "EVENT_NONE"
    },
    "intervalLoggingPeriod": 5,
    "name": f"{prefixo}_CAL_Energia Mensal Total (KWh)",
    "purgePeriod": 1,
    "purgeValuesLimit": 100,
    "textRenderer": {
        "type": "ANALOG",
        "format": "0.0",
        "suffix": ""
    },
    "tolerance": 0.0
}

json_final["dataPoints"].append(mensal_total)

# ANUAL

context_anual = []
vars_anual = []

for i in range(num_skids):
    var = letras[i]

    context_anual.append({
        "varName": var,
        "dataPointXid": f"{prefixo}_CAL_Energia Anual {i+1} (GWh)"
    })

    vars_anual.append(f"{var}.value")

script_anual = "energy = " + " + ".join(vars_anual) + ";\nreturn energy;"

anual_total = {
    "xid": f"{prefixo}_CAL_Energia Anual Total (GWh)",
    "loggingType": "INTERVAL",
    "intervalLoggingPeriodType": "MINUTES",
    "intervalLoggingType": "INSTANT",
    "purgeType": "YEARS",
    "pointLocator": {
        "dataType": "NUMERIC",
        "updateEvent": "CONTEXT_UPDATE",
        "context": context_anual,
        "executionDelayPeriodType": "SECONDS",
        "executionDelaySeconds": 0,
        "script": script_anual,
        "settable": False,
        "updateCronPattern": ""
    },
    "eventDetectors": [],
    "engineeringUnits": "",
    "purgeStrategy": "PERIOD",
    "chartColour": None,
    "chartRenderer": None,
    "dataSourceXid": f"{prefixo}_Dados Calculados",
    "defaultCacheSize": 1,
    "description": "",
    "deviceName": f"{prefixo}_Dados Calculados",
    "discardExtremeValues": False,
    "discardHighLimit": 1.7976931348623157E308,
    "discardLowLimit": -1.7976931348623157E308,
    "enabled": True,
    "eventTextRenderer": {
        "type": "EVENT_NONE"
    },
    "intervalLoggingPeriod": 5,
    "name": f"{prefixo}_CAL_Energia Anual Total (GWh)",
    "purgePeriod": 1,
    "purgeValuesLimit": 100,
    "textRenderer": {
        "type": "ANALOG",
        "format": "0.0",
        "suffix": ""
    },
    "tolerance": 0.0
}

json_final["dataPoints"].append(anual_total)

# ENERGIA ESPERADA

with open("Configuracao/JsonsConfig/EnergiaEsperada.json", "r", encoding="utf-8") as f:
    template_esperada = json.load(f)


for i in range(1, num_skids + 1):

    texto = json.dumps(template_esperada)


    texto = texto.replace("USN", prefixo)
    texto = texto.replace("Esperada 1", f"Esperada {i}")
    texto = texto.replace("Instalada 1", f"Instalada {i}")

    bloco = json.loads(texto)

    ponto = bloco["dataPoints"][0]


    json_final["dataPoints"].append(ponto)


# PR

with open("Configuracao/JsonsConfig/PR.json", "r", encoding="utf-8") as f:
    template_pr = json.load(f)


for i in range(1, num_skids + 1):

    texto = json.dumps(template_pr)


    texto = texto.replace("USN", prefixo)
    texto = texto.replace("PR 1", f"PR {i}")
    texto = texto.replace("Smart1", f"Smart{i}")
    texto = texto.replace("Instalada 1 (KWp)", f"Instalada {i} (KWp)")
    texto = texto.replace("Esperada 1 (KWh)", f"Esperada {i} (KWh)")

    bloco = json.loads(texto)

    ponto = bloco["dataPoints"][0]


    json_final["dataPoints"].append(ponto)


# POTENCIA TOTAL LOGGERS

with open("Configuracao/JsonsConfig/PotenciaAtivaTotalLoggers.json", "r", encoding="utf-8") as f:
    template_pot = json.load(f)

# cria context e script dinâmico
context_pot = []
vars_pot = []

for i in range(num_skids):
    var = letras[i]

    context_pot.append({
        "varName": var,
        "dataPointXid": f"{prefixo}_Smart{i+1}_MED_Potência Ativa Total (KW)"
    })

    vars_pot.append(f"{var}.value")

script_pot = "return " + " + ".join(vars_pot) + ";"


texto = json.dumps(template_pot)


texto = texto.replace("USN", prefixo)

bloco = json.loads(texto)

ponto = bloco["dataPoints"][0]


ponto["pointLocator"]["context"] = context_pot
ponto["pointLocator"]["script"] = script_pot


json_final["dataPoints"].append(ponto)


with open(f"saida/Calculos.json", "w", encoding="utf-8") as f:
    json.dump(json_final, f, indent=3, ensure_ascii=False)


print("\nJSON gerado com sucesso!")