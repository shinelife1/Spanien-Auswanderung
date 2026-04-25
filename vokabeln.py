import customtkinter as ctk
import json
import os
import random
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# =============================================================================
# 1. KONFIGURATION & DESIGN
# =============================================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DATA_FILE = "vokabel_ultimate_data.json"

class VokabelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🇪🇸 Vocabulary Master Ultimate GUI - Spain 2026")
        self.geometry("1000x850")
        
        # Daten laden (Fix hier enthalten)
        self.daten = self.laden()
        
        self.quiz_pool = []
        self.quiz_index = 0
        self.runde_korrekt = 0
        self.limit = 0

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=40)

        self.zeige_hauptmenue()

    # =============================================================================
    # 2. DATEN-LOGIK (DER FIX)
    # =============================================================================

    def laden(self):
        """ Lädt die JSON-Datenbank ohne die vorhandenen Daten zu löschen. """
        default_data = {
            "abteile": {"Allgemein": {"vokabeln": {"Hola": "Hallo"}, "saetze": {"Como estas?": "Wie geht es dir?"}}},
            "stats": {"punkte": 0, "korrekt": 0, "falsch": 0},
            "settings": {"modus": "SP_DE", "typ": "vokabeln", "aktiv_abteil": "Allgemein"}
        }

        if not os.path.exists(DATA_FILE):
            return default_data

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                
                # Wenn 'abteile' schon da ist, ist alles gut - wir laden einfach
                if "abteile" in d and d["abteile"]:
                    # Nur fehlende Keys ergänzen, nichts löschen!
                    if "settings" not in d: d["settings"] = default_data["settings"]
                    if "stats" not in d: d["stats"] = default_data["stats"]
                    return d
                
                # FALLBACK: Migration nur wenn 'abteile' komplett fehlt
                elif "vokabeln" in d or "saetze" in d:
                    new_struct = default_data.copy()
                    new_struct["abteile"]["Allgemein"]["vokabeln"] = d.get("vokabeln", {})
                    new_struct["abteile"]["Allgemein"]["saetze"] = d.get("saetze", {})
                    new_struct["stats"] = d.get("stats", default_data["stats"])
                    return new_struct
                
                return d
        except Exception as e:
            print(f"Schwerer Fehler beim Laden: {e}")
            return default_data

    def speichern(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.daten, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def get_rang_info(self, punkte):
        if punkte < 100: return "Principiante", 100 - punkte
        elif punkte < 300: return "Turista", 300 - punkte
        elif punkte < 600: return "Residente", 600 - punkte
        elif punkte < 1000: return "Local", 1000 - punkte
        else: return "Hidalgo", 0

    # =============================================================================
    # 3. UI: HAUPTMENÜ
    # =============================================================================

    def zeige_hauptmenue(self):
        self.clear_screen()
        self.unbind("<Return>")
        
        s = self.daten["stats"]
        sett = self.daten["settings"]
        
        # Sicherstellen dass Abteil existiert
        abt_name = sett.get("aktiv_abteil", "Allgemein")
        if abt_name not in self.daten["abteile"]:
            abt_name = list(self.daten["abteile"].keys())[0]
            sett["aktiv_abteil"] = abt_name
        
        typ = sett.get("typ", "vokabeln")
        pool = self.daten["abteile"][abt_name][typ]
        
        rang, bis_next = self.get_rang_info(s["punkte"])
        zeit = datetime.now(ZoneInfo("Europe/Berlin")).strftime("%H:%M:%S")

        dash = ctk.CTkFrame(self.container, corner_radius=15, border_width=2, border_color="#3a7ebf")
        dash.pack(fill="x", pady=(0, 25))

        ctk.CTkLabel(dash, text="VOCABULARY MASTER ULTIMATE", font=("Arial", 32, "bold"), text_color="#3a7ebf").pack(pady=(20, 5))
        ctk.CTkLabel(dash, text=f"🕒 {zeit} | 📂 {abt_name.upper()} ({len(pool)} {typ})", font=("Arial", 14, "italic")).pack(pady=5)

        stats_box = ctk.CTkFrame(dash, fg_color="transparent")
        stats_box.pack(pady=15)
        ctk.CTkLabel(stats_box, text=f"👤 {rang}", font=("Arial", 16, "bold"), text_color="#e6b800").grid(row=0, column=0, padx=25)
        ctk.CTkLabel(stats_box, text=f"🏆 {s['punkte']} Pkt", font=("Arial", 16, "bold"), text_color="#2fa572").grid(row=0, column=1, padx=25)
        ctk.CTkLabel(stats_box, text=f"✅ {s['korrekt']} | ❌ {s['falsch']}", font=("Arial", 16)).grid(row=0, column=2, padx=25)

        btn_box = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_box.pack(expand=True)

        menu = [
            ("🚀 Marathon-Quiz starten", self.setup_quiz, "#3a7ebf"),
            ("📖 Freies Üben", self.start_ueben, "#3a7ebf"),
            ("➕ Hinzufügen", self.ansicht_hinzufuegen, "#3a7ebf"),
            ("📁 Abteil verwalten", self.ansicht_verwalten, "#3a7ebf"),
            ("🔍 Suchen", self.ansicht_suche, "#2fa572"),
            ("⚙️ Einstellungen", self.ansicht_einstellungen, "#e6b800"),
            ("❌ Beenden", self.safe_exit, "#721c24")
        ]

        for t, c, col in menu:
            ctk.CTkButton(btn_box, text=t, command=c, font=("Arial", 16, "bold"), 
                          height=48, width=400, fg_color=col, hover_color="#1a1a1a").pack(pady=7)

    # =============================================================================
    # 4. QUIZ LOGIK
    # =============================================================================

    def setup_quiz(self):
        self.clear_screen()
        typ = self.daten["settings"]["typ"]
        pool = self.daten["abteile"][self.daten["settings"]["aktiv_abteil"]][typ]
        
        if not pool:
            ctk.CTkLabel(self.container, text="Abteil ist leer!", font=("Arial", 24), text_color="red").pack(pady=100)
            ctk.CTkButton(self.container, text="Zurück", command=self.zeige_hauptmenue).pack()
            return

        ctk.CTkLabel(self.container, text="QUIZ KONFIGURATION", font=("Arial", 22, "bold")).pack(pady=30)
        count = len(pool)
        steps = count - 1 if count > 1 else 1
        slider = ctk.CTkSlider(self.container, from_=1, to=count, number_of_steps=steps, width=400)
        slider.pack(pady=20)
        slider.set(min(10, count))
        val_lbl = ctk.CTkLabel(self.container, text=f"Anzahl: {int(slider.get())}", font=("Arial", 16, "bold"))
        val_lbl.pack()
        slider.configure(command=lambda v: val_lbl.configure(text=f"Anzahl: {int(v)}"))

        def start():
            self.limit = int(slider.get())
            self.quiz_pool = random.sample(list(pool.items()), self.limit)
            self.quiz_index, self.runde_korrekt = 0, 0
            self.naechste_frage()

        ctk.CTkButton(self.container, text="START", fg_color="green", height=50, width=200, command=start).pack(pady=40)

    def naechste_frage(self):
        self.clear_screen()
        if self.quiz_index >= self.limit:
            self.quiz_beendet()
            return
        bar = ctk.CTkProgressBar(self.container, width=600)
        bar.pack(pady=30)
        bar.set((self.quiz_index + 1) / self.limit)
        sp, de = self.quiz_pool[self.quiz_index]
        f, z = (sp, de) if self.daten["settings"]["modus"] == "SP_DE" else (de, sp)
        ctk.CTkLabel(self.container, text=f"Frage {self.quiz_index+1}/{self.limit}", font=("Arial", 14, "italic")).pack()
        ctk.CTkLabel(self.container, text=f, font=("Arial", 38, "bold"), text_color="#3a7ebf").pack(pady=40)
        ent = ctk.CTkEntry(self.container, width=400, height=50, font=("Arial", 20))
        ent.pack(pady=10); ent.focus()
        def check(event=None):
            if ent.get().strip().lower() == z.lower():
                self.daten["stats"]["punkte"] += 10
                self.daten["stats"]["korrekt"] += 1
                self.runde_korrekt += 1
            else:
                self.daten["stats"]["falsch"] += 1
                self.daten["stats"]["punkte"] = max(0, self.daten["stats"]["punkte"] - 5)
            self.quiz_index += 1
            self.naechste_frage()
        self.bind("<Return>", check)
        ctk.CTkButton(self.container, text="OK", command=check, width=150).pack(pady=20)

    def quiz_beendet(self):
        self.unbind("<Return>"); self.speichern(); self.clear_screen()
        ctk.CTkLabel(self.container, text="RUNDE BEENDET", font=("Arial", 32, "bold")).pack(pady=50)
        ctk.CTkLabel(self.container, text=f"{self.runde_korrekt} von {self.limit} richtig!", font=("Arial", 22)).pack()
        ctk.CTkButton(self.container, text="MENÜ", command=self.zeige_hauptmenue, width=200).pack(pady=50)

    # =============================================================================
    # 5. WEITERE FUNKTIONEN
    # =============================================================================

    def start_ueben(self):
        abt = self.daten["settings"]["aktiv_abteil"]
        pool = self.daten["abteile"][abt][self.daten["settings"]["typ"]]
        if not pool: return
        def uebung():
            self.clear_screen()
            q, l = random.choice(list(pool.items()))
            f, z = (q, l) if self.daten["settings"]["modus"] == "SP_DE" else (l, q)
            lbl = ctk.CTkLabel(self.container, text=f, font=("Arial", 36, "bold"), text_color="#3a7ebf")
            lbl.pack(pady=60)
            ent = ctk.CTkEntry(self.container, width=350, height=45); ent.pack(); ent.focus()
            def vergl(e=None):
                if ent.get().strip().lower() == "?": lbl.configure(text=z, text_color="orange")
                elif ent.get().strip().lower() == z.lower(): uebung()
            self.bind("<Return>", vergl)
            ctk.CTkButton(self.container, text="Menü", command=self.zeige_hauptmenue, fg_color="#721c24").pack(pady=40)
        uebung()

    def ansicht_hinzufuegen(self):
        self.clear_screen()
        abt, typ = self.daten["settings"]["aktiv_abteil"], self.daten["settings"]["typ"]
        ctk.CTkLabel(self.container, text=f"Hinzufügen zu {abt}", font=("Arial", 22, "bold")).pack(pady=30)
        sp_in = ctk.CTkEntry(self.container, placeholder_text="Spanisch", width=400, height=40); sp_in.pack(pady=10)
        de_in = ctk.CTkEntry(self.container, placeholder_text="Deutsch", width=400, height=40); de_in.pack(pady=10)
        def save():
            if sp_in.get() and de_in.get():
                self.daten["abteile"][abt][typ][sp_in.get().strip()] = de_in.get().strip()
                self.speichern(); self.zeige_hauptmenue()
        ctk.CTkButton(self.container, text="Speichern", command=save, fg_color="green").pack(pady=30)
        ctk.CTkButton(self.container, text="Abbruch", command=self.zeige_hauptmenue).pack()

    def ansicht_verwalten(self):
        self.clear_screen()
        abt, typ = self.daten["settings"]["aktiv_abteil"], self.daten["settings"]["typ"]
        pool = self.daten["abteile"][abt][typ]
        scroll = ctk.CTkScrollableFrame(self.container, width=800, height=500); scroll.pack()
        for k, v in pool.items():
            f = ctk.CTkFrame(scroll); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{k} = {v}").pack(side="left", padx=10)
            ctk.CTkButton(f, text="X", width=40, fg_color="red", command=lambda x=k: [pool.pop(x), self.speichern(), self.ansicht_verwalten()]).pack(side="right")
        ctk.CTkButton(self.container, text="Zurück", command=self.zeige_hauptmenue).pack(pady=20)

    def ansicht_einstellungen(self):
        self.clear_screen(); sett = self.daten["settings"]
        def toggle_m(): sett["modus"] = "DE_SP" if sett["modus"] == "SP_DE" else "SP_DE"; self.ansicht_einstellungen()
        def toggle_t(): sett["typ"] = "saetze" if sett["typ"] == "vokabeln" else "vokabeln"; self.ansicht_einstellungen()
        ctk.CTkButton(self.container, text=f"Modus: {sett['modus']}", command=toggle_m).pack(pady=10)
        ctk.CTkButton(self.container, text=f"Typ: {sett['typ']}", command=toggle_t).pack(pady=10)
        for a in self.daten["abteile"]:
            col = "green" if a == sett["aktiv_abteil"] else "gray"
            ctk.CTkButton(self.container, text=a, fg_color=col, command=lambda x=a: [sett.update({"aktiv_abteil":x}), self.ansicht_einstellungen()]).pack(pady=2)
        ctk.CTkButton(self.container, text="Zurück", command=self.zeige_hauptmenue).pack(pady=20)

    def ansicht_suche(self):
        self.clear_screen(); ent = ctk.CTkEntry(self.container, width=400); ent.pack(pady=20); ent.focus()
        res = ctk.CTkScrollableFrame(self.container, width=700, height=400); res.pack()
        def search(e=None):
            for w in res.winfo_children(): w.destroy()
            q = ent.get().lower()
            for an, ac in self.daten["abteile"].items():
                for tk in ["vokabeln", "saetze"]:
                    for s, d in ac[tk].items():
                        if q in s.lower() or q in d.lower():
                            ctk.CTkLabel(res, text=f"[{an}] {s} = {d}").pack(anchor="w")
        self.bind("<Return>", search)
        ctk.CTkButton(self.container, text="Zurück", command=self.zeige_hauptmenue).pack(pady=20)

    def safe_exit(self):
        self.speichern(); self.quit()

if __name__ == "__main__":
    app = VokabelApp(); app.mainloop()
