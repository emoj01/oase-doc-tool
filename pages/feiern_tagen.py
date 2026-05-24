# pages/feiern_tagen.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QTextEdit, QSpinBox, QLabel, QHBoxLayout, QApplication
    )
from PySide6.QtCore import Qt

class FeiernTagen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        layout.addWidget(self._facilities())
        layout.addWidget(self._facilities_description())

    def _facilities(self) -> QFrame:
        card, card_layout = self._basic_card("Räumlichkeiten")
        inner_layout = QHBoxLayout()
        inner_layout.setContentsMargins(0,0,0,0)
        inner_layout.setSpacing(20)

        # Amount of rooms
        self.f_n_rooms = QSpinBox()
        self.f_n_rooms.setRange(0,99)
        self.f_n_rooms.setValue(3)

        # Total capacity
        self.f_room_capacity = QSpinBox()
        self.f_room_capacity.setRange(0,9999)
        self.f_room_capacity.setValue(200)

        inner_layout.addWidget(QLabel("Anzahl Veranstaltungsräume"))
        inner_layout.addWidget(self.f_n_rooms, alignment=Qt.AlignLeft)
        inner_layout.addStretch()
        inner_layout.addWidget(QLabel("Raumkapazität (gesamt)"))
        inner_layout.addWidget(self.f_room_capacity, alignment=Qt.AlignLeft)

        card_layout.addLayout(inner_layout)

        return card

    def _facilities_description(self):
        card, layout = self._basic_card("Beschreibung")
        self.f_desc = QTextEdit()
        self.f_desc.setPlaceholderText("Text zu den Räumlichkeiten...")
        layout.addWidget(self.f_desc)

        return card

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

