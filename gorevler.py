class Hedef:
    """
    Görüntü İşleme ekibinden gelen her bir hedefi temsil eden sınıf.
    GÜNCELLEME: Artık X ve Y koordinatlarını da taşıyor.
    """
    def __init__(self, tip, mesafe, x, y, renk="KIRMIZI"):
        self.tip = tip        # ÖRNEK: "F16", "FUZE", "IHA", "DOST_UNSUR"
        self.mesafe = mesafe  # Metre cinsinden uzaklık
        self.x = x            # Ekrandaki Yatay Piksel Konumu (0-640 arası)
        self.y = y            # Ekrandaki Dikey Piksel Konumu (0-480 arası)
        self.renk = renk      # Görsel kontrol için ek bilgi

class AtisKontrolSistemi:
    def __init__(self):
        self.aktif_gorev = None # 2 (Sürü) veya 3 (Dost/Düşman)
        
        # Ekranın tam orta noktası (Kameranın baktığı yer)
        # Varsayım: Çözünürlük 640x480. Bunu kamerana göre değiştirebilirsin.
        self.MERKEZ_X = 320
        self.MERKEZ_Y = 240
        
        # AŞAMA 3 KURALLARI (Alt Sınır, Üst Sınır, Puan)
        # [cite_start]Kaynak: Şartname Tablo 7 ve Metin [cite: 274, 279-281]
        self.VERITABANI = {
            "F16":          {"alt": 10, "ust": 15, "puan": 30},
            "HELIKOPTER":   {"alt": 5,  "ust": 15, "puan": 15},
            "FUZE":         {"alt": 5,  "ust": 15, "puan": 15},
            "IHA":          {"alt": 0,  "ust": 15, "puan": 10},
            "MINI_IHA":     {"alt": 0,  "ust": 15, "puan": 10},
            "GENEL_DUSMAN": {"alt": 0,  "ust": 20, "puan": 10},
            "DOST_UNSUR":   {"alt": 99, "ust": 99, "puan": 0}   # Asla vurulmayacak
        }

    # --- HEDEF SEÇİM MANTIĞI ---
    def hedefi_sec(self, algilanan_hedefler):
        vurulacak_en_iyi_hedef = None
        en_yuksek_skor = -9999 

        for hedef in algilanan_hedefler:
            
            # --- ADIM 1: DOST KONTROLÜ ---
            if self.aktif_gorev == 3 and hedef.tip == "DOST_UNSUR":
                continue 

            # --- ADIM 2: KURAL KONTROLÜ ---
            kural = self.VERITABANI.get(hedef.tip)
            
            # Görev 2 (Sürü) için varsayılan kural
            if self.aktif_gorev == 2 and kural is None:
                 kural = self.VERITABANI["GENEL_DUSMAN"]
            
            if kural is None: continue

            alt_sinir = kural["alt"]
            ust_sinir = kural["ust"]
            hedef_puani = kural["puan"]

            # --- ADIM 3: MENZİL KONTROLÜ ---
            # [cite_start]Kaynak: Şartname Madde 6.3 [cite: 279-281]
            if hedef.mesafe < alt_sinir: continue # Çok yakın (Geçmiş olsun)
            if hedef.mesafe > ust_sinir: continue # Çok uzak (Bekle)

            # --- ADIM 4: AKILLI PUANLAMA ---
            # Hedef sınıra ne kadar yakınsa o kadar acildir.
            kalan_omur = hedef.mesafe - alt_sinir
            oncelik_skoru = hedef_puani - (kalan_omur * 5)
            
            if oncelik_skoru > en_yuksek_skor:
                en_yuksek_skor = oncelik_skoru
                vurulacak_en_iyi_hedef = hedef

        return vurulacak_en_iyi_hedef

    # --- NİŞAN HESAPLAMA (YENİ EKLENEN KISIM) ---
    def nisan_verisi_olustur(self, hedef):
        """
        Seçilen hedefin merkeze olan uzaklığını hesaplar.
        Motorlara gidecek 'Hata Payı'nı üretir.
        """
        if hedef is None:
            return None
        
        # Hata Hesaplama (Target - Center)
        # Eğer sonuç Pozitif (+) ise hedef Sağda/Aşağıda
        # Eğer sonuç Negatif (-) ise hedef Solda/Yukarıda
        hata_x = hedef.x - self.MERKEZ_X
        hata_y = hedef.y - self.MERKEZ_Y
        
        return hata_x, hata_y

# ======================================================
# --- TEST SENARYOSU (Main Loop İçinde Böyle Kullanacaksın) ---
# ======================================================

if __name__ == "__main__":
    # 1. SİSTEMİ BAŞLAT
    kontrol_sistemi = AtisKontrolSistemi()
    kontrol_sistemi.aktif_gorev = 3 # Dost/Düşman Modu

    # 2. SENA'DAN GELEN VERİLER (Simülasyon)
    # Artık X ve Y de geliyor! (Ekran 640x480)
    gelen_paket = [
        Hedef("DOST_UNSUR", 12, 100, 400),       # Sol altta bir dost
        Hedef("F16", 14, 450, 100),              # Sağ üstte bir F16 (Vurulmalı!)
        Hedef("IHA", 14, 320, 240)               # Tam merkezde ama puanı düşük
    ]

    # 3. KARAR VER (Kimi Vurayım?)
    secilen = kontrol_sistemi.hedefi_sec(gelen_paket)

    # 4. HESAPLA VE KOMUT ÜRET
    if secilen:
        hata_verisi = kontrol_sistemi.nisan_verisi_olustur(secilen)
        
        if hata_verisi:
            h_x, h_y = hata_verisi
            print(f"✅ HEDEF KİLİTLENDİ: {secilen.tip} (Mesafe: {secilen.mesafe}m)")
            print(f"🎯 Hedef Konumu: X={secilen.x}, Y={secilen.y}")
            print(f"⚙️  MOTOR KOMUTU: Pan(X) {h_x} piksel dön, Tilt(Y) {h_y} piksel dön.")
            
            # Ateş Serbest Bölgesi (Deadzone)
            if abs(h_x) < 20 and abs(h_y) < 20:
                print("🔥 ATEŞ! Hedef namlunun ucunda!")
            else:
                print("🔄 Nişan alınıyor...")
    else:
        print("❌ Uygun hedef yok, taramaya devam.")