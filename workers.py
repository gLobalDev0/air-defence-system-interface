import serial
import cv2
from PySide6.QtGui import QImage
from PySide6.QtCore import QThread, Signal, Qt

# =========================================================================
# 1. İŞÇİ: ARDUINO HABERLEŞME VE BATARYA (SerialThread)
# =========================================================================
class SerialThread(QThread):
    # Pili ana ekrana bildirmek için sinyal (Sayı gönderir)
    battery_signal = Signal(int) 

    def __init__(self, port='COM3', baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.is_running = True

    def run(self):
        # 1. Bağlantıyı Aç
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Sistem: Arduino {self.port} üzerinden bağlandı.")
        except Exception as e:
            print(f"HATA: Arduino bağlanamadı! ({e})")
            print("İPUCU: Arduino takılı değilse bu hata normaldir, program çalışmaya devam eder.")
            self.ser = None

        # 2. Sonsuz Döngü (Arka Planda Çalışır - Arayüzü Dondurmaz)
        while self.is_running:
            if self.ser and self.ser.is_open:
                try:
                    if self.ser.in_waiting > 0:
                        line = self.ser.readline().decode(errors="ignore").strip()
                        if line:
                            try:
                                value = float(line)
                                # --- SENİN BATARYA MATEMATİĞİN ---
                                percent = (value - 10.5) / (12.6 - 10.5) * 100
                                percent = max(0, min(100, percent))
                                
                                # Ana ekrana fırlat
                                self.battery_signal.emit(int(percent))
                            except ValueError:
                                pass
                except Exception:
                    pass
            
            # İşlemciyi dinlendir (Çok önemli - Donmayı engeller)
            self.msleep(50) 

    def stop(self):
        self.is_running = False
        if self.ser:
            self.ser.close()
        self.wait()

# =========================================================================
# 2. İŞÇİ: KAMERA VE GÖRÜNTÜ İŞLEME (VisionThread)
# =========================================================================
class VisionThread(QThread):
    change_pixmap_signal = Signal(QImage) # Resmi ana ekrana atar

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0) # Kamerayı başlat
        
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                # BGR -> RGB Çevrimi
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                
                # Resmi biraz küçültelim ki arayüz rahatlasın (640x480 idealdir)
                p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                
                self.change_pixmap_signal.emit(p)
            
            self.msleep(30) # 30 FPS hızında çalışması için bekleme

        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()