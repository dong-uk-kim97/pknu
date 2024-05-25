import os
import socket
import subprocess
from ftplib import FTP
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QVBoxLayout, QPushButton, QComboBox, QLabel
from PyQt5.QtCore import QThread, pyqtSignal


class FTPSender(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FTP Sender")
        self.resize(1920, 1080)

        self.ftp = FTP()
        self.selected_folder_signal = pyqtSignal(str)

        layout = QVBoxLayout()

        self.select_button = QPushButton("Select Folder")
        self.select_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_button)

        self.folder_combobox = QComboBox()
        layout.addWidget(QLabel("Choose yolov5 folder:"))
        layout.addWidget(self.folder_combobox)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_folder)
        layout.addWidget(self.send_button)

        self.run_detect_button = QPushButton("Run detect.py")
        self.run_detect_button.clicked.connect(self.run_detect)
        layout.addWidget(self.run_detect_button)

        self.setLayout(layout)
        self.read_current_directory()

    def read_current_directory(self):
        current_directory = os.getcwd()
        folders = [folder for folder in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, folder))]
        self.folder_combobox.addItems(folders)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_path = folder_path
            self.send_button.setEnabled(True)
            self.run_detect_button.setEnabled(True)
            self.selected_folder_signal.emit(folder_path)

    def send_folder(self):
        try:
            self.ftp.connect("your_ftp_host", "your_ftp_port")
            self.ftp.login("your_ftp_username", "your_ftp_password")
            self.ftp.cwd("/")  # 서버의 루트 디렉토리로 이동
            self.send_files_in_folder(self.folder_path)
            self.ftp.quit()
        except Exception as e:
            print(f"Error: {e}")

    def send_files_in_folder(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            self.ftp.cwd(os.path.basename(root))  # 서버의 현재 디렉토리로 이동
            for file in files:
                file_path = os.path.join(root, file)
                self.ftp.storbinary(f"STOR {file}", open(file_path, "rb"), 1024)
                print(f"{file} sent successfully")
            for dir in dirs:
                self.ftp.mkd(dir)  # 서버에 디렉토리 생성
                self.send_files_in_folder(os.path.join(root, dir))
            self.ftp.cwd("..")  # 상위 디렉토리로 이동

    def run_detect(self):
        self.detect_thread = DetectThread(self.folder_path)
        self.detect_thread.start()


class SendSelectedFolderThread(QThread):
    def __init__(self, selected_folder_signal):
        super().__init__()
        self.selected_folder_signal = selected_folder_signal
        self.selected_folder_signal.connect(self.send_selected_folder)

    def send_selected_folder(self, folder_path):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("localhost", 12345))
            sock.sendall(folder_path.encode())
            sock.close()
        except Exception as e:
            print(f"Error: {e}")


class DetectThread(QThread):
    progress_signal = pyqtSignal(str)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        try:
            subprocess.run(["python", "detect.py","--source", self.folder_path, "--weights", "yolov5s.pt"], capture_output=True, text=True)
            progress_str = self.detect_thread.stdout.read().strip()
            self.progress_signal.emit(progress_str)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication([])
    window = FTPSender()
    selected_folder_thread = SendSelectedFolderThread(window.selected_folder_signal)
    selected_folder_thread.start()
    window.show()
    app.exec_()


