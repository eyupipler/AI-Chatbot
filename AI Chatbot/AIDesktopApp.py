from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt, QTimer, QSize, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage, QTransform, QPainter
from AIBackend import Conversation
from AISE import SEApp
import AIObjDetection
import sys
from tkinter import messagebox
import time
import datetime
import subprocess
import requests


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.conversation = Conversation()
        self.video_running = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Chatbot')
        #self.setWindowIcon(QIcon('ICON(OPTIONAL)'))
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black")

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("background-color: black; border-radius: 10; color: white")

        self.input_box = QLineEdit()
        self.input_box.setMaximumHeight(50)
        self.input_box.setMinimumHeight(50)
        self.input_box.setFocusPolicy(Qt.StrongFocus)
        self.input_box.installEventFilter(self)
        self.input_box.setStyleSheet("background-color: #BFBFBF; border-radius: 10; margin-top: 10; margin-bottom: 10")

        self.input_box.setPlaceholderText("/w [Şehir Adı / City Name]       /c [Değer / Value][Döviz Kodu / Currency Code]")

        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon('Assets/sendbutton.ico'))
        icon_size = QSize(20, 20)
        self.send_button.setIconSize(icon_size)
        self.send_button.icon().pixmap(icon_size)
        self.send_button.setToolTip('Mesaj Gönder')
        self.send_button.setStyleSheet("background-color: #000000; color: white; font-weight: bold; border-radius: 10; margin-top: 10; margin-bottom: 10; margin-right: 10")
        self.send_button.clicked.connect(self.send_message)

        self.attach_button = QPushButton()
        self.attach_button.setIcon(QIcon('Assets/attach-file.ico'))
        icon_size = QSize(20, 20)
        self.attach_button.setIconSize(icon_size)
        self.attach_button.setToolTip('PDF Yükle (Deneysel)')
        self.attach_button.setStyleSheet("background-color: #000000; color: white; font-weight: bold; border-radius: 10; margin-right: 10; margin-left: 10")
        self.attach_button.clicked.connect(self.upload_pdf)

        self.video_button = QPushButton("Video İşlemeyi Çalıştır")
        self.video_button.setIcon(QIcon('Assets/videoprocessingbutton.ico'))
        icon_size = QSize(100, 100)
        self.video_button.setIconSize(icon_size)
        self.video_button.setToolTip('Video İşlemeyi Çalıştır')
        self.video_button.setStyleSheet("background-color: #000000; color: white; font-weight: bold; border-radius: 10")
        self.video_button.clicked.connect(self.open_object_detection)

        self.log_button = QPushButton("Kayıtları Aç")
        self.log_button.setIcon(QIcon('Assets/logbutton.ico'))
        icon_size = QSize(100, 100)
        self.log_button.setIconSize(icon_size)
        self.log_button.setToolTip('Kayıtları Aç')
        self.log_button.setStyleSheet("background-color: #000000; color: white; font-weight: bold; border-radius: 10")
        self.log_button.clicked.connect(self.open_logs)

        self.run_search_button = QPushButton("Arama Motorunu Çalıştır")
        self.run_search_button.setIcon(QIcon('Assets/sebutton.ico'))
        icon_size = QSize(100, 100)
        self.run_search_button.setIconSize(icon_size)
        self.run_search_button.setToolTip('Arama Motorunu Çalıştır')
        self.run_search_button.setStyleSheet("background-color: #000000; color: white; font-weight: bold; border-radius: 10")
        self.run_search_button.clicked.connect(self.open_search_engine)

        self.run_img_processing = QPushButton("Resim İşlemeyi Çalıştır")
        self.run_img_processing.setIcon(QIcon('Assets/imgprocessing.ico'))
        icon_size = QSize(100, 100)
        self.run_img_processing.setIconSize(icon_size)
        self.run_img_processing.setToolTip('Resim İşlemeyi Çalıştır')
        self.run_img_processing.setStyleSheet("background-color: #000000; color: white; font-weight: bold; border-radius: 10")
        self.run_img_processing.clicked.connect(self.open_img_processing)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setHidden(True)

        hbox = QHBoxLayout()
        hbox.addWidget(self.input_box)
        hbox.addWidget(self.attach_button)
        hbox.addWidget(self.send_button)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.video_button)
        hbox2.addWidget(self.run_search_button)
        hbox2.addWidget(self.run_img_processing)

        vbox = QVBoxLayout()
        vbox.addWidget(self.chat_history)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.log_button)

        self.setLayout(vbox)
        self.timer = QTimer()

    def upload_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "PDF Dosyası Seç", "", "PDF Dosyaları (*.pdf);;Tüm Dosyalar (*)", options=options)
        file_dialog = self.findChild(QFileDialog)
        if file_dialog:
            file_dialog.setStyleSheet("background-color: white; color: black;")

        if file_name:
            self.conversation.send_pdf(file_name)

    @staticmethod
    def open_search_engine():
        subprocess.Popen([sys.executable, 'AISE.py'])

    @staticmethod
    def open_img_processing():
        subprocess.Popen([sys.executable, 'ImgProcessing.py'])

    @staticmethod
    def open_object_detection():
        subprocess.Popen([sys.executable, 'AIObjDetection.py'])

    def eventFilter(self, obj, event):
        if obj is self.input_box and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return:
                self.send_message()
                return True
        return super().eventFilter(obj, event)

    def send_message(self):
        message = self.input_box.text()
        self.input_box.clear()
        user_message = "You >>> " + message
        self.add_message_to_chat(user_message)

        if message.startswith("/w"):
            city = message.split(" ", 1)[1]
            city = city.replace("ı", "i").replace("İ", "i")
            weather_data = self.get_weather_data(city)
            if weather_data:
                response = f"{city} şehrinde sıcaklık {weather_data['main']['temp']}°C"
            else:
                response = "Belirtilen şehir için hava durumu verisi bulunamadı"

        elif message.startswith("/c"):
            currency = message.split(" ", 1)[1]
            currency_code = currency.upper()

            try:
                url = f"https://api.freecurrencyapi.com/API-KEY"
                response = requests.get(url)
                data = response.json()

                if not data.get('success', False):
                    raise Exception(data.get('error', {}).get('info', 'Unknown error'))
                rate = data['rates'].get(currency_code)

                if rate is None:
                    raise KeyError(f"Currency code '{currency_code}' not found")
                response = f"1 USD = {rate} {currency_code}"

            except KeyError as e:
                response = f"Geçerli bir döviz kodu girmediniz."

            except Exception as e:
                response = f"Döviz dönüşümü başarısız: API'den beklenmeyen bir hata oluştu. Lütfen daha sonra tekrar deneyin."

        else:
            response = self.conversation.send_message(message)

        bot_message = "Chatbot >>> " + response + "\n"
        self.add_message_to_chat(bot_message)

        self.log_message(user_message)
        self.log_message(bot_message)

    def get_weather_data(self, city):
        api_key = 'OPENWEATHER/API-KEY'
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'main' in data and 'temp' in data['main'] and 'weather' in data and len(
                    data['weather']) > 0 and 'description' in data['weather'][0]:
                return data
            else:
                return None
        else:
            return None

    def add_message_to_chat(self, message):
        current_text = self.chat_history.toPlainText()
        message_with_timestamp = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message} "
        self.chat_history.setPlainText(current_text + message_with_timestamp + "\n")

        scrollbar = self.chat_history.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    @staticmethod
    def log_message(message):
        with open('Logs/chat_logs.txt', 'a') as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | " + message + "\n")

    @staticmethod
    def open_logs():
        subprocess.Popen(r'explorer /open,"Logs"')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    font = QFont("Arial", 12)
    app.setFont(font)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec_())
