import customtkinter as ctk
import requests
import json
import os
import threading
from PIL import Image
import io
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
class HypeSquadManager:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Made by Emperor Slay")
        self.window.geometry("460x520")
        self.window.resizable(False, False)
        self.token = ctk.StringVar()
        self.show_token = False
        self.house = ctk.IntVar(value=1)
        self.house_images = {}
        self.house_buttons = {}
        self.colors = {1: "#5865F2", 2: "#faa61a", 3: "#43b581"}
        self.setup_ui()
        self.load_token()
        self.load_all_images()
    def load_all_images(self):
        threading.Thread(target=self.load_local_image, args=(2, "img/brilliance.png"), daemon=True).start()
        online = {
            1: "https://cdn.discordapp.com/badge-icons/8a88d63823d8a71cd5e390baa45efa02.png",
            3: "https://cdn.discordapp.com/badge-icons/3aa41de486fa12454c3761e8e223442e.png",
        }
        for house_id, url in online.items():
            threading.Thread(target=self.load_online_image, args=(house_id, url), daemon=True).start()
    def load_local_image(self, house_id, path):
        try:
            img = Image.open(path).convert("RGBA")
            img = img.resize((50, 50), Image.LANCZOS)
            self.house_images[house_id] = ctk.CTkImage(light_image=img, dark_image=img, size=(50, 50))
            self.window.after(0, self.update_button_image, house_id)
        except Exception as e:
            self.window.after(0, self.add_log, f"❌ Failed to load local image: {e}")

    def load_online_image(self, house_id, url):
        try:
            response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                img = Image.open(io.BytesIO(response.content)).convert("RGBA")
                img = img.resize((50, 50), Image.LANCZOS)
                self.house_images[house_id] = ctk.CTkImage(light_image=img, dark_image=img, size=(50, 50))
                self.window.after(0, self.update_button_image, house_id)
        except Exception as e:
            self.window.after(0, self.add_log, f"❌ Failed to load image {house_id}: {e}")

    def update_button_image(self, house_id):
        if house_id in self.house_buttons and house_id in self.house_images:
            self.house_buttons[house_id].configure(image=self.house_images[house_id], text="")

    def setup_ui(self):
        ctk.CTkLabel(
            self.window,
            text="HypeSquad Manager",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(20, 10))

        token_frame = ctk.CTkFrame(self.window)
        token_frame.pack(padx=25, pady=5, fill="x")

        ctk.CTkLabel(token_frame, text="Token:").pack(anchor="w", padx=12, pady=(10, 0))
        self.token_entry = ctk.CTkEntry(
            token_frame, textvariable=self.token,
            placeholder_text="Enter your token here",
            show="*", width=340
        )
        self.token_entry.pack(padx=12, pady=(5, 5))

        row = ctk.CTkFrame(token_frame, fg_color="transparent")
        row.pack(pady=(0, 10))
        ctk.CTkButton(row, text="👁️ Show/Hide", command=self.toggle_token, width=130, height=30).pack(side="left", padx=5)
        ctk.CTkButton(row, text="💾 Save Token", command=self.save_token,
                      fg_color="#198345", hover_color="#165e34", width=130, height=30).pack(side="left", padx=5)

        house_frame = ctk.CTkFrame(self.window)
        house_frame.pack(padx=25, pady=10, fill="x")

        ctk.CTkLabel(house_frame, text="Select House:",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(12, 10))

        buttons_row = ctk.CTkFrame(house_frame, fg_color="transparent")
        buttons_row.pack(pady=(0, 5))

        houses = {1: "Bravery", 2: "Brilliance", 3: "Balance"}

        for house_id in houses:
            col = ctk.CTkFrame(buttons_row, fg_color="transparent")
            col.pack(side="left", padx=12)

            btn = ctk.CTkButton(
                col,
                text="...",
                width=80, height=80,
                corner_radius=16,
                font=ctk.CTkFont(size=11),
                fg_color=self.colors[house_id] if house_id == 1 else "#2b2d31",
                hover_color=self.colors[house_id],
                command=lambda hid=house_id: self.select_house(hid)
            )
            btn.pack()
            self.house_buttons[house_id] = btn

            ctk.CTkLabel(col, text=houses[house_id],
                         font=ctk.CTkFont(size=11)).pack(pady=(5, 0))

        self.selected_label = ctk.CTkLabel(
            house_frame, text="Selected: Bravery",
            font=ctk.CTkFont(size=12)
        )
        self.selected_label.pack(pady=(5, 12))

        btn_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="➕ Add Badge", command=self.run_add,
                      fg_color="#3498db", hover_color="#2980b9", width=160, height=42).pack(side="left", padx=8)
        ctk.CTkButton(btn_frame, text="➖ Remove Badge", command=self.run_remove,
                      fg_color="#e74c3c", hover_color="#c0392b", width=160, height=42).pack(side="left", padx=8)

        self.status = ctk.CTkLabel(self.window, text="Ready", font=ctk.CTkFont(size=12))
        self.status.pack(pady=5)

        self.log = ctk.CTkTextbox(self.window, height=80)
        self.log.pack(padx=25, pady=(0, 15), fill="both", expand=True)

    def select_house(self, house_id):
        self.house.set(house_id)
        names = {1: "Bravery", 2: "Brilliance", 3: "Balance"}
        for hid, btn in self.house_buttons.items():
            btn.configure(fg_color=self.colors[hid] if hid == house_id else "#2b2d31")
        self.selected_label.configure(text=f"Selected: {names[house_id]}")

    def toggle_token(self):
        self.show_token = not self.show_token
        self.token_entry.configure(show="" if self.show_token else "*")

    def load_token(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json") as f:
                    data = json.load(f)
                    self.token.set(data.get("token", ""))
                    self.add_log("✅ Token loaded from config")
            except:
                self.add_log("❌ Error loading token")

    def save_token(self):
        if self.token.get().strip():
            with open("config.json", "w") as f:
                json.dump({"token": self.token.get().strip()}, f)
            self.add_log("💾 Token saved successfully")
        else:
            self.add_log("❌ Please enter a token")

    def add_log(self, msg):
        self.log.insert("end", f"{msg}\n")
        self.log.see("end")
        self.status.configure(text=msg[:40])

    def run_add(self):
        threading.Thread(target=self.add_badge, daemon=True).start()

    def run_remove(self):
        threading.Thread(target=self.remove_badge, daemon=True).start()

    def add_badge(self):
        token = self.token.get().strip()
        if not token:
            self.add_log("❌ Token is required")
            return
        house_id = self.house.get()
        houses = {1: "Bravery", 2: "Brilliance", 3: "Balance"}
        self.add_log(f"🔄 Adding {houses[house_id]} badge...")
        try:
            res = requests.post(
                "https://discord.com/api/v9/hypesquad/online",
                headers={"Authorization": token, "Content-Type": "application/json"},
                json={"house_id": house_id}
            )
            if res.status_code == 204:
                self.add_log("✅ Badge added successfully!")
            elif res.status_code == 401:
                self.add_log("❌ Invalid token")
            elif res.status_code == 400:
                self.add_log("⚠️ You already have a HypeSquad badge")
            else:
                self.add_log(f"❌ Error: {res.status_code}")
        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}")

    def remove_badge(self):
        token = self.token.get().strip()
        if not token:
            self.add_log("❌ Token is required")
            return
        self.add_log("🔄 Removing badge...")
        try:
            res = requests.delete(
                "https://discord.com/api/v9/hypesquad/online",
                headers={"Authorization": token}
            )
            if res.status_code == 204:
                self.add_log("✅ Badge removed successfully!")
            elif res.status_code == 401:
                self.add_log("❌ Invalid token")
            elif res.status_code == 404:
                self.add_log("⚠️ You don't have a HypeSquad badge")
            else:
                self.add_log(f"❌ Error: {res.status_code}")
        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}")

    def run(self):
        self.window.mainloop()
if __name__ == "__main__":
    app = HypeSquadManager()
    app.run()
