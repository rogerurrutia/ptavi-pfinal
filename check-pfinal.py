#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script de comprobaci�n de entrega de pr�ctica

Para ejecutarlo, desde la shell: 
 $ python check-pfinal.py login_laboratorio

"""

import os
import random
import sys
import subprocess


# Diccionario con la relaci�n de nombres de usuario
# en los laboratorios (clave) y nombres de usuario en GitHub (valor)
github_dict = {
    "iarranz": "igarag",
    "smarin": "silviamaa",
    "miriammz": "miriammz",
    "rgalan": "raquelgalan",
    "jmarugan": "jfernandezmaru",
    "jcdb": "jcdb",
    "jcdb": "jcdb",
    "maferna": "mghfdez",
    "mtejedor": "mtejedorg",
    "apavo": "apavo",
    "oterino": "aoterinoc",
    "ndiaz": "nathdiaza",
    "crodrigu": "crodriguezgarci",
    "ilope": "ilope236",
    "opedraza": "olallasanchez",
    "calvarez": "calvarezpe",
    "dpascual": "dpascualhe",
    "avera": "Abel-V",
    "amoles": "alvaromv83",
    "aramas": "aramas",
    "jbaos": "JaviBM11",
    "rsierra": "rsierrangulo",
    "imalo": "nmalo5",
    "mireya": "mireepink",
    "albagc": "albagcs",
    "rpablos": "raquelpt",
    "cgarcia": "celiagarcia",
    "lyanezgu": "lyanezgu",
    "omarled": "auronff10",
    "roger": "rogerurrutia",
    "lsoria": "lsoriai",
    "zhiyuan": "ziyua",
    "mcapitan": "mcapitan",
    "juanmis": "Jmita", 
    "molina": "jmartinezmolina",
    "afrutos": "alejandrodefrutos",
}

if len(sys.argv) != 2:
    print
    sys.exit("Usage : $ python check-pfinal.py login_laboratorio")

if sys.argv[1] not in github_dict:
    print
    print "Usage: $ python check-pfinal.py login_laboratorio"
    print "donde login_laboratorio es tu login en los laboratorios Linux"
    print
    sys.exit()

repo_git = "http://github.com/" + github_dict[sys.argv[1]] + "/ptavi-pfinal"

files = ['README.md',
         'LICENSE',
         '.gitignore',
         'uaclient.py',
         'uaserver.py',
         'proxy_registar.py',
         'ua1.xml',
         'ua2.xml',
         'pr.xml',
         'llamada.libpcap',
         'error.libpcap',
         'check-pfinal.py',
         'mp32rtp',
         'cancion.mp3',
         'avanzadas.txt',
         'passwords.txt',
         '.git']

python_files = ['uaclient.py',
                'uaserver.py',
                'proxy_registrar.py']

avanzadasDict = {
    u"Cabecera proxy": 0.2,
    u"Reestablecer usuarios conectados": 0.2,
    u'Integraci�n de (c)vlc': 0.2,
    u"Pr�ctica realizada en ingl�s": 0.2,
    u"Integraci�n de (c)vlc con hilos": 0.3,
    u"Consistencia frente a valores err�neos": 0.5,
    u"Hilos para el env�o de audio v�a RTP": 0.7,
    u"Mecanismo de registro seguro": 1.0
    }


aleatorio = str(int(random.random() * 1000000))

error = 0
error_ficheros = 0
ficheros_entregados = 0
avanzadas = 0
numero_avanzadas = 0
puntuacion_max_avanzadas = 0

print 


print 
print "Clonando el repositorio " + repo_git + "\n"
os.system('git clone ' + repo_git + ' /tmp/' + aleatorio + ' > /dev/null 2>&1')
try:
    student_file_list = os.listdir('/tmp/' + aleatorio)
except OSError:
    error = 1
    print "Error: No se ha podido acceder al repositorio " + repo_git + "."
    print 
    sys.exit()


for file in student_file_list:
    if file in files:
        if file in ["avanzadas.txt", "passwords.txt"]:
            avanzadas = 1
        else:
            ficheros_entregados += 1
    else:
        error = 1
        error_ficheros = 1
        print "Error: Fichero entregado incorrecto: " + file
        print



if ficheros_entregados == len(files)-1:
    print "La entrega de la parte b�sica es correcta."
    print

if avanzadas:
    print "Se ha implementado funcionalidades avanzadas."
    print
else:
    print "No se han implementado funcionalidades avanzadas. No hay fichero avanzadas.txt"
    print
    
for filename in student_file_list:
    if filename == "avanzadas.txt":
        fich = open('/tmp/' + aleatorio + '/' + filename, 'r')
        while 1:
            line = fich.readline()
            if not line:
                break
            line = line[:-1]
            if line.decode('utf-8') in avanzadasDict:
                numero_avanzadas += 1
                puntuacion_max_avanzadas += avanzadasDict[line.decode('utf-8')]
            else:
                error = 1
                print "Error: En avanzadas.txt, se ha encontrado una funcionalidad avanzada no especificada: " + line
    if filename not in student_file_list and filename not in ["avanzadas.txt", "passwords.txt"]:
        error = 1
        error_ficheros = 1
        print "Error: " + filename + " no encontrado. Tienes que subirlo al repositorio."
        print 
    if ".libpcap" in filename:
        output = subprocess.Popen(["tshark", "-r", "/tmp/" + aleatorio + "/" + filename], stdout=subprocess.PIPE)
        output2 = subprocess.Popen(["wc"], stdin=output.stdout, stdout=subprocess.PIPE)
        lines = output2.communicate()[0].split()[0]
        if int(lines) < 1:
            print "Error: La captura realizada y guardada en " + filename + " est� vac�a."
            error = 1
        elif int(lines) > 50:
            error = 1
            print "Aviso: La captura realizada y guardada en " + filename + " contiene m�s de 50 paquetes."
            print "       Probablemente no est� filtrada convenientemente."
            print 

if error_ficheros:
    print "Error: solamente hay que subir al repositorio los ficheros indicados en las instrucciones."
    print 
    print "Utiliza 'git ls-files' para ver los ficheros que hay actualmente en el repositorio."
    print "Utiliza 'git rm fichero' para borrar los que no han de estar."
    print "Utiliza 'git mv fichero_antiguo fichero_nuevo' si tienen nombre incorrecto."
    print
    print "Al finalizar este proceso, haz un commit y pasa el check otra vez."

if puntuacion_max_avanzadas > 2.0:
    puntuacion_max_avanzadas = 2.0

if avanzadas:
    print
    print "Se han implementado " + str(numero_avanzadas) + " requisitos avanzados"
    print "La puntuaci�n m�xima que se puede obtener por requisitos avanzados es de " + str(puntuacion_max_avanzadas) + " puntos"
    print 

if not error:
    print "La salida de pep8 es: (si todo va bien, no ha de mostrar nada)"
    print
    paths = ''
    for python_file in python_files:
        paths += ' /tmp/' + aleatorio + '/' + python_file
    os.system('pep8 --repeat --show-source --statistics' + paths)
    print
    print "*****************************************************"
    print "Resultado del check: La entrega parece que se ha realizado bien."
    print "Comprueba de todas formas los mensajes del script de check."
else:
    print
    print "***************************************************"    
    print "Resultado del check: Existen errores en la entrega."
print