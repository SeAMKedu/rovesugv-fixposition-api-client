import re
import threading
import tkinter as tk
from io import BytesIO
from typing import Any

import requests
from PIL import Image, ImageTk, UnidentifiedImageError


class App(threading.Thread):
    """GUI application for showing the camera stream."""

    def __init__(self):
        self.closed = False
        threading.Thread.__init__(self)
        self.start()
    
    def close(self):
        """Called when the GUI window is closed."""
        self.closed = True
        self.root.quit()

    def run(self):
        """Run the GUI application."""
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.title("Fixposition Camera Stream")

        self.label = tk.Label(self.root)
        self.label.pack(side="bottom", fill="both", expand=True)

        self.root.mainloop()


class APIClient:
    """
    Docstring

    :param host: Hostname or IP address of the Fixposition device.

    """
    _version = "v2"

    def __init__(self, host: str) -> None:
        self.host = host
        self.base_url = f"http://{self.host}/api/{self._version}"
        self.chunk_size = 1024 * 1024


    def api_request(
            self, 
            endpoint: str, 
            method: str, 
            data: dict[str, Any] = {}, 
            params: dict[str, Any] = {},
            files: dict = {}, 
        ) -> dict[str, Any]:
        """Send a HTTP request to the API."""
        url = f"{self.base_url}{endpoint}"

        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files)
            else:
                data = {} if not data else data
                response = requests.post(url, json=data)
        
        return response.json()


    def download_file(self, endpoint: str, params: dict):
        """Download and save a file."""
        url = f"{self.base_url}{endpoint}"

        response = requests.get(url, params=params, stream=True)

        content_disposition = response.headers.get("Content-Disposition", "")
        filename = content_disposition.split("filename=")[1]

        #total_size = int(response.headers.get("Content-Length", "0"))
        #downloaded = 0

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                if not chunk:
                    break
                file.write(chunk)

    def download_log_file(self, endpoint: str, data: dict):
        """Download and save a log file."""
        url = f"http//{self.host}:21100{endpoint}"
        response = requests.post(url, json=data)
        filename = re.findall('filename="(.+)"', str(response.headers))[0]
        with open(filename, "wb") as file:
            file.write(response.content)


    def stream(self, endpoint: str):
        """Stream images from the Fixposition device's onboard camera."""
        url = f"{self.base_url}{endpoint}"

        response = requests.get(url, stream=True)
        if not response.status_code == 200:
            return

        app = App()

        counter = 0
        image_data = b""
        for chunk in response.iter_content(chunk_size=self.chunk_size):
            if not chunk:
                app.close()
                break
            # Exit the loop when the GUI app is closed
            if app.closed:
                break
            
            # Chunks:
            # b'--boundarydonotcross\r\n'
            #
            # b'Content-type: image/jpeg\r\nX-Timestamp: 1757408620.691116\r\nContent-Length: 21042\r\n\r\n'
            # b'\xff\xd8\xff\xe0\x00...\xb4(\xa0\x0ek'
            # b'\xc5\xcd\x84\x81~\xb4x5O...\xfaP\x07\xff\xd9\r\n--boundarydonotcross\r\n'
            #
            # b'Content-type: image/jpeg\r\nX-Timestamp: 1757408621.030241\r\nContent-Length: 20997\r\n\r\n'
            # b'\xff\xd8\xff\xe0\x00\x10JFIF\x00...\xd0QE\x14\x00QE\x14\x00QE\x14'
            # b'\x01Z\xef\xee\xd6\x1d\xe6I\xdb...\x86\xed\xc5\x00\x7f\xff\xd9\r\n--boundarydonotcross\r\n'

            if len(chunk) > 1000:
                image_data += chunk
                counter += 1
            if counter < 2:
                continue

            # Show the image on the GUI app.
            try:
                image = Image.open(BytesIO(image_data))
                image_tk = ImageTk.PhotoImage(image=image)
                app.label.configure(image=image_tk)
                image_data = b""
                counter = 0
            except UnidentifiedImageError:
                print("[ERROR] UnidentifiedImageError, stopping...")
                break
        
        app.close()
