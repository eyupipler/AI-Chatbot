import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextBrowser, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer, QSize
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from tkinter import messagebox

class SEApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Neurazum Search Engine')
        self.setWindowIcon(QIcon('Assets/neurazumicon.ico'))
        self.resize(800, 600)

        self.query_label = QLabel('Aramak istediğiniz şeyi yazın:')
        self.query_input = QLineEdit()
        self.query_input.setMaximumHeight(30)
        self.query_input.setStyleSheet("border-radius: 10")

        self.search_button = QPushButton()
        self.search_button.setIcon(QIcon('Assets/search.ico'))
        self.search_button.setIconSize(QtCore.QSize(50, 50))
        self.search_button.setStyleSheet("background-color: transparent; border: none; color: white")
        self.search_button.setToolTip('Ara')

        self.result_browser = QTextBrowser()
        self.result_browser.setStyleSheet("border-radius: 10; border: none; background-color: transparent;")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.query_input)
        self.layout.addWidget(self.search_button)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.query_label)
        self.vertical_layout.addLayout(self.layout)
        self.vertical_layout.addWidget(self.result_browser)

        self.setLayout(self.vertical_layout)

        self.search_button.clicked.connect(self.search_google)
        self.query_input.returnPressed.connect(self.search_google)
        self.result_browser.anchorClicked.connect(self.open_link)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def search_google(self):
        query = self.query_input.text()

        with open('Logs/search_logs.txt', 'a') as f:
            f.write(f"{datetime.now()} - {query}\n")

        self.result_browser.setHtml("<h4>Aranıyor...</h4>")
        QApplication.processEvents()

        search_results = search(query, num_results=10, lang="tr")
        results_text = ""
        for i, result in enumerate(search_results, 1):
            try:
                response = requests.get(result)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.title.string
                summary = soup.find("meta", {"name": "description"})
                summary_content = summary["content"] if summary else ""
                results_text += f"{i} >>> {title}\n{summary_content}\n<a href='{result}'>{result}</a><br><br>"

            except requests.HTTPError as e:
                print(f"Hata: {e}")
            except Exception as e:
                print(f"Hata: {e}")
            finally:
                if 'results_text' not in locals():
                    results_text = ""

        if results_text:
            with open('Logs/results_logs.txt', 'a') as f:
                f.write(f"{datetime.now()} - {query}\n{results_text}\n\n")

            self.result_browser.setHtml(results_text)
        else:
            messagebox.showwarning("Hata", "Arama Motoru Yanıt Vermedi")

        # Veriyi topla ve dosyaya kaydet
        with open('Logs/MLLogs/ml_logs.txt', 'a') as f:
            f.write(f"{datetime.now()} - {query}\n")

    def open_link(self, link):
        QDesktopServices.openUrl(QUrl(link))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    font = QFont("Arial", 10)
    app.setFont(font)
    window = SEApp()
    window.show()
    sys.exit(app.exec_())
