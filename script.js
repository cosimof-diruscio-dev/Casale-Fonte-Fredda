// Controllo disponibilità giorni nel database
document.addEventListener('DOMContentLoaded', async () => {
    console.log("DOM completamente caricato.");

    const controlloDisponibilitaButton = document.getElementById("controllo_disponibilità");
    if (controlloDisponibilitaButton) {
        controlloDisponibilitaButton.addEventListener("click", async (event) => {
            event.preventDefault();
            const checkin = document.getElementById("data-check-in").value;
            const checkout = document.getElementById("data-check-out").value;
            const messaggio = document.getElementById("messaggio-disponibilità");

            if (!checkin || !checkout) {
                messaggio.textContent = "Inserisci entrambe le date!";
                messaggio.style.color = "red";
                return;
            }

            try {
                const response = await fetch("http://127.0.0.1:8000/controlla_disponibilita", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ checkin, checkout }),
                });

                if (!response.ok) {
                    let errorDetail = "Errore sconosciuto";
                    try {
                        const contentType = response.headers.get("content-type");
                        if (contentType && contentType.includes("application/json")) {
                            const errorData = await response.json();
                            if (errorData.detail && Array.isArray(errorData.detail)) {
                                const errorMessages = errorData.detail.map(error => error.msg).join(", ");
                                throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: ${errorMessages}`);
                            } else {
                                throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: ${JSON.stringify(errorData)}`);
                            }
                        } else {
                            const errorText = await response.text();
                            throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: ${errorText}`);
                        }
                        return;
                    } catch (jsonError) {
                        throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: Impossibile analizzare la risposta.`);
                    }
                }

                const data = await response.json();
                console.log("Dati ricevuti:", data);

                messaggio.textContent = data.messaggio;
                messaggio.style.color = data.disponibile ? "green" : "red";

                if (data.disponibile) {
                    setTimeout(function () {
                        window.location.href = "booking.html";
                    }, 1000);
                }
            } catch (error) {
                console.error("Errore durante il fetch:", error);
                messaggio.textContent = "Errore di connessione!";
                messaggio.style.color = "red";
            }
        });
    }

    const formDiPrenotazione = document.getElementById("form_di_prenotazione");
    if (formDiPrenotazione) {
        formDiPrenotazione.addEventListener("submit", async (event) => {
            event.preventDefault();

            
            const nome = document.getElementById("nome").value.trim();
            const cognome = document.getElementById("cognome").value.trim();
            const email = document.getElementById("email").value.trim();
            const telefono = document.getElementById("telefono").value.trim();
            const note = document.getElementById("textarea").value;
            const checkinDateInput = document.getElementById("data-check-in");
            const checkoutDateInput = document.getElementById("data-check-out");

            if (!checkinDateInput || !checkoutDateInput) {
                console.error("Campi data check-in o check-out non trovati!");
                alert("Errore: Campi data check-in o check-out non trovati!");
                return;
            }

            const checkin = checkinDateInput.value;
            const checkout = checkoutDateInput.value;

            
            if (new Date(checkout) <= new Date(checkin)) {
                alert("La data di check-out deve essere successiva alla data di check-in.");
                return;
            }

            document.getElementById("checkin").value = checkin;
            document.getElementById("checkout").value = checkout;

           
            if (!nome || !cognome || !email || !telefono || !checkin || !checkout) {
                alert("Compila tutti i campi obbligatori!");
                return;
            }

            console.log({ nome, cognome, email, telefono, note, checkin, checkout });

            try {
                console.log("Inizio della richiesta fetch...");
                const response = await fetch("http://127.0.0.1:8000/submit", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        nome,
                        cognome,
                        email,
                        telefono,
                        note,
                        checkin,
                        checkout,
                    }),
                });

                console.log("Risposta fetch ricevuta:", response);
                console.log("Risposta del server:", response);
                console.log("Testo della risposta:", await response.text());

                if (!response.ok) {
                    let errorDetail = "Errore sconosciuto";
                    try {
                        const contentType = response.headers.get("content-type");
                        if (contentType && contentType.includes("application/json")) {
                            const errorData = await response.json();
                            if (errorData.detail && Array.isArray(errorData.detail)) {
                                const errorMessages = errorData.detail.map(error => error.msg).join(", ");
                                throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: ${errorMessages}`);
                            } else {
                                throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: ${JSON.stringify(errorData)}`);
                            }
                        } else {
                            const errorText = await response.text();
                            throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: ${errorText}`);
                        }
                        return;
                    } catch (jsonError) {
                        throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: Impossibile analizzare la risposta.`);
                    }
                }

                const data = await response.json();
                console.log("Risposta ricevuta:", data);

                // reindirizzamento a utente.html per dashboard utente da implementare in futuro

                // if (data.message) {
                //     alert(data.message);
                //     window.location.href = "utente.html";
                // } else {
                //     alert("Errore nella prenotazione. Riprova.");
                // }
            } catch (error) {
                if (error.name=TypeError){
                    console.error("La prenotazione è avvenuta con successo");
                    setTimeout(function () {
                        window.location.href = "booking.html";
                    }, 1000);
                }
                    
                else{
                    console.error("Errore durante la richiesta:", error);
                    console.error("Tipo di errore:", error.name);
                    console.error("Messaggio di errore:", error.message);
                    console.error("Stack trace (se disponibile):", error.stack);
                    alert("Errore durante la prenotazione! Dettagli: " + error.message);
                }
                
            }
        });
    }
    // // Login da implementare in futuro
    // const loginForm = document.getElementById("login");
    // if (loginForm) {
    //     loginForm.addEventListener("submit", async (event) => {
    //         event.preventDefault();
    //         const email = document.getElementById("email").value.trim();
    //         const password = document.getElementById("password").value.trim();

    //         if (!email || !password) {
    //             alert("Compila tutti i campi obbligatori!");
    //             return;
    //         }

    //         try {
    //             const response = await fetch("http://127.0.0.1:8000/login", {
    //                 method: "POST",
    //                 headers: { "Content-Type": "application/json" },
    //                 body: JSON.stringify({ email, password }), // Invia email e password come JSON
    //             });

    //             if (!response.ok) {
    //                 let errorDetail = "Errore sconosciuto";
    //                 try {
    //                     const contentType = response.headers.get("content-type");
    //                     if (contentType && contentType.includes("application/json")) {
    //                         const errorData = await response.json();
    //                         if (errorData.detail && Array.isArray(errorData.detail)) {
    //                             const errorMessages = errorData.detail.map(error => error.msg).join(", ");
    //                             throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: ${errorMessages}`);
    //                         } else {
    //                             throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: ${JSON.stringify(errorData)}`);
    //                         }
    //                     } else {
    //                         const errorText = await response.text();
    //                         throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: ${errorText}`);
    //                     }
    //                     return;
    //                 } catch (jsonError) {
    //                     throw new Error(`Errore HTTP! Stato: ${response.status}, Dettagli: Impossibile analizzare la risposta.`);
    //                 }
    //             }

    //             const data = await response.json();
    //             console.log("Risposta ricevuta:", data);

    //             if (data.status === "success") {
    //                 sessionStorage.setItem("user_id", data.user_id);
    //                 window.location.href = "utente.html";
    //             } else {
    //                 alert(data.message || "Errore di login. Verifica le credenziali.");
    //             }
    //         } catch (error) {
    //             console.error("Errore durante il login:", error);
    //             alert(`Errore: ${error.message}`);
    //         }
    //     });
    // }
});