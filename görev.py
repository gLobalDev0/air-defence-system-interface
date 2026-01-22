from PySide6.QtWidgets import QLabel, QPushButton, QFrame, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
from PySide6.QtCore import Qt, QTimer

class TaskManager:
    def __init__(self, window):
        self.window = window
        # Ana penceredeki rect3 (Sağ büyük dikdörtgen) koordinatlarını baz alıyoruz
        self.start_x = 890
        self.start_y = 100
        self.area_width = 800
        self.area_height = 840
        
        # Görev çerçevelerini tutacak liste
        self.frames = []
        
        # Arayüzü Kur
        self.setup_ui()

    def create_frame(self, y, height, title):
        """Görevler için standart neon çerçeve oluşturur"""
        frame = QFrame(self.window)
        frame.setGeometry(self.start_x + 20, y, self.area_width - 40, height)
        frame.setStyleSheet("""
            QFrame {
                border: 2px solid #037849; 
                border-radius: 15px;
                background-color: rgba(0, 20, 0, 150);
            }
        """)
        
        # Başlık Label'ı
        lbl_title = QLabel(title, frame)
        lbl_title.setGeometry(20, 10, 300, 30)
        lbl_title.setStyleSheet("color: #00FFFF; font-family: Impact; font-size: 20px; border: none; background: transparent;")
        
        # Play Butonu (Başlat)
        btn_play = QPushButton("▶ BAŞLAT", frame)
        btn_play.setGeometry(self.area_width - 160, 10, 100, 30)
        btn_play.setStyleSheet("""
            QPushButton {
                color: white; border: 1px solid #00FFFF; border-radius: 5px; font-weight: bold; background: transparent;
            }
            QPushButton:hover { background-color: #037849; }
        """)
        
        frame.show()
        return frame, btn_play

    def setup_ui(self):
        # --- GÖREV 1: MANUEL ATIŞ (Farklı Menziller) ---
        # [cite: 190] Farklı Menzillerde Duran Hedef İmhası
        self.frame1, self.btn_start1 = self.create_frame(self.start_y + 20, 220, "GÖREV 1: MANUEL ATIŞ")
        
        # Sayaç (5 Dakika) 
        self.lbl_timer1 = QLabel("05 : 00 : 00", self.frame1)
        self.lbl_timer1.setGeometry(350, 10, 150, 30)
        self.lbl_timer1.setStyleSheet("color: yellow; font-size: 22px; font-weight: bold; border: none; background: transparent;")

        # Hedef Listesi (Check Box Mantığı) - Şartnamedeki Hedefler 
        # Çizimindeki kutucuklar burada dinamik etiketlere dönüştü.
        self.targets_ui = {}
        target_names = ["Balistik Füze", "İHA", "Helikopter", "Savaş Uçağı", "Mini İHA"]
        
        x_pos = 30
        y_pos = 60
        for i, name in enumerate(target_names):
            # Kutucuk (Check)
            lbl_box = QLabel("☐", self.frame1)
            lbl_box.setGeometry(x_pos, y_pos, 30, 30)
            lbl_box.setStyleSheet("color: white; font-size: 24px; border: none; background: transparent;")
            
            # İsim
            lbl_name = QLabel(name, self.frame1)
            lbl_name.setGeometry(x_pos + 30, y_pos + 5, 150, 20)
            lbl_name.setStyleSheet("color: #ccc; font-size: 14px; border: none; background: transparent;")
            
            self.targets_ui[name] = {"box": lbl_box, "text": lbl_name}
            
            # 2 sütunlu dizilim
            if i == 2: # 3. elemandan sonra sağ sütuna geç
                x_pos = 400
                y_pos = 60
            else:
                y_pos += 40

        # Vurulan Sayısı (Çizimden)
        self.lbl_hit1 = QLabel("Vurulan Hedef: [ 0 / 5 ]", self.frame1)
        self.lbl_hit1.setGeometry(400, 170, 250, 30)
        self.lbl_hit1.setStyleSheet("color: white; font-size: 16px; font-weight: bold; border: none; background: transparent;")


        # --- GÖREV 2: SÜRÜ SALDIRISI (Otonom) ---
        # [cite: 195] Sürü Saldırısı ve İmhası
        self.frame2, self.btn_start2 = self.create_frame(self.start_y + 260, 180, "GÖREV 2: SÜRÜ (OTONOM)")
        
        # Durum Bilgisi (Çizimdeki 'Veri Gelecek' kısmı)
        self.lbl_status2 = QLabel("SİSTEM HAZIR - VERİ BEKLENİYOR...", self.frame2)
        self.lbl_status2.setGeometry(30, 60, 400, 30)
        self.lbl_status2.setStyleSheet("color: #00ff66; font-size: 16px; border: none; background: transparent;")

        # İstatistikler  (4 Tur olduğu için tur sayacı eklendi)
        self.lbl_tur2 = QLabel("TUR: 0 / 4", self.frame2)
        self.lbl_tur2.setGeometry(30, 110, 150, 30)
        self.lbl_tur2.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: 1px solid white; border-radius: 5px; qproperty-alignment: AlignCenter; background: transparent;")

        self.lbl_hit2 = QLabel("Vurulan Toplam Hedef: [ 0 ]", self.frame2)
        self.lbl_hit2.setGeometry(200, 110, 300, 30)
        self.lbl_hit2.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none; background: transparent;")


        # --- GÖREV 3: DOST / DÜŞMAN (Katmanlı) ---
        # [cite: 199] Farklı Katmanlardaki Hareketli Hedefler
        self.frame3, self.btn_start3 = self.create_frame(self.start_y + 460, 200, "GÖREV 3: DOST / DÜŞMAN")

        # Anlık Tespit (Çizimdeki 'Tespit Edilen')
        self.lbl_detected = QLabel("RADAR TARANIYOR...", self.frame3)
        self.lbl_detected.setGeometry(30, 60, 300, 30)
        self.lbl_detected.setStyleSheet("color: orange; font-size: 16px; font-weight: bold; border: none; background: transparent;")

        # Dost / Düşman Sayacı (Çizimdeki ayrım) 
        # Dost (Mavi)
        self.lbl_friend = QLabel("DOST: 0", self.frame3)
        self.lbl_friend.setGeometry(30, 110, 120, 40)
        self.lbl_friend.setStyleSheet("color: #00AAFF; font-size: 20px; font-weight: bold; border: 2px solid #00AAFF; border-radius: 10px; qproperty-alignment: AlignCenter; background: transparent;")
        
        # Düşman (Kırmızı)
        self.lbl_foe = QLabel("DÜŞMAN: 0", self.frame3)
        self.lbl_foe.setGeometry(170, 110, 140, 40)
        self.lbl_foe.setStyleSheet("color: #FF3333; font-size: 20px; font-weight: bold; border: 2px solid #FF3333; border-radius: 10px; qproperty-alignment: AlignCenter; background: transparent;")

        self.lbl_hit3 = QLabel("Vurulan Tehdit: [ 0 ]", self.frame3)
        self.lbl_hit3.setGeometry(350, 115, 250, 30)
        self.lbl_hit3.setStyleSheet("color: white; font-size: 16px; border: none; background: transparent;")


        # --- ACİL DUR BUTONU ---
        #  Zorunlu Acil Durdurma Butonu
        self.btn_emergency = QPushButton("ACİL DURDUR", self.window)
        self.btn_emergency.setGeometry(self.start_x + 20, self.start_y + 680, self.area_width - 40, 60)
        self.btn_emergency.setStyleSheet("""
            QPushButton {
                background-color: rgba(200, 0, 0, 0.2);
                color: red;
                border: 3px solid red;
                border-radius: 30px;
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background-color: red;
                color: white;
            }
            QPushButton:pressed {
                background-color: darkred;
                border-color: darkred;
            }
        """)
        self.btn_emergency.show()
        
        # Çizimdeki "Emin misin?" yazısı butonun altına
        self.lbl_sure = QLabel("( Sistemin Gücünü Keser ! )", self.window)
        self.lbl_sure.setGeometry(self.start_x + 20, self.start_y + 745, self.area_width - 40, 20)
        self.lbl_sure.setAlignment(Qt.AlignCenter)
        self.lbl_sure.setStyleSheet("color: gray; font-size: 12px; font-style: italic; background: transparent;")
        self.lbl_sure.show()

    # --- GÜNCELLEME FONKSİYONLARI (Logic Dosyasının Kullanacağı Yerler) ---

    def update_task1_hit(self, target_name, count):
        """Görev 1: Bir hedef vurulduğunda kutucuğu işaretler"""
        if target_name in self.targets_ui:
            # Kutuyu dolu yap (☑) ve rengi yeşil yap
            self.targets_ui[target_name]["box"].setText("☑")
            self.targets_ui[target_name]["box"].setStyleSheet("color: #00ff66; font-size: 24px; border: none; background: transparent;")
            self.targets_ui[target_name]["text"].setStyleSheet("color: #00ff66; font-size: 14px; font-weight: bold; border: none; background: transparent;")
            
            self.lbl_hit1.setText(f"Vurulan Hedef: [ {count} / 5 ]")

    def update_task2_data(self, tur, vurulan, status_text="SÜRÜ SALDIRISI BAŞLADI"):
        """Görev 2: Tur ve vurulan sayısını günceller"""
        self.lbl_tur2.setText(f"TUR: {tur} / 4")
        self.lbl_hit2.setText(f"Vurulan Toplam Hedef: [ {vurulan} ]")
        self.lbl_status2.setText(status_text)

    def update_task3_stats(self, dost_sayisi, dusman_sayisi, vurulan_dusman):
        """Görev 3: Dost/Düşman sayılarını günceller"""
        self.lbl_friend.setText(f"DOST: {dost_sayisi}")
        self.lbl_foe.setText(f"DÜŞMAN: {dusman_sayisi}")
        self.lbl_hit3.setText(f"Vurulan Tehdit: [ {vurulan_dusman} ]")