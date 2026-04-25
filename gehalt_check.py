import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GehaltsRechner(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🇪🇸 Brutto-Netto-Rechner Spanien")
        self.geometry("500x600")

        # UI Header
        self.label = ctk.CTkLabel(self, text="Gehaltsrechner Spanien", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # Input Frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.lbl_brutto = ctk.CTkLabel(self.input_frame, text="Jahresbrutto (€):")
        self.lbl_brutto.pack(pady=(10, 0))
        
        self.entry_brutto = ctk.CTkEntry(self.input_frame, placeholder_text="z.B. 30000")
        self.entry_brutto.pack(pady=10, padx=20, fill="x")

        self.calc_button = ctk.CTkButton(self, text="Berechnen", command=self.berechnen, fg_color="#2fa572")
        self.calc_button.pack(pady=20)

        # Result Frame
        self.res_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.res_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.res_label = ctk.CTkLabel(self.res_frame, text="Gib ein Gehalt ein...", font=("Arial", 14), justify="left")
        self.res_label.pack(pady=20, padx=20)

    def berechnen(self):
        try:
            brutto = float(self.entry_brutto.get())
            
            # 1. Sozialversicherung (ca. 6.47% für Arbeitnehmer)
            seg_social = brutto * 0.0647
            
            # 2. IRPF (Einkommensteuer) - Vereinfachte Stufen 2024/25
            # Dies ist eine Schätzung, da IRPF von Familiensituation abhängt
            if brutto <= 12450:
                irpf_rate = 0.19
            elif brutto <= 20200:
                irpf_rate = 0.24
            elif brutto <= 35200:
                irpf_rate = 0.30
            elif brutto <= 60000:
                irpf_rate = 0.37
            else:
                irpf_rate = 0.45
            
            # Freibetrag (Minimum Personal) ca. 5.550€
            steuerpflichtig = max(0, brutto - 5550)
            irpf = steuerpflichtig * irpf_rate
            
            netto_jahr = brutto - seg_social - irpf
            netto_monat_12 = netto_jahr / 12
            netto_monat_14 = netto_jahr / 14 # In Spanien oft 14 Gehälter üblich

            self.res_label.configure(text=(
                f"Ergebnis für {brutto:,.2f} € Brutto:\n\n"
                f" Sozialversicherung:  - {seg_social:,.2f} €\n"
                f" Einkommensteuer:      - {irpf:,.2f} €\n"
                f"----------------------------------\n"
                f" Netto pro Jahr:       {netto_jahr:,.2f} €\n\n"
                f" Netto (12 Gehälter):  {netto_monat_12:,.2f} €\n"
                f" Netto (14 Gehälter):  {netto_monat_14:,.2f} €"
            ))
        except ValueError:
            self.res_label.configure(text="Bitte eine gültige Zahl eingeben!")

if __name__ == "__main__":
    app = GehaltsRechner()
    app.mainloop()
