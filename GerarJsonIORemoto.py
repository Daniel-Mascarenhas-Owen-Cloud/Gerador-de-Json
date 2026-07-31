import copy
import json
import os
import sys


os.makedirs("saida", exist_ok=True)


def perguntar_inteiro(pergunta, minimo=1, maximo=None):
    valor = input(pergunta)

    while (
        not valor.isdigit()
        or int(valor) < minimo
        or (maximo is not None and int(valor) > maximo)
    ):
        if maximo is None:
            print(f"Valor inválido! Informe um número a partir de {minimo}.")
        else:
            print(
                f"Valor inválido! Informe um número entre {minimo} e {maximo}."
            )
        valor = input(pergunta)

    return valor


def perguntar_local():
    local = input(
        "Onde está esse IO Remoto?\n"
        "1. Skid\n"
        "2. Cabine\n"
        "Opção: "
    ).upper()

    while local not in ("1", "SKID", "2", "CABINE"):
        print("Local inválido!")
        local = input(
            "Onde está esse IO Remoto?\n"
            "1. Skid\n"
            "2. Cabine\n"
            "Opção: "
        ).upper()

    return "SKID" if local in ("1", "SKID") else "CABINE"


def perguntar_sim_nao(pergunta):
    resposta = input(pergunta).upper()

    while resposta not in ("S", "N"):
        print("Resposta inválida!")
        resposta = input(pergunta).upper()

    return resposta


def aplicar_placeholders(
    valor,
    prefix_usina,
    usina,
    IP,
    numero_io,
    numero_qgbt,
    local_equipamento,
    numero_local
):
    texto = json.dumps(valor, ensure_ascii=False)
    texto = (
        texto
        .replace("USN", prefix_usina)
        .replace("Nome Usina", usina)
        .replace("000.000.000.000", IP)
        .replace("Remota1", f"Remota{numero_io}")
        .replace("IO1", f"IO{numero_io}")
        .replace(
            "QGBT1",
            f"{'QGBT' if local_equipamento == 'Skid' else 'QMT'}{numero_qgbt}"
        )
        .replace("Skid 1", f"{local_equipamento} {numero_local}")
    )
    return json.loads(texto)


def salvar_json(caminho, valor):
    texto = json.dumps(valor, indent=3, ensure_ascii=False)
    texto = texto.replace(
        "1.7976931348623157e+308",
        "1.7976931348623157E308"
    )

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)


def gerar_io_remoto(
    numero_io,
    tipo_io_remoto,
    usina,
    prefix_usina,
    template_data_source,
    template_data_points,
    templates_point_links
):
    print(f"\n--- IO Remoto {numero_io} ---")

    IP = input("IP do IO Remoto: ")
    slave_id = int(perguntar_inteiro("Slave ID do IO Remoto: "))
    local_io_remoto = perguntar_local()

    local_equipamento = (
        "Skid" if local_io_remoto == "SKID" else "Cabine"
    )
    numero_local = str(numero_io)
    numero_qgbt = str(numero_io)

    if local_io_remoto == "SKID":
        numero_local = perguntar_inteiro("Qual o número do Skid? ")
        numero_qgbt = numero_local

    monitora_disjuntor_geral = perguntar_sim_nao(
        "Esse IO Remoto monitora o status do disjuntor geral [S/n]? "
    )

    modulo_disjuntor_fechado = None
    entrada_disjuntor_fechado = None
    modulo_disjuntor_aberto = None
    entrada_disjuntor_aberto = None

    if monitora_disjuntor_geral == "S":
        modulo_disjuntor_fechado = perguntar_inteiro(
            "Qual módulo monitora Disjuntor Fechado? "
        )
        entrada_disjuntor_fechado = perguntar_inteiro(
            "Qual entrada monitora Disjuntor Fechado? ",
            maximo=8
        )
        modulo_disjuntor_aberto = perguntar_inteiro(
            "Qual módulo monitora Disjuntor Aberto? "
        )
        entrada_disjuntor_aberto = perguntar_inteiro(
            "Qual entrada monitora Disjuntor Aberto? ",
            maximo=8
        )

    comanda_disjuntor_geral = perguntar_sim_nao(
        "Esse IO Remoto comanda o disjuntor geral [S/n]? "
    )

    modulo_saida_fechar = None
    saida_fechar = None
    modulo_saida_abrir = None
    saida_abrir = None

    if comanda_disjuntor_geral == "S":
        print("Qual saída utilizada para fechar?")
        modulo_saida_fechar = perguntar_inteiro("Módulo: ")
        saida_fechar = perguntar_inteiro("Saída: ", maximo=8)

        print("Qual saída utilizada para abrir?")
        modulo_saida_abrir = perguntar_inteiro("Módulo: ")
        saida_abrir = perguntar_inteiro("Saída: ", maximo=8)

    data_source = copy.deepcopy(template_data_source)
    data_points = copy.deepcopy(template_data_points)

    xids_disjuntor_geral = {
        "USN_QGBT1_STA_Disjuntor Geral Aberto",
        "USN_QGBT1_STA_Disjuntor Geral Fechado"
    }

    if monitora_disjuntor_geral == "N":
        data_points = [
            ponto
            for ponto in data_points
            if ponto.get("xid") not in xids_disjuntor_geral
        ]
    else:
        for ponto in data_points:
            if ponto.get("xid") in xids_disjuntor_geral:
                aberto = ponto["xid"].endswith("Aberto")
                modulo = (
                    modulo_disjuntor_aberto
                    if aberto
                    else modulo_disjuntor_fechado
                )
                entrada = (
                    entrada_disjuntor_aberto
                    if aberto
                    else entrada_disjuntor_fechado
                )
                ponto["pointLocator"]["context"][0]["dataPointXid"] = (
                    f"USN_IO1_STA_MOD{modulo}_Estado da Entrada Digital "
                    + entrada
                )

    for ponto in data_points:
        point_locator = ponto.get("pointLocator", {})
        if "slaveId" in point_locator:
            point_locator["slaveId"] = slave_id

    argumentos_replace = (
        prefix_usina,
        usina,
        IP,
        str(numero_io),
        numero_qgbt,
        local_equipamento,
        numero_local
    )

    json_io_remoto = aplicar_placeholders(
        {
            "dataSources": [data_source],
            "dataPoints": data_points
        },
        *argumentos_replace
    )

    destino_io_remoto = f"saida/IORemoto{numero_io}.json"
    salvar_json(destino_io_remoto, json_io_remoto)

    if comanda_disjuntor_geral == "S":
        for template_point_link in templates_point_links:
            point_link = copy.deepcopy(template_point_link)
            fechar = point_link["sourcePointId"].endswith(
                "Fechar Disjuntor"
            )
            modulo_saida = (
                modulo_saida_fechar if fechar else modulo_saida_abrir
            )
            numero_saida = saida_fechar if fechar else saida_abrir
            point_link["targetPointId"] = (
                f"USN_IO1_CMD_MOD{modulo_saida}_Saida Digital "
                + numero_saida
            )
            point_link = aplicar_placeholders(
                point_link,
                *argumentos_replace
            )
            nome_point_link = point_link["sourcePointId"] + ".json"
            destino_point_link = os.path.join("saida", nome_point_link)
            salvar_json(destino_point_link, point_link)

    print(f"Arquivo Json gerado em {destino_io_remoto}!")
    if comanda_disjuntor_geral == "S":
        print("Point links gerados separadamente na pasta saida!")


tipo_io_remoto = (
    sys.argv[1].upper()
    if len(sys.argv) > 1
    else input("Qual o tipo do IO remoto? ").upper()
)

while tipo_io_remoto != "D":
    print("Tipo inválido!")
    tipo_io_remoto = input("Qual o tipo do IO remoto? ").upper()

usina = sys.argv[2] if len(sys.argv) > 2 else input("Nome da usina: ")
prefix_usina = (
    sys.argv[3] if len(sys.argv) > 3 else input("Prefixo da usina: ")
)
quantidade_io_remoto = int(
    sys.argv[4]
    if len(sys.argv) > 4
    else perguntar_inteiro("Quantos IOs Remotos existem? ")
)

prefixo_template = f"IO_REMOTO_TIPO_{tipo_io_remoto}"
diretorio_template = "IO Remoto"

arquivo_data_source = os.path.join(
    diretorio_template,
    f"{prefixo_template}_DataSource.json"
)
arquivo_data_points = os.path.join(
    diretorio_template,
    f"{prefixo_template}_DataPoints.json"
)
arquivos_point_links = (
    os.path.join(
        diretorio_template,
        "USN_QGBT1_CMD_Abrir Disjuntor.json"
    ),
    os.path.join(
        diretorio_template,
        "USN_QGBT1_CMD_Fechar Disjuntor.json"
    )
)

with open(arquivo_data_source, "r", encoding="utf-8") as arquivo:
    template_data_source = json.load(arquivo)

with open(arquivo_data_points, "r", encoding="utf-8") as arquivo:
    template_data_points = json.loads("[" + arquivo.read() + "]")

templates_point_links = []
for arquivo_point_link in arquivos_point_links:
    with open(arquivo_point_link, "r", encoding="utf-8") as arquivo:
        templates_point_links.append(json.load(arquivo))

for numero_io in range(1, quantidade_io_remoto + 1):
    gerar_io_remoto(
        numero_io,
        tipo_io_remoto,
        usina,
        prefix_usina,
        template_data_source,
        template_data_points,
        templates_point_links
    )
