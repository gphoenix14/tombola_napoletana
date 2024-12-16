import sys
import tkinter as tk
import random

# Mappatura dei numeri con la rispettiva entità principale della tombola napoletana
numero_to_nome = {
    1: "L’Italia",
    2: "’A Piccerella",
    3: "’A Jatta",
    4: "’O puorco",
    5: "’A Mano",
    6: "Chella ca guarda ’nterra",
    7: "’O Vase",
    8: "’A Madonna",
    9: "’A Figliata",
    10: "’E Fasule",
    11: "’E Suricille",
    12: "’O Surdate",
    13: "Sant’Antonio",
    14: "’O ’Mbriaco",
    15: "’O Guaglione",
    16: "’O Culo",
    17: "’A Disgrazzia",
    18: "’O Sanghe",
    19: "’A Resata",
    20: "’A Festa",
    21: "’A Femmena annura",
    22: "’O Pazzo",
    23: "’O Scemo",
    24: "’E Gguardie",
    25: "Natal’",
    26: "Nanninella",
    27: "’O Cantero",
    28: "’E Zzizze",
    29: "’O Pate d’e Ccriature",
    30: "’E Ppalle d’o Tenente",
    31: "’O Padrone ’e Casa",
    32: "’O Capitone",
    33: "L’Anne ’e Cristo",
    34: "’A Capa",
    35: "L’Aucelluzz",
    36: "’E Ccastagnelle",
    37: "’O Monaco",
    38: "’E Mmazzate",
    39: "’A Funa n’Ganna",
    40: "’A Paposcia",
    41: "’O Curtiello",
    42: "’O Cafè",
    43: "’Onna pereta fore ’o barcone",
    44: "’E Ccancelle",
    45: "’O Vino bbuono",
    46: "’E Denare",
    47: "’O Muorto",
    48: "’O Muorto che pparla",
    49: "’O Piezzo ’e Carne",
    50: "’O Ppane",
    51: "’O Ciardino",
    52: "’A Mamma",
    53: "’O Viecchio",
    54: "’O Cappiello",
    55: "’A Museca",
    56: "’A Caruta",
    57: "’O Scartellato",
    58: "’O Paccotto",
    59: "’E Pile",
    60: "Se lamenta",
    61: "’O Cacciatore",
    62: "’O Muorto acciso",
    63: "’A Sposa",
    64: "’A Sciammeria",
    65: "’O Chianto",
    66: "’E ddoie Zetelle",
    67: "’O Totaro int”a Chitarra",
    68: "’A Zuppa cotta",
    69: "Sott’e ’Ncoppa",
    70: "’O Palazzo",
    71: "L’Ommo ’e Merda",
    72: "’A Maraviglia",
    73: "’O Spitale",
    74: "’A Rotta",
    75: "Pullecenella",
    76: "’A Funtana",
    77: "’E Riavulille",
    78: "’A bella Figliola",
    79: "’O Mariuolo",
    80: "’A Vocca",
    81: "’E Sciure",
    82: "’A Tavula ’mbandita",
    83: "’O Maletiempo",
    84: "’A Cchiesa",
    85: "Ll’Aneme ’o Priatorio",
    86: "’A Puteca",
    87: "’E Perucchie",
    88: "’E Casecavalle",
    89: "’A Vecchia",
    90: "’A Paura"
}


# Leggi il numero di giocatori
# Se si utilizza sys.argv:
# if len(sys.argv) < 2:
#     print("Specificare il numero di giocatori")
#     sys.exit(1)
# n_giocatori = int(sys.argv[1])

# Oppure chiedi input da utente:
n_giocatori = int(input("Inserisci il numero di giocatori: "))

# Genera cartelle random per i giocatori
# Ogni cartella: 3 righe x 5 colonne = 15 numeri unici da 1 a 90
def genera_cartella():
    numeri = random.sample(range(1,91), 15)
    cartella = [numeri[i*5:(i+1)*5] for i in range(3)]
    return cartella

giocatori_cartelle = [genera_cartella() for _ in range(n_giocatori)]

# Stato estrazioni
numeri_estratti = []
numeri_disponibili = list(range(1,91))

# Controllo vincite
# ambo, terno, quaterna, cinquina (linea intera), tombola
# ambo = 2 in una riga, terno=3 in una riga, quaterna=4 in una riga, cinquina=5 in una riga, tombola=15 su tutta la cartella
def controlla_cartella(cartella, estratti):
    # restituisce un dizionario con True/False per ambo,terno,quaterna,cinquina e tombola
    # Verifica ogni riga, conta quanti estratti ci sono
    risultati = {
        "ambo": False,
        "terno": False,
        "quaterna": False,
        "cinquina": False,
        "tombola": False
    }
    totale_estratti_nella_cartella = 0
    for riga in cartella:
        count_estratti = sum(1 for num in riga if num in estratti)
        totale_estratti_nella_cartella += count_estratti
        if count_estratti == 2:
            risultati["ambo"] = True
        if count_estratti == 3:
            risultati["terno"] = True
        if count_estratti == 4:
            risultati["quaterna"] = True
        if count_estratti == 5:
            risultati["cinquina"] = True
    if totale_estratti_nella_cartella == 15:
        risultati["tombola"] = True
    return risultati

