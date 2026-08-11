import json
import copy
import os
import re
import sys
from pathlib import Path


os.makedirs("saida", exist_ok=True)

PASTA_MODELO = Path("Parque")
ARQUIVO_DATASOURCES = PASTA_MODELO / "DataSources.json"
ARQUIVO_DATAPOINTS = PASTA_MODELO / "DataPoints.json"
ARQUIVO_POINTLINKS = PASTA_MODELO / "PointLinks.json"
ARQUIVO_REFERENCIA_ORDEM = Path("Originais/Parque/RPX_.json")
PREFIXOS_REFERENCIA_FILHAS = (
    "RPA",
    "RPB",
    "RPC",
    "RPD",
    "RPE",
    "RPF",
)

PADROES_NUMERADOS_POR_SKID = (
    "CAL_Energia Esperada",
    "CAL_Energia Mensal",
    "CAL_Energia Anual",
    "CAL_PR Ajustado",
    "CAL_PR Simples",
    "VIR_Capacidade Instalada",
    "PTL_Energia Esperada",
    "PTL_Energia Mensal",
    "PTL_Energia Anual",
    "PTL_PR Ajustado",
    "PTL_PR Simples",
    "PTL_Capacidade Instalada",
)

EQUIPAMENTOS_COMPARTILHADOS = (
    ("etm", "ETM", "ETMs", 1),
    ("multimedidor", "multimedidor", "multimedidores", 1),
    ("trafo", "trafo", "trafos", 4),
    ("nobreak", "nobreak", "nobreaks", 1),
)

ETM_SUFFIXES = (
    "ETM_",
    "MED_Temperatura do Ar",
    "MED_Temperatura do M",
    "MED_Irradia",
    "MED_Acumulado Di",
    "MED_Albedometro",
    "MED_Chuva",
    "MED_C",
    "MED_Dire",
    "MED_Indice Albedo",
    "MED_Piran",
    "MED_Raz",
    "MED_Tens",
    "MED_Umidade do Ar",
    "MED_Velocidade do Vento",
    "MED_Absorvidade",
    "STA_Monitor de Conexao ETM",
)

prefixo_destino = sys.argv[1].upper()
nome_destino = sys.argv[2]


def perguntar_inteiro(texto, padrao=None):
    while True:
        sufixo = f" (Enter para usar {padrao})" if padrao is not None else ""
        valor = input(f"{texto}{sufixo}: ").strip()
        if not valor and padrao is not None:
            return padrao
        try:
            return int(valor)
        except ValueError:
            print("Informe um numero inteiro.")


def perguntar_lista_inteiros(texto, padrao=None):
    while True:
        sufixo = (
            f" (Enter para usar {','.join(map(str, padrao))})"
            if padrao else ""
        )
        valor = input(f"{texto}{sufixo}: ").strip()
        if not valor and padrao:
            return padrao[:]
        try:
            resultado = [
                int(parte.strip())
                for parte in valor.split(",")
                if parte.strip()
            ]
            if resultado:
                return resultado
        except ValueError:
            pass
        print("Informe numeros separados por virgula. Exemplo: 5,5")


def perguntar_texto(texto, padrao=""):
    sufixo = f" (Enter para usar {padrao})" if padrao else ""
    valor = input(f"{texto}{sufixo}: ").strip()
    return valor or padrao


def perguntar_prefixo_usina_filha(texto, usinas_filhas, padrao=""):
    prefixos_validos = {usina["prefixo"] for usina in usinas_filhas}
    while True:
        prefixo = perguntar_texto(texto, padrao).upper()
        if prefixo in prefixos_validos:
            return prefixo
        print("Informe um prefixo de usina filha ja cadastrado.")


def perguntar_inversores_por_skid(quantidade_skids):
    inversores_por_skid = []
    for skid in range(1, quantidade_skids + 1):
        quantidade = perguntar_inteiro(f"Quantidade de inversores no skid {skid}")
        inversores_por_skid.append(quantidade)
    return inversores_por_skid


