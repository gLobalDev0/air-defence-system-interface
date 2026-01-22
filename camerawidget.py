from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage

class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Sadece görüntüyü tutacak bir etiket (Label)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        # Çerçeve rengi ve arka plan
        self.label.setStyleSheet("background-color: black; border: 1px solid #037849;")
        
        # Düzen (Layout)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.setLayout(layout)

    # Bu fonksiyonu artık Main Thread dışarıdan çağıracak
    def update_image(self, qt_img):
        """Dışarıdan gelen QImage formatındaki resmi ekrana basar"""
        pixmap = QPixmap.fromImage(qt_img)
        
        # Resmi etiketin boyutuna uydur (KeepAspectRatio = Oranı bozma)
        scaled_pixmap = pixmap.scaled(
            self.label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled_pixmap)