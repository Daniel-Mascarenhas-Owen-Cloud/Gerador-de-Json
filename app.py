import subprocess
import sys


def gerar_json_io_remoto(usina, prefixo):
    tipo_io_remoto = input("Tipo do IO Remoto: ").upper()
    quantidade_io_remoto = input("Quantos IOs Remotos existem? ")

    subprocess.run([
        "python",
        "GerarJsonIORemoto.py",
        tipo_io_remoto,
        usina,
        prefixo,
        quantidade_io_remoto
    ])


usina = input("Nome da usina: ").strip()
prefixo = input("Prefixo da usina: ")

while True:

    action = input(
        "\nQual Json quer gerar?\n"
        "0. Configuração\n"
        "1. Inversor\n"
        "2. SmartLogger\n"
        "3. ETM\n"
        "4. NCU\n"
        "5. Tracker\n"
        "6. Nobreak\n"
        "7. Multimedidor\n"
        "8. Gerar tudo\n"
        "9. Cálculos\n"
        "10. Relé\n"
        "11. Câmeras\n"
        "12. Medidor\n"
        "13. Trafo\n"
        "14. Combiner Box\n"
        "15. DJBT\n"
        "16. IO Remoto\n"
    ).upper()

    if action not in [
        "CONFIGURAÇÃO", "CONFIG", "0",
        "INVERSOR", "1",
        "SMARTLOGGER", "2",
        "ETM", "3",
        "NCU", "4",
        "TRACKER", "5",
        "NOBREAK", "6",
        "MULTIMEDIDOR", "7",
        "GERAR TUDO", "8",
        "CALCULOS", "9",
        "RELÉ", "RELE", "10",
        "CÁMERAS", "11",
        "MEDIDOR", "12",
        "TRAFO", "13",
        "COMBINER BOX", "COMBINER", "CBX", "14",
        "DJBT", "15",
        "IO REMOTO", "IO", "16",
    ]:
        print("\nOpção inválida!\n")
        sys.exit()

    gerarTudo = False
    if action in ["GERAR TUDO", "8"]:
        gerarTudo = True
        tipo_inversor = input("Tipo do inversor: ").upper()

# ---------------- CONFIG ----------------

    if action in ["CONFIGURAÇÃO", "CONFIG", "0"] or gerarTudo:

        if not gerarTudo:
            tipo_inversor = input("Tipo do inversor: ").upper()

        subprocess.run([
            "python",
            "GerarJsonConfig.py",
            prefixo,
            tipo_inversor
        ])

        if not gerarTudo:
            sys.exit()

# ---------------- INVERSOR ----------------

    if action in ["INVERSOR", "1"] or gerarTudo:

        qtd_skids = int(input("Quantos Skids existem? "))
        if not gerarTudo:
            tipo_inversor = input("Tipo do inversor ? ").upper()

        for i in range(qtd_skids):

            print(f"\n--- Skid {i+1} ---")

            ip = input("IP do DataSource: ")
            inv_quantidade = input("Quantidade de inversores: ")
            numero_slaveid = input("Primeiro slaveId: ")

            subprocess.run([
                "python",
                "GerarJsonInversor.py",
                tipo_inversor,
                usina,
                prefixo,
                str(i+1),
                ip,
                inv_quantidade,
                numero_slaveid
            ])

        if not gerarTudo:
            sys.exit()

# ---------------- SMARTLOGGER ----------------

    if action in ["SMARTLOGGER", "2"] or gerarTudo:

        qtd_skids = int(input("Quantos Skids existem? "))
        tipo_smart = input("Tipo do SmartLogger: ").upper()

        for i in range(qtd_skids):

            print(f"\n--- SmartLogger Skid {i+1} ---")

            ip = input("IP do SmartLogger: ")
            slaveID = input("Qual o SlaveId do SmartLogger? ")
            quantidade_inversores = input(
                "Quantos inversores existem neste SmartLogger? "
            )

            subprocess.run([
                "python",
                "GerarJsonSmart.py",
                tipo_smart,
                usina,
                prefixo,
                str(i+1),
                ip,
                slaveID,
                quantidade_inversores,
                str(qtd_skids)
            ])

        if not gerarTudo:
            sys.exit()

# ---------------- ETM ----------------

    if action in ["ETM", "3"] or gerarTudo:

        quantidade = int(input("Quantos ETM existem? "))
        tipo = input("Tipo do ETM: ").upper()
        if tipo == "C":
            slaveId = "60"
        else:
            slaveId = input("Qual SlaveId: ")

        for i in range(quantidade):

            print(f"\n--- ETM {i+1} ---")

            ip = input("IP do ETM: ")

            subprocess.run([
                "python",
                "GerarJsonETM.py",
                tipo,
                prefixo,
                ip,
                slaveId,
                str(i+1)
            ])

        if not gerarTudo:
            sys.exit()

# ---------------- NCU ----------------

    if action in ["NCU", "4"] or gerarTudo:

        quantidade = int(input("Quantas NCUs existem? "))
        tipo = input("Tipo da NCU: ")

        for i in range(quantidade):

            print(f"\n--- NCU {i+1} ---")

            ip = input("IP do DataSource: ")

            argumentos = [
                "python",
                "GerarJsonNCU.py",
                tipo,
                usina,
                prefixo,
                str(i+1),
                ip
            ]

            if tipo.strip().upper() == "C":
                quantidade_trackers = input("Quantas SKC existem nesta NCU? ")
                argumentos.append(quantidade_trackers)

                for numero_tracker in range(1, int(quantidade_trackers) + 1):
                    quantidade_motores = input(
                        f"Quantos motores tem a SKC {i+1}.{numero_tracker}? "
                    )
                    argumentos.append(quantidade_motores)

            subprocess.run(argumentos)

        if not gerarTudo:
            sys.exit()

# ---------------- TRACKER ----------------

    if action in ["TRACKER", "5"] or gerarTudo:

        quantidade = int(input("Quantas NCUs com Trackers existem? "))
        tipo_tracker = input("Tipo do Tracker: ")

        for i in range(quantidade):

            print(f"\n--- Tracker grupo {i+1} ---")

            ip = input("IP do Tracker: ")
            qtd_trackers = input("Quantidade de Trackers: ")

            subprocess.run([
                "python",
                "GerarJsonTracker.py",
                tipo_tracker,
                usina,
                prefixo,
                str(i+1),
                ip,
                qtd_trackers
            ])

        if not gerarTudo:
            sys.exit()

# ---------------- IO REMOTO ----------------

    if action in ["IO REMOTO", "IO", "16"] or gerarTudo:

        gerar_json_io_remoto(usina, prefixo)

        if not gerarTudo:
            sys.exit()

# ---------------- NOBREAK ----------------

    if action in ["NOBREAK", "6"] or gerarTudo:

        print("\n--- Nobreak ---")

        tipo_equipamento = input("Tipo do Nobreak: ")
        ip = input("IP do Nobreak: ")

        subprocess.run([
            "python",
            "GerarJsonNobreak.py",
            tipo_equipamento,
            usina,
            prefixo,
            ip
        ])

        if not gerarTudo:
            sys.exit()

# ---------------- MULTIMEDIDOR ----------------

    if action in ["MULTIMEDIDOR", "7"] or gerarTudo:

        quantidade = int(input("Quantos Multimedidores existem? "))
        tipo_multimedidor = input("Tipo do Multimedidor: ")

        for i in range(quantidade):

            print(f"\n--- Multimedidor {i+1} ---")

            ip = input("IP do DataSource: ")
            slave_id = input("Slave Address: ")

            subprocess.run([
                "python",
                "GerarJsonMultimedidor.py",
                tipo_multimedidor,
                usina,
                prefixo,
                str(i+1),
                ip,
                slave_id
            ])

        if not gerarTudo:
            sys.exit()

# ---------------- CALCULOS ----------------

    if action in ["CALCULOS", "CALCULO", "9"] or gerarTudo:

        qtd_skids = int(input("Quantos skids existem? "))
        if not gerarTudo:
            tipo_inversor = input("Tipo do inversor: ").upper()

        inversores = []

        for i in range(qtd_skids):

            print(f"\n--- Skid {i+1} ---")

            qtd = input("Quantidade de inversores neste skid: ")
            inversores.append(qtd)

        subprocess.run([
            "python",
            "GerarJsonCalculos.py",
            prefixo,
            str(qtd_skids),
            ",".join(inversores),
            tipo_inversor
        ])

        if not gerarTudo:
            sys.exit()


# ---------------- RELÉ ----------------

    if action in ["RELÉ", "RELE", "10"] or gerarTudo:

        qtd_rele = int(input("Quantos relés existem? ").strip())
        tipo_rele = input("Qual o tipo dos relés? ").strip()

        for i in range(qtd_rele):

            print(f"\n--- Relé {i+1} ---")

            ip = input("IP do Relé: ").strip()
            slave_id = input("Qual o SlaveId do relé? ").strip()
            numero_rele = input("Qual o número do relé? ").strip()
            Cabine = input("Qual a cabine do relé? ").strip()

            numeroDoGerador = i + 1

            subprocess.run([
                "python",
                "GerarJsonRele.py",
                tipo_rele,
                usina,
                prefixo,
                ip,
                str(slave_id),
                str(numero_rele),
                str(Cabine),
                str(numeroDoGerador)
            ])

        if not gerarTudo:
            sys.exit()

# ---------------- CAMERAS ----------------

    if action in ["CAMERAS", "11"] or gerarTudo:

        qtd_cameras = input("Quantas câmeras existem? ")
        ip = input("IP das Câmeras: ")
        offset = input("Qual o offset de início das Câmeras? ")


        subprocess.run([
            "python",
            "GerarJsonCameras.py",
            usina,
            prefixo,
            ip,
            offset,
            qtd_cameras
            ])

        if not gerarTudo:
            sys.exit()



# ---------------- MEDIDOR ----------------

    if action in ["MEDIDOR", "12"] or gerarTudo:

        quantidade = int(input("Quantos Medidores existem? "))
        tipo_multimedidor = input("Tipo do Medidor: ")

        for i in range(quantidade):

            print(f"\n--- Multimedidor {i+1} ---")

            ip = input("IP do DataSource: ")

            subprocess.run([
                "python",
                "GerarJsonMedidor.py",
                tipo_multimedidor,
                usina,
                prefixo,
                ip,
                str(i+1)
            ])

        if not gerarTudo:
            sys.exit()

# ---------------- COMBINER BOX ----------------

    if action in ["COMBINER BOX", "COMBINER", "CBX", "14"] or gerarTudo:

        qtd_skids = int(input("Quantos Skids com Combiner Box existem? "))
        tipo_combiner = input("Tipo da Combiner Box: ").upper()

        for i in range(qtd_skids):

            print(f"\n--- Combiner Box Skid {i+1} ---")

            ip = input("IP do DataSource: ")
            cbx_quantidade = int(input("Quantidade de Combiner Boxes: "))
            slave_ids = []

            for cbx in range(cbx_quantidade):
                slave_ids.append(input(f"SlaveId da Combiner Box {cbx + 1}: "))

            subprocess.run([
                "python",
                "GerarJsonCombinerBox.py",
                tipo_combiner,
                usina,
                prefixo,
                str(i+1),
                ip,
                str(cbx_quantidade),
                ",".join(slave_ids)
            ])

        if not gerarTudo:
            sys.exit()
            

# ---------------- TRAFO ----------------

    if action in ["Trafo", "13"] or gerarTudo:

        quantidade = int(input("Quantos Trafos existem? "))
        tipo_trafo = input("Tipo do Trafo: ")

        for i in range(quantidade):

            print(f"\n--- Trafo {i+1} ---")

            ip = input("IP do DataSource: ")

            slave_id = input("Slave Address: ")

            skid = input("Número do Skid: ")

            numero_trafo = input("Número do Trafo: ")

            subprocess.run([
                "python",
                "GerarJsonTrafo.py",
                tipo_trafo,
                usina,
                prefixo,
                ip,
                slave_id,
                skid,
                numero_trafo,
                str(i+1)
            ])
            

# ---------------- DJBT ----------------

    if action in ["DJBT", "15"] or gerarTudo:

        tipo = input("Tipo do Disjuntor BT: ").upper()

        print("\n--- DJBT ---")

        ip = input("IP do DJBT: ")

        skid = input("Número do Skid: ")

        numero_djbt = input("Qual o número do disjuntor? ").strip()

        subprocess.run([
            "python",
            "GerarJsonDJBT.py",
            tipo,
            prefixo,
            usina,
            ip,
            skid,
            numero_djbt
        ])

        if not gerarTudo:
            sys.exit()


    if not gerarTudo:
        sys.exit()

    print("\nTodos os JSON foram gerados!")

    unir = input("\nDeseja unir os arquivos em um unico arquivo? (S/N): ").upper()

    if unir == "S":
        subprocess.run(["python","UnirJsons.py"])
        sys.exit()
