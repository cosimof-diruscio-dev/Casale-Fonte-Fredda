# Casale Fonte Fredda — Sito Prenotazioni

Sito web per la casa vacanze **"Casale Fonte Fredda"** (Rovellato, Marche): presentazione della struttura, verifica della disponibilità e prenotazione online del soggiorno.

Progetto sviluppato nell'ambito del **Project-Work "Click-Relax: Tradizione ed Innovazione al Casale Fonte Fredda"**.

## Funzionalità

- **Home page** (`index.html`) — presentazione del casale, del territorio marchigiano, indicazioni stradali, mappa e Street View, video promozionale delle Marche.
- **Verifica disponibilità** — controllo della disponibilità per intervallo di date (checkin/checkout) direttamente dalla home.
- **Prenotazione** (`booking.html`) — modulo con nome, cognome, email, telefono, note, date di check-in/check-out e accettazione dei termini. Salva la prenotazione nel database.
- **Backend API REST** — gestione disponibilità, salvataggio prenotazioni e stub per autenticazione/gestione utenti.

## Stack tecnologico

| Livello | Tecnologie |
|---|---|
| Frontend | HTML5, CSS3, JavaScript (vanilla, `fetch`) |
| Backend | Python 3, **FastAPI**, Uvicorn |
| Database | SQLite (`casale.db`) |
| Email | `smtplib` + Gmail SMTP |
| Immagini | AVIF, WebP |

## Struttura del progetto

```
.
├── main.py              # Backend FastAPI (API + database + email)
├── casale.db            # Database SQLite (users, reserves)
├── index.html           # Home page
├── booking.html         # Pagina prenotazione
├── styles.css           # Stile home page
├── booking.css          # Stile pagina prenotazione
├── script.js            # Logica frontend (fetch verso le API)
├── run_casale.bat       # Avvio Uvicorn (main:app, porta 8000)
├── images/              # Immagini del sito (copertine, foto, banner)
├── docs/                # Specifica OpenAPI esportata (openapi.json, openapi3_1.json)
├── in sviluppo/         # Funzionalità in lavorazione (login, area utente)
│   ├── login.html
│   ├── utente.html
│   └── utente js/utentejs.js
├── flowchart tesi.pdf   # Flowchart della tesi/progetto
└── LICENSE.md
```

## Requisiti ed esecuzione

Requisiti: **Python 3.9+** e le dipendenze:

```
pip install fastapi uvicorn pydantic
```

Avvio del server:

```
uvicorn main:app --reload --port 8000
```

(su Windows è disponibile lo script `run_casale.bat`).

Poi apri nel browser:

- Home: <http://127.0.0.1:8000> → non serve, apri direttamente `index.html`
- Backend: <http://127.0.0.1:8000/docs> (Swagger UI generato da FastAPI)

> Il frontend richiama le API su `http://127.0.0.1:8000`: il file HTML va aperto **mentre il server Uvicorn è in esecuzione**, altrimenti i controlli di disponibilità e le prenotazioni restituiscono errori di connessione.

## API disponibili

| Metodo | Percorso | Descrizione | Stato |
|---|---|---|---|
| GET | `/` | Messaggio di benvenuto | Funzionante |
| POST | `/controlla_disponibilita` | Verifica disponibilità in un intervallo di date | Funzionante |
| POST | `/submit` | Salva utente + prenotazione | Funzionante |
| POST | `/login` | Login utente | Stub (in sviluppo) |
| GET | `/user/{user_id}/` | Dettaglio utente | Stub |
| GET | `/reserve/{user_id}/` | Prenotazioni di un utente | Stub |
| PUT | `/reserve/{reserve_id}` | Modifica prenotazione | Stub |
| DELETE | `/reserve/{reserve_id}` | Elimina prenotazione | Stub |

La logica completa di login, modifica/cancellazione prenotazioni è presente **commentata** in `main.py` e andrà attivata con l'area utente.

## Schema del database (`casale.db`)

**`users`** — `user_id` (PK), `email` (UNIQUE), `password`, `telefono`, `nome`, `cognome`

**`reserves`** — `reserve_id` (PK), `user_id` (FK), `checkin`, `checkout`, `note`, `confermata`

La creazione automatica delle tabelle (`init_db`) è commentata: il database `casale.db` viene creato inizialmente in maniera manuale.

## Note e limiti attuali

- **Invio email di conferma**: il codice è presente (`send_email`) ma la chiamata è disabilitata (blocco `try` commentato in `/submit`) e attiva solo in modalità debug.
- **Credenziali SMTP hardcoded** in `main.py`: prima di mettere online il progetto spostarle in variabili d'ambiente. Da non condividere mai.
- La verifica disponibilità controlla l'**overlap** delle date, ma non distingue ancora più prenotazioni concorrenti sulla stessa stanza (struttura prenotata in blocco).
- Pagine `login.html`, `utente.html` e relativi JS sono **in fase di sviluppo**.

## Licenza

Tutti i diritti riservati — © 2025 **Di Ruscio Cosimo Francesco**. È vietata la copia, la modifica, la distribuzione o l'uso senza esplicita autorizzazione scritta (vedi `LICENSE.md`).