import random, time
from animations import ketik, BOLD, RESET, GREEN, RED, MAGENTA, CYAN, YELLOW
from datajamu import ramuan_jatim, pantun_jamu, sinonim_jamu
from difflib import SequenceMatcher

# ====== Mode: Tebak Jamu (guess by ingredients) ======
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

#============= Game Tebak Jamu ==============
def mode_tebak_jamu():
    ketik("\n=== MODE TEBAK JAMU ===", delay=0.02)
    ketik("AI bakal nunjukin bahan suatu jamu, kamu kudu nebak jamu sing dimaksud.")
    ketik("Kamu punya 3 kesempatan. Yuk!")
    
    jamus = list(ramuan_jatim.keys())
    target = random.choice(jamus)
    info = ramuan_jatim[target]
    bahan_list = info["bahan"]
    
    # Ganti baris tersebut dengan:
    ketik(f"\n🫖 ===== Bahan-bahan ==== :")
    for bahan in bahan_list:
        ketik(f"   🌿 {bahan}")
    
    attempts = 3
    while attempts > 0:
        guess = input("Tebakanmu: ").strip().lower()
        
        # Normalisasi untuk perbandingan
        guess_clean = guess.replace(" ", "").replace("-", "").replace("_", "")
        target_clean = target.lower().replace(" ", "").replace("-", "").replace("_", "")
        
        # LOGICA PENGEECEKAN YANG BENAR:
        is_correct = (
            # 1. Exact match (case insensitive)
            guess == target.lower() or
            # 2. Clean match (tanpa spasi/hyphen)
            guess_clean == target_clean or
            # 3. Sinonim untuk target spesifik
            (target.lower() in sinonim_jamu and guess in sinonim_jamu[target.lower()]) or
            # 4. Fuzzy matching dengan threshold tinggi
            similarity(guess, target) > 0.85
        )
        
        # DEBUG: Tampilkan informasi untuk testing (bisa dihapus setelah fix)
        # print(f"DEBUG: Target='{target}', Guess='{guess}', Correct={is_correct}")
        # if target.lower() in sinonim_jamu:
        #     print(f"DEBUG: Sinonim target: {sinonim_jamu[target.lower()]}")
        
        if is_correct:
            ketik(f"{GREEN}Wah bener rek! Jawaban: {target}{RESET}")
            ketik(f"AI: Cerita singkat: {info.get('cerita','-')}")
            return
        else:
            attempts -= 1
            if attempts > 0:
                # Beri feedback yang lebih membantu
                similarity_score = similarity(guess, target)
                if similarity_score > 0.7:
                    ketik(f"{YELLOW}Hampir! Cek ejaan maning. Kesempatan: {attempts}")
                else:
                    ketik(f"Aduh salah. Kesempatan tersisa: {attempts}")
    
    ketik(f"{RED}Habis kesempatan! Jawaban sing bener yaiku: {target}{RESET}")
    ketik(f"Manfaat: {info.get('manfaat','-')}")

def menu_pantun():
    while True:
        ketik("\n=== MENU PANTUN JAMU ===")
        ketik("1. Ndelok daftar jamu")
        ketik("2. Ndelok pantun jamu")
        ketik("3. Kembali")

        pilih = input("Pilih menu (1/2/3): ").strip()

        if pilih == "1":
            ketik("\nDaftar Jamu:")
            for jamu in pantun_jamu:
                ketik(f"- {jamu}")  # Tampilkan aslinya (capital case)

        elif pilih == "2":
            nama_input = input("lebokno jenege jamu: ").strip().lower()
            
            # ===== CARI JAMU YANG COCOK =====
            jamu_found = None
            
            # 1. Cari exact match di keys pantun_jamu (case insensitive)
            for jamu_key in pantun_jamu.keys():
                if nama_input == jamu_key.lower():
                    jamu_found = jamu_key
                    break
            
            # 2. Jika tidak ketemu, cari dengan normalisasi (tanpa spasi/dash)
            if not jamu_found:
                nama_input_clean = nama_input.replace(" ", "").replace("-", "").replace("_", "")
                for jamu_key in pantun_jamu.keys():
                    jamu_clean = jamu_key.lower().replace(" ", "").replace("-", "").replace("_", "")
                    if nama_input_clean == jamu_clean:
                        jamu_found = jamu_key
                        break
            
            # 3. Jika masih tidak ketemu, cari di sinonim
            if not jamu_found:
                nama_input_clean = nama_input.replace(" ", "").replace("-", "").replace("_", "")
                for jamu_key in pantun_jamu.keys():
                    jamu_lower = jamu_key.lower()
                    if jamu_lower in sinonim_jamu:
                        sinonim_clean = [s.replace(" ", "").replace("-", "").replace("_", "") 
                                       for s in sinonim_jamu[jamu_lower]]
                        if nama_input_clean in sinonim_clean:
                            jamu_found = jamu_key
                            break
            # =============================

            if jamu_found:
                ketik("\n--- PANTUN JAMU ---")
                ketik(pantun_jamu[jamu_found])
            else:
                ketik("Jamu ora ditemukne bess... 😅")

        elif pilih == "3":
            break

        else:
            ketik("Pilihan tidak valid!")