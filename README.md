🇪🇸 Alicante Master Center 2026
Das Alicante Master Center ist eine All-in-One Kontrollzentrale für die Planung und Durchführung deines Umzugs und Lebens in Spanien. Die Anwendung dient als Hub für verschiedene spezialisierte Tools – vom Budget-Rechner bis zum Immobilien-Scraper.
🚀 Features & Tools
Das Dashboard fungiert als Launcher für folgende Module:
💰 Budget Rechner (rechner.py): Behalte deine Ausgaben im Griff.
💶 Brutto-Netto Rechner (gehalt_check.py): Gehaltskalkulation nach spanischem Steuerrecht.
📋 Umzugs-Checkliste (checklist.py): Verpasse keinen wichtigen Schritt (NIE, Empadronamiento etc.).
🎓 Vokabel Trainer (vokabeln.py): Lerne Spanisch mit System.
🏠 Immobilien & Wetter (wetter.py): Live-Scraping von Wohnungsangeboten in Alicante/San Juan & Wetter-Updates.
🌐 Internet-Vergleicher (internet_check.py): Faser- und Mobilfunkanbieter im Check.
⚖️ Mietvertrag-Prüfer & ⚡ Strom-Monitor: (In Entwicklung)
🛠️ Technische Voraussetzungen
Die App basiert auf Python 3.12+ und nutzt moderne Bibliotheken für GUI und Automatisierung.
Benötigte Bibliotheken
Installiere die Abhängigkeiten mit folgendem Befehl:
bash
pip install customtkinter requests selenium webdriver-manager verbecc
Verwende Code mit Vorsicht.
Hinweis: Falls du Python 3.14 nutzt und Probleme mit verbecc hast, achte auf die spezifischen Import-Fixes im Vokabel-Modul.
📂 Projektstruktur
Alle Skripte müssen sich im selben Verzeichnis befinden, damit der Launcher sie finden kann:
Verwende Code mit Vorsicht.
⌨️ Bedienung
Starte das Hauptmenü:
bash
python zentrale.py
Verwende Code mit Vorsicht.
Klicke auf das gewünschte Tool. Es öffnet sich ein eigenständiges Fenster, während das Kontrollzentrum im Hintergrund aktiv bleibt.
