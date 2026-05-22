from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QFileDialog,
    QWidget, 
)

from PySide6.QtGui import QIcon

from PySide6.QtCore import Qt, QSize
import os

class StartupDialog(QDialog):
    def __init__(self):
        super().__init__()

        #window setup
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog) #removing the native header
        self.setAttribute(Qt.WA_TranslucentBackground) #removing the initial frame background
        self.setFixedSize(480,300)

        base_frame = QVBoxLayout(self)
        base_frame.setContentsMargins(20,20,20,20)

        body = QWidget()
        body.setObjectName("start-dialogue-body")
        base_frame.addWidget(body)

        main_layout = QVBoxLayout(body)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        
        main_layout.addWidget(self._header())
        main_layout.addStretch()

    def _header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("start-dialogue-header")
        header.setFixedHeight(72)

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