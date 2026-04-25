import customtkinter as ctk
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class UmzugsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Checkliste: San José (Alicante)")
        self.geometry("600x800")
        
        skript_verzeichnis = os.path.dirname(os.path.abspath(__file__))
        self.dateiname = os.path.join(skript_verzeichnis, "fortschritt.json")

        self.daten = []
        self.laden()

        # UI: Header
        self.label = ctk.CTkLabel(self, text="Auswanderung Alicante 🇪🇸", font=("Roboto", 24, "bold"))
        self.label.pack(pady=(20, 10))

        # UI: Fortschrittsanzeige
        self.progress_label = ctk.CTkLabel(self, text="Fortschritt: 0%", font=("Roboto", 14))
        self.progress_label.pack(pady=(0, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.pack(pady=(0, 20))
        self.progress_bar.set(0)

        # UI: Eingabe
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")
        
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Neuer Meilenstein...")
        self.entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.add_button = ctk.CTkButton(self.input_frame, text="Hinzufügen", width=100, command=self.neue_aufgabe)
        self.add_button.pack(side="right", padx=10)

        # UI: Liste
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=550, height=500)
        self.scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.setup_checkliste()

    def update_progress(self):
        if not self.daten:
            self.progress_bar.set(0)
            self.progress_label.configure(text="Fortschritt: 0%")
            return
        
        erledigt_count = sum(1 for item in self.daten if item["erledigt"])
        prozent = erledigt_count / len(self.daten)
        self.progress_bar.set(prozent)
        self.progress_label.configure(text=f"Fortschritt: {int(prozent * 100)}%")

    def setup_checkliste(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for index, item in enumerate(self.daten):
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5, padx=5)

            var = ctk.BooleanVar(value=item["erledigt"])
            cb = ctk.CTkCheckBox(
                row_frame, 
                text=item["aufgabe"], 
                variable=var,
                command=lambda i=index, v=var: self.status_aendern(i, v)
            )
            cb.pack(side="left", padx=10)

            btn_del = ctk.CTkButton(row_frame, text="X", width=30, fg_color="#A12", hover_color="#711", command=lambda i=index: self.loeschen(i))
            btn_del.pack(side="right", padx=2)

            btn_down = ctk.CTkButton(row_frame, text="↓", width=30, command=lambda i=index: self.verschieben(i, 1))
            btn_down.pack(side="right", padx=2)
            
            btn_up = ctk.CTkButton(row_frame, text="↑", width=30, command=lambda i=index: self.verschieben(i, -1))
            btn_up.pack(side="right", padx=2)
        
        self.update_progress()

    def verschieben(self, index, richtung):
        neu_index = index + richtung
        if 0 <= neu_index < len(self.daten):
            self.daten[index], self.daten[neu_index] = self.daten[neu_index], self.daten[index]
            self.setup_checkliste()
            self.dateisystem_speichern()

    def loeschen(self, index):
        self.daten.pop(index)
        self.setup_checkliste()
        self.dateisystem_speichern()

    def status_aendern(self, index, var):
        self.daten[index]["erledigt"] = var.get()
        self.update_progress()
        self.dateisystem_speichern()

    def neue_aufgabe(self):
        text = self.entry.get()
        if text:
            self.daten.append({"aufgabe": text, "erledigt": False})
            self.entry.delete(0, 'end')
            self.setup_checkliste()
            self.dateisystem_speichern()

    def laden(self):
        if os.path.exists(self.dateiname):
            try:
                with open(self.dateiname, "r", encoding="utf-8") as f:
                    inhalt = json.load(f)
                    if isinstance(inhalt, dict):
                        self.daten = [{"aufgabe": k, "erledigt": v} for k, v in inhalt.items()]
                    else:
                        self.daten = inhalt
            except Exception:
                self.standard_daten()
        else:
            self.standard_daten()

    def standard_daten(self):
        standard = [
            "NIE beantragen", 
            "Empadronamiento Alicante", 
            "Internet anmelden", 
            "Bankkonto (ES IBAN)",
            "Krankenversicherung SIP Karte",
            "Mietvertrag San José finalisieren"
        ]
        self.daten = [{"aufgabe": s, "erledigt": False} for s in standard]

    def dateisystem_speichern(self):
        try:
            with open(self.dateiname, "w", encoding="utf-8") as f:
                json.dump(self.daten, f, indent=4)
        except Exception as e:
            print(f"Speicherfehler: {e}")

if __name__ == "__main__":
    app = UmzugsApp()
    app.mainloop()
