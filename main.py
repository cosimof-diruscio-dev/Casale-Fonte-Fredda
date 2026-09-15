from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form, HTTPException, Body, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict, List
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydantic import BaseModel, ValidationError
import uvicorn
import sqlite3
import logging
import smtplib
import os
app = FastAPI()

# Configura il logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configurazione CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


RELEASE_NAME = "3.8 14/4/2025"
DEBUG0 = True
DEBUG2 = False
SERVER_MODE = True

DATABASE_NAME = "casale.db"

# definizione della classe per il formato json
class Prenotazione(BaseModel):
    nome: str
    cognome: str
    email: str
    telefono: str
    note: str = ""
    checkin: str
    checkout: str

# controllo della disponibilità
def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato data non valido (YYYY-MM-DD)")

# invio dell'email di conferma   
def send_email(to_address: str, body: str):
    # inserire prossimamente controllo maggiore della sintaassi e-mail mediante espressione regolare
    if not to_address or "@" not in to_address:
        print("Errore: indirizzo email non valido!", to_address)
        return

    if DEBUG0:
        print("invio email a", to_address, "con testo:", body)
    fromaddr = "all.inover0@gmail.com"
    toaddr = to_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Conferma prenotazione"

    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(fromaddr, "pdjv vflu yutf elka")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print("Email inviata con successo!")
    except Exception as e:
        print(f"Errore durante l'invio dell'email: {e}")
# sezione database
# connessione database
def get_db_connection():

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# SCREENSHOT ALLA PARTE COMMENTATA
# inizializzazione dataabse e creazione tabelle
# def init_db():  
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Tabella utenti
#     cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             email TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL,
#             telefono TEXT,
#             nome TEXT,
#             cognome TEXT
#         )
#         """
#     )

#     # Tabella prenotazioni
#     cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS reserves (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             checkin DATE NOT NULL,
#             checkout DATE NOT NULL,
#             note TEXT,
#             confermata TEXT
           
#         )
#         """
#     )
#     conn.commit()
#     conn.close()

# Inizializza il database all'avvio dell'applicazione solo per la prima volta
# if not os.path.exists(DATABASE_NAME):
#     init_db()
#     print(f"Database '{DATABASE_NAME}' creato e inizializzato.")
# else:
#     print(f"Database '{DATABASE_NAME}' già esistente.")

# test di connessione e stampa del database eseguito nel terminale python
conn = get_db_connection()
cursor = conn.cursor()
print("\nlista utenti")
cursor.execute("SELECT * from users")
userdump = cursor.fetchall()
for row in userdump:
    print(row[0], row[1], row[2])
print("\nlista riserve")
cursor.execute("SELECT * from reserves")
userdump = cursor.fetchall()
for row in userdump:
    print(row[0], row[1], row[2], row[3])



# test di connessione di FASTAPI alla route principale
@app.get("/")
async def root():
    return {"message": "Benvenuto al Casale Fonte delle Pietre API!"}

