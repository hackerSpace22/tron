#!/usr/bin/python
# Repräsentation einer IPv4-Adresse
# programmiert von codepunX

class Ip:
    ########################################################
    # ATTRIBUTE:
    __a = 0     # Erstes Byte
    __b = 0     # Zweites Byte
    __c = 0     # Drittes Byte
    __d = 0     # Viertes Byte
    __prefix = None # Präfix der Subnetzmaske

    ########################################################
    # KONSTRUKTOR:
    #def __init__(self):

    ########################################################
    # SETTERs:

    # Setze IP-Adresse per Nummern
    def setNum(self, a, b, c, d, prefix=None):
        self.__a = a
        self.__b = b
        self.__c = c
        self.__d = d
        self.__prefix=prefix

    # Setze IP-Adresse per String
    def setString(self, s):
        try:
            p1 = s.find(".")
            self.__a = int(s[0:p1])
            p2 = s.find(".",p1+1)
            self.__b = int(s[p1+1:p2])
            p3 = s.find(".",p2+1)
            self.__c = int(s[p2+1:p3])
            p4 = s.find("/",p3+1)
            if p4<p3:
                p4 = len(s)
            else:
                self.__prefix=int(s[p4+1:len(s)])
            self.__d = int(s[p3+1:p4])
        except: #all errors
            print("Error")

    ########################################################
    # GETTERs:
    def getNumA(self):
        return __a

    def getNumB(self):
        return __b

    def getNumC(self):
        return __c

    def getNumD(self):
        return __d

    def getPrefix(self):
        return __prefix

    # Liefere Adresse als String
    def getString(self):
        s = str(self.__a) + "." + str(self.__b) + "." + str(self.__c) + "." + str(self.__d)
        if self.__prefix!=None:
            s = s + "/" + str(self.__prefix)
        return s

    # Liefere Subnetzmaske als Ip
    def getSubnetMask(self):
        if self.__prefix!=None:
            #TODO: das geht schöner!
            if self.__prefix==1: return Ip.fromNum(128,0,0,0)
            elif self.__prefix==2: return Ip.fromNum(192,0,0,0)
            elif self.__prefix==3: return Ip.fromNum(224,0,0,0)
            elif self.__prefix==4: return Ip.fromNum(240,0,0,0)
            elif self.__prefix==5: return Ip.fromNum(248,0,0,0)
            elif self.__prefix==6: return Ip.fromNum(252,0,0,0)
            elif self.__prefix==7: return Ip.fromNum(254,0,0,0)
            elif self.__prefix==8: return Ip.fromNum(255,0,0,0)
            elif self.__prefix==9: return Ip.fromNum(255,128,0,0)
            elif self.__prefix==10: return Ip.fromNum(255,192,0,0)
            elif self.__prefix==11: return Ip.fromNum(255,224,0,0)
            elif self.__prefix==12: return Ip.fromNum(255,240,0,0)
            elif self.__prefix==13: return Ip.fromNum(255,248,0,0)
            elif self.__prefix==14: return Ip.fromNum(255,252,0,0)
            elif self.__prefix==15: return Ip.fromNum(255,254,0,0)
            elif self.__prefix==16: return Ip.fromNum(255,255,0,0)
            elif self.__prefix==17: return Ip.fromNum(255,255,128,0)
            elif self.__prefix==18: return Ip.fromNum(255,255,192,0)
            elif self.__prefix==19: return Ip.fromNum(255,255,224,0)
            elif self.__prefix==20: return Ip.fromNum(255,255,240,0)
            elif self.__prefix==21: return Ip.fromNum(255,255,248,0)
            elif self.__prefix==22: return Ip.fromNum(255,255,252,0)
            elif self.__prefix==23: return Ip.fromNum(255,255,254,0)
            elif self.__prefix==24: return Ip.fromNum(255,255,255,0)
            elif self.__prefix==25: return Ip.fromNum(255,255,255,128)
            elif self.__prefix==26: return Ip.fromNum(255,255,255,192)
            elif self.__prefix==27: return Ip.fromNum(255,255,255,224)
            elif self.__prefix==28: return Ip.fromNum(255,255,255,240)
            elif self.__prefix==29: return Ip.fromNum(255,255,255,248)
            elif self.__prefix==30: return Ip.fromNum(255,255,255,252)
            elif self.__prefix==31: return Ip.fromNum(255,255,255,254)
            elif self.__prefix==32: return Ip.fromNum(255,255,255,255)
        else:
            return None

    ########################################################
    # METHODEN:

    # Ausgabe als String
    def __str__(self):
        return self.getString()

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    # Ermitteln der Addressklasse
    def getClass(self):
        if self.__a >= 0 and self.__a <= 127:
            return Ip.A
        elif self.__a >= 128 and self.__a <= 191:
            return Ip.B
        elif self.__a >= 192 and self.__a <= 223:
            return Ip.C
        elif self.__a >= 224 and self.__a <= 239:
            return Ip.D
        elif self.__a >= 240 and self.__a <= 255:
            return Ip.E
        else:
            return None

    # Ermitteln, ob es eine private Adresse ist
    def isPrivate(self):
        if self.__a==10:
            return True
        elif self.__a==172 and (self.__b >= 16 and self.__b <= 31):
            return True
        elif self.__a==192 and self.__b==168:
            return True
        else:
            return False

    # Ermitteln, ob es eine öffentliche Adresse ist
    def isPublic(self):
        return not self.isPrivate()

    # Hat das Objekt eine gültige Adresse zugewiesen
    def isValid(self):
        if self.__a==0 and self.__b==0 and self.__c==0 and self.__d==0:
            return False
        else:
            return True

    ########################################################
    # INSTANZIERUNG (FACTORY-METHODS):

    # erzeuge ein Objekt auf Basis eines Strings (dottec-decimal schreibweise)
    def fromString(s):
        ip = Ip()
        ip.setString(s)
        return ip
    fromString = staticmethod(fromString)

    # erzeuge ein Objekt durch Angabe der vier Zahlen
    def fromNum(a, b, c, d):
        ip = Ip()
        ip.setNum(a, b, c, d)
        return ip
    fromNum = staticmethod(fromNum)


############################################################
### Modultest:
def test():
    ip = Ip()
    print(ip)
    print("isValid=" + str(ip.isValid()))
    
    print()
    ip1 = Ip.fromNum(192, 168, 2, 1)
    print(ip1)
    print("Class=" + ip1.getClass())
    print("Public=" + str(not ip1.isPrivate()))

    print()
    ip2 = Ip.fromString("93.87.112.3/17")
    print(ip2)
    print("Class=" + str(ip2.getClass()))
    print("Public=" + str(ip2.isPublic()))
    print("SubnetMask=" + str(ip2.getSubnetMask()))

#test()