def carregar_lista_json(caminho, chave):
    dados = json.loads(caminho.read_text(encoding="utf-8-sig"))
    if isinstance(dados, list):
        return dados
    return dados.get(chave, [])


def sufixo_sem_prefixo(texto):
    if "_" not in texto:
        return texto
    return texto.split("_", 1)[1]


def texto_equipamento(texto, equipamento):
    sufixo = sufixo_sem_prefixo(texto)

    if equipamento == "etm":
        return any(sufixo.startswith(prefixo) for prefixo in ETM_SUFFIXES)
    if equipamento == "multimedidor":
        return "_MM" in texto
    if equipamento == "trafo":
        return "_TRF" in texto
    if equipamento == "nobreak":
        return "_UPS" in texto
    return False


def numero_trafo(texto):
    match = re.search(r"_TRF(\d+)_", texto)
    return int(match.group(1)) if match else None


def numero_qgbt(texto):
    match = re.search(r"_QGBT(\d+)_", texto)
    return int(match.group(1)) if match else None


def numero_io(texto):
    match = re.search(r"_IO(\d+)_", texto)
    return int(match.group(1)) if match else None


def link_tem_equipamento(link, equipamento):
    return (
        texto_equipamento(link.get("sourcePointId", ""), equipamento)
        or texto_equipamento(link.get("targetPointId", ""), equipamento)
    )


def indice_usina_filha_por_placeholder(texto):
    match = re.search(r"\bUS(\d+)_", texto)
    return int(match.group(1)) if match else None


def texto_identificacao(item):
    return " ".join(
        str(item.get(campo, ""))
        for campo in ("xid", "name", "sourcePointId", "targetPointId")
    )


def contem_inversor_modelo(texto):
    return re.search(r"\b(?:USN|US\d+)_Inv_1\.1_", texto) is not None


def contem_smart_modelo(texto):
    return re.search(r"\b(?:USN|US\d+)_Smart1_", texto) is not None


def contem_numero_skid_modelo(texto):
    return any(
        re.search(
            rf"\b(?:USN|US\d+)_(?:Smart1_)?{re.escape(padrao)} 1\b",
            texto
        )
        for padrao in PADROES_NUMERADOS_POR_SKID
    )


def contem_timestamp_smart_modelo(texto):
    return "USN_Smart1_VIR_" in texto


def substituir_numero_skid(texto, prefixo, numero):
    for padrao in PADROES_NUMERADOS_POR_SKID:
        texto = re.sub(
            rf"\b{re.escape(prefixo)}_((?:Smart\d+_)?)"
            rf"{re.escape(padrao)} 1\b",
            rf"{prefixo}_\1{padrao} {numero}",
            texto
        )
    return texto


def substituir_numero_skid_usina_filha(texto, prefixo, numero):
    for padrao in PADROES_NUMERADOS_POR_SKID:
        texto = re.sub(
            rf"\bUS\d+_((?:Smart\d+_)?)"
            rf"{re.escape(padrao)} 1\b",
            rf"{prefixo}_\1{padrao} {numero}",
            texto
        )
    return texto


def converter_texto_por_mapa(texto, mapa, inversor=None):
    placeholder = mapa["placeholder"]
    skid_origem = mapa["skid_origem"]
    skid_destino = mapa["skid_destino"]

    if inversor is not None:
        texto = texto.replace(
            "USN_Inv_1.1",
            f"USN_Inv_{skid_destino}.{inversor}"
        )
        texto = re.sub(
            r"\bUS\d+_Inv_1\.1",
            f"{placeholder}_Inv_{skid_origem}.{inversor}",
            texto
        )
        texto = texto.replace(
            "Inversor 1.1",
            f"Inversor {skid_destino}.{inversor}"
        )

    texto = texto.replace("USN_Smart1", f"USN_Smart{skid_destino}")
    texto = re.sub(
        r"\bUS\d+_Smart1",
        f"{placeholder}_Smart{skid_origem}",
        texto
    )

    texto = substituir_numero_skid(texto, "USN", skid_destino)
    texto = substituir_numero_skid_usina_filha(
        texto,
        placeholder,
        skid_origem
    )

    return texto


