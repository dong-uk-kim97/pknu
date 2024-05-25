import os
import socket
import subprocess
from ftplib import FTP
from multiprocessing import Process
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

        self.select_button = QPushButton("폴더 선택")
        self.select_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_button)

        self.folder_combobox = QComboBox()
        layout.addWidget(QLabel("yolov5 폴더 선택:"))
        layout.addWidget(self.folder_combobox)

        self.send_button = QPushButton("보내기")
        self.send_button.clicked.connect(self.send_folder)
        self.send_button.setEnabled(False)
        layout.addWidget(self.send_button)

        self.run_detect_button = QPushButton("detect.py 실행")
        self.run_detect_button.clicked.connect(self.run_detect)
        self.run_detect_button.setEnabled(False)
        layout.addWidget(self.run_detect_button)

        self.setLayout(layout)
        self.read_current_directory()

    def read_current_directory(self):
        current_directory = os.getcwd()
        folders = [folder for folder in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, folder))]
        self.folder_combobox.addItems(folders)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "폴더 선택")
        if folder_path:
            self.folder_path = folder_path
            self.send_button.setEnabled(True)
            self.run_detect_button.setEnabled(True)
            self.selected_folder_signal.emit(folder_path)

    def send_folder(self):
        try:
            self.ftp.connect("FTP 호스트", "FTP 포트")
            self.ftp.login("FTP 사용자명", "FTP 비밀번호")
            self.ftp.cwd("/")  # 서버의 루트 디렉토리로 이동
            self.send_files_in_folder(self.folder_path)
            self.ftp.quit()
        except Exception as e:
            print(f"오류: {e}")
            self.send_button.setEnabled(False)

    def send_files_in_folder(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            self.ftp.cwd(os.path.basename(root))  # 서버의 현재 디렉토리로 이동
            for file in files:
                file_path = os.path.join(root, file)
                self.ftp.storbinary(f"STOR {file}", open(file_path, "rb"), 1024)
            for dir in dirs:
                try:
                    self.ftp.mkd(dir)  # 서버에 디렉토리 생성
                except:
                    pass
                self.send_files_in_folder(os.path.join(root, dir))
            self.ftp.cwd("..")  # 상위 디렉토리로 이동

    def run_detect(self):
        for i in range(1, 6):
            detect_thread = DetectThread(f"rtsp://192.168.0.10{i}:554/stream")
            detect_thread.start()


class DetectThread(QThread):
    progress_signal = pyqtSignal(str)

    def __init__(self, cam_url):
        super().__init__()
        self.cam_url = cam_url

    def run(self):
        try:
            subprocess.run(["python", "detect.py", "--source", self.cam_url, "--weights", "yolov5s.pt"], capture_output=True, text=True)
            progress_str = self.detect_thread.stdout.read().strip()
            self.progress_signal.emit(progress_str)
        except Exception as e:
            print(f"오류: {e}")


if __name__ == "__main__":
    app = QApplication([])
    window = FTPSender()
    window.show()
    app.exec_()