# Tracciamento di chi ha fatto cosa per evitare di ripetere
giocatori_vincite = [ {"ambo":False,"terno":False,"quaterna":False,"cinquina":False,"tombola":False} for _ in range(n_giocatori) ]

# Creazione interfaccia grafica
root = tk.Tk()
root.title("Tombola - Finestra Principale")

# Label estrazione
label_estrazione = tk.Label(root, text="Premi 'Estrazione' per estrarre un numero", font=("Arial", 14))
label_estrazione.pack()

# Frame per i numeri da 1 a 90
frame_numeri = tk.Frame(root)
frame_numeri.pack()

etichette_numeri = {}
for i in range(1,91):
    lbl = tk.Label(frame_numeri, text=str(i), width=3, borderwidth=1, relief="solid", font=("Arial", 10))
    lbl.grid(row=(i-1)//10, column=(i-1)%10)
    etichette_numeri[i] = lbl

# Area per visualizzare le vincite
frame_vincite = tk.Frame(root)
frame_vincite.pack()

label_vincite = tk.Label(frame_vincite, text="Vincite:", font=("Arial", 12))
label_vincite.pack(anchor="w")

testo_vincite = tk.Text(frame_vincite, width=50, height=10, state="disabled")
testo_vincite.pack()

# Finestra per ogni giocatore
finestre_giocatori = []
etichette_cartelle = [] # etichette_cartelle[giocatore][riga][colonna] = Label
for g in range(n_giocatori):
    fg = tk.Toplevel(root)
    fg.title(f"Giocatore {g+1}")
    cart = giocatori_cartelle[g]
    lbls = []
    for r in range(3):
        row_lbls = []
        for c in range(5):
            num = cart[r][c]
            l = tk.Label(fg, text=str(num), width=4, borderwidth=1, relief="solid", font=("Arial", 12))
            l.grid(row=r, column=c, padx=5, pady=5)
            row_lbls.append(l)
        lbls.append(row_lbls)
    finestre_giocatori.append(fg)
    etichette_cartelle.append(lbls)

# Funzione per aggiornare cartelle
def aggiorna_cartelle():
    for g in range(n_giocatori):
        cart = giocatori_cartelle[g]
        for r in range(3):
            for c in range(5):
                num = cart[r][c]
                lbl = etichette_cartelle[g][r][c]
                if num in numeri_estratti:
                    lbl.config(bg="yellow")
                else:
                    lbl.config(bg="white")

# Funzione per controllare e aggiornare vincite
def aggiorna_vincite():
    for g in range(n_giocatori):
        res = controlla_cartella(giocatori_cartelle[g], numeri_estratti)
        for chiave in res:
            if res[chiave] and not giocatori_vincite[g][chiave]:
                giocatori_vincite[g][chiave] = True
    # Mostra chi ha fatto cosa
    testo_vincite.config(state="normal")
    testo_vincite.delete("1.0", tk.END)
    # Riporta i giocatori che hanno fatto ambo,terno,quaterna,cinquina,tombola
    for chiave in ["ambo","terno","quaterna","cinquina","tombola"]:
        # verifica quali giocatori hanno quella vincita
        vincitori = [f"Giocatore {i+1}" for i,v in enumerate(giocatori_vincite) if v[chiave]]
        if vincitori:
            testo_vincite.insert(tk.END, f"{chiave.capitalize()}: {', '.join(vincitori)}\n")
    testo_vincite.config(state="disabled")

# Funzione estrazione numero
def estrai_numero():
    if not numeri_disponibili:
        label_estrazione.config(text="Tutti i numeri sono stati estratti!")
        return
    numero = random.choice(numeri_disponibili)
    numeri_disponibili.remove(numero)
    numeri_estratti.append(numero)

    # Aggiorna label estrazione con il numero e l'entità
    entita = numero_to_nome[numero]
    label_estrazione.config(text=f"Numero estratto: {numero} - {entita}")
    print(entita)

    # Evidenzia il numero nella finestra principale
    etichette_numeri[numero].config(bg="green", fg="white")

    # Aggiorna cartelle
    aggiorna_cartelle()

    # Aggiorna vincite
    aggiorna_vincite()


# Bottone estrazione
btn_estrai = tk.Button(root, text="Estrazione", command=estrai_numero, font=("Arial", 12))
btn_estrai.pack(pady=10)

root.mainloop()
