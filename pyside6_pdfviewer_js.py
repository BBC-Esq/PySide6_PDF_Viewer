import os
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QMenuBar, QMenu, QFileDialog)
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class PDFViewer(QMainWindow):import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMenuBar, QMenu, QFileDialog, QTreeView, QSplitter, QLabel, QSizePolicy
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem, QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, Qt, QDir

class PDFFileSystemModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalHeaderLabels(["PDF Files and Folders"])
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.current_path = self.root_path
        self.populate_model(self.invisibleRootItem(), self.current_path)
        
    def populate_model(self, parent_item, directory_path):
        parent_item.removeRows(0, parent_item.rowCount())
        directory = QDir(directory_path)
        up_item = QStandardItem("")
        up_item.setData(os.path.dirname(directory_path), Qt.UserRole)
        up_item.setIcon(QIcon.fromTheme("go-up"))
        parent_item.appendRow(up_item)
        directories = directory.entryInfoList(QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot, QDir.SortFlag.Name)
        for dir_info in directories:
            dir_item = QStandardItem(dir_info.fileName())
            dir_item.setData(dir_info.filePath(), Qt.UserRole)
            dir_item.setIcon(QIcon.fromTheme("folder"))
            parent_item.appendRow(dir_item)
            placeholder = QStandardItem("Loading...")
            dir_item.appendRow(placeholder)
        pdf_files = directory.entryInfoList(["*.pdf"], QDir.Filter.Files, QDir.SortFlag.Name)
        for file_info in pdf_files:
            file_item = QStandardItem(file_info.fileName())
            file_item.setData(file_info.filePath(), Qt.UserRole)
            file_item.setIcon(QIcon.fromTheme("application-pdf"))
            parent_item.appendRow(file_item)
    
    def navigate_to(self, path):
        self.current_path = path
        self.populate_model(self.invisibleRootItem(), path)

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
        self.main_layout = QVBoxLayout(central_widget)
        self.path_label = QLabel()
        self.tree_model = PDFFileSystemModel()
        self.path_label.setText(self.tree_model.current_path)
        self.path_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.path_label)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_layout.addWidget(self.splitter)
        self.nav_widget = QWidget()
        self.nav_layout = QVBoxLayout(self.nav_widget)
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.clicked.connect(self.on_tree_clicked)
        self.tree_view.expanded.connect(self.on_tree_expanded)
        self.nav_layout.addWidget(self.tree_view)
        self.splitter.addWidget(self.nav_widget)
        self.viewer_widget = QWidget()
        self.viewer_layout = QVBoxLayout(self.viewer_widget)
        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PluginsEnabled, True)
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PdfViewerEnabled, True)
        self.viewer_layout.addWidget(self.webView)
        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)
        self.prev_button = QPushButton("Previous Page")
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button = QPushButton("Next Page")
        self.next_button.clicked.connect(self.next_page)
        self.buttons_layout.addWidget(self.prev_button)
        self.buttons_layout.addWidget(self.next_button)
        self.buttons_widget.setFixedHeight(50)
        self.viewer_layout.addWidget(self.buttons_widget)
        self.splitter.addWidget(self.viewer_widget)
        self.splitter.setSizes([250, 550])
        self.setCentralWidget(central_widget)
        self.resize(800, 1024)
        
    def on_tree_clicked(self, index):
        item = self.tree_model.itemFromIndex(index)
        file_path = item.data(Qt.UserRole)
        if item.text() == "":
            self.tree_model.navigate_to(file_path)
            self.path_label.setText(file_path)
            return
        if os.path.isdir(file_path):
            self.tree_model.navigate_to(file_path)
            self.path_label.setText(file_path)
            return
        if file_path and file_path.lower().endswith('.pdf'):
            self.pdf_path = file_path
            self.current_page = 1
            self.path_label.setText(file_path)
            self.load_pdf()
            
    def on_tree_expanded(self, index):
        item = self.tree_model.itemFromIndex(index)
        file_path = item.data(Qt.UserRole)
        if item.rowCount() == 1 and item.child(0).text() == "Loading...":
            item.removeRow(0)
            self.tree_model.populate_model(item, file_path)
            
    def open_pdf(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)")
        if filename:
            self.pdf_path = filename.replace('\\', '/')
            self.current_page = 1
            self.path_label.setText(self.pdf_path)
            self.load_pdf()
            
    def load_pdf(self):
        self.webView.load(QUrl.fromUserInput(f'file:///{self.pdf_js_path}?file=file:///{self.pdf_path}#page={self.current_page}'))
        
    def next_page(self):
        self.current_page += 1
        self.load_pdf()
        
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_pdf()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec())

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
