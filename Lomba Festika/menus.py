import random, time, re
from datajamu import ramuan_jatim, respon_lucu, apik, loro, kesel
from animations import ketik, progress_bar, show_cup_animation, RESET, BOLD, CYAN, YELLOW
from minigames import mode_tebak_jamu, menu_pantun

# ===== Helper =====
def input_ya_tidak(prompt):
    while True:
        jawaban = input(prompt).strip().lower()
        if jawaban in ["iyo", "ora", "iyo", "engga", "gak"]:
            return "iyo" if jawaban in ["yo", "iyo"] else "ora"
        ketik("MbokSri: Mangga, jawab 'yo' utawa 'ora', rek!")

def preprocess_gejala(user_input):
    """Normalisasi input gejala"""
    # Normalisasi teks
    raw = user_input.lower().strip()
    
    # Ganti karakter non-alfanumerik dengan spasi
    raw = re.sub(r'[^\w\s]', ' ', raw)
    
    # Split dan hapus empty strings
    words = [w.strip() for w in raw.split() if w.strip()]
    
    # Gabungkan kata-kata yang mungkin merupakan gejala multi-word
    gejala_processed = []
    i = 0
    while i < len(words):
        # Coba match 2-word phrases dulu
        if i + 1 < len(words):
            two_word = f"{words[i]}_{words[i+1]}"
            # Cek apakah two_word ada di daftar gejala manapun
            found = False
            for data in ramuan_jatim.values():
                if two_word in data["gejala"]:
                    gejala_processed.append(two_word)
                    i += 2
                    found = True
                    break
            if found:
                continue
        
        # Kalau tidak match, pakai single word
        gejala_processed.append(words[i])
        i += 1
    
    return gejala_processed

def hitung_skor(gejala_user, ramuan):
    """Hitung skor dengan partial matching"""
    skor = {}
    for nama, daftar_gejala in ramuan.items():
        match_count = 0
        for gejala_input in gejala_user:
            # Exact match
            if gejala_input in daftar_gejala:
                match_count += 2
            # Partial match (gejala input mengandung kata dari daftar gejala)
            else:
                for gejala_db in daftar_gejala:
                    if gejala_input in gejala_db or gejala_db in gejala_input:
                        match_count += 1
                        break
        skor[nama] = match_count
    return skor

def rekomendasi(user_input):
    """Sistem rekomendasi yang lebih akurat"""
    gejala_user = preprocess_gejala(user_input)
    
    if not gejala_user:
        return "Ora Ono Jamu Cocok", random.choice(respon_lucu)
    
    # Mapping gejala ke jamu
    mapping_jamu = {nama: data["gejala"] for nama, data in ramuan_jatim.items()}
    skor = hitung_skor(gejala_user, mapping_jamu)
    
    # Cek apakah ada gejala "apik"
    is_apik = any(gejala in apik for gejala in gejala_user)
    
    # Filter hanya jamu dengan skor > 0
    kandidat_match = [(nama, score) for nama, score in skor.items() if score > 0]
    
    if not kandidat_match:
        return "Ora Ono Jamu Cocok", random.choice(respon_lucu)
    
    # INPUT "APIK" → 1 JAMU RANDOM DARI YANG MATCH
    if is_apik:
        jamu_terpilih = random.choice([nama for nama, _ in kandidat_match])
        info_jamu = ramuan_jatim[jamu_terpilih]
        return jamu_terpilih, f"Alhamdulillah supaya tetep sehat tak rekomendasikan jamu {jamu_terpilih} iki yaa soale {info_jamu['manfaat']}"
    
    # Urutkan berdasarkan skor tertinggi
    kandidat_match.sort(key=lambda x: x[1], reverse=True)
    
    # INPUT 1 GEJALA → JAMU DENGAN SKOR TERTINGGI
    if len(gejala_user) == 1:
        jamu_terpilih = kandidat_match[0][0]
        return jamu_terpilih, f"Aku milih {jamu_terpilih} soale cocok karo gejalamu."
    
    # INPUT 2+ GEJALA → 2 JAMU DENGAN SKOR TERTINGGI
    else:
        if len(kandidat_match) >= 2:
            jamu1, jamu2 = kandidat_match[0][0], kandidat_match[1][0]
            fusion = f"{jamu1} + {jamu2}"
            return fusion, f"Aku milih {fusion} soale gejalamu cocok karo {jamu1} lan {jamu2}."
        else:
            jamu_terpilih = kandidat_match[0][0]
            return jamu_terpilih, f"Aku milih {jamu_terpilih} soale gejalamu paling cocok."

