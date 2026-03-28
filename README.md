<div align="center">

<img src="img/brilliance.png" width="80" alt="HypeSquad Logo"/>

# HypeSquad Manager

**A simple tool to manage your Discord HypeSquad badge**

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.x-1F6AA8?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## $ Features

-  Switch between all 3 HypeSquad houses — **Bravery**, **Brilliance**, **Balance**
-  Add or ➖ Remove your HypeSquad badge instantly
-  Save your token locally for quick access
-  Show/Hide token for privacy
-  Visual badge icons for easy selection
-  Sleek dark mode UI

---

## $ Getting Started

###  Requirements

- Python 3.8+
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YourUsername/HypeSquad-Manager.git
cd HypeSquad-Manager
```

**2. Install dependencies**
```bash
pip install customtkinter requests Pillow
```

**3. Run the app**
```bash
python main.py
```

---

## $ Build as EXE

To compile into a standalone `.exe`:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --add-data "img/brilliance.png;img" --name "HypeSquadManager" main.py
```

The output will be in the `dist/` folder.

---

## $ Project Structure

```
HypeSquad-Manager/
├── main.py
├── config.json        # Auto-generated after saving token
├── img/
│   └── brilliance.png
└── README.md
```

---

## $ Author

Made by **Emperor Slay**
