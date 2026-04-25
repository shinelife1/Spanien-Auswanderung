import customtkinter as ctk
import time
import csv
import webbrowser
import threading
import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from zoneinfo import ZoneInfo

# --- EINSTELLUNGEN ---
API_KEY = "b63b8c55d7818e59ad4e33868e1225a3" 
STADT = "Sant Joan d'Alacant"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MasterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🇪🇸 Noah's Spain Dashboard 2026")
        self.geometry("1000x800")

        # --- NAVIGATION / HEADER ---
        self.header = ctk.CTkLabel(self, text="ALICANTE MASTER DASHBOARD", font=("Arial", 28, "bold"), text_color="#3a7ebf")
        self.header.pack(pady=20)

        # Tab-System erstellen
        self.tabview = ctk.CTkTabview(self, width=950, height=650)
        self.tabview.pack(padx=20, pady=10)
        
        self.tab_weather = self.tabview.add("☀️ Wetter & Info")
        self.tab_scraper = self.tabview.add("🏠 Wohnungssuche")

        self.setup_weather_tab()
        self.setup_scraper_tab()

    # --- WETTER TAB ---
    def setup_weather_tab(self):
        self.wetter_box = ctk.CTkTextbox(self.tab_weather, width=500, height=300, font=("Arial", 16))
        self.wetter_box.pack(pady=20)
        
        btn = ctk.CTkButton(self.tab_weather, text="DATEN AKTUALISIEREN", command=self.update_weather_info)
        btn.pack(pady=10)
        self.update_weather_info()

    def update_weather_info(self):
        # Wetter holen (API Link korrigiert)
        url = f"http://openweathermap.org{STADT},ES&appid={API_KEY}&units=metric&lang=de"
        try:
            r = requests.get(url).json()
            temp = r['main']['temp']
            desc = r['weather'][0]['description']
            w_text = f"🌡️ Temperatur: {temp}°C\n☁️ Himmel: {desc.capitalize()}\n"
        except:
            w_text = "⚠️ Wetterdaten aktuell nicht verfügbar (Key prüfen!).\n"

        # Feiertage
        heute = datetime.now().strftime("%d.%m.")
        feiertage = {"01.05.": "Tag der Arbeit", "24.06.": "San Juan (Alicante Festival!)"}
        event = feiertage.get(heute, "Kein spezieller Feiertag heute.")

        bericht = f"📍 Ort: {STADT}\n" + "━"*30 + f"\n{w_text}\n📅 Events: {event}\n"
        bericht += "\n💡 Tipp: " + ("Regenschirm mitnehmen!" if "regen" in w_text.lower() else "Ab an den Playa San Juan! 🏖️")
        
        self.wetter_box.delete("1.0", "end")
        self.wetter_box.insert("1.0", bericht)

    # --- SCRAPER TAB ---
    def setup_scraper_tab(self):
        self.start_btn = ctk.CTkButton(self.tab_scraper, text="🚀 SUCHE STARTEN (ALICANTE + SAN JUAN)", command=self.run_scraper_thread)
        self.start_btn.pack(pady=10, fill="x", padx=50)

        self.status_lbl = ctk.CTkLabel(self.tab_scraper, text="Bereit.")
        self.status_lbl.pack()

        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_scraper, width=850, height=450, label_text="Ergebnisse")
        self.scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.load_csv_data()

    def load_csv_data(self):
        for w in self.scroll_frame.winfo_children(): w.destroy()
        if os.path.exists('wohnungen_alicante.csv'):
            try:
                with open('wohnungen_alicante.csv', mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.add_card(row)
            except:
                pass

    def add_card(self, row):
        card = ctk.CTkFrame(self.scroll_frame, fg_color="#2b2b2b", corner_radius=8)
        card.pack(fill="x", pady=5, padx=5)
        
        txt = f"💰 {row['Preis']} | 🛏️ {row.get('Zimmer', 'N/A')} | 📐 {row.get('Flaeche', 'N/A')}\n📍 {row['Titel'][:60]}..."
        ctk.CTkLabel(card, text=txt, justify="left").pack(side="left", padx=15, pady=10)
        ctk.CTkButton(card, text="LINK", width=60, command=lambda: webbrowser.open(row['Link'])).pack(side="right", padx=10)

    def run_scraper_thread(self):
        self.start_btn.configure(state="disabled", text="SUCHE LÄUFT...")
        self.status_lbl.configure(text="Scraper gestartet...", text_color="white")
        threading.Thread(target=self.scrape_logic, daemon=True).start()

    def scrape_logic(self):
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        try:
            driver.get("https://www.idealista.com/de/buscar/alquiler-viviendas/san-juan-de-alicante-alicante/alicante/?ordenado-por=precios-asc")
            time.sleep(5)
            
            try:
                driver.find_element(By.XPATH, "//button[contains(., 'Aceptar')]").click()
                time.sleep(2)
            except:
                pass
            
            listings = driver.find_elements(By.TAG_NAME, "article")
            results = []

            for item in listings:
                try:
                    text = item.text
                    lines = text.split("\n")
                    if len(lines) < 2: continue
                    
                    zimm = next((l for l in lines if "hab" in l.lower()), "N/A")
                    sqm = next((l for l in lines if "m²" in l), "N/A")
                    preis = next((l for l in lines if "€" in l), "N/A")
                    link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                    
                    results.append({'Titel': lines[0], 'Preis': preis, 'Zimmer': zimm, 'Flaeche': sqm, 'Link': link})
                except:
                    continue

            # Speichern mit Zugriffsschutz
            try:
                with open('wohnungen_alicante.csv', 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['Titel', 'Preis', 'Zimmer', 'Flaeche', 'Link'])
                    writer.writeheader()
                    writer.writerows(results)
                self.after(0, self.load_csv_data)
                self.after(0, lambda: self.status_lbl.configure(text="✅ Suche abgeschlossen!", text_color="green"))
            except PermissionError:
                self.after(0, lambda: self.status_lbl.configure(text="❌ Fehler: CSV offen!", text_color="red"))

        except Exception as e:
            print(f"Fehler: {e}")
            self.after(0, lambda: self.status_lbl.configure(text="⚠️ Fehler beim Scraping", text_color="orange"))
        finally:
            driver.quit()
            self.after(0, lambda: self.start_btn.configure(state="normal", text="🚀 SUCHE STARTEN"))

if __name__ == "__main__":
    app = MasterApp()
    app.mainloop()
