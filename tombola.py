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
n_giocatori = int(input("Inserisci il numero di giocatori: "))

# Leggi il nome dei giocatori
nomi_giocatori = []
for i in range(n_giocatori):
    nome = input(f"Inserisci il nome del giocatore {i+1}: ")
    nomi_giocatori.append(nome)

def genera_cartella():
    numeri = random.sample(range(1,91), 15)
    cartella = [numeri[i*5:(i+1)*5] for i in range(3)]
    return cartella

giocatori_cartelle = [genera_cartella() for _ in range(n_giocatori)]

# Stato estrazioni
numeri_estratti = []
numeri_disponibili = list(range(1,91))

# Controllo vincite
def controlla_cartella(cartella, estratti):
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

giocatori_vincite = [ {"ambo":False,"terno":False,"quaterna":False,"cinquina":False,"tombola":False} for _ in range(n_giocatori) ]

# Manteniamo il primo vincitore per ogni tipo di combinazione
primi_vincitori = {"ambo": None, "terno": None, "quaterna": None, "cinquina": None, "tombola": None}

root = tk.Tk()
root.title("Tombola - Finestra Principale")
root.geometry("1000x800")

# Font grande
font_grande = ("Arial", 18)

label_estrazione = tk.Label(root, text="Premi 'Estrazione' per estrarre un numero", font=font_grande)
label_estrazione.pack(pady=10)

frame_numeri = tk.Frame(root)
frame_numeri.pack(pady=10)

