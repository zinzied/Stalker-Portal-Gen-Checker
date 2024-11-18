# Stalker Portal MAC Generator & Checker
![Capture d'écran 2024-07-31 231543](https://github.com/user-attachments/assets/142399e6-c067-4422-b568-db03d2f32870)
          
This Python application is a Stalker Portal MAC address generator and checker. It generates MAC addresses, checks them against a specified Stalker Portal, and retrieves information such as the number of channels and expiry date. The application is built using PyQt5 for the GUI and leverages threading for concurrent processing.

## Features

- Generate MAC addresses starting from a specified address.
- Check MAC addresses against a Stalker Portal.
- Retrieve and display information such as the number of channels and expiry date.
- Save results to a text file.
- Simple and intuitive GUI built with PyQt5.

## Requirements

- Python 3.x
- PyQt5
- Requests
- Cryptography

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/stalker-portal-mac-checker.git
    cd stalker-portal-mac-checker
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure you have a file named `agents.txt` in the same directory, containing user-agent strings, one per line.

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. Enter the Stalker Portal URL with port in the "Enter Stalker Portal with Port" field.

3. Optionally, enter a full MAC address to start from in the "Enter a full MAC address to start from" field.

4. Click the "Start" button to begin the process.

5. The application will generate MAC addresses, check them against the specified Stalker Portal, and display the results in the text area.

6. Click the "Stop" button to stop the process and close the application.

## Example

1. Enter `http://example.com:8080` in the "Enter Stalker Portal with Port" field.
2. Enter `00:1A:79:XX:XX:XX` in the "Enter a full MAC address to start from" field.
3. Click "Start" to begin checking MAC addresses.
4. The results will be displayed in the text area and saved to a file named `example.com_YYYY-MM-DD_HH-MM-SS.txt`.
5. For educational purpose only the usage is on own risk.
## Credit

This project is maintained by [Fairy-root](https://github.com/fairy-root). Great Thanks to Him For let me Forked his project: [iptv-mac-checker](https://github.com/fairy-root/iptv-mac-checker)

### Donations
If you feel like showing your love and/or appreciation for this project, then how about shouting me a coffee or Milk :)

[<img src="https://github.com/zinzied/Website-login-checker/assets/10098794/24f9935f-3637-4607-8980-06124c2d0225">](https://www.buymeacoffee.com/Zied)


