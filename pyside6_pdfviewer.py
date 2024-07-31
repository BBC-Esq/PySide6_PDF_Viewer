from PySide6.QtCore import QUrl, Qt, QSettings
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QFileDialog, QPushButton, QMenu
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
import os

class SearchLineEdit(QLineEdit):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Return:
            self.main_window.search_text(self.text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(0, 28, 1000, 750)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PluginsEnabled, True)
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PdfViewerEnabled, True)
        self.layout.addWidget(self.webView)
        
        self.search_input = SearchLineEdit(self)
        self.search_input.setPlaceholderText("Enter text to search...")
        self.layout.addWidget(self.search_input)

        self.settings = QSettings("MyCompany", "PDFViewer")
        self.recent_files = self.settings.value("recentFiles", [])
        
        self.create_file_menu()

    def create_file_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        self.recent_menu = QMenu('Recent Files', self)
        file_menu.addMenu(self.recent_menu)
        self.update_recent_files_menu()

    def update_recent_files_menu(self):
        self.recent_menu.clear()
        for file in self.recent_files:
            action = QAction(os.path.basename(file), self)
            action.setData(file)
            action.triggered.connect(self.open_recent_file)
            self.recent_menu.addAction(action)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if filename:
            self.load_file(filename)

    def load_file(self, filename):
        self.webView.setUrl(QUrl("file:///" + filename.replace('\\', '/')))
        self.add_to_recent_files(filename)

    def add_to_recent_files(self, filename):
        if filename in self.recent_files:
            self.recent_files.remove(filename)
        self.recent_files.insert(0, filename)
        self.recent_files = self.recent_files[:5]  # Keep only 5 recent files
        self.settings.setValue("recentFiles", self.recent_files)
        self.update_recent_files_menu()

    def open_recent_file(self):
        action = self.sender()
        if action:
            self.load_file(action.data())

    def search_text(self, text):
        flag = QWebEnginePage.FindFlag.FindCaseSensitively
        if text:
            self.webView.page().findText(text, flag)
        else:
            self.webView.page().stopFinding()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


# Works - tested on txt, htm/html, images, svg, pdf, and mp3