# ===== Tampilkan resep animasi per jamu =====
def tampilkan_resep_jamu(jamu):
    info = ramuan_jatim.get(jamu)
    if not info: return
    ketik(f"\n{BOLD}{jamu.upper()}{RESET} — asal {info['asal']}", delay=0.02)
    ketik(f"{CYAN}Manfaat:{RESET} {info.get('manfaat','-')}", delay=0.01)
    print()
    print("\n   ===============================")
    print("            🧺  BAHAN - BAHAN       ")
    print("   ===============================\n")
    for b in info["bahan"]:
        ketik(f"  - {b}", delay=0.01)
    print()
    ketik("Lampahan-Lampahan :", delay=0.01)
    for i, l in enumerate(info["langkah"],1):
        progress_bar(steps=5, delay=0.25)
        ketik(f"  {i}. {l}", delay=0.01)
    print()
    show_cup_animation(frames=5, delay=0.18)
    ketik(f"{YELLOW}MbokSri: Jamu wis siap — sugeng ngombe!{RESET}\n", delay=0.02)

def tampilkan_kombinasi_bahan(jamu_list):
    print("\n   ===============================")
    print("       🧺  KOMBINASI 2 BAHAN")
    print("   ===============================\n")
    semua_bahan = []
    for j in jamu_list:
        info = ramuan_jatim.get(j)
        if info:
            semua_bahan.extend(info["bahan"])
    for b in semua_bahan:
        print(f"  ➤ {b}")
        time.sleep(0.15)
    print("\n   ===============================\n")

# ====== List jamu ======
def list_jamu_names():
    print("\nDaftar Jamu (sing kasedhiya):")
    for j in sorted(ramuan_jatim.keys()):
        print(" -", j)
    print()

