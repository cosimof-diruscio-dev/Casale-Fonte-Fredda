document.addEventListener('DOMContentLoaded', async () => {
    const userId = sessionStorage.getItem("user_id");

    if (!userId) {
        // Se l'utente non è autenticato, reindirizza al login
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/user/${userId}/`);
        if (!response.ok) {
            throw new Error(`Errore HTTP! Stato: ${response.status}`);
        }
        const userData = await response.json();
        console.log("Dati utente:", userData);

        document.getElementById("user-name").textContent = `${userData.nome} (${userData.cognome})`;

        const reserveResponse = await fetch(`http://127.0.0.1:8000/reserve/${userId}/`);
        if (!reserveResponse.ok) {
            throw new Error(`Errore HTTP! Stato: ${reserveResponse.status}`);
        }
        const reservesData = await reserveResponse.json();

        if (reservesData.length > 0) {
            const prenotazioniList = document.getElementById("prenotazioni-list");
            reservesData.forEach((prenotazione) => {
                const li = document.createElement("li");
                li.textContent = `Prenotazione dal ${new Date(prenotazione.checkin).toLocaleDateString()} al ${new Date(prenotazione.checkout).toLocaleDateString()} - ${prenotazione.note} (Stato: ${prenotazione.confermata ? "Confermata" : "Non Confermata"})`;
                prenotazioniList.appendChild(li);
            });
        } else {
            const messaggio = document.createElement("p");
            messaggio.textContent = "Nessuna prenotazione trovata.";
            document.body.appendChild(messaggio);
        }
    } catch (error) {
        console.error("Errore durante il caricamento delle prenotazioni o dei dati utente:", error);
        alert("Si è verificato un errore durante il caricamento delle prenotazioni. Riprova più tardi.");
    }
});