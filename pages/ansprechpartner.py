# pages/ansprechpartner.py

from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QApplication, QFormLayout, QLineEdit


class Ansprechpartner(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        layout.addWidget(self._partner())
        layout.addStretch()

    def _partner(self):
        card, layout = self._basic_card("Ansprechpartner")

        entries = ["Name Ansprechpartner", "Funktion", "Mail", "Ansprechpartner"]
        form = QFormLayout()
        form.setContentsMargins(28,0,0,0)
        form.setSpacing(12)
        layout.addLayout(form)

        self.f_partner = {}
        for entry in entries:
            input = QLineEdit()
            if entry == "Funktion":
                input.setPlaceholderText(entry + " (z.B. Geschäftsführer)")
            else:
                input.setPlaceholderText(entry)
            input.setFixedWidth(350)
            self.f_partner[entry] = input
            form.addRow(QLabel(entry), input)

        return card

    def _basic_card(self, _title: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        card.setProperty("type","card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(20)

        title = QLabel(_title)
        title.setProperty("type", "h3")
        card_layout.addWidget(title)

        return card, card_layout

    def mousePressEvent(self, event):
        fw = QApplication.focusWidget()
        if fw:
            fw.clearFocus()
        return super().mousePressEvent(event)
    
    def get_data(self) -> dict:
        return {
            key: val.text() for key, val in self.f_partner.items()
        }
    
    def set_data(self, data):
        for key, val in data.items():
            if key in self.f_partner:
                self.f_partner[key].setText(val)