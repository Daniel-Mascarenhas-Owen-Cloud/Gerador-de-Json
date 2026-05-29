import subprocess
import sys

usina = input("Nome da usina: ")
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
        "8. GERAR TUDO\n"
        "9. CALCULOS\n"
        "10. Relé\n"
        "11. Câmeras\n"
        "12. Medidor\n"
        "13. Trafo\n"
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
        "TRAFO", "13"
    ]:
        print("\nOpção inválida!\n")
        sys.exit()

    gerarTudo = False
    if action in ["GERAR TUDO", "8"]:
        gerarTudo = True

# ---------------- CONFIG ----------------

    if action in ["CONFIGURAÇÃO", "CONFIG", "0"]:

        subprocess.run([
            "python",
            "GerarJsonConfig.py",
            prefixo
        ])

        if not gerarTudo:
            sys.exit()

# ---------------- INVERSOR ----------------

    if action in ["INVERSOR", "1"] or gerarTudo:

        qtd_skids = int(input("Quantos Skids existem? "))
        tipo_inversor = input("Tipo do inversor (B ou C): ").upper()

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

            subprocess.run([
                "python",
                "GerarJsonSmart.py",
                tipo_smart,
                usina,
                prefixo,
                str(i+1),
                ip,
                slaveID
            ])

        if not gerarTudo:
            sys.exit()

# ---------------- ETM ----------------

    if action in ["ETM", "3"] or gerarTudo:

        quantidade = int(input("Quantos ETM existem? "))
        tipo = input("Tipo do ETM: ").upper()
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

            subprocess.run([
                "python",
                "GerarJsonNCU.py",
                tipo,
                usina,
                prefixo,
                str(i+1),
                ip
            ])

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
            str(qtd_skids)
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

        quantidade = int(input("Quantos Multimedidores existem? "))
        tipo_multimedidor = input("Tipo do Multimedidor: ")

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

    if not gerarTudo:
        sys.exit()

    print("\nTodos os JSON foram gerados!")

    unir = input("\nDeseja unir os arquivos em um unico arquivo? (S/N): ").upper()

    if unir == "S":
        subprocess.run(["python","UnirJsons.py"])
        sys.exit()

        
    

    