def converter_item_por_mapa(item, mapa, inversor=None):
    if isinstance(item, str):
        return converter_texto_por_mapa(item, mapa, inversor)
    if isinstance(item, list):
        return [
            converter_item_por_mapa(valor, mapa, inversor)
            for valor in item
        ]
    if isinstance(item, dict):
        return {
            chave: converter_item_por_mapa(valor, mapa, inversor)
            for chave, valor in item.items()
        }
    return item


def expandir_por_skids(lista, mapa_skids, expandir_timestamp_smart=True):
    resultado = []
    for item in lista:
        texto = texto_identificacao(item)
        if contem_timestamp_smart_modelo(texto) and not expandir_timestamp_smart:
            resultado.append(item)
            continue

        expandir_inversor = contem_inversor_modelo(texto)
        expandir_smart = contem_smart_modelo(texto)
        expandir_numero_skid = contem_numero_skid_modelo(texto)

        if expandir_inversor:
            for mapa in mapa_skids:
                for inversor in range(1, mapa["qtd_inversores"] + 1):
                    resultado.append(
                        converter_item_por_mapa(
                            copy.deepcopy(item),
                            mapa,
                            inversor
                        )
                    )
        elif expandir_smart or expandir_numero_skid:
            for mapa in mapa_skids:
                resultado.append(
                    converter_item_por_mapa(copy.deepcopy(item), mapa)
                )
        else:
            resultado.append(item)

    return resultado


def substituir_prefixo(texto, antigo, novo):
    return re.sub(rf"\b{re.escape(antigo)}_", f"{novo}_", texto)



def xid_do_item(item):
    return " ".join(
        str(item.get(campo, ""))
        for campo in ("xid", "sourcePointId", "targetPointId")
    )


def usa_prefixo(texto, prefixo):
    return re.search(rf"\b{re.escape(prefixo)}_", texto) is not None


def indice_smart(texto, prefixo):
    match = re.search(rf"\b{re.escape(prefixo)}_Smart(\d+)_", texto)
    return int(match.group(1)) if match else None


def indice_inversor(texto, prefixo):
    match = re.search(rf"\b{re.escape(prefixo)}_Inv_(\d+)\.(\d+)_", texto)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def deve_manter_por_quantidade(item, prefixo, inversores_por_skid):
    texto = xid_do_item(item)
    total_skids = len(inversores_por_skid)

    smart = indice_smart(texto, prefixo)
    if smart is not None and smart > total_skids:
        return False

    inversor = indice_inversor(texto, prefixo)
    if inversor is None:
        return True

    skid, numero_inversor = inversor
    if skid > total_skids:
        return False
    return numero_inversor <= inversores_por_skid[skid - 1]


def gerar_mapa_skids(usinas_filhas):
    mapa = []
    skid_destino = 1
    for indice_usina, usina in enumerate(usinas_filhas, start=1):
        for skid_origem, qtd_inversores in enumerate(
            usina["inversores_por_skid"],
            start=1
        ):
            mapa.append({
                "placeholder": f"US{indice_usina}",
                "prefixo_origem": usina["prefixo"],
                "skid_origem": skid_origem,
                "skid_destino": skid_destino,
                "qtd_inversores": qtd_inversores
            })
            skid_destino += 1
    return mapa


def converter_texto(texto, usinas_filhas, mapa_skids):
    texto = substituir_prefixo(texto, "USN", prefixo_destino)

    for indice_usina, usina in enumerate(usinas_filhas, start=1):
        texto = substituir_prefixo(texto, f"US{indice_usina}", usina["prefixo"])

    for item in mapa_skids:
        # Corrige destino geral em Smart/Inv quando a quantidade de skids
        # for igual ou menor que a estrutura do modelo.
        texto = texto.replace(
            f"{prefixo_destino}_Smart{item['skid_destino']}_",
            f"{prefixo_destino}_Smart{item['skid_destino']}_"
        )
        texto = texto.replace(
            f"{prefixo_destino}_Inv_{item['skid_destino']}.",
            f"{prefixo_destino}_Inv_{item['skid_destino']}."
        )

    return texto


