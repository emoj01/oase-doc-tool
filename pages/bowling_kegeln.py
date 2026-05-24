# pages/bowling_kegeln.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QTextEdit, QLineEdit, QSpinBox, QDoubleSpinBox, QLabel, QHBoxLayout, QApplication, QComboBox
    )
from PySide6.QtCore import Qt

import yaml

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

class BowlingKegeln(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        layout.addWidget(self._info())
        
        layout.addStretch()

    def _info(self):
        card, layout = self._basic_card("Bowling / Kegeln")

        row_1 = self._new_row()
        self.f_bowling_kegeln = QComboBox()
        #popup_frame = self.f_bowling_kegeln.view().parentWidget()
        #popup_frame.setContentsMargins(0,0,0,0)
        #popup_frame.setStyleSheet(f"border: 1.5px solid {config["colors"]["border"]};")
        # popup_frame.setContentsMargins(0,0,0,0)
        # self.f_bowling_kegeln.view().setFrameShape(QFrame.NoFrame)
        # popup_frame.setFrameShape(QFrame.NoFrame)

        
        self.f_bowling_kegeln.addItems(["Bowling", "Kegeln"])
        row_1.addWidget(QLabel("Kegeln / Bowling"))
        row_1.addWidget(self.f_bowling_kegeln)
        layout.addLayout(row_1)

        row_2 = self._new_row()
        self.f_anz_bahnen = QSpinBox()
        self.f_anz_bahnen.setRange(0,99)
        row_2.addWidget(QLabel("Anz. Bahnen"))
        row_2.addWidget(self.f_anz_bahnen)
        layout.addLayout(row_2)

        row_3 = self._new_row()
        self.f_bahn_preis = QDoubleSpinBox()
        self.f_bahn_preis.setDecimals(2)
        self.f_bahn_preis.setSuffix(" €")
        row_3.addWidget(QLabel("Preis pro Bahn, Stunde"))
        row_3.addWidget(self.f_bahn_preis)
        layout.addLayout(row_3)

        row_4 = self._new_row()
        self.f_opening_hours = QLineEdit()
        self.f_opening_hours.setPlaceholderText("Öffnungszeiten")
        row_4.addWidget(QLabel("Öffnungszeiten"))
        row_4.addWidget(self.f_opening_hours)
        layout.addLayout(row_4)

        return card                

    def _new_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setContentsMargins(0,0,0,0)
        row.setSpacing(12)
        return row
    
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