# ===== Mode Obrolan =====
def Obrolan():
    ketik("\n -RACIK MISTERI- \n", delay=0.02)
    ketik("MbokSri: Halo rek! Piye kabare? Katon e awakmu ra seger yo?")
    ketik("MbokSri: Ojo kuwatir, kene tak ewangi nggolekno ramuan jamu tradhisional sing iso gawe awakmu waras meneh.")
    ketik("MbokSri: Coba ceritakno disik, awakmu saiki sing dirasakne opo?")
    
    user_input = input("Aku: ").strip()
    
    ketik("MbokSri lagi mikir dhisik... 🤔", delay=0.02)
    time.sleep(1.2)

    nama_jamu, alasan = rekomendasi(user_input)

    # ============== JIKA TIDAK ADA JAMU ==============
    if nama_jamu == "Ora Ono Jamu Cocok":
        ketik(f"\nMbokSri: {alasan}")
        ketik("\nMbokSri: Wah, kayane gejalamu kurang cocok karo jamu tradisional.")
        ketik("MbokSri: Yo wes, langsung wae guyonan nagnggo pantun ben ora ngrasa jenuh wae!")
        menu_pantun()
        return

    # ============== JIKA JAMU DITEMUKAN ==============
    is_apik = any(gejala in apik for gejala in preprocess_gejala(user_input))
    
    if is_apik:
        ketik(f"\nMbokSri: {alasan}")
        ketik("MbokSri: Iki jamu sing tak rekomendasikan, mugo-mugo awakmu tetep fit!")
    else:
        info = ramuan_jatim.get(nama_jamu, None)
        if info:
            ketik(f"\nMbokSri: Cocok iki rek, awakmu pas banget ngombe {BOLD}{nama_jamu}{RESET} saka {info['asal']}.")
            ketik(f"MbokSri: {alasan}")
        else:
            ketik(f"\nMbokSri: {alasan}")

    # ============== TANYA RESEP ==============
    ketik(f"\nMbokSri: Kowe pengin tak bikinké resepé ora? (iyo/ora): ")
    if input_ya_tidak("Aku: ") == "iyo":

        # ======== RESEP KOMBINASI ========
        if "+" in nama_jamu:
            jamu_list = [j.strip() for j in nama_jamu.split("+")]

            ketik("\nMBokSri: Kowe pengin resepé sing endi rek?")
            for idx, j in enumerate(jamu_list, 1):
                ketik(f"{idx}. {j}")
            ketik(f"{len(jamu_list)+1}. Loro-lorone")
            
            pilihan = input("Pilih nomor: ").strip()

            if pilihan == "1":
                pilih_jamu = [jamu_list[0]]
            elif pilihan == "2":
                pilih_jamu = [jamu_list[1]]
            else:
                pilih_jamu = jamu_list

            # tampilkan resep masing-masing
            for j in pilih_jamu:
                tampilkan_resep_jamu(j)

            # tampilkan bahan kombinasi
            tampilkan_kombinasi_bahan(pilih_jamu)

        else:
            # ======== RESEP TUNGGAL ========
            tampilkan_resep_jamu(nama_jamu)


        # ============== SETELAH RESEP → TANYA CERITA ==============
        ketik(f"\nMbokSri: Pengin tak critakno sejarah lan ceritaé uga? (iyo/ora): ")
        jawaban_cerita = input_ya_tidak("Aku: ")

        if jawaban_cerita == "iyo":

            # Cerita kombinasi
            if "+" in nama_jamu:
                jamu_list = [j.strip() for j in nama_jamu.split("+")]

                ketik("\nMbokSri: Cerita sing endi rek?")
                for idx, j in enumerate(jamu_list, 1):
                    ketik(f"{idx}. {j}")
                ketik(f"{len(jamu_list)+1}. Loro-lorone")

                pilihan = input("Pilih nomor: ").strip()

                if pilihan == "1":
                    pilih_cerita = [jamu_list[0]]
                elif pilihan == "2":
                    pilih_cerita = [jamu_list[1]]
                else:
                    pilih_cerita = jamu_list

                for j in pilih_cerita:
                    info = ramuan_jatim.get(j)
                    if info and "cerita" in info:
                        ketik(f"\n{CYAN}Cerita {j}:{RESET}")
                        ketik(info['cerita'], delay=0.02)
                        print()

                ketik("MbokSri: Saiki wes ngerti critane rek!")
            
            # Cerita tunggal
            else:
                info = ramuan_jatim.get(nama_jamu)
                if info and "cerita" in info:
                    ketik(f"\n{CYAN}Cerita {nama_jamu}:{RESET}")
                    ketik(info['cerita'], delay=0.02)
                    ketik("MbokSri: Saiki wes ngerti critane rek!")
        
        else:
            ketik("MbokSri: Yo wes, ora popo rek. Sing penting wes iso nggawe jamune! 😊")
            return

    else:
        # ============== GAMAU RESEP → TANYA CERITA SAJA ==============
        ketik(f"\nMbokSri: Pengin tak ceritakno sejarah lan ceritaé ora? (iyo/ora): ")
        jawaban_cerita = input_ya_tidak("Aku: ")

        if jawaban_cerita == "iyo":
            info = ramuan_jatim.get(nama_jamu)
            if info and "cerita" in info:
                ketik(f"\n{CYAN}Cerita {nama_jamu}:{RESET}")
                ketik(info['cerita'], delay=0.02)
                ketik("MbokSri: Saiki wes ngerti critane rek!")
        else:
            ketik("MbokSri: Sip rek, yen butuh jamu maneh tak bantu maneh!")
