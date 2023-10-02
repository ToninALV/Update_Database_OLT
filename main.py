import time
import paramiko
import os

hostname = ["BDP-CEN-01-BNG-005","BET-GUA-01-BNG-003","CEM-TLP-01-BNG-009","DVL-VSA-01-BNG-014","CPO-ANT-01-BNG-004","IRP-CAN-01-BNG-005","LPT-CEN-01-BNG-004","PDS-JARF-01-BNG-007","SDT-CEN-01-BNG-005"]
ips = ["177.73.193.38","177.73.193.32","177.73.193.48","177.73.193.11","177.73.193.35","177.73.193.0","177.73.193.3","177.73.193.6","177.73.193.26"]

port = "6422"
username = "administrator"
password = "AS@@28198@2k22!8*C0r3#"

#path01 = "C:\\Python\\Update_Database_OLT\\comando.txt"
#path02 = "C:\\Python\\Update_Database_OLT\\clientes.txt"

path01 = "comando.txt"
path02 = "clientes.txt"
path03 = "total.txt"

try:
    os.remove(path01)
    os.remove(path02)
    os.remove(path03)
except:
    pass

def menu ():
    print("""
----- LOCAIS DE AUTENTICAÇÃO -----
          
(1) BOM DESPACHO
(2) BETIM
(3) TELEPORTO
(4) DIVINÓPOLIS
(5) CAMPO BELO
(6) IGARAPÉ
(7) LAGOA DA PRATA
(8) PERDÕES
(9) SAMONTE
""")

    host = int(input("Selecione o local de autenticação: "))
    match host:
        case 1:
            host = ips[0]
            print(f"Você selecionou {hostname[0]}!")
        case 2:
            host = ips[1]
            print(f"Você selecionou {hostname[1]}!")
        case 3:
            host = ips[2]
            print(f"Você selecionou {hostname[2]}!")
        case 4:
            host = ips[3]
            print(f"Você selecionou {hostname[3]}!")
        case 5:
            host = ips[4]
            print(f"Você selecionou {hostname[4]}!")
        case 6:
            host = ips[5]
            print(f"Você selecionou {hostname[5]}!")
        case 7:
            host = ips[6]
            print(f"Você selecionou {hostname[6]}!")
        case 8:
            host = ips[7]
            print(f"Você selecionou {hostname[7]}!")
        case 9:
            host = ips[8]
            print(f"Você selecionou {hostname[8]}!")
        case _:
            print("Opção Inválida, Tente Novamente!!!")
            return menu()

    return host

def get_vlans():
    cevlan_list = []

    pevlan = input("Digite a PEVLAN: ")
    if pevlan.isdigit():
        pass
    else:
        print("Valor digitado não é válido, Tente Novamente!")
        pass

    option = input("Deseja inserir um range de VLANS ? (S/N): ").upper()
    if option == "S":
        vlan_inicial = int(input("Digite a primeira VLAN: "))
        vlan_final = int(input("Digite a última VLAN: "))
        range = int(input("Digite a quantidade de Saltos por VLAN:: "))
        vlan = vlan_inicial
        while vlan <= vlan_final:
            cevlan_list.append(vlan)
            vlan = vlan + range    
        list_vlans = [pevlan, cevlan_list]

        return list_vlans    
    elif option == "N":
        pass

    cevlan = input("Digite a CEVLAN: ")
    if cevlan.isdigit():
        cevlan_list.append(cevlan)
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

def conect_equipament(command, host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=username, password=password)
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

    host = menu()
    
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
        clientes = conect_equipament(command, host)

        with open(path01, 'w') as arquivo:
            arquivo.write(clientes)

        with open(path02, 'a') as clientes_txt:
            clientes_txt.write(f'\nVLAN {cevlan}\n\n')
        arquivo = open(path01, 'r')

        c = 0
        for line in arquivo:
            if ("User name") in line:
                pppoe = line.split()
                pppoe = pppoe[3]
                with open(path02, 'a') as clientes_txt:
                    clientes_txt.write(f'{pppoe}\n')
                    c += 1  
        i += 1

        with open(path02, 'a') as clientes_txt:
            clientes_txt.write(f'\nClientes na VLAN {cevlan}: {c}\n\n')

    valor_total = []
    with open(path02, 'r') as total_clientes:
        for line in total_clientes:
            if ("Clientes na VLAN") in line:
                total = line.split()
                total = total[4]
                if total.isdigit():
                    valor_total.append(int(total))

        valor_total = sum(valor_total)
        with open(path03, "a") as arquivo:
            arquivo.write(f'Quantidade total desta busca: {valor_total}\n')

    try:
        os.remove(path01)
    except:
        pass

get_clients()