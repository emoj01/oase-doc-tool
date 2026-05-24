from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QFormLayout,
    QWidget, QStackedWidget, QApplication, QMessageBox
)

from PySide6.QtGui import QIcon, QPixmap

from PySide6.QtCore import Qt, QSize
import os
from pathlib import Path

import json

class StartupDialog(QDialog):
    def __init__(self):
        super().__init__()

        #window setup
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog) #removing the native header
        self.setAttribute(Qt.WA_TranslucentBackground) #removing the initial frame background
        self.setFixedSize(440,320)

        self.main = self._main()

        base_frame = QVBoxLayout(self)
        base_frame.setContentsMargins(20,20,20,20)

        wrapper = QWidget()
        wrapper.setObjectName("start-dialogue-wrapper")
        base_frame.addWidget(wrapper)

        main_layout = QVBoxLayout(wrapper)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        
        main_layout.addWidget(self._header())
        main_layout.addWidget(self._main())
        main_layout.addStretch()

        self.main.addWidget(self._initial_page())
        self.main.addWidget(self._start_new())
        self.main.addWidget(self._load_file_page())
        self._switch_page(0)

    def _header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("start-dialogue-header")
        header.setFixedHeight(64)

        layout = QHBoxLayout(header)

        # window title and subtitle
        title_layout = QVBoxLayout() 
        title_layout.setContentsMargins(12,0,0,0)
        title_layout.setSpacing(0)       
        title = QLabel("OASE")
        title.setProperty("type", "h1")
        title_layout.addWidget(title)

        subtitle = QLabel("Info-Tool")
        subtitle.setProperty("type", "text-muted")
        title_layout.addWidget(subtitle)
        title_layout.addStretch()

        #close button
        btn_close = QPushButton()
        btn_close.setObjectName("start-dialogue-btn-close")
        btn_close.setFlat(True)
        btn_close.setIcon(QIcon("assets/icons/close.svg"))
        btn_close.setIconSize(QSize(18,18))
        btn_close.clicked.connect(self.reject)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addWidget(btn_close, alignment=Qt.AlignTop)

        return header

    def _main(self) -> QStackedWidget:

        self.main = QStackedWidget()
        self.main.setObjectName("startup-dialogue-main")

        return self.main
    
    def _initial_page(self) -> QFrame:
        content = QFrame()
        content.setObjectName("start-dialogue-initial-page")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(32,32,32,32)
        layout.setSpacing(24)

        # First div
        paragraph = QVBoxLayout()
        paragraph.setSpacing(0)
        q1 = QLabel("Wie möchtest du fortfahren?")
        q1.setProperty("type", "h1")
        paragraph.addWidget(q1, alignment=Qt.AlignCenter)

        subtitle = QLabel("Wähle eine Option zum Fortfahren")
        subtitle.setProperty("type", "text-muted")
        paragraph.addWidget(subtitle, alignment=Qt.AlignCenter)

        # Second div
        choices_container = QHBoxLayout()

        choice_1= self._choice_card(1,"assets/icons/file-plus.svg", "Neue Datei", "Von vorne Beginnen")
        choice_2 = self._choice_card(2,"assets/icons/folder-open.svg", "Datei laden", "Gespeicherte Datei öffnen")

        choices_container.addWidget(choice_1, alignment=Qt.AlignCenter)
        choices_container.addWidget(choice_2, alignment=Qt.AlignCenter)

        layout.addLayout(paragraph)
        layout.addLayout(choices_container)

        return content
    
    def _start_new(self) -> QFrame:
        content = QFrame()
        content.setObjectName("start-dialogue-start-new")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32,32,32,32)
        layout.setSpacing(24)
        label = QLabel("Für welche OASE möchtest du ein neues Dokument anlegen?")
        label.setWordWrap(True)
        layout.addWidget(label)

        self.f_oase_new_name = QLineEdit()
        self.f_oase_new_name.setPlaceholderText("Name des Hauses (z.B. Haus Adelheide)")
        form = QFormLayout()
        form.setSpacing(10)
        form.addRow("OASE – ", self.f_oase_new_name)
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        generate_btn = self._icon_button("assets/icons/file-plus-corner.svg",
                                        (120,32),(20,20),
                                        "start-dialogue-btn-green",
                                        "Dokument anlegen!",
                                        lambda: self._generate_new_file(self.f_oase_new_name.text()))
        go_back_btn = self._icon_button("assets/icons/undo.svg",
                                        (120,32),(20,20),
                                        "start-dialogue-btn-red",
                                        "Abbrechen",
                                        lambda: self._switch_page(0))
        
        btn_layout.addWidget(generate_btn)
        btn_layout.addWidget(go_back_btn)
        layout.addLayout(btn_layout)

        return content

    
    def _choice_card(self, page_idx, icon_path, _title, _subtitle) -> QFrame:
        card = QPushButton()
        card.setCursor(Qt.PointingHandCursor)
        card.setObjectName("start-dialogue-choice-card")
        card.setFlat(True)
        card.setMinimumSize(160, 100)
        card.clicked.connect(lambda: self._switch_page(page_idx) )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(8,12,8,12)
        
        # icon
        icon_frame = QLabel()
        icon = QIcon(icon_path)
        icon_frame.setPixmap(icon.pixmap(32,32))

        # title,subtitle
        title = QLabel(_title)
        title.setProperty("type", "h2")
        subtitle = QLabel(_subtitle)

        layout.addWidget(icon_frame, alignment=Qt.AlignCenter)
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        return card
    
    def _switch_page(self, index: int):
        self.main.setCurrentIndex(index)

    def mousePressEvent(self, event):
        fw = QApplication.focusWidget()
        if fw:
            fw.clearFocus()
        return super().mousePressEvent(event)
    
    def _generate_new_file(self,name: str):
        content = {}
        name = str.replace(str.strip(name), " ", "_") +".json"

        dir = Path("data")
        dir.mkdir(parents=True, exist_ok=True)

        file_path = dir / name 

        if file_path.exists():
            QMessageBox.warning(self, "Fehler", "Dateiname existiert schon.")
        else:
            with open(file_path,"w", encoding="utf-8") as f:
                json.dump(content,f, indent=4,ensure_ascii=False)

            QMessageBox.information(self, "Erfolg", "Datei erfolgreich angelegt.")
            self.result = name
            self.accept()

    def _load_file_page(self):
        content = QFrame()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32,32,32,32)
        layout.setSpacing(24)
        files = self._list_existing()
        if files:
            btn_layout = QVBoxLayout()
            layout.setSpacing(0)
            for file in files:
                file_path = str.replace(file, " ", "_") +".json"
                btn = QPushButton(file)
                btn.setFlat(True)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setProperty("type", "load-list-btn")
                btn.clicked.connect(lambda checked, fp=file_path: self._load_file(fp))
                btn_layout.addWidget(btn)
            layout.addLayout(btn_layout)
        else:
            layout.addWidget(QLabel("Keine gespeicherten Einträge."), alignment=Qt.AlignCenter)
        go_back_btn = self._icon_button("assets/icons/undo.svg",
                                        (120,32),(20,20),
                                        "start-dialogue-btn-red",
                                        "Abbrechen",
                                        lambda: self._switch_page(0))
        layout.addWidget(go_back_btn, alignment=Qt.AlignCenter)
        return content
            

    def _list_existing(self, directory="data"):
        dir_path = Path.cwd() / directory

        try:
            return [str.replace(str.replace(f.name, "_", " "),".json", "") for f in dir_path.iterdir() if f.is_file()]

        except FileNotFoundError:
            print("Error: Ordner nicht gefunden.")
            return []

        except Exception as e:
            print(f"Fehler: {e}")
            return []
        
    def _icon_button(
        self,
        icon_path: str,
        btn_size: tuple[int, int] = (120, 32),
        icon_size: tuple[int, int] = (20, 20),
        button_type=None,
        btn_tooltip: str = "",
        func=None
    ) -> QPushButton:

        btn = QPushButton()
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedSize(QSize(*btn_size))

        if button_type:
            btn.setProperty("type", button_type)

        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(*icon_size))

        btn.setToolTip(btn_tooltip)

        if func:
            btn.clicked.connect(func)

        return btn
    
    def _load_file(self, file_path):
        self.result = file_path
        self.accept()

    