def converter_item(item, usinas_filhas, mapa_skids):
    if isinstance(item, str):
        return converter_texto(item, usinas_filhas, mapa_skids)
    if isinstance(item, list):
        return [converter_item(valor, usinas_filhas, mapa_skids) for valor in item]
    if isinstance(item, dict):
        return {
            chave: converter_item(valor, usinas_filhas, mapa_skids)
            for chave, valor in item.items()
        }
    return item


def filtrar_por_quantidades(lista, usinas_filhas, mapa_skids):
    total_skids = sum(len(usina["inversores_por_skid"]) for usina in usinas_filhas)
    inversores_destino = []
    for usina in usinas_filhas:
        inversores_destino.extend(usina["inversores_por_skid"])

    resultado = []
    for item in lista:
        if not deve_manter_por_quantidade(item, "USN", inversores_destino):
            continue

        manter = True
        for indice_usina, usina in enumerate(usinas_filhas, start=1):
            placeholder = f"US{indice_usina}"
            if not deve_manter_por_quantidade(
                item,
                placeholder,
                usina["inversores_por_skid"]
            ):
                manter = False
                break

        if manter:
            resultado.append(item)

    return resultado


def ajustar_contextos_usinas_filhas(data_points, quantidade_usinas):
    if quantidade_usinas <= 0:
        return

    for ponto in data_points:
        point_locator = ponto.get("pointLocator", {})
        contexto = point_locator.get("context", [])
        script = point_locator.get("script", "")
        if not isinstance(contexto, list) or not isinstance(script, str):
            continue
        if not contexto or not all(
            re.fullmatch(r"UF\d+", item.get("varName", ""))
            for item in contexto
        ):
            continue

        primeiro_xid = contexto[0].get("dataPointXid", "")
        match = re.match(r"US\d+_(.+)", primeiro_xid)
        if not match:
            continue

        sufixo = match.group(1)
        point_locator["context"] = [
            {
                "varName": f"UF{indice}",
                "dataPointXid": f"US{indice}_{sufixo}"
            }
            for indice in range(1, quantidade_usinas + 1)
        ]

        soma = " + ".join(
            f"UF{indice}.value"
            for indice in range(1, quantidade_usinas + 1)
        )
        if re.search(r"/\s*2\b", script):
            point_locator["script"] = f"return ({soma}) / {quantidade_usinas};"
        else:
            point_locator["script"] = f"return {soma};"


def substituir_placeholder_usina(texto, indice_origem, indice_destino):
    return re.sub(
        rf"\bUS{indice_origem}_",
        f"US{indice_destino}_",
        texto
    )


def substituir_equipamento_numerado(texto, prefixo, numero):
    texto = re.sub(rf"_{prefixo}\d+_", f"_{prefixo}{numero}_", texto)
    return texto


def expandir_links_qgbt_io(links, qgbts_por_usina):
    resultado = []
    bases_qgbt = []

    for link in links:
        texto = texto_identificacao(link)
        if "_QGBT" not in texto and "_IO" not in texto:
            resultado.append(link)
            continue

        indice_usina = indice_usina_filha_por_placeholder(texto)
        qgbt = numero_qgbt(texto)
        io = numero_io(texto)
        if indice_usina == 1 and (qgbt == 1 or io == 1):
            bases_qgbt.append(link)

    for indice_usina, quantidade_qgbts in enumerate(qgbts_por_usina, start=1):
        for numero in range(1, quantidade_qgbts + 1):
            for base in bases_qgbt:
                novo = copy.deepcopy(base)
                for campo in ("xid", "sourcePointId", "targetPointId"):
                    if campo not in novo:
                        continue
                    valor = substituir_placeholder_usina(
                        novo[campo],
                        1,
                        indice_usina
                    )
                    valor = substituir_equipamento_numerado(valor, "QGBT", numero)
                    valor = substituir_equipamento_numerado(valor, "IO", numero)
                    novo[campo] = valor
                resultado.append(novo)

    return resultado


