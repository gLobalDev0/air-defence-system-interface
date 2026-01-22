from PySide6.QtWidgets import QWidget 
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QColor, QFont
import math

class RadarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.angle = 0  # Cihazın anlık açısı
        
        self.glow = QColor("#00ff66")   # radar yeşil rengi
        self.bg = QColor("#000000")     # arka fon
        self.text_color = QColor("#00FFFF") # Alt yazı rengi (Turkuaz)

    def set_angle(self, val):
        self.angle = val % 360 
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Arka Fon
        painter.fillRect(self.rect(), self.bg)

        w = self.width()
        h = self.height()
        
        # --- MERKEZ AYARLARI ---
        r = min(w, h) // 2 - 55  # Yarıçap
        cx = w // 2 - 50         # Yatay konum
        cy = h // 2 - 30         # Dikey konum

        # 1. Radar Çemberleri
        pen = QPen(self.glow, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for k in range(1, 5):
            painter.drawEllipse(cx - r*k/4, cy - r*k/4, r*k/2, r*k/2)

        # 2. Çizgiler 
        
        # --- ANA EKSENLER (Çok az çıkmalı - 1.05) ---
        main_ext = 1.05 
        painter.drawLine(cx - r* main_ext, cy, cx + r*main_ext, cy)
        painter.drawLine(cx, cy - r*main_ext, cx, cy + r*main_ext)
        
        # --- ARA EKSENLER (Çevreden çıkmamalı - 1.0) ---
        diag_r = r * 1.0 
        diag_x = diag_r * 0.707 
        diag_y = diag_r * 0.707 
        
        painter.drawLine(cx - diag_x, cy - diag_y, cx + diag_x, cy + diag_y) 
        painter.drawLine(cx - diag_x, cy + diag_y, cx + diag_x, cy - diag_y) 
        
        # 3. Yön Yazıları
        painter.setPen(QColor("#80FEBD"))
        font = QFont()
        font.setPointSize(10) 
        painter.setFont(font)

        # Yazıların konum ayarı
        text_gap_main = 10  
        text_gap_diag = 20  

        # --- ANA YÖNLER ---
        # 0° (Sağ)
        painter.drawText(cx + r + text_gap_main, cy + 5, "0°")       
        
        # 180° (Sol)
        painter.drawText(cx - r - text_gap_main - 28, cy + 5, "180°") 
        
        # 90° (Üst)
        painter.drawText(cx - 10, cy - r - text_gap_main + 5, "90°")  
        
        # 270° (Alt)
        painter.drawText(cx - 12, cy + r + text_gap_main + 10, "270°") 

        # --- ARA YÖNLER (Çaprazlar) ---
        t_dist = r + text_gap_diag
        tx = t_dist * 0.707
        ty = t_dist * 0.707

        # 45°
        painter.drawText(cx + tx - 5, cy - ty + 5, "45°")
        # 135°
        painter.drawText(cx - tx - 25, cy - ty + 5, "135°")
        # 225°
        painter.drawText(cx - tx - 25, cy + ty + 10, "225°")
        # 315°
        painter.drawText(cx + tx - 5, cy + ty + 10, "315°")


        # 4. Hareketli İbre
        painter.setPen(QPen(self.text_color, 4)) 
        angle_rad = math.radians(self.angle) 
        
        x2 = cx + r * math.cos(angle_rad)
        y2 = cy - r * math.sin(angle_rad) 
        
        painter.drawLine(cx, cy, x2, y2)
        
        # Ucuna top
        painter.setBrush(self.text_color)
        painter.drawEllipse(x2 - 5, y2 - 5, 10, 10)

        # 5. Alttaki Büyük Yazı
        painter.setPen(self.text_color)
        font_big = QFont("Arial", 16, QFont.Bold)
        painter.setFont(font_big)
        
        derece_text = f"{int(self.angle)}°"
        text_rect = QRectF(cx - 50, cy + r + 45, 100, 30)
        painter.drawText(text_rect, Qt.AlignCenter, derece_text)