# Trial resetter for iMyFone AnyTo

This is a PyQt5-based launcher and trial reset tool for **iMyFone AnyTo**, designed with a dark-themed UI and quality-of-life features to make resetting the trial and launching the app easy and sleek.

---

## 🚀 Features

- **Trial Reset**:  Resets the trial version.
- **Admin Launch**: Opens AnyTo.exe with elevated permissions.
- **UI with Logs**: See logs of all actions inside the interface.
- **Dark Theme**: Beautiful dark-mode interface with styled buttons and text.
---

## 🖥️ Requirements

- **Windows OS**
- **Python 3.6+**
- **PyQt5**: Install via:

```bash
pip install PyQt5
```

---

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/unlimited-mode-launcher.git
   ```

2. Navigate into the project:
   ```bash
   cd unlimited-mode-launcher
   ```

3. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install PyQt5
   ```

---

## ▶️ Running the Launcher

Simply run:

```bash
python main.py
```

The script will auto-request admin privileges if not already running as admin.

---

## 🛠️ How it Works

- Deletes specific folders and registry keys tied to iMyFone AnyTo's trial.
- Generates a new GUID to fool the app into thinking it’s a fresh install.
- Offers a GUI to launch the app or reset trial with one click.

---

## ⚠️ Disclaimer

> This tool is meant for **educational purposes** only.  
> Misuse or redistribution of software in violation of its license or terms of service is your responsibility.

---

## 👤 Credits

- Built by **zeaxile**
- Join the community: [Discord Invite](https://discord.gg/2GJnQvzqqW)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
