# pages/uebernachten.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QFormLayout,
    QTextEdit, QLineEdit, QSpinBox, QDoubleSpinBox, QLabel, QHBoxLayout, QApplication, QScrollArea
    )
from PySide6.QtCore import Qt

class Uebernachten(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0,0,0,0)
        top_row.setSpacing(20)

        top_row.addWidget(self._room_info())
        top_row.addWidget(self._breakfast_info())

        layout.addLayout(top_row)
        layout.addWidget(self._description())
        


    def _room_info(self):
        room_info_card, room_info_layout = self._basic_card("Zimmer")

        self.f_zimmer = {}

        form = QFormLayout()
        form.setSpacing(12)

        room_info = ["Anzahl Einzel", "Preis Einzel", "Preis Einzel als Doppel", "Anzahl Doppel", "Preis Doppel"]

        for info in room_info:
            if "Anzahl" in info:
                field = QSpinBox()
                field.setRange(0, 999)
            else:
                field = QDoubleSpinBox()
                field.setDecimals(2)
                field.setRange(0, 9999)
                field.setSuffix(" €")

            self.f_zimmer[info] = field
            form.addRow(info, field)

        room_info_layout.addLayout(form)
        return room_info_card
    
    def _breakfast_info(self):
        card, layout = self._basic_card("Frühstück")
        info = ["Zeiten Frühstück", "Preis Frühstück"]

        row_1 = QHBoxLayout()
        label_1 = QLabel(info[0])
        self.f_fruehstueck_zeiten = QLineEdit()
        self.f_fruehstueck_zeiten.setPlaceholderText(info[0])
        row_1.addWidget(label_1)
        row_1.addWidget(self.f_fruehstueck_zeiten)

        row_2 = QHBoxLayout()
        label_2 = QLabel(info[1])
        self.f_fruehstueck_preis = QDoubleSpinBox()
        self.f_fruehstueck_preis.setRange(0,999)
        self.f_fruehstueck_preis.setDecimals(2)
        self.f_fruehstueck_preis.setSuffix(" €")
        row_2.addWidget(label_2)
        row_2.addWidget(self.f_fruehstueck_preis)

        layout.addLayout(row_1)
        layout.addLayout(row_2)
        layout.addStretch()

        return(card)
    
    def _description(self):
        desc_card, desc_layout = self._basic_card("Zimmerbeschreibung")
        self.f_beschreibung = QTextEdit()
        desc_layout.addWidget(QLabel("Text zu den Zimmern"))
        desc_layout.addWidget(self.f_beschreibung)

        return desc_card

    def _basic_card(self, _title: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        card.setProperty("type","card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)

        title = QLabel(_title)
        title.setProperty("type", "h3")
        card_layout.addWidget(title)

        return card, card_layout
    
    def mousePressEvent(self, event):
        fw = QApplication.focusWidget()

        if fw:
            fw.clearFocus()
        return super().mousePressEvent(event)

