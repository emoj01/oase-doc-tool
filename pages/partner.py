# pages/partner.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QFrame, QScrollArea, QLineEdit, QLabel, QApplication
    )

class Partner(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        scroll = QScrollArea()
        scroll.setProperty("type", "bg-light")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(self._partner())

        layout.addWidget(scroll)

    def _partner(self) -> QFrame:
        card, card_layout = self._basic_card("Partner")

        self.f_partner = []

        entries = [
            ["Name Regiment", "Kaserne", "Straße, Nr.", "PLZ, Ort"],
            ["Name Pfarramt", "Kaserne", "Straße, Nr.", "PLZ, Ort"],
            ["Stadt", "Straße, Nr.", "PLZ, Ort"]
        ]

        for entry in entries:
            form = QFormLayout()
            form.setContentsMargins(28,0,0,0)
            form.setSpacing(12)

            dict = {}
            for field in entry:
                input = QLineEdit()
                input.setPlaceholderText(field)
                input.setFixedWidth(350)
                dict[field] = input
                form.addRow(field, input)  # ← Label + Feld in einer Zeile

            self.f_partner.append(dict)
            card_layout.addLayout(form)

        return card

    def _basic_card(self, _title: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        card.setProperty("type","card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(50)

        title = QLabel(_title)
        title.setProperty("type", "h3")
        card_layout.addWidget(title)

        return card, card_layout

    def mousePressEvent(self, event):
        fw = QApplication.focusWidget()
        if fw:
            fw.clearFocus()
        return super().mousePressEvent(event)