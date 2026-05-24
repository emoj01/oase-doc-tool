# pages/allgemein.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QFrame, QLabel, QLineEdit, QScrollArea, QPushButton
)
from PySide6.QtCore import Qt

class AllgemeinPage(QWidget):
    def __init__(self):
        super().__init__()

        # Content Wrapper
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0,0,0,0)

        # Adding a Scroll Widget
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        outer.addWidget(scroll)

        # Content Widget, which will get scrolled
        content = QWidget()
        content.setProperty("type", "bg-light")
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        # Address and Contact
        first_row = QHBoxLayout()
        first_row.setSpacing(20)
        first_row.addWidget(self._address_card())
        first_row.addWidget(self._contact_card())
        layout.addLayout(first_row)

        # Opening Hours
        layout.addWidget(self._opening_hours_card())

        layout.addStretch()

    # | Cards |__________________________________________________________________________
    def _make_card(self, title: str) -> tuple[QFrame, QFormLayout]:
        card = QFrame()
        card.setProperty("type", "card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Card Header
        _title = QLabel(title.upper())
        _title.setProperty("type", "h3")
        layout.addWidget(_title)

        form = QFormLayout()
        form.setSpacing(10)
        layout.addLayout(form)
        layout.addStretch()

        return card, form

    
    def _address_card(self) -> QFrame:
        card, form = self._make_card("Addresse")
        
        self.f_street = QLineEdit()
        self.f_street.setPlaceholderText("Straße")
        self.f_h_number = QLineEdit()
        self.f_h_number.setPlaceholderText("Hausnummer")
        self.f_zip = QLineEdit()
        self.f_zip.setPlaceholderText("Postleitzahl")
        self.f_city = QLineEdit()
        self.f_city.setPlaceholderText("Stadt")

        form.addRow("Straße", self.f_street)
        form.addRow("Hausnummer", self.f_h_number)
        form.addRow("Postleitzahl", self.f_zip)
        form.addRow("Stadt", self.f_city)

        return card

    def _contact_card(self) -> QFrame:
        card, form = self._make_card("Kontakt")

        self.f_phone = QLineEdit()
        self.f_phone.setPlaceholderText("Telefon")
        self.f_fax = QLineEdit()
        self.f_fax.setPlaceholderText("Fax")
        self.f_mail = QLineEdit()
        self.f_mail.setPlaceholderText("E-Mail")

        form.addRow("Telefon", self.f_phone)
        form.addRow("Fax", self.f_fax)
        form.addRow("E-Mail", self.f_mail)

        return card

    def _opening_hours_card(self) -> QFrame:
        card = QFrame()
        card.setProperty("type","card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        _title = QLabel("ÖFFNUNGSZEITEN")
        _title.setProperty("type", "h3")
        layout.addWidget(_title)

        self.oh_layout = QVBoxLayout()
        self.oh_layout.setSpacing(8)
        layout.addLayout(self.oh_layout)

        # First row
        self._add_oh_entry()

        # Add row button
        add_btn = QPushButton("+ Zeile hinzufügen")
        add_btn.setObjectName("add-btn")
        add_btn.clicked.connect(lambda: self._add_oh_entry())
        layout.addWidget(add_btn, alignment=Qt.AlignLeft)

        return card

    def _add_oh_entry(self, days_text: str ="", time_text: str =""):
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(8)

        days = QLineEdit()
        days.setPlaceholderText("z.B. Mo-Fr")
        days.setText(days_text)
        time = QLineEdit()
        time.setPlaceholderText("z.B. 08:00-20:00")
        time.setText(time_text)

        remove_btn = QPushButton("×")
        remove_btn.setObjectName("remove-btn")
        remove_btn.setFixedSize(32,32)
        remove_btn.clicked.connect(lambda: self._remove_oh_entry(row_widget))

        # adding all the elements
        row_layout.addWidget(QLabel("Tage"))
        row_layout.addWidget(days, stretch=2)
        row_layout.addWidget(QLabel("Zeit"))
        row_layout.addWidget(time, stretch=2)
        row_layout.addWidget(remove_btn)

        self.oh_layout.addWidget(row_widget)

    def _remove_oh_entry(self, row_widget: QWidget):
        self.oh_layout.removeWidget(row_widget)
        row_widget.deleteLater()

    def get_data(self) -> dict:
        opening_hours = []
        for i in range(self.oh_layout.count()):
            row_widget = self.oh_layout.itemAt(i).widget()
            row_layout = row_widget.layout()
            
            # Index 1 = days QLineEdit, Index 3 = time QLineEdit
            days = row_layout.itemAt(1).widget().text()
            time = row_layout.itemAt(3).widget().text()

            opening_hours.append((days,time))

        return {
            "Straße": self.f_street.text(),
            "Hausnummer": self.f_h_number.text(),
            "PLZ": self.f_zip.text(),
            "Stadt": self.f_city.text(),
            "Telefon": self.f_phone.text(),
            "Fax": self.f_fax.text(),
            "E-Mail": self.f_mail.text(),
            "Öffnungszeiten": opening_hours
        }

    def set_data(self, data: dict):
        self._clear_oh_entries()
        
        self.f_street.setText(data.get("Straße",""))
        self.f_h_number.setText(data.get("Hausnummer",""))
        self.f_zip.setText(data.get("PLZ",""))
        self.f_city.setText(data.get("Stadt",""))
        self.f_phone.setText(data.get("Telefon",""))
        self.f_fax.setText(data.get("Fax",""))
        self.f_mail.setText(data.get("E-Mail",""))

        for entry in data.get("Öffnungszeiten", []):
            self._add_oh_entry(days_text=entry[0], time_text=entry[1])

    def _clear_oh_entries(self):
        while self.oh_layout.count():
            item = self.oh_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

    


        