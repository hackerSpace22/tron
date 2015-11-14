#!/usr/bin/python
# Plattformabhängige Tools (Shell bzw. Kommandozeile) als Funktionen zur Verfügung stellen
# programmiert von codepunX

############################################################
# Verwendete Bibliotheken:
import platform
from subprocess import *
import time
from socket import gethostbyaddr
import sys
from Net.Ip import Ip

############################################################
# Hilfsfunktionen:

# Ermitteln auf welcher Plattform das System läuft
#   siehe https://github.com/hpcugent/easybuild/wiki/OS_flavor_name_version
def isWindows():
    return platform.system() == "Windows"
def isLinux():
    return platform.system() == "Linux"
def isMac():
    return platform.system() == "Darwin"

# Ermitteln der eigenen IP-Adresse im lokalen Netzwerk
def getLocalIp(interface="eth0"):
    if isWindows():
        ifconfig = check_output("ipconfig", shell=True)
        ip = grep(ifconfig, "IPv4")[0]
        p1 = ip.find(": ")
        ip = ip[p1+2:len(ip)]
        #sm = grep(ifconfig, "Subn")
        return Ip.fromString(ip)
    
    elif isMac():
        if interface[0:3]=="eth": interface="en" + interface[3]
        if interface[0:4]=="wlan": interface="en" + str(int(interface[4])+1)
        ifconfig = check_output("ifconfig " + interface, shell=True)
        ifconfig = grep(ifconfig, "inet ")[0]
        p1 = ifconfig.find("inet ")
        p2 = ifconfig.find(" ",p1+5)
        #print(str(p1)+" "+str(p2))
        ip = ifconfig[p1+5:p2]
        return Ip.fromString(ip)
    
    else: #Linux
        ifconfig = check_output("ifconfig " + interface, shell=True)
        ifconfig = grep(ifconfig, "Mask:")[0]
        p1 = ifconfig.find("inet addr:")
        p2 = ifconfig.find("  ",p1)
        ip = ifconfig[p1+10:p2]
        return Ip.fromString(ip)

# Ermitteln des Standard Gateways (Router-IP ins INET)
def getDefaultGateway():
    if isWindows():
        ifconfig = check_output("ipconfig", shell=True)
        ip = grep(ifconfig, "gateway")[0]
        p1 = ip.find(": ")
        ip = ip[p1+2:len(ip)]
        return Ip.fromString(ip)
    
    elif isMac():
        s = check_output("route -n get default", shell=True)
        s = grep(s, "gateway")[0]
        p1 = s.find(": ")
        # print s[16:p1]
        return Ip.fromString(s[p1+2:len(s)-3])
    
    else: #Linux
        s = check_output("route -n | grep '^0.0.0.0'", shell=True)
        p1 = s.find(" ",16)
        # print s[16:p1]
        return Ip.fromString(s[16:p1])

# Reverse lookup
def nslookup(ip):
    try:
        return gethostbyaddr(str(ip))[0]
    except:
        return ""

# Ping
def ping(host, count=1, ttl=None, size=None):
    try:
        if isWindows():
            cmd = "ping "
            if count!=None: cmd += "-n "+str(count) + " "
            if ttl!=None: cmd += "-i "+str(ttl) + " "
            if size!=None: cmd += "-l "+str(size) + " "
            s = check_output(cmd + str(host), shell=True)
            s = grep(s, "Empfangen")[0]
            p1 = s.find(", Empfangen = ")
            p2 = s.find(",", p1+1)
            return int(s[p1+14:p2])>0
    
        elif isMac():
            cmd = "ping "
            if count!=None: cmd += "-c "+str(count) + " "
            if ttl!=None: cmd += "-m "+str(ttl) + " "
            if size!=None: cmd += "-s "+str(size) + " "
            s = check_output(cmd + host, shell=True)
            s = grep(s, "received")[0]
            p1 = s.find(", ")
            p2 = s.find(" packets", p1)
            return int(s[p1+2:p2])>0

        else:   #Linux
            return
        
    except(CalledProcessError):
        # ping war nicht erfolgreich
        return False

# ARP-Cache auslesen
def arpcache(ip=None, mac=None):
    if ip!=None:
        s = check_output("arp -a " + str(ip), shell=True)
        s = grep(s, str(ip)+" ")[0]
        if isWindows():
            return s[24:41]
        
    if mac!=None:
        result = []
        s = check_output("arp -a", shell=True)
        s = grep(s, str(mac)+" ")
        for line in s:
            if isWindows():
                p1 = line.find(" ",2)
                result.append(line[2:p1])
        return result

# Suche Zeilen die den angegebenen Suchtext enthalten
def grep(s, search):
    result = []
    lines = str(s).split("\\r\\n")
    #print(lines)
    for line in lines:
        if line.find(search)>=0:
            #print(line)
            result.append(line)
    return result

############################################################
### Modultest:
def test():
    print("isWindows()=" + str(isWindows()))
    print("isLinux()=" + str(isLinux()))
    print("isMac()=" + str(isMac()))
    ip = getLocalIp("wlan0")
    print("getLocalIp()=" + str(ip) + " (" + nslookup(ip) + ")")
    stdgw = getDefaultGateway()
    print("getDefaultGateway()=" + str(stdgw) + " (" + nslookup(stdgw) + ")")
    print("ping(" + str(stdgw) + ")=" + str(ping(stdgw)))
    stdgw_mac = arpcache(stdgw)
    print("arpcache(ip=" + str(stdgw) + ")=" + stdgw_mac)
    print("arpcache(mac=" + str(stdgw_mac) + ")=" + str(arpcache(mac=stdgw_mac)))

#test()
