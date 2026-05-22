# pages/startseite.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QTextEdit, QLabel, QApplication
    )

class Startseite(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)

        title = QLabel("Einleitender Text")
        title.setProperty("type", "h3")
        card_layout.addWidget(title)

        self.f_text = QTextEdit()
        self.f_text.setPlaceholderText("Einleitender Text für die Startseite...")
        card_layout.addWidget(self.f_text)

        layout.addWidget(card)
        layout.addStretch()

    def mousePressEvent(self, event):
        fw = QApplication.focusWidget()

        if fw:
            fw.clearFocus()
        return super().mousePressEvent(event)