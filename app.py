import subprocess
import sys

while 1:

    action = input("Qual Json quer gerar?\n" \
    "1. Inversor.\n2. SmartLogger.\n3. ETM.\n4. NCU.\n5. Tracker\n6. Nobreak\n")
    action = action.upper()

    if action == "INVERSOR" or action == "1":
        subprocess.run(["python", "GerarJsonInversor.py"])
        sys.exit()
        
    elif action == "SMARTLOGGER" or action == "2":
        subprocess.run(["python", "GerarJsonSmart.py"])
        sys.exit()

    elif action == "ETM" or action == "3":
        subprocess.run(["python", "GerarJsonETM.py"])
        sys.exit()
    
    elif action == "NCU" or action == "4"   :
        subprocess.run(["python", "GerarJsonNCU.py"])
        sys.exit()    

    elif action == "TRACKER" or action == "5":
        subprocess.run(["python", "GerarJsonTracker.py"])
        sys.exit()  

    elif action == "NOBREAK" or action == "6":
        subprocess.run(["python", "GerarJsonNobreak.py"])
        sys.exit()    

    else:
        print("Json Inválido\n")
