import sys
import os
import subprocess
import webbrowser
import ctypes
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__' and not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas",
        sys.executable,
        f'"{os.path.abspath(__file__)}"',
        None, 1
    )
    sys.exit()

def run_trial_reset():
    folders = [
        os.path.expandvars("%AppData%\\iMyFone"),
        os.path.expandvars("%LocalAppData%\\iMyFone"),
        "C:\\ProgramData\\iMyFone"
    ]

    new_guid = os.urandom(16).hex().upper()
    results = ["[INFO] Running trial reset..."]
    results.append(f"[INFO] New GUID: {new_guid}")

    commands = [
        ('Deleting old registry (AnyTo)', 'reg delete "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /f'),
        ('Deleting old registry (iMyfoneDown)', 'reg delete "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\iMyfoneDown" /f'),
        ('Creating fresh registry key', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /f'),
        ('Setting GUID', f'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /v guid /t REG_SZ /d "{new_guid}" /f'),
        ('Disabling version collection', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /v bVersionCollect /t REG_SZ /d false /f'),
        ('Disabling AB test version', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /v 697_ABTestVersion /t REG_SZ /d false /f'),
        ('Setting PackageSetting to A', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /v 697_PackageSetting /t REG_SZ /d A /f'),
        ('Disabling AB test group', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\AnyTo" /v v697ABtest_NormalGroup /t REG_SZ /d false /f'),
        ('Resetting joystick limit', 'reg add "HKLM\\SOFTWARE\\WOW6432Node\\iMyfone\\joystick" /v "(Default)" /t REG_DWORD /d 900 /f')
    ]

    for label, cmd in commands:
        try:
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            results.append(f"[OK] {label}")
        except subprocess.CalledProcessError:
            results.append(f"[FAILED] {label}")

    for folder in folders:
        if os.path.exists(folder):
            try:
                subprocess.run(f'rmdir /s /q "{folder}"', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                results.append(f"[OK] Deleted folder: {folder}")
            except subprocess.CalledProcessError:
                results.append(f"[FAILED] Could not delete folder: {folder}")
        else:
            results.append(f"[SKIPPED] Folder not found: {folder}")

    return "\n".join(results)

def launch_app():
    app_path = "C:\\Program Files (x86)\\iMyFone\\iMyFone AnyTo\\AnyTo.exe"
    if not os.path.exists(app_path):
        folder = QFileDialog.getExistingDirectory(None, "Locate iMyFone AnyTo Folder", "C:\\")
        if not folder:
            return "[CANCELLED] Launch aborted. Folder not selected."
        candidate = os.path.join(folder, "AnyTo.exe")
        if not os.path.exists(candidate):
            return f"[FAILED] 'AnyTo.exe' not found in selected folder: {folder}"
        app_path = candidate

    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas",
            app_path,
            None, None, 1
        )
        return "[OK] Launching iMyFone AnyTo with admin rights..."
    except Exception as e:
        return f"[FAILED] Failed to launch app: {str(e)}"

class LauncherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trial Reset")
        self.setGeometry(100, 100, 600, 400)

        
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #333;
                color: white;
                padding: 12px;
                border-radius: 10px;
                font-size: 14px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                color: #555;
                font-size: 12px;
            }
            QLabel.version {
                color: #aaa;
                font-size: 10px;
                margin-top: 10px;
            }
        """)

        
        layout = QVBoxLayout()

        
        self.watermark = QLabel("Logs")
        self.watermark.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.watermark)

       
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        
        button_layout = QHBoxLayout()

        self.reset_btn = QPushButton("Reset Trial")
        self.reset_btn.setToolTip("Click to reset trial version of AnyTo")
        self.reset_btn.clicked.connect(self.run_reset)
        button_layout.addWidget(self.reset_btn)

        self.launch_btn = QPushButton("Launch AnyTo")
        self.launch_btn.setToolTip("Click to launch AnyTo.exe")
        self.launch_btn.clicked.connect(self.launch_app)
        button_layout.addWidget(self.launch_btn)

        self.discord_btn = QPushButton("Discord")
        self.discord_btn.setToolTip("Click to join the Discord community")
        self.discord_btn.clicked.connect(lambda: webbrowser.open("https://discord.gg/2GJnQvzqqW"))
        button_layout.addWidget(self.discord_btn)

        layout.addLayout(button_layout)

        
        self.version_label = QLabel("Made by zeaxile")
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setObjectName("version")
        layout.addWidget(self.version_label)

        self.setLayout(layout)

        
        self.setWindowOpacity(0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

        
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
        self.tray_icon = QSystemTrayIcon(QIcon(logo_path), self)
        self.tray_icon.setToolTip("Unlimited Mode Launcher")
        self.tray_icon.show()

        
        tray_menu = QMenu(self)
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.show)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        tray_menu.addAction(open_action)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)

        
        self.setWindowIcon(QIcon(logo_path))

    def run_reset(self):
        self.output.append("Resetting trial...\n")
        result = run_trial_reset()
        self.output.append(result)

    def launch_app(self):
        self.output.append("Launching app...\n")
        result = launch_app()
        self.output.append(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = LauncherApp()
    launcher.show()
    sys.exit(app.exec_())
