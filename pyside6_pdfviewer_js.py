import os
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QMenuBar, QMenu, QFileDialog)
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.pdf_js_path = os.path.join(script_directory, "PDF_js", "web", "viewer.html").replace('\\', '/')
        self.pdf_path = ""
        self.current_page = 1

        menu_bar = QMenuBar(self)
        file_menu = QMenu("Choose PDF", self)
        open_action = QAction("Open PDF...", self)
        open_action.triggered.connect(self.open_pdf)
        file_menu.addAction(open_action)
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)

        central_widget = QWidget(self)
        self.viewer_widget = QWebEngineView()

        self.next_button = QPushButton("Next Page")
        self.next_button.clicked.connect(self.next_page)

        self.prev_button = QPushButton("Previous Page")
        self.prev_button.clicked.connect(self.prev_page)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.next_button)
        buttons_widget.setLayout(buttons_layout)
        buttons_widget.setFixedHeight(50)

        layout = QVBoxLayout()
        layout.addWidget(self.viewer_widget)
        layout.addWidget(buttons_widget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.resize(800, 1024)

    def open_pdf(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_name:
            self.pdf_path = file_name.replace('\\', '/')
            self.viewer_widget.load(QUrl.fromUserInput(f'file:///{self.pdf_js_path}?file=file:///{self.pdf_path}#page={self.current_page}'))

    def next_page(self):
        self.current_page += 1
        self.viewer_widget.load(QUrl.fromUserInput(f'file:///{self.pdf_js_path}?file=file:///{self.pdf_path}#page={self.current_page}'))

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.viewer_widget.load(QUrl.fromUserInput(f'file:///{self.pdf_js_path}?file=file:///{self.pdf_path}#page={self.current_page}'))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    viewer = PDFViewer()
    viewer.show()

    sys.exit(app.exec())
