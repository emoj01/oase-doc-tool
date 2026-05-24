import sys
import yaml

from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtGui import QFontDatabase, QPalette, QColor
from PySide6.QtCore import Qt

from app import OaseApp
from dialogs.startup_dialog import StartupDialog

# Loading config
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


# Loading stylesheet
def load_stylesheet():
    style = ""
    for path in config["paths"]["stylesheets"]:
        with open(path, "r", encoding="utf-8") as f:
            style += f.read() + "\n"

    for key, value in config["colors"].items():
        style = style.replace(f"$({key})", value)

    return style

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # System Dark Mode ignorieren
    app.setStyle("Fusion")

    palette = QApplication.palette()
    palette.setColor(QPalette.ColorRole.Base, QColor(config["colors"]["surface"]))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(config["colors"]["surface"]))
    palette.setColor(QPalette.ColorRole.Text, QColor(config["colors"]["text"]))
    palette.setColor(QPalette.ColorRole.Window, QColor(config["colors"]["bg"]))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(config["colors"]["text"]))
    QApplication.setPalette(palette)

    # Loading the font
    QFontDatabase.addApplicationFont("assets/fonts/IBM_Plex_Sans/static/IBMPlexSans-Regular.ttf")
    QFontDatabase.addApplicationFont("assets/fonts/IBM_Plex_Sans/static/IBMPlexSans-Bold.ttf")
    QFontDatabase.addApplicationFont("assets/fonts/IBM_Plex_Mono/IBMPlexMono-Regular.ttf")

    #applying the stylesheet   
    app.setStyleSheet(load_stylesheet())

    # Starting an app window
    dialog = StartupDialog()
    if dialog.exec() == QDialog.Accepted:
        # Nutzer hat eine Wahl getroffen
        window = OaseApp(dialog.result)
        window.show()
        sys.exit(app.exec())
    else:
        # Nutzer hat abgebrochen
        sys.exit(0)