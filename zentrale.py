import customtkinter as ctk
import subprocess
import sys
import os

# Design-Einstellungen
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MasterCenter(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🇪🇸 Alicante Master Center 2026")
        self.geometry("500x1000") # Maximale Höhe für alle Tools

        # --- UI ELEMENTE ---
        self.header = ctk.CTkLabel(self, text="SPANIEN KONTROLLZENTRUM", font=("Arial", 24, "bold"), text_color="#3a7ebf")
        self.header.pack(pady=30)

        self.info = ctk.CTkLabel(self, text="Wähle eine Anwendung zum Starten:", font=("Arial", 14))
        self.info.pack(pady=5)

        # Buttons zum Starten der Unter-Apps
        self.btn_finance = ctk.CTkButton(self, text="💰 BUDGET RECHNER", 
                                          command=lambda: self.start_app("rechner.py"),
                                          height=50, width=350, font=("Arial", 16, "bold"))
        self.btn_finance.pack(pady=8)

        self.btn_gehalt = ctk.CTkButton(self, text="💶 BRUTTO-NETTO RECHNER", 
                                          command=lambda: self.start_app("gehalt_check.py"),
                                          height=50, width=350, font=("Arial", 16, "bold"),
                                          fg_color="#8e44ad", hover_color="#7d3c98") # Lila Akzent
        self.btn_gehalt.pack(pady=8)

        self.btn_checklist = ctk.CTkButton(self, text="📋 UMZUGS-CHECKLISTE", 
                                          command=lambda: self.start_app("checklist.py"),
                                          height=50, width=350, font=("Arial", 16, "bold"),
                                          fg_color="#e67e22", hover_color="#d35400")
        self.btn_checklist.pack(pady=8)

        self.btn_mietcheck = ctk.CTkButton(self, text="(Bald)⚖️ MIETVERTRAG-PRÜFER", 
                                          command=lambda: self.start_app("mietcheck.py"),
                                          height=50, width=350, font=("Arial", 16, "bold"),
                                          fg_color="#c0392b", hover_color="#a93226")
        self.btn_mietcheck.pack(pady=8)

        self.btn_internet = ctk.CTkButton(self, text="🌐 INTERNET-VERGLEICHER", 
                                          command=lambda: self.start_app("internet_check.py"),
                                          height=50, width=350, font=("Arial", 16, "bold"),
                                          fg_color="#2980b9", hover_color="#1f618d")
        self.btn_internet.pack(pady=8)

        self.btn_strom = ctk.CTkButton(self, text="(Bald)⚡ STROM-MONITOR", 
                                          command=lambda: self.start_app("strom.py"),
                                          height=50, width=350, font=("Arial", 16, "bold"),
                                          fg_color="#f1c40f", hover_color="#d4ac0d", text_color="black")
        self.btn_strom.pack(pady=8)

        self.btn_vocab = ctk.CTkButton(self, text="🎓 VOKABEL TRAINER", 
                                        command=lambda: self.start_app("vokabeln.py"),
                                        height=50, width=350, font=("Arial", 16, "bold"))
        self.btn_vocab.pack(pady=8)

        self.btn_scraper = ctk.CTkButton(self, text="🏠 IMMOBILIEN & WETTER", 
                                          command=lambda: self.start_app("wetter.py"),
                                          height=50, width=350, font=("Arial", 16, "bold"),
                                          fg_color="#2fa572", hover_color="#1e6e4c")
        self.btn_scraper.pack(pady=8)

        self.footer = ctk.CTkLabel(self, text="Status: Bereit", font=("Arial", 12, "italic"), text_color="gray")
        self.footer.pack(side="bottom", pady=20)

    def start_app(self, dateiname):
        """Startet eine andere Python-Datei als eigenständigen Prozess."""
        skript_verzeichnis = os.path.dirname(os.path.abspath(__file__))
        voller_pfad = os.path.join(skript_verzeichnis, dateiname)
        
        if os.path.exists(voller_pfad):
            self.footer.configure(text=f"Starte {dateiname}...", text_color="green")
            subprocess.Popen([sys.executable, voller_pfad])
        else:
            self.footer.configure(text=f"Fehler: {dateiname} nicht gefunden!", text_color="#e74c3c")

if __name__ == "__main__":
    app = MasterCenter()
    app.mainloop()
