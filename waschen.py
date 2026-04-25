import customtkinter as ctk
from datetime import datetime

class StromMonitor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Spanien Strom-Monitor")
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Strompreis-Check", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Lade Status...", font=("Arial", 16))
        self.status_label.pack(pady=10)

        self.info_text = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.info_text.pack(pady=10)

        self.check_price()

    def check_price(self):
        now = datetime.now()
        hour = now.hour
        is_weekend = now.weekday() >= 5 # 5=Samstag, 6=Sonntag

        if is_weekend or (0 <= hour < 8):
            status = "GÜNSTIG (Valle) 🟢"
            color = "#2ecc71"
            info = "Jetzt ist die beste Zeit zum Waschen!"
        elif hour in [8, 9, 14, 15, 16, 17, 22, 23]:
            status = "MITTEL (Llano) 🟡"
            color = "#f1c40f"
            info = "Akzeptabel, aber nachts/am Wochenende ist es billiger."
        else:
            status = "TEUER (Punta) 🔴"
            color = "#e74c3c"
            info = "Warte lieber bis 22 Uhr oder das Wochenende!"

        self.status_label.configure(text=status, text_color=color)
        self.info_text.configure(text=info)

if __name__ == "__main__":
    app = StromMonitor()
    app.mainloop()
