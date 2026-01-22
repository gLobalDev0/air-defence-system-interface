from PySide6.QtWidgets import QPushButton, QMenu
from PySide6.QtGui import QAction

class InterfaceButtons:
    def __init__(self, window):
        self.window = window
        self.setup_ui()

    def setup_ui(self):
        # --- ORTAK AYARLAR ---
        btn_y = 25
        btn_h = 45
        btn_w = 140
        gap = 15
        
        start_x = 990

        # ==========================================================
        # 1. BUTON: CONNECT / DISCONNECT
        # ==========================================================
        self.window.btn = QPushButton("Disconnected", self.window)
        self.window.btn.setGeometry(start_x, btn_y, btn_w, btn_h)
        
        # Başlangıç Stili (KIRMIZI - Bağlı Değil)
        self.window.btn.setStyleSheet("""
            QPushButton {
                background-color: #800000; /* Koyu Kırmızı */
                color: white;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
                border: 2px solid #ff3333;
            }
            QPushButton:hover {
                background-color: #a00000;
            }
        """)

        # Tıklama olayını KENDİ İÇİMİZDEKİ fonksiyona bağladık
        self.window.btn.clicked.connect(self.baglanti_durumunu_degistir)
        self.window.btn.raise_()


        # ==========================================================
        # 2. BUTON: MOD SEÇİMİ (NO MODE)
        # ==========================================================
        btn2_x = start_x + btn_w + gap

        self.window.btn_1 = QPushButton("No Mode", self.window)
        self.window.btn_1.setGeometry(btn2_x, btn_y, btn_w, btn_h)

        self.window.btn_1.setStyleSheet("""
            QPushButton {
                background-color: #037849;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
                padding-right: 15px;
                text-align: center;
            }
            QPushButton::menu-indicator {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                right: 10px;
                width: 10px;
                height: 10px;
            }
            QPushButton:hover {
                background-color: #049f60;
            }
        """)

        # --- Menü (Dropdown) ---
        menu = QMenu(self.window)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                color: black;
                font-size: 12px;
                border: 1px solid #037849;
            }
            QMenu::item:selected {
                background-color: #037849;
                color: white;
            }
        """)

        # Seçenekler
        action_no_mod = QAction("No Mode", self.window)
        action_manuel = QAction("Manuel", self.window)
        action_otonom = QAction("Otonom", self.window)
        action_yari_otonom = QAction("Yarı Otonom", self.window)

        # Seçilen modu butona yazdır
        action_no_mod.triggered.connect(lambda: self.window.btn_1.setText("No Mode"))
        action_manuel.triggered.connect(lambda: self.window.btn_1.setText("Manuel"))
        action_otonom.triggered.connect(lambda: self.window.btn_1.setText("Otonom"))
        action_yari_otonom.triggered.connect(lambda: self.window.btn_1.setText("Yarı Otonom"))

        # Menüye ekle
        menu.addAction(action_no_mod)
        menu.addAction(action_manuel)
        menu.addAction(action_otonom)
        menu.addAction(action_yari_otonom)

        # Menüyü butona bağla
        self.window.btn_1.setMenu(menu)
        self.window.btn_1.raise_()

    # ==========================================================
    # BUTON FONKSİYONLARI (Main.py'yi kirletmemek için burada)
    # ==========================================================
    def baglanti_durumunu_degistir(self):
        """Butona basınca rengi ve yazıyı değiştirir"""
        
        # Butonun o anki yazısını oku
        mevcut_yazi = self.window.btn.text()

        if mevcut_yazi == "Disconnected":
            # --- BAĞLANMA İŞLEMİ ---
            self.window.btn.setText("Connected")
            
            # YEŞİL Stil (Bağlandı)
            self.window.btn.setStyleSheet("""
                QPushButton {
                    background-color: #037849; 
                    color: white;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 8px;
                    border: 2px solid #00ff66;
                }
                QPushButton:hover { background-color: #049f60; }
            """)
            print("Buton Modülü: Bağlantı açıldı (Yeşil).")
            
            # İPUCU: İleride Thread başlatma kodunu buraya ekleyebilirsin
            # Örn: self.window.serial_thread.start()

        else:
            # --- KOPARMA İŞLEMİ ---
            self.window.btn.setText("Disconnected")
            
            # KIRMIZI Stil (Koptu)
            self.window.btn.setStyleSheet("""
                QPushButton {
                    background-color: #800000;
                    color: white;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 8px;
                    border: 2px solid #ff3333;
                }
                QPushButton:hover { background-color: #a00000; }
            """)
            print("Buton Modülü: Bağlantı kesildi (Kırmızı).")
            
            # İPUCU: İleride Thread durdurma kodunu buraya ekleyebilirsin
            # Örn: self.window.serial_thread.stop()