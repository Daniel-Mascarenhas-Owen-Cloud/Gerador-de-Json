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
    ).upper()

# ---------------- CONFIG ----------------

    if action in ["CONFIGURAÇÃO", "CONFIG", "0"]:

        subprocess.run([
            "python",
            "GerarJsonConfig.py",
            prefixo
        ])

        sys.exit()

# ---------------- INVERSOR ----------------

    elif action in ["INVERSOR", "1"]:

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

        sys.exit()

# ---------------- SMARTLOGGER ----------------

    elif action in ["SMARTLOGGER", "2"]:

        qtd_skids = int(input("Quantos Skids existem? "))
        tipo_smart = input("Tipo do SmartLogger: ").upper()

        for i in range(qtd_skids):

            print(f"\n--- SmartLogger Skid {i+1} ---")

            ip = input("IP do SmartLogger: ")

            subprocess.run([
                "python",
                "GerarJsonSmart.py",
                tipo_smart,
                usina,
                prefixo,
                str(i+1),
                ip
            ])

        sys.exit()

# ---------------- ETM ----------------

    elif action in ["ETM", "3"]:

        quantidade = int(input("Quantos ETM existem? "))
        tipo = input("Tipo do ETM: ").upper()

        for i in range(quantidade):

            print(f"\n--- ETM {i+1} ---")

            ip = input("IP do ETM: ")

            subprocess.run([
                "python",
                "GerarJsonETM.py",
                tipo,
                prefixo,
                ip
            ])

        sys.exit()

# ---------------- NCU ----------------

    elif action in ["NCU", "4"]:

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

        sys.exit()

# ---------------- TRACKER ----------------

    elif action in ["TRACKER", "5"]:

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

        sys.exit()

# ---------------- NOBREAK ----------------

    elif action in ["NOBREAK", "6"]:

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

        sys.exit()

# ---------------- MULTIMEDIDOR ----------------

    elif action in ["MULTIMEDIDOR", "7"]:

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

        sys.exit()

# ---------------- CALCULOS ----------------

    elif action in ["CALCULOS", "CALCULO", "9"]:

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

        sys.exit()

# ---------------- GERAR TUDO ----------------

    elif action in ["GERAR TUDO", "8"]:

        print("\n=== CONFIGURAÇÃO DOS EQUIPAMENTOS ===\n")

        subprocess.run(["python", "GerarJsonConfig.py", prefixo])

        qtd_skids = int(input("Quantos Skids existem? "))

        tipo_inversor = input("Tipo do inversor: ").upper()
        tipo_smart = input("Tipo do SmartLogger: ").upper()

        inversores_lista = []

# INVERSORES

        for i in range(qtd_skids):

            print(f"\n--- Skid Inversor {i+1} ---")

            ip_inv = input("IP do DataSource: ")
            inv_quantidade = input("Quantidade de inversores: ")
            numero_slaveid = input("Primeiro slaveId: ")

            inversores_lista.append(inv_quantidade)

            subprocess.run([
                "python","GerarJsonInversor.py",
                tipo_inversor,usina,prefixo,str(i+1),
                ip_inv,inv_quantidade,numero_slaveid
            ])

# SMARTLOGGER

        for i in range(qtd_skids):

            print(f"\n--- SmartLogger Skid {i+1} ---")

            ip_smart = input("IP do SmartLogger: ")

            subprocess.run([
                "python","GerarJsonSmart.py",
                tipo_smart,usina,prefixo,str(i+1),ip_smart
            ])

# CALCULOS

        print("\nGerando cálculos...")

        subprocess.run([
            "python",
            "GerarJsonCalculos.py",
            prefixo,
            str(qtd_skids),
            ",".join(inversores_lista),
        ])

        print("\nTodos os JSON foram gerados!")

        unir = input("\nDeseja unir os arquivos em um unico arquivo? (S/N): ").upper()

        if unir == "S":
            subprocess.run(["python","UnirJsons.py"])

        sys.exit()

    else:
        print("Json Inválido\n")