# SCREENSHOT 
# API per gestire le date disponibili con controllo delle date
@app.post("/controlla_disponibilita")
async def controlla_disponibilita(body: Dict = Body(...)):
    checkin_str = body.get("checkin")
    checkout_str = body.get("checkout")

    if not checkin_str or not checkout_str:
        raise HTTPException(status_code=400, detail="Inserisci entrambe le date!")

    checkin_date = parse_date(checkin_str)
    checkout_date = parse_date(checkout_str)

    if checkout_date <= checkin_date:
        raise HTTPException(status_code=400, detail="La data di check-out deve essere successiva alla data di check-in.")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) FROM reserves
        WHERE checkin < ? AND checkout > ?
        """,
        (checkout_date, checkin_date),
    )
    count = cursor.fetchone()[0]
    conn.close()

    if count > 0:
        return {"disponibile": False, "messaggio": "Non disponibile!"}
    else:
        return {"disponibile": True, "messaggio": "Disponibile! Prenotazione confermata."}
    
# SCREENSHOT 
# funzione principale. richiesta di prenotazione, con diversi log.info per i test di connessione
@app.post("/submit")
async def handle_form(prenotazione: Prenotazione):
    
    logging.info(f"Ricevuta richiesta a /submit con dati: {prenotazione}")

    try:
        # Estrarre i dati direttamente dall'oggetto prenotazione
        nome = prenotazione.nome
        cognome = prenotazione.cognome
        email = prenotazione.email
        telefono = prenotazione.telefono
        textarea = prenotazione.note  
        checkin_date_str = prenotazione.checkin
        checkout_date_str = prenotazione.checkout

        if not checkin_date_str or not checkout_date_str:
            raise HTTPException(status_code=400, detail="Date di check-in e check-out mancanti!")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Controllo se l'utente esiste già nel database
        cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()

        if row is None:
            cursor.execute(
                "INSERT INTO users (email, password, telefono, nome, cognome) VALUES (?, ?, ?, ?, ?)",
                (email, "password_default", telefono, nome, cognome),
            )
            user_id = cursor.lastrowid
            logging.info(f"Utente inserito con ID: {user_id}")
        else:
            user_id = row[0]
            logging.info(f"Utente già presente con ID: {user_id}")

        # Inserimento della prenotazione anche se l'utente non ha effettuato il login
        cursor.execute(
            "INSERT INTO reserves (user_id, checkin, checkout, note, confermata) VALUES (?, ?, ?, ?, ?)",
            (user_id, checkin_date_str, checkout_date_str, textarea, 1),
        )
        conn.commit()
        conn.close()

        
        email_body = f"""
        Salve {cognome} {nome},

        Siamo lieti di averla con noi! La sua prenotazione è stata ricevuta con successo.

        Dettagli:
        - Nome: {nome} 
        - Cognome: {cognome}
        - Email: {email}
        - Telefono: {telefono}
        - Check-in: {checkin_date_str}
        - Check-out: {checkout_date_str}
        - Note aggiuntive: Note aggiuntive: {prenotazione.note if prenotazione.note else "Nessuna nota aggiuntiva"}.

        Per modifiche o cancellazioni entro 24h prima del soggiorno, ci contatti a:
        casalefontedellepietre@gmail.com.

        Grazie per aver scelto Casale Fonte delle Pietre!

        Cordiali saluti,
        Il Team di Casale Fonte delle Pietre
        """
        
        #try:
            #send_email(email, email_body)
        #except Exception as email_error:
        #    logging.error(f"Errore durante l'invio dell'email: {email_error}")
        
        logging.info("Prenotazione salvata e email inviata con successo")
        return {"message": "Prenotazione ricevuta con successo! Controlla la tua email per i dettagli."}

    except ValidationError as e:
        error_messages = [error["msg"] for error in e.errors()]
        return JSONResponse(content={"detail": error_messages}, status_code=422)
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e)}, status_code=e.status_code)
    except Exception as e:
        logging.error(f"Errore in handle_form: {e}")
        return JSONResponse(content={"detail": "Errore interno del server"}, status_code=500)

# Rotta per effettuare il login
@app.post("/login", tags=["Autenticazione"])
async def login_stub():
    return {"message": "Funzione di login in fase di sviluppo."}

# Rotta per recuperare un utente che sarà collegata all'admin page
@app.get("/user/{user_id}/", tags=["Utenti"])
async def get_user_stub(user_id: int):
    return {"message": f"Funzione per recuperare utente {user_id} in fase di sviluppo."}

# Rotta per recuperare una prenotazione che sarà collegata all'admin page
@app.get("/reserve/{user_id}/", tags=["Prenotazioni"])
async def get_reserve_stub(user_id: int):
    return {"message": f"Funzione per recuperare le prenotazioni dell'utente {user_id} in fase di sviluppo."}

# API legata al login da implementare in futuro
# @app.post("/login")
# async def login(email: str = Form(...), password: str = Form(...)):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT id FROM users WHERE email = ? AND password = ?", (email, password)
#     )
#     user = cursor.fetchone()
#     conn.close()

#     if user:
#         return {"status": "success", "user_id": user["id"], "message": "Login riuscito"}
#     else:
#         raise HTTPException(status_code=401, detail="Credenziali non valide")

# @app.get("/user/{user_id}/")
# async def get_user(user_id: int):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, nome, cognome FROM users WHERE id = ?", (user_id,))
#     user = cursor.fetchone()
#     conn.close()

#     if user:
#         return user
#     else:
#         raise HTTPException(status_code=404, detail="Utente non trovato")

# @app.get("/reserve/{user_id}/")
# async def get_user_reserves(user_id: int):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         "SELECT id, user_id, checkin, checkout, note, confermata FROM reserves WHERE user_id = ?",
#         (user_id,),
#     )
#     reserves = cursor.fetchall()
#     conn.close()

#     if reserves:
#         return reserves
#     else:
#         return []

# Rotta per modificare una prenotazione
@app.put("/reserve/{reserve_id}", tags=["Prenotazioni"])
async def update_reserve_stub(reserve_id: int):
    return {
        "message": f"Funzione di modifica prenotazione con ID {reserve_id} in fase di sviluppo. Sarà attiva dopo l'integrazione con il login utente."
    }

# Rotta per eliminare una prenotazione
@app.delete("/reserve/{reserve_id}", tags=["Prenotazioni"])
async def delete_reserve_stub(reserve_id: int):
    return {
        "message": f"Funzione di eliminazione prenotazione con ID {reserve_id} in fase di sviluppo. Sarà attiva dopo l'integrazione con il login utente."
    }

# esecuzione di Python come server tramite uvicorn
if (SERVER_MODE):
    if __name__ == "__main__":
        uvicorn.run(app, host="127.0.0.1", port=8000)