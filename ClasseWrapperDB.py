#classe wrapper
#funzioni di connetti e di disconnetti + varie
#le variabili di istanza sono le 4 variabili per la connetti
#invece la connetti è una variabile di classe 

#importo il modulo 
import pymssql
from pymssql import output
from pymssql import _mssql

class WrapperDB:
    
    conn = 0
    
    #def __init__(self, server="192.168.40.16\\SQLEXPRESS", user="CRD2122", \
    def __init__(self, server="213.140.22.237\\SQLEXPRESS", user="CRD2122", \
               password="xxx123##", database="CRD2122"):
        self._server=server
        self._user=user
        self._password=password
        self._database=database
        
        
    def connetti(self):
        #connessione
        try:
            WrapperDB.conn = pymssql.connect(server = self._server, user = self._user, \
                        password = self._password, database = self._database)
            #print(f"\nConnessione effettuata! (DB: {self._database})\n")
            return WrapperDB.conn	
        except:
            print(f"\nConnessione NON riuscita! (DB: {self._database})\n")
            return 0
        
            
    def disconnetti(self, co):
        #disconnessione	
        try:
            co.close()
            #print(f"\nCHIUSURA connessione! (DB: {self._database})\n") 
        except:
            print(f"\nCHIUSURA connessione NON riuscita! (DB: {self._database})\n")
            return 0
        

    def elencoPost(self, as_dict = False):
        #restituisce una lista di tuple se as_dict = False
        #altrimenti restituisce una lista di coppie chiave/valore (dictionary)
        conn = self.connetti()
        lista = []
        try:
            cur = conn.cursor(as_dict = as_dict)
            sql = "SELECT Id, Autore, Testo, [Like] FROM PC_FB_Post ORDER BY [Like] DESC"
            cur.execute(sql)
            lista = cur.fetchall()
        except:
            err = "Houston abbiamo un problema..."
            print(f"[elencoPost] {err}")
        self.disconnetti(conn)
        return lista

    
    def singoloPost(self, id):
        #restituisce un singolo post
        ret = {}
        conn = self.connetti()
        try:
            cursore = conn.cursor(as_dict = True)
            sql = f"""
                SELECT Id, Autore, Testo, [Like] 
                FROM PC_FB_Post 
                WHERE id = {id}   
                """
            cursore.execute(sql)
            ret = cursore.fetchone()
        except:
            err = "Houston abbiamo un problema..."
            print(f"[singoloPost] {err}")
        self.disconnetti(conn)
        return ret    

    
    #def inserisciPost(self, autore, testo):
    def inserisciPost(self, parametri):
        #inserisce un nuovo post
        #parametri: (autore, testo)
        try:
            c = self.connetti() 
            cursore = c.cursor()
            sql = "INSERT INTO PC_FB_Post (Autore, Testo) VALUES (%s , %s)"
            cursore.execute(sql, parametri)
            c.commit()
            #print("INSERIMENTO POST AVVENUTO")
            self.disconnetti(c)
            return True            
        except:
            #print("\INSERIMENTO POST/i: Si sono verificati degli errori!")
            self.disconnetti(c)
            return False


    def inserisciPostSP(self, parametri):
        #inserisce un nuovo post
        #parametri: (autore, testo)
        try:
            #dichiaro id come valore di output per la SP
            id = output(int)
            #aggiungo id ai parametri
            parametri = parametri + (id,)
            c = self.connetti() 
            cursore = c.cursor()
            res = cursore.callproc('dbo.PC_InserisciPost', parametri)
            c.commit()
            #print("INSERIMENTO POST AVVENUTO")
            #return True            
            return res[2]
        except _mssql.MssqlDatabaseException as e:
            print("A MSSQLDatabaseException has been caught.")
            print('Number = ',e.number)
            print('Severity = ',e.severity)
            print('State = ',e.state)
            print('Message = ',e.message)
            return -1
        except Exception as err:
            #print("\INSERIMENTO POST/i: Si sono verificati degli errori!")
            print(str(err))
            self.disconnetti(c)
            #return False
            return -1

    def daiLikeAPost(self, id, is_like = True):
        #mette like a post
        #se is_like è False toglie un like
        try:
            c = self.connetti() 
            cursore = c.cursor()
            sql = "UPDATE PC_FB_Post SET [Like] = "
            if is_like == True: 
                sql += "[Like] + 1 "
            else:
                sql += "[Like] - 1 "
            sql += "WHERE id = %d"
            cursore.execute(sql, id)
            c.commit()
            #print("LIKE A POST AVVENUTO")
            self.disconnetti(c)
            return True                        
        except:
            #print("\LIKE A POST/i: Si sono verificati degli errori!")
            self.disconnetti(c)
            return False


    def eliminaPost(self, id):
        #elimina un post
        try:
            c = self.connetti() 
            cursore = c.cursor()
            sql = "DELETE PC_FB_Post WHERE id = %d"
            cursore.execute(sql, id)
            c.commit()
            #print("ELIMINA POST AVVENUTO")
            self.disconnetti(c)
            return True            
            
        except:
            #print("\ELIMINA POST/i: Si sono verificati degli errori!")
            self.disconnetti(c)
            return False

    


	    