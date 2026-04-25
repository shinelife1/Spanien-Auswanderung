import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class InternetVergleicher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🇪🇸 Internet-Tarif-Vergleicher")
        self.geometry("600x700")

        # Tarifdaten (Monatspreis, Anschlussgebühr, Mindestlaufzeit)
        self.tarife = {
            "Digi (Fibra Smart)": {"preis": 15.00, "setup": 0, "speed": "500 Mbps", "info": "Günstigster Anbieter in Alicante (eigenes Netz)."},
            "Digi (Normal)": {"preis": 25.00, "setup": 0, "speed": "1 Gbps", "info": "Nutzt Movistar-Netz, wo kein Smart-Glasfaser liegt."},
            "O2 España": {"preis": 35.00, "setup": 0, "speed": "500 Mbps", "info": "Keine Mindestlaufzeit, sehr stabiles Movistar-Netz."},
            "Movistar (Mifibra)": {"preis": 29.90, "setup": 0, "speed": "600 Mbps", "info": "Aktionspreis für 12 Mon., danach oft teurer (ca. 50€)."},
            "Orange España": {"preis": 33.00, "setup": 0, "speed": "600 Mbps", "info": "Oft Kombi-Pakete mit TV möglich."}
        }

        # UI: Header
        self.header = ctk.CTkLabel(self, text="Glasfaser-Vergleich Spanien", font=("Arial", 24, "bold"), text_color="#3a7ebf")
        self.header.pack(pady=20)

        self.sub = ctk.CTkLabel(self, text="Berechnet die Kosten für das erste Jahr (12 Monate):", font=("Arial", 14))
        self.sub.pack(pady=5)

        # UI: ScrollFrame für Ergebnisse
        self.result_frame = ctk.CTkScrollableFrame(self, width=540, height=500)
        self.result_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.anzeigen()

    def berechne_jahr(self, monatspreis, setup):
        return (monatspreis * 12) + setup

    def anzeigen(self):
        # Sortieren nach günstigstem Jahrs-Preis
        sortierte_tarife = dict(sorted(self.tarife.items(), key=lambda item: self.berechne_jahr(item[1]['preis'], item[1]['setup'])))

        for name, daten in sortierte_tarife.items():
            jahr_gesamt = self.berechne_jahr(daten['preis'], daten['setup'])
            
            card = ctk.CTkFrame(self.result_frame, fg_color="#2b2b2b", corner_radius=10)
            card.pack(fill="x", pady=10, padx=5)

            # Linke Seite: Name & Speed
            lbl_name = ctk.CTkLabel(card, text=name, font=("Arial", 16, "bold"))
            lbl_name.pack(anchor="w", padx=15, pady=(10, 0))
            
            lbl_speed = ctk.CTkLabel(card, text=f"Geschwindigkeit: {daten['speed']}", font=("Arial", 12, "italic"), text_color="gray")
            lbl_speed.pack(anchor="w", padx=15)

            # Rechte Seite / Info:
            lbl_info = ctk.CTkLabel(card, text=daten['info'], font=("Arial", 12), wraplength=400, justify="left")
            lbl_info.pack(anchor="w", padx=15, pady=5)

            # Preis-Highlight
            price_box = ctk.CTkFrame(card, fg_color="#3a7ebf", corner_radius=5)
            price_box.pack(side="bottom", fill="x", padx=10, pady=10)
            
            lbl_price = ctk.CTkLabel(price_box, text=f"{daten['preis']} € / Monat  ➔  Gesamt 12 Mon: {jahr_gesamt:.2f} €", 
                                     font=("Arial", 14, "bold"), text_color="white")
            lbl_price.pack(pady=5)

if __name__ == "__main__":
    app = InternetVergleicher()
    app.mainloop()