etichette_numeri = {}
for i in range(1,91):
    lbl = tk.Label(frame_numeri, text=str(i), width=3, borderwidth=1, relief="solid", font=font_grande)
    lbl.grid(row=(i-1)//10, column=(i-1)%10, padx=5, pady=5)
    etichette_numeri[i] = lbl

frame_vincite = tk.Frame(root)
frame_vincite.pack(pady=10)

label_vincite = tk.Label(frame_vincite, text="Vincite:", font=font_grande)
label_vincite.pack(anchor="w")

testo_vincite = tk.Text(frame_vincite, width=50, height=10, state="disabled", font=font_grande)
testo_vincite.pack()

# Finestre giocatori
finestre_giocatori = []
etichette_cartelle = []
etichette_probabilita = []

for g in range(n_giocatori):
    fg = tk.Toplevel(root)
    fg.title(f"{nomi_giocatori[g]}")
    fg.geometry("600x400")
    cart = giocatori_cartelle[g]
    lbls = []
    for r in range(3):
        row_lbls = []
        for c in range(5):
            num = cart[r][c]
            l = tk.Label(fg, text=str(num), width=4, borderwidth=1, relief="solid", font=("Arial", 24))
            l.grid(row=r, column=c, padx=10, pady=10)
            row_lbls.append(l)
        lbls.append(row_lbls)
    et_prob = tk.Label(fg, text="Probabilità di estrarre un numero utile: N/A", font=("Arial", 14))
    et_prob.grid(row=4, column=0, columnspan=5, pady=10)
    etichette_probabilita.append(et_prob)
    finestre_giocatori.append(fg)
    etichette_cartelle.append(lbls)

def lampeggia(label, colore1, colore2, count):
    # Lampeggia count volte alternando il colore
    if count > 0:
        attuale = label.cget("bg")
        nuovo = colore2 if attuale == colore1 else colore1
        label.config(bg=nuovo)
        label.after(500, lampeggia, label, colore1, colore2, count-1)
    else:
        # Finito il lampeggio, imposta definitivamente in giallo
        label.config(bg="yellow")

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

def aggiorna_vincite():
    testo_vincite.config(state="normal")
    testo_vincite.delete("1.0", tk.END)
    # Controllo nuove vincite
    for g in range(n_giocatori):
        res = controlla_cartella(giocatori_cartelle[g], numeri_estratti)
        for chiave in res:
            if res[chiave] and not giocatori_vincite[g][chiave]:
                giocatori_vincite[g][chiave] = True
                # Se non abbiamo ancora un vincitore per questa combinazione, assegniamo il primo
                if primi_vincitori[chiave] is None:
                    primi_vincitori[chiave] = g

    # Stampa solo il primo vincitore per ogni combinazione
    for chiave in ["ambo","terno","quaterna","cinquina","tombola"]:
        if primi_vincitori[chiave] is not None:
            winner_index = primi_vincitori[chiave]
            testo_vincite.insert(tk.END, f"{chiave.capitalize()}: {nomi_giocatori[winner_index]}\n")

    testo_vincite.config(state="disabled")

    # Se qualcuno ha fatto tombola, fine del gioco
    if primi_vincitori["tombola"] is not None:
        winner_index = primi_vincitori["tombola"]
        label_estrazione.config(text=f"{nomi_giocatori[winner_index]} ha fatto TOMBOLA! Il gioco termina.")
        btn_estrai.config(state="disabled")

def aggiorna_probabilita():
    rimanenti = 90 - len(numeri_estratti)
    if rimanenti == 0:
        for et_prob in etichette_probabilita:
            et_prob.config(text="Probabilità di estrarre un numero utile: 0%")
        return

    for g in range(n_giocatori):
        cart = giocatori_cartelle[g]
        tutti_numeri = [n for riga in cart for n in riga]
        numeri_non_estratti = set(tutti_numeri) - set(numeri_estratti)
        numeri_rimanenti = set(range(1,91)) - set(numeri_estratti)
        utili = len(numeri_non_estratti.intersection(numeri_rimanenti))
        if rimanenti > 0:
            prob = utili / rimanenti
        else:
            prob = 0.0
        etichette_probabilita[g].config(text=f"Probabilità di estrarre un numero utile: {prob*100:.2f}%")

def fine_gioco_se_necessario():
    # Se non ci sono più numeri disponibili e nessuno ha fatto tombola, finisce il gioco
    if not numeri_disponibili:
        if primi_vincitori["tombola"] is None:
            label_estrazione.config(text="Non ci sono più numeri, nessuna tombola! Il gioco termina.")
        btn_estrai.config(state="disabled")

def estrai_numero():
    if not numeri_disponibili:
        label_estrazione.config(text="Tutti i numeri sono stati estratti!")
        fine_gioco_se_necessario()
        return

    # Se qualcuno ha già fatto tombola, non estrarre più
    if primi_vincitori["tombola"] is not None:
        return

    numero = random.choice(numeri_disponibili)
    numeri_disponibili.remove(numero)
    numeri_estratti.append(numero)

    entita = numero_to_nome[numero]
    label_estrazione.config(text=f"Numero estratto: {numero} - {entita}")

    etichette_numeri[numero].config(bg="green", fg="white")

    aggiorna_cartelle()

    # Avvia lampeggio dei numeri appena estratti nelle cartelle per 3 volte
    for g in range(n_giocatori):
        cart = giocatori_cartelle[g]
        for r in range(3):
            for c in range(5):
                if cart[r][c] == numero:
                    # Il label attuale è giallo, facciamolo lampeggiare
                    # Alterniamo tra giallo e bianco 3 volte (1,5 secondi totali)
                    lampeggia(etichette_cartelle[g][r][c], "yellow", "white", 3)

    aggiorna_vincite()

    # Se dopo aver aggiornato le vincite qualcuno ha tombola, termina il gioco
    if primi_vincitori["tombola"] is not None:
        winner_index = primi_vincitori["tombola"]
        print(f"{nomi_giocatori[winner_index]} ha vinto!")
        return

    aggiorna_probabilita()
    fine_gioco_se_necessario()

btn_estrai = tk.Button(root, text="Estrazione", command=estrai_numero, font=font_grande)
btn_estrai.pack(pady=20)

aggiorna_probabilita()

root.mainloop()
