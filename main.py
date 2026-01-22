import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QImage
from PySide6.QtCore import Qt, QRectF, Slot

# --- SENİN MODÜLLERİN ---
from radar import RadarWidget
from camerawidget import CameraWidget 
from butons import InterfaceButtons 
from görev import TaskManager
from batarya import BataryaWidget 

# --- YENİ AYIRDIĞIMIZ DOSYAYI ÇAĞIRIYORUZ ---
from workers import SerialThread, VisionThread

# =========================================================================
# 3. PATRON: ANA ARAYÜZ (MyWindow)
# =========================================================================
class MyWindow(QMainWindow):  
     
    def __init__(self):
        super().__init__()
       
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Interface")
        self.setGeometry(100,100, 1700,1000)

        # --- ÇERÇEVE DEĞİŞKENLERİ ---
        self.rect_color = "white"
        self.glow_color = QColor("#037849")  
        self.rect_x = 15
        self.rect_y = 620
        self.rect_width = 860
        self.rect_height = 370
        self.opacity = 0.0                

        self.rect1_color = "black"
        self.glow1_color =  QColor("#037849")
        self.rect1_x = 15
        self.rect1_y = 10
        self.rect1_width = 600
        self.rect1_height = 860

        self.rect2_color = "white"
        self.glow2_color = QColor("#037849")  
        self.rect2_x = 890
        self.rect2_y = 10
        self.rect2_width = 800
        self.rect2_height = 75

        self.rect3_color = "white"
        self.glow3_color = QColor("#037849")  
        self.rect3_x = 890
        self.rect3_y = 100
        self.rect3_width = 800
        self.rect3_height = 840
        self.opacity = 0.0

        # --- WIDGET'LAR ---
        self.camera_widget = CameraWidget(self)
        offset = 4 
        self.camera_widget.setGeometry(
            self.rect1_x + offset, 
            self.rect1_y + offset, 
            self.rect1_height - (offset * 2), 
            self.rect1_width - (offset * 2)
        )
        self.camera_widget.lower()

        self.radar = RadarWidget(self)
        self.radar.setGeometry(17, 622, 500, 366)
        self.radar.raise_()

        self.batarya = BataryaWidget(self)
        self.batarya.move(900, 20) 
        
        # Başlık
        self.title_label = QLabel(self)
        self.title_label.setGeometry(1250, self.rect2_y, 420, self.rect2_height) 
        self.title_label.setText("HAVA SAVUNMA SİSTEMİ\nAR-GE")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #00FFFF; 
                background-color: transparent; 
                border: none; 
                font-family: 'Impact', 'Arial Black', sans-serif; 
                font-size: 28px; 
                font-weight: bold; 
                line-height: 0.8; 
            }
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.raise_()

        self.buttons = InterfaceButtons(self)
        self.tasks = TaskManager(self)

        # --- THREAD (İŞÇİ) BAŞLATMA ALANI ---
        
        # 1. Kamera İşçisini Başlat
        self.vision_thread = VisionThread()
        self.vision_thread.change_pixmap_signal.connect(self.goru_guncelle)
        self.vision_thread.start()

        # 2. Arduino İşçisini Başlat
        self.serial_thread = SerialThread(port='COM3') 
        self.serial_thread.battery_signal.connect(self.batarya_guncelle)
        self.serial_thread.start()

    # --- SİNYAL YAKALAYICILAR (SLOTS) ---

    @Slot(QImage)
    def goru_guncelle(self, qt_img):
        """Kameradan gelen resmi widget'a basar"""
        self.camera_widget.update_image(qt_img)

    @Slot(int)
    def batarya_guncelle(self, yuzde):
        """Arduino'dan gelen pil yüzdesini günceller"""
        self.batarya.deger_guncelle(yuzde)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Sol Alt Çerçeve
        rect = QRectF(self.rect_x, self.rect_y, self.rect_width, self.rect_height)
        color = QColor(self.rect_color)
        color.setAlphaF(self.opacity)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        pen = QPen(self.glow_color, 3)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 8, 8)

        # Kamera Çerçevesi
        rect1 = QRectF(self.rect1_x, self.rect1_y, self.rect1_height, self.rect1_width)
        color = QColor(self.rect1_color)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect1, 8, 8)

        pen = QPen(self.glow1_color, 3)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect1, 8, 8)

        # Görev Listesi Çerçevesi
        rect3 = QRectF(self.rect3_x, self.rect3_y, self.rect3_width, self.rect3_height)
        color = QColor(self.rect3_color)
        color.setAlphaF(self.opacity)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect3, 8, 8)

        pen = QPen(self.glow3_color, 3)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect3, 8, 8)

        # Üst İnce Çerçeve
        rect2 = QRectF(self.rect2_x, self.rect2_y, self.rect2_width, self.rect2_height)
        color = QColor(self.rect2_color)
        color.setAlphaF(self.opacity)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect2, 8, 8)

        pen = QPen(self.glow2_color, 3)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect2, 8, 8)

    def closeEvent(self, event):
        self.vision_thread.stop()
        self.serial_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())