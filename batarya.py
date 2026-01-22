from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPainter, QBrush, QColor, QPen
from PySide6.QtCore import Qt, QRectF

class BataryaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.yuzde = 0  # Başlangıç değeri
        
        # --- ÖNEMLİ: Şeffaflık Ayarı ---
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Widget'ın genel boyutu (İkon + Yazı için)
        self.setFixedSize(60, 80) 

        # Yüzde yazısını gösteren etiket
        self.yazi_label = QLabel("0%", self)
        self.yazi_label.setGeometry(0, 45, 60, 20) 
        self.yazi_label.setAlignment(Qt.AlignCenter)
        
        # Yazı Arka Planı Şeffaf
        self.yazi_label.setStyleSheet("background-color: transparent; color: white; font: bold 14px;")

    def deger_guncelle(self, yeni_yuzde):
        """Batarya değerini günceller ve şekli yeniden çizer"""
        # Sınırlandırma (0 ile 100 arasında)
        self.yuzde = max(0, min(100, yeni_yuzde))
        
        # Yazıyı güncelle
        self.yazi_label.setText(f"%{self.yuzde}")
        
        # Şekli güncelle (paintEvent'i tetikler)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # --- Batarya Çizimi Ayarları ---
        rect_x = 10
        rect_y = 10
        rect_w = 40  # Batarya gövde genişliği
        rect_h = 20  # Batarya gövde yüksekliği

        # 1. Bataryanın Dış Çerçevesi (Boş Kısım)
        dis_cerceve = QRectF(rect_x, rect_y, rect_w, rect_h)
        painter.setPen(QPen(Qt.white, 2))  # Beyaz çerçeve
        painter.setBrush(Qt.NoBrush)       # İçi boş
        painter.drawRoundedRect(dis_cerceve, 3, 3) 

        # 2. Bataryanın Ucu (+ Kutbu)
        uc_kisim = QRectF(rect_x + rect_w, rect_y + 5, 4, 10)
        painter.setBrush(QBrush(Qt.white))
        painter.drawRoundedRect(uc_kisim, 1, 1)

        # 3. İçindeki Doluluk Oranı
        if self.yuzde > 0:
            # Dolacak maksimum genişlik (Çerçeve kalınlığı için 4 piksel düştük)
            max_dolum_genisligi = rect_w - 4 
            
            # Yüzdeye göre genişlik hesapla
            anlik_genislik = max_dolum_genisligi * (self.yuzde / 100)
            
            # Dolum dikdörtgeni
            ic_dikdortgen = QRectF(rect_x + 2, rect_y + 2, anlik_genislik, rect_h - 4)
            
            # Renk Ayarı (Yeşil)
            painter.setBrush(QBrush(QColor("#037849")))
            painter.setPen(Qt.NoPen) 
            painter.drawRoundedRect(ic_dikdortgen, 2, 2)