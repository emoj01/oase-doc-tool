# PySide6 imports
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QLineEdit, QStackedWidget, QPushButton
)
from PySide6.QtGui import QIcon

from PySide6.QtCore import Qt, QSize

# Loading the config file
import yaml
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Importing pages
from pages.allgemeines import AllgemeinPage
from pages.startseite import Startseite
from pages.feiern_tagen import FeiernTagen
from pages.uebernachten import Uebernachten
from pages.bowling_kegeln import BowlingKegeln
from pages.partner import Partner
from pages.ansprechpartner import Ansprechpartner

# The main app
class OaseApp(QMainWindow):
    def __init__(self, house_name):
        # setting the window properties
        super().__init__()
        self.setWindowTitle(config["app"]["title"])
        self.resize(config["app"]["window"]["size"]["width"],
                    config["app"]["window"]["size"]["height"])
        self.setMinimumSize(config["app"]["window"]["min_size"]["width"],
                            config["app"]["window"]["min_size"]["height"])
        self.setCentralWidget(QLabel("Hallo OASE!"))

        self.house_name = str.replace(house_name, ".json", "")
        self.house_name = str.replace(self.house_name, "_", " ")

        # Main Widget
        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        root.setLayout(main_layout)

        # Adding Header and Body
        main_layout.addWidget(self._header())
        main_layout.addLayout(self._body(), stretch=1)

        self._switch_page(0)

    # function to build a header widget
    def _header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(64)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(28,0,28, 0)

        title = QLabel("OASE – " + self.house_name)
        layout.addWidget(title)

        # house_name = QLineEdit()
        # house_name.setPlaceholderText("Bezeichnung d. OASE (z.B. \"Haus Adelheide\")") 
        # layout.addWidget(house_name)

        layout.addStretch() # moving content to the left
        save_btn = QPushButton()
        save_btn.setObjectName("save-btn")
        save_btn.setFlat(True)
        save_btn.setIcon(QIcon("assets/icons/save_white.svg"))
        save_btn.setToolTip("Eingaben speichern..")
        save_btn.setIconSize(QSize(24,24))
        layout.addWidget(save_btn)

        gen_doc_btn = QPushButton()
        gen_doc_btn.setObjectName("gen-doc-btn")
        gen_doc_btn.setFlat(True)
        gen_doc_btn.setIcon(QIcon("assets/icons/generate_doc_white.svg"))
        gen_doc_btn.setToolTip("Dokument generieren..")
        gen_doc_btn.setIconSize(QSize(24,24))
        layout.addWidget(gen_doc_btn)

        header.setLayout(layout)

        return header

    def _body(self) -> QHBoxLayout:
        body = QHBoxLayout()
        body.setObjectName("body")
        body.setContentsMargins(0,0,0,0)
        body.setSpacing(0)

        main_content = self._main_content()

        body.addWidget(self._sidebar())
        body.addWidget(main_content)

        return body
    
    def _sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12,20,12,20)
        layout.setSpacing(4)

        # navigtion header
        nav_label = QLabel("SEITEN")
        nav_label.setObjectName("navbar-header")
        layout.addWidget(nav_label)

        self.nav_buttons = []

        # pages
        pages = [
            ("🏠  Allgemeines", AllgemeinPage()),
            ("🎬  Startseite", Startseite()),
            ("🎉  Feiern & Tagen", FeiernTagen()),
            ("🛏  Übernachten", Uebernachten()),
            ("🎳  Bowling & Kegeln", BowlingKegeln()),
            ("🤝  Partner", Partner()),
            ("👤  Ansprechpartner", Ansprechpartner())
                  ]
        for i, (label, page) in enumerate(pages):
            self.stacked.addWidget(page)
            btn = QPushButton(label)
            btn.setProperty("type", "nav")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx = i: self._switch_page(idx))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)

        layout.addStretch()
        sidebar.setLayout(layout)

        return sidebar

    def _main_content(self) ->QStackedWidget:
        self.stacked = QStackedWidget()
        self.stacked.setObjectName("main-content")

        return self.stacked
    
    def _switch_page(self, index: int):
        self.stacked.setCurrentIndex(index)

        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