def perguntar_equipamentos_compartilhados(usinas_filhas):
    configuracoes = {}
    primeiro_prefixo = usinas_filhas[0]["prefixo"] if usinas_filhas else ""

    print("\n--- Equipamentos compartilhados ---")
    for chave, nome, plural, padrao in EQUIPAMENTOS_COMPARTILHADOS:
        quantidade = perguntar_inteiro(f"Quantidade de {plural} compartilhados")
        prefixo = ""
        if quantidade > 0:
            prefixo = perguntar_prefixo_usina_filha(
                f"Prefixo da usina filha usada para {nome}",
                usinas_filhas,
                primeiro_prefixo
            )
        configuracoes[chave] = {
            "quantidade": quantidade,
            "prefixo": prefixo
        }

        if chave != "trafo" and quantidade > padrao:
            print(
                f"Aviso: o modelo atual possui {padrao} {nome}. "
                "Revise o JSON se a quantidade for maior."
            )

    print("\n--- QGBTs/comandos ---")
    qgbts_por_usina = []
    for indice, usina in enumerate(usinas_filhas, start=1):
        quantidade = perguntar_inteiro(
            f"Quantidade de QGBTs/comandos da usina filha {indice} "
            f"({usina['prefixo']})"
        )
        qgbts_por_usina.append(quantidade)

    return configuracoes, qgbts_por_usina


def manter_data_point_por_equipamentos(ponto, configuracoes):
    xid = ponto.get("xid", "")

    for equipamento, config in configuracoes.items():
        if not texto_equipamento(xid, equipamento):
            continue

        quantidade = config["quantidade"]
        if quantidade <= 0:
            return False

        if equipamento == "trafo":
            trafo = numero_trafo(xid)
            if trafo is not None and trafo > quantidade:
                return False

    return True


def manter_point_link_por_equipamentos(link, configuracoes, qgbts_por_usina):
    texto = texto_identificacao(link)

    for equipamento, config in configuracoes.items():
        if not link_tem_equipamento(link, equipamento):
            continue

        quantidade = config["quantidade"]
        if quantidade <= 0:
            return False

        if equipamento == "trafo":
            trafo = numero_trafo(texto)
            if trafo is not None and trafo > quantidade:
                return False

    if "_QGBT" in texto or "_IO" in texto:
        indice_usina = indice_usina_filha_por_placeholder(texto)
        qgbt = numero_qgbt(texto)
        if indice_usina is None or qgbt is None:
            return True
        if indice_usina > len(qgbts_por_usina):
            return False
        return qgbt <= qgbts_por_usina[indice_usina - 1]

    return True


def filtrar_equipamentos(data, configuracoes, qgbts_por_usina):
    data["dataPoints"] = [
        ponto
        for ponto in data.get("dataPoints", [])
        if manter_data_point_por_equipamentos(ponto, configuracoes)
    ]
    data["pointLinks"] = [
        link
        for link in data.get("pointLinks", [])
        if manter_point_link_por_equipamentos(
            link,
            configuracoes,
            qgbts_por_usina
        )
    ]


def ajustar_origem_equipamentos(data, configuracoes, usinas_filhas):
    if not usinas_filhas:
        return

    primeiro_prefixo = usinas_filhas[0]["prefixo"]
    for equipamento, config in configuracoes.items():
        prefixo_origem = config["prefixo"]
        if config["quantidade"] <= 0 or not prefixo_origem:
            continue

        for link in data.get("pointLinks", []):
            if (
                prefixo_origem != primeiro_prefixo
                and link_tem_equipamento(link, equipamento)
            ):
                link["sourcePointId"] = substituir_prefixo(
                    link.get("sourcePointId", ""),
                    primeiro_prefixo,
                    prefixo_origem
                )


def validar(data):
    avisos = []
    pontos = data.get("dataPoints", [])
    links = data.get("pointLinks", [])
    xids = [ponto.get("xid") for ponto in pontos if ponto.get("xid")]
    xids_set = set(xids)

    duplicados = sorted({xid for xid in xids if xids.count(xid) > 1})
    if duplicados:
        avisos.append(f"XIDs duplicados em dataPoints: {len(duplicados)}")

    nomes = [
        ponto.get("xid")
        for ponto in pontos
        if ponto.get("xid")
        and ponto.get("name") is not None
        and ponto.get("name") != ponto.get("xid")
    ]
    if nomes:
        avisos.append(f"dataPoints com name diferente de xid: {len(nomes)}")

    devices = [
        ponto.get("xid")
        for ponto in pontos
        if ponto.get("dataSourceXid") is not None
        and ponto.get("deviceName") is not None
        and ponto.get("dataSourceXid") != ponto.get("deviceName")
    ]
    if devices:
        avisos.append(
            f"dataPoints com deviceName diferente de dataSourceXid: {len(devices)}"
        )

    targets_ausentes = [
        link.get("targetPointId")
        for link in links
        if link.get("targetPointId", "").startswith(f"{prefixo_destino}_")
        and link.get("targetPointId") not in xids_set
    ]
    if targets_ausentes:
        avisos.append(
            "pointLinks com targetPointId ausente no proprio JSON: "
            f"{len(targets_ausentes)}"
        )

    return avisos


def eh_link_compartilhado(link, prefixo_destino, primeiro_prefixo):
    source = link.get("sourcePointId", "")
    target = link.get("targetPointId", "")

    if not source.startswith(f"{primeiro_prefixo}_"):
        return False
    if not target.startswith(f"{prefixo_destino}_"):
        return False

    # Estes grupos pertencem ao mapeamento de skids/inversores das usinas
    # filhas, nao ao equipamento compartilhado.
    grupos_por_skid = [
        "_Inv_",
        "_Smart",
        "_CAL_Energia Mensal ",
        "_CAL_Energia Anual ",
        "_CAL_PR ",
        "_CAL_Energia Esperada ",
        "_VIR_Capacidade Instalada ",
    ]
    return not any(grupo in source for grupo in grupos_por_skid)


def aplicar_origem_compartilhada(data, prefixo_compartilhado, usinas_filhas):
    if not usinas_filhas:
        return

    primeiro_prefixo = usinas_filhas[0]["prefixo"]
    if not prefixo_compartilhado or prefixo_compartilhado == primeiro_prefixo:
        return

    prefixos_validos = {usina["prefixo"] for usina in usinas_filhas}
    if prefixo_compartilhado not in prefixos_validos:
        print(
            "Aviso: prefixo de equipamento compartilhado nao encontrado "
            "entre as usinas filhas. Mantendo a primeira usina filha."
        )
        return

    for link in data.get("pointLinks", []):
        if eh_link_compartilhado(link, prefixo_destino, primeiro_prefixo):
            link["sourcePointId"] = substituir_prefixo(
                link["sourcePointId"],
                primeiro_prefixo,
                prefixo_compartilhado
            )


def texto_para_referencia_ordem(texto, usinas_filhas):
    texto = substituir_prefixo(texto, prefixo_destino, "RPX")
    for indice, usina in enumerate(usinas_filhas):
        if indice < len(PREFIXOS_REFERENCIA_FILHAS):
            texto = substituir_prefixo(
                texto,
                usina["prefixo"],
                PREFIXOS_REFERENCIA_FILHAS[indice]
            )
    return texto


def ordenar_com_referencia(data, usinas_filhas):
    if not ARQUIVO_REFERENCIA_ORDEM.exists():
        return

    referencia = json.loads(
        ARQUIVO_REFERENCIA_ORDEM.read_text(encoding="utf-8-sig")
    )

    ordem_data_points = {
        ponto.get("xid"): indice
        for indice, ponto in enumerate(referencia.get("dataPoints", []))
        if ponto.get("xid")
    }
    ordem_point_links = {
        (link.get("sourcePointId"), link.get("targetPointId")): indice
        for indice, link in enumerate(referencia.get("pointLinks", []))
    }

    def ordem_ponto(item):
        indice, ponto = item
        chave = texto_para_referencia_ordem(ponto.get("xid", ""), usinas_filhas)
        return ordem_data_points.get(chave, len(ordem_data_points) + indice)

    def ordem_link(item):
        indice, link = item
        chave = (
            texto_para_referencia_ordem(
                link.get("sourcePointId", ""),
                usinas_filhas
            ),
            texto_para_referencia_ordem(
                link.get("targetPointId", ""),
                usinas_filhas
            )
        )
        return ordem_point_links.get(chave, len(ordem_point_links) + indice)

    data["dataPoints"] = [
        ponto
        for _, ponto in sorted(enumerate(data.get("dataPoints", [])), key=ordem_ponto)
    ]
    data["pointLinks"] = [
        link
        for _, link in sorted(enumerate(data.get("pointLinks", [])), key=ordem_link)
    ]


print("\n--- Parque ---")
quantidade_usinas = perguntar_inteiro("Quantas usinas filhas existem")

usinas_filhas = []
for indice in range(1, quantidade_usinas + 1):
    print(f"\n--- Usina filha {indice} ---")
    prefixo = perguntar_texto("Prefixo da usina filha").upper()
    quantidade_skids = perguntar_inteiro("Quantidade de skids")
    inversores_por_skid = perguntar_inversores_por_skid(quantidade_skids)

    usinas_filhas.append({
        "prefixo": prefixo,
        "inversores_por_skid": inversores_por_skid
    })

configuracoes_equipamentos, qgbts_por_usina = perguntar_equipamentos_compartilhados(
    usinas_filhas
)

mapa_skids = gerar_mapa_skids(usinas_filhas)

modelo = {
    "dataSources": carregar_lista_json(ARQUIVO_DATASOURCES, "dataSources"),
    "dataPoints": expandir_por_skids(
        carregar_lista_json(ARQUIVO_DATAPOINTS, "dataPoints"),
        mapa_skids
    ),
    "pointLinks": expandir_por_skids(
        expandir_links_qgbt_io(
            carregar_lista_json(ARQUIVO_POINTLINKS, "pointLinks"),
            qgbts_por_usina
        ),
        mapa_skids,
        expandir_timestamp_smart=False
    )
}

ajustar_contextos_usinas_filhas(modelo["dataPoints"], quantidade_usinas)

filtrar_equipamentos(
    modelo,
    configuracoes_equipamentos,
    qgbts_por_usina
)

json_final = converter_item(modelo, usinas_filhas, mapa_skids)
ajustar_origem_equipamentos(
    json_final,
    configuracoes_equipamentos,
    usinas_filhas
)
ordenar_com_referencia(json_final, usinas_filhas)

saida = Path("saida") / f"{prefixo_destino}_Parque.json"
with saida.open("w", encoding="utf-8") as arquivo:
    json.dump(json_final, arquivo, indent=3, ensure_ascii=False)

with saida.open("r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()

conteudo = conteudo.replace("1.7976931348623157e+308", "1.7976931348623157E308")

with saida.open("w", encoding="utf-8") as arquivo:
    arquivo.write(conteudo)

print(f"\nArquivo Json gerado em {saida}!")
print("dataSources:", len(json_final.get("dataSources", [])))
print("dataPoints:", len(json_final.get("dataPoints", [])))
print("pointLinks:", len(json_final.get("pointLinks", [])))

avisos = validar(json_final)
if avisos:
    print("\nAvisos:")
    for aviso in avisos:
        print("-", aviso)
