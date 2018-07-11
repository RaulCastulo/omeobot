import telebot
import time
import os
import subprocess
from operator import itemgetter
from telebot import types
from datetime import datetime
"""
Otros nodos
temp_warning = 45
temp_critical = 50

Nodos Blade
temp_warning = 60
temp_critical = 65
"""

def consulta_temperaturas_kraken():
    temp_warning = 45
    temp_critical = 50
	
    system_temp = subprocess.getoutput("ssh chacmol clush -w kraken ipmi-sensors -t temperature | grep \"System Temp\" | awk \'{print $9}\'")
    peripheral_temp = subprocess.getoutput("ssh chacmol clush -w kraken ipmi-sensors -t temperature | grep \"Peripheral Temp\" | awk \'{print $9}\'")
	
    kraken_system_temp = int(system_temp.rstrip("00").rstrip("."))
    kraken_peripheral_temp = int(peripheral_temp.rstrip("00").rstrip("."))

    temp_max = max(kraken_system_temp,kraken_peripheral_temp)
    info_status_temp = ""

    if (kraken_system_temp >= temp_critical) and (kraken_peripheral_temp < temp_warning):
        info_status_temp = "kraken: " + str(temp_max) + "C Status: CRITICAL"
    elif (kraken_system_temp >= temp_critical) and (kraken_peripheral_temp >= temp_warning and kraken_peripheral_temp < temp_critical):
        info_status_temp = "kraken: " + str(temp_max) + "C Status: CRITICAL"
    elif (kraken_system_temp >= temp_critical) and (kraken_peripheral_temp >= temp_critical):
        info_status_temp = "kraken: " + str(temp_max) + "C Status: CRITICAL"
    elif (kraken_system_temp >= temp_warning and kraken_system_temp < temp_critical) and (kraken_peripheral_temp < temp_warning):
        info_status_temp = "kraken: " + str(temp_max) + "C Status: WARNING"
    elif (kraken_system_temp >= temp_warning and kraken_system_temp < temp_critical) and (kraken_peripheral_temp >= temp_warning and kraken_peripheral_temp < temp_critical):
        info_status_temp = "kraken: " + str(temp_max) + "C Status: WARNING"
    elif (kraken_system_temp >= temp_warning and kraken_system_temp < temp_critical) and (kraken_peripheral_temp >= temp_critical):
        info_status_temp = "kraken: " + str(temp_max) + "C Status: CRITICAL"
    elif (kraken_system_temp < temp_warning) and (kraken_peripheral_temp < temp_warning):
        pass
    elif (kraken_system_temp < temp_warning) and (kraken_peripheral_temp >= temp_warning and kraken_peripheral_temp < temp_critical):
        info_status_temp = "kraken: " + str(temp_max) + "C Status: WARNING"
    else:
        info_status_temp = "kraken: " + str(temp_max) + "C Status: CRITICAL"

    if info_status_temp == "":
        info_status_temp = "kraken Status Temperature: NORMAL"

    return info_status_temp

def consulta_temperaturas_nodos(node_list, node_name):
    if node_name == "oss":
        temp_warning = 45
        temp_critical = 50
    else:
        temp_warning = 60
        temp_critical = 65
	
    consulta_system_temp = subprocess.getoutput("ssh chacmol clush -w " + node_list + " ipmi-sensors -t temperature | grep \"System Temp\" | awk \'{print $1,$9}\'")
    lista_auxiliar_system_temp = consulta_system_temp.splitlines()
    datos_system_temp=[]

    for elemento in lista_auxiliar_system_temp:
        arreglo_aux=elemento.split(": ")
        arreglo_aux[0] = int(arreglo_aux[0].lstrip(node_name))
        arreglo_aux[1] = int(arreglo_aux[1].rstrip("00").rstrip("."))
        datos_system_temp.append(arreglo_aux)

    datos_system_temp.sort(key=itemgetter(0))

    consulta_peripheral_temp = subprocess.getoutput("ssh chacmol clush -w " + node_list + " ipmi-sensors -t temperature | grep \"Peripheral Temp\" | awk \'{print $1,$9}\'")
    lista_auxiliar_peripheral_temp = consulta_peripheral_temp.splitlines()
    datos_peripheral_temp=[]

    for elemento in lista_auxiliar_peripheral_temp:
        arreglo_aux=elemento.split(": ")	
        arreglo_aux[0] = int(arreglo_aux[0].lstrip(node_name))
        arreglo_aux[1] = int(arreglo_aux[1].rstrip("00").rstrip("."))
        datos_peripheral_temp.append(arreglo_aux)

    datos_peripheral_temp.sort(key=itemgetter(0))

    temperaturas_nodos = []
    if len(datos_system_temp) == len(datos_peripheral_temp):
        numero_elementos = len(datos_system_temp)
        for indice in range(numero_elementos):
            arreglo_aux = []
            arreglo_aux.append(node_name+str(datos_system_temp[indice][0]))
            arreglo_aux.append(datos_system_temp[indice][1])
            arreglo_aux.append(datos_peripheral_temp[indice][1])
            temperaturas_nodos.append(arreglo_aux)
            arreglo_aux = []


    temp_max = 0
    info_status_temp = ""
    for elemento in temperaturas_nodos:
        temp_max = max(elemento[1],elemento[2])
		
        if (elemento[1] >= temp_critical) and (elemento[2] < temp_warning):
            info_status_temp = info_status_temp + (elemento[0] + ": " + str(temp_max) + "C Status: CRITICAL\n")
        elif (elemento[1] >= temp_critical) and (elemento[2] >= temp_warning and elemento[2] < temp_critical):
            info_status_temp = info_status_temp + (elemento[0] + ": " + str(temp_max) + "C Status: CRITICAL\n")
        elif (elemento[1] >= temp_critical) and (elemento[2] >= temp_critical):
            info_status_temp = info_status_temp + (elemento[0] + ": " + str(temp_max) + "C Status: CRITICAL\n")
        elif (elemento[1] >= temp_warning and elemento[1] < temp_critical) and (elemento[2] < temp_warning):
            info_status_temp = info_status_temp + (elemento[0] + ": " + str(temp_max) + "C Status: WARNING\n")
        elif (elemento[1] >= temp_warning and elemento[1] < temp_critical) and (elemento[2] >= temp_warning and elemento[2] < temp_critical):
            info_status_temp = info_status_temp + (elemento[0] + ": " + str(temp_max) + "C Status: WARNING\n")
        elif (elemento[1] >= temp_warning and elemento[1] < temp_critical) and (elemento[2] >= temp_critical):
            info_status_temp = info_status_temp + (elemento[0] + ": " + str(temp_max) + "C Status: CRITICAL\n")
        elif (elemento[1] < temp_warning) and (elemento[2] < temp_warning):
            pass
        elif (elemento[1] < temp_warning) and (elemento[2] >= temp_warning and elemento[2] < temp_critical):
            info_status_temp = info_status_temp + (elemento[0] + ": " + str(temp_max) + "C Status: WARNING\n")
        else:
            info_status_temp = info_status_temp + (elemento[0] + ": " + str(temp_max) + "C Status: CRITICAL\n")

    if info_status_temp == "":
        info_status_temp = node_list + " Status Temperature: NORMAL"

    return info_status_temp


bot = telebot.TeleBot("462397223:AAHSB40mXlifDJoJilaYgJeJ_lBJYGggsms")

contador = 300
while True:	
    if contador%300 == 0:
        print(time.strftime("%d-%m-%Y %H:%M:%S"))
        info_temp_status_nodes = consulta_temperaturas_nodos("node[1-40]","node")
        if info_temp_status_nodes != "node[1-40] Status Temperature: NORMAL":
            bot.send_message(str(-290650208),info_temp_status_nodes)
        else:
            print(info_temp_status_nodes)
        
        info_temp_status_oss = consulta_temperaturas_nodos("oss[1-5]","oss")	
        if info_temp_status_oss != "oss[1-5] Status Temperature: NORMAL":
            bot.send_message(str(-290650208),info_temp_status_oss)
        else:
            print(info_temp_status_oss)
        
        info_temp_status_kraken = consulta_temperaturas_kraken()
        if info_temp_status_kraken != "kraken Status Temperature: NORMAL":
            bot.send_message(str(-290650208),info_temp_status_kraken)
        else:
            print(info_temp_status_kraken)
        
        contador = 0

    contador +=10
    time.sleep(10)

