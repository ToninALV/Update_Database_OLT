import time
import paramiko
import os

hostname = ["BDP-CEN-01-BNG-005","BET-GUA-01-BNG-003","CEM-TLP-01-BNG-009","CLU-CEN-01-BNG-014","CPO-ANT-01-BNG-004","IRP-CAN-01-BNG-005","LPT-CEN-01-BNG-004","PDS-JARF-01-BNG-007","SDT-CEN-01-BNG-005"]

ips = ["177.73.193.38","177.73.193.32","177.73.193.48","177.73.193.11","177.73.193.35","177.73.193.0","177.73.193.3","177.73.193.6","177.73.193.26"]

port = "6422"
username = "administrator"
password = "AS@@28198@2k22!8*C0r3#"

#path01 = "C:\Python\Colect_Clients_to_F1A_per_vlan\comando.txt"
#path02 = "C:\Python\Colect_Clients_to_F1A_per_vlan\clientes.txt" 

path01 = "C:\Python\Update_Database_OLT\comando.txt"
path02 = "C:\Python\Update_Database_OLT\clientes.txt"

try:
    os.remove(path01)
except:
    pass

def menu ():
    print("""
(1) BOM DESPACHO
(2) BETIM
(3) TELEPORTO
(4) CLÁUDIO
(5) CAMPO BELO
(6) IGARAPÉ
(7) LAGOA DA PRATA
(8) PERDÕES
(9) SAMONTE
""")

    host = int(input("Selecione o local de autenticação: "))

    if host == 1:
        host = ips[0]
        print(f"Você selecionou {hostname[0]}!")
    elif host == 2:
        host = ips[1]
        print(f"Você selecionou {hostname[1]}!")
    elif host == 3:
        host = ips[2]
        print(f"Você selecionou {hostname[2]}")
    elif host == 4:
        host = ips[3]
        print(f"Você selecionou {hostname[3]}!")
    elif host == 5:
        host = ips[4]
        print(f"Você selecionou {hostname[4]}!")
    elif host == 6:
        host = ips[5]
        print(f"Você selecionou {hostname[5]}!")
    elif host == 7:
        host = ips[6]
        print(f"Você selecionou {hostname[6]}!")
    elif host == 8:
        host = ips[7]
        print(f"Você selecionou {hostname[7]}!")
    elif host == 9:
        host = ips[8]
        print(f"Você selecionou {hostname[8]}!")

    return(host)

def get_vlans():
    cevlan_list = []
    pevlan = input("Digite a PEVLAN: ")
    if pevlan.isdigit():
        pass
    else:
        print("Valor digitado não é válido, Tente Novamente!")
        pass
    while True:
        option = input("Deseja inserir mais CEVLAN ? (S/N): ").upper()
        if option == "S":
            cevlan = input("Digite a CEVLAN: ")
            if cevlan.isdigit():
                cevlan_list.append(cevlan)
                pass
            else:
                print("Opção Inválida, Tente Novamente!")
        elif option == "N":
            break
        else:
            print("Opção Inválida, Tente Novamente!")
            pass
    list_vlans = [pevlan, cevlan_list]

    return list_vlans

def conect_equipament(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(menu(), port=port, username=username, password=password)
    print("-----CONEXÃO ESTABELECIDA-----")
    
    #open_shell = ssh.invoke_shell()
    #open_shell.send(terminal_lenght)
    stdin, stdout, stderr = ssh.exec_command(command)
    stdout = stdout.read().decode('ascii').strip("\n")
    clientes = stdout
    
    #clientes = open_shell.send(command)
    #clientes = open_shell.recv(65535).decode('utf-8')
    clientes = str(stdout)
    
    ssh.close()
    print("CONEXÃO FINALIZADA")
    return clientes

def get_clients():
    list_vlans = get_vlans()
    print(list_vlans)
    pevlan = list_vlans[0]
    cevlan_list = list_vlans[1]
    i = 0
    while i != len(cevlan_list):  
        cevlan = cevlan_list[i]
        #terminal_lenght = 'mmi-mode enable\n'
        #command = f'display access-user pevlan {pevlan} cevlan {cevlan} verbose | include name | no-more\n'
        command = f"""
            mmi-mode enable\n
            display access-user pevlan {pevlan} cevlan {cevlan} verbose | include name | no-more\n
        """
        clientes = conect_equipament(command)

        with open(path01, 'w') as arquivo:
            arquivo.write(clientes)

        with open(path02, 'a') as clientes_txt:
            clientes_txt.write(f'\nVLAN {cevlan}\n\n')
        arquivo = open(path01, 'r')
        for line in arquivo:
            if ("User name") in line:
                pppoe = line.split()
                pppoe = pppoe[3]
                with open(path02, 'a') as clientes_txt:
                    clientes_txt.write(f'{pppoe}\n')       
        i += 1

get_clients()