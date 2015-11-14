#!/usr/bin/python
# TRON (TRace-ON) - your personal guard in the network
# programmiert von codepunX

APP_NAME = "TRON"
APP_INFO = "TRON (TRace-ON) - your personal guard in the network"
APP_VERSION = 0.1
# Versionen
#   0.1 2015-11-14  Erste Version mit ARP-Spoofing Erkennung und GUI

############################################################
# Globale Einstellungen:
g_interface = "wlan0"   # Schnittstelle die überprüft wird


############################################################
# Verwendete Bibliotheken:

from Net.Ip import Ip
from Net import Toolkit
import time
import _thread
import os
import tkinter
from tkinter import *
from tkinter.ttk import *


############################################################
# Hilfsfunktionen:

# Meldungen auf die Konsole ausgeben
def log(s):
    print(s)

# Meldungen auf die Konsole, die aktuellste Meldung in der GUI (Status) anzeigen
def logStatus(s):
    log(s)
    varStatus.set(s)

############################################################
# Hauptfunktionen:
def antiArpSpoof(host_ip, stdgw_ip, stdgw_mac):
    # Initialisierung
    logStatus("Initializing ARP-Spoof detection ...")

    # Das Standardgateway muss direkt (mit IPv4:TTL=1) erreicht werden können,
    # sonst könnte es bereits gespoofed sein.
    if not Toolkit.ping(stdgw_ip, ttl=1):
        logStatus("Could not reach StdGW via ping directly.")
        logStatus("StdGw ist spoofed or ICMP is deactivated!")
        logStatus("ALERT:Can not verfiy StdGw operation - STOPPED!")
        return
    logStatus("StdGw is directly reachable per PING --> not spoofed!")

    logStatus("Doing continous anti-ARP-Spoofing checking...")
    try:
        warn = False
        alert = False
        while True:
            time.sleep(1)   # überprüfe jede Sekunde

            # Hat sich die MAC-Adresse des StdGW im ARP-cache geändert?
            mac = Toolkit.arpcache(stdgw_ip)
            if mac!=stdgw_mac:
                # Ja, dann könnte eine ARP-Spoofing Attacke im Laufen sein
                if not warn:
                    logStatus("WARNING:Detected MAC-address change of standard-gateway to " + mac)
                    warn = True
                    top.deiconify() # Zeige Fenster als Popup bei Warnungen
                if not Toolkit.ping(stdgw_ip):
                    logStatus("ALERT:Lost network connection!")
                    # TODO: Netzausfall, möglicherweise auch Isolate-Host Angriff
                elif not Toolkit.ping(stdgw_ip, ttl=1):
                    # Zwischen Host und StdGW liegt ein anderer dazwischen --> Man-in-the-Middle
                    if not alert:
                        alert = True
                        top.deiconify() # Zeige Fenster als Popup bei Alarmen
                        logStatus("ALERT:Detected ARP-spoofing attack from " + mac + "!");
                    attacker_ip = hostinfo(mac=mac, excludeip=stdgw_ip, label="attacker")
                    if attacker_ip!=None:
                        countermeasures(attacker_ip)
                    #return
            else:
                # Nein, dann besteht keine Gefahr
                if warn or alert:
                    warn = False
                    alert = False
                    logStatus("Doing continous anti-ARP-Spoofing checking...")
                
    except(KeyboardInterrupt,SystemExit):
        logStatus("Anti-ARP-spoofing stopped.")

# Informationen über einen Host sammeln (z.B. vom Angreifer):
def hostinfo(ip=None, mac=None, excludeip=None, label="Host"):
    s = "Retrieving " + label + " info: \n"
    if mac!=None:
        # Suche nach Host über die MAC-Adresse im ARP-Cache
        s += "  mac-address: " + mac + " \n"
        ips = Toolkit.arpcache(mac=mac)
        for i in ips:
            if excludeip==None or str(i)!=str(excludeip):
                ip = i

    if ip!=None:
        s += "  ip-address:  " + str(ip) + " \n"
        s += "  hostname:    " + Toolkit.nslookup(ip)
        logStatus(s)
        return ip
    log(s)

# Gegenmaßnamen um den Angreifer abzuwehren
def countermeasures(ip):
    print("Performing countermeasures against attacker " + str(ip))
    # TODO - noch zu implementieren
    return
        
############################################################
# Hauptprogramm (mit GUI):
top = tkinter.Tk()  # Hauptfenster
varStatus = StringVar()
def main():
    ## GUI:
    top.title(APP_NAME + " V" + str(APP_VERSION) )  # Fenstertitel
    if "nt" == os.name:
        top.wm_iconbitmap(bitmap = "res/tron.ico")  # Fenstericon
    else:
        top.wm_iconbitmap(bitmap = "@res/tron.xbm") # Fenstericon
    
    # Komponenten im Hauptfenster:
    varHeader = StringVar()
    Label( top, textvariable=varHeader, relief=FLAT ).pack()    # Titelzeile
    varHeader.set(APP_INFO)

    Label( top, text="Host:", anchor=W, justify=LEFT, relief=FLAT ).pack()
    varHost = StringVar()
    Label( top, textvariable=varHost, relief=SUNKEN ).pack()

    Label( top, text="Status:", anchor=W, justify=LEFT, relief=FLAT ).pack()
    Label( top, textvariable=varStatus, relief=RAISED ).pack()

    ## Initialisierung:
    # Informationen über das geschützte System
    host_ip = Toolkit.getLocalIp(g_interface)
    log("Host IP address:  " + str(host_ip) + " (" + Toolkit.nslookup(host_ip) + ")")
    stdgw_ip = Toolkit.getDefaultGateway()
    log("Standard gateway: " + str(stdgw_ip) + " (" + Toolkit.nslookup(stdgw_ip) + ")")
    stdgw_mac = Toolkit.arpcache(stdgw_ip)
    log("StdGw MAC-address:" + stdgw_mac)
    varHost.set("Host IP address:  " + str(host_ip) + " (" + Toolkit.nslookup(host_ip) + ")\n" +
                "Standard gateway: " + str(stdgw_ip) + " (" + Toolkit.nslookup(stdgw_ip) + ")\n" +
                "StdGw MAC-address:" + stdgw_mac)

    ## Arbeitsthreads (Angriffserkennung) starten
    top.iconify()   # minimiere Hauptfenster solange alles OK ist
    try:
        _thread.start_new_thread(antiArpSpoof,(host_ip, stdgw_ip, stdgw_mac,))
    except:
        log("ERROR: unable to start thread")
    
    top.mainloop()  # Benutzer- und Mauseingaben verarbeiten

main()  # starte Hauptprogramm
