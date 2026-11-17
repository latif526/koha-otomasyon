import time
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

def hedef_saati_bekle():
    """Sabah 06:30:00 için tam zamanında tetikleme yapar."""
    simdi = datetime.now()
    hedef = simdi.replace(hour=6, minute=29, second=55, microsecond=0)
    
    if simdi >= hedef:
        hedef += timedelta(days=1)
        
    bekleme_suresi = (hedef - simdi).total_seconds()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Sabah 06:30 açılışı bekleniyor. Kalan süre: {bekleme_suresi/60:.1f} dakika...")
    time.sleep(bekleme_suresi)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Hedef saate ulaşıldı, işlem başlatılıyor!")

def koha_otomatik_randevu():
    hedef_saati_bekle()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Koha sistemine bağlanılıyor...")
        page.goto("https://koha.ekutuphane.gov.tr/")

        # 1. Giriş Bilgileri
        page.fill("input#userid", "10652116844")
        page.fill("input#password", "c9uyD")
        page.click("input#auth_submit")
        
        page.wait_for_load_state("domcontentloaded")
        print("Giriş başarılı, masa seçimine geçiliyor...")

        # 2. Masa Seçimi (Önce 109, doluysa 114)
        masalar = ["109", "114"]
        basarili = False

        for masa in masalar:
            try:
                print(f"Salon 3 için {masa} numaralı masa deneniyor...")
                page.click(f"text={masa}", timeout=5000)
                page.click("text=Onayla", timeout=5000)
                
                print(f"BAŞARILI! {masa} numaralı masa rezerve edildi.")
                basarili = True
                break
            except Exception as e:
                print(f"{masa} numaralı masa seçilemedi veya dolu, diğerine geçiliyor...")

        if not basarili:
            print("İstenen masaların ikisi de anlık olarak dolu!")

        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    koha_otomatik_randevu()
