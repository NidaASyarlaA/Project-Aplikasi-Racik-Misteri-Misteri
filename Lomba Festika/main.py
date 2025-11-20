from textwrap import dedent
from animations import ketik, BOLD, CYAN, RESET
from menus import Obrolan, list_jamu_names
from minigames import mode_tebak_jamu, menu_pantun

# ====== Main menu UI ======
def main_menu():
    banner = dedent(f"""\n
    {BOLD}{CYAN}=== RACIK MISTERI — Mboksri ==={RESET}
    Pilih mode:
      1) Rekomendasi jamu
      2) Tebak Jamu (game)
      3) Pantun Jamu
      4) Daftar jamu
      5) Metu
    """)
    print(banner)
    while True:
        pilihan = input("Lebokno pilihan (1-5): ").strip()
        if pilihan == "1":
            Obrolan()
        elif pilihan == "2":
            mode_tebak_jamu()
        elif pilihan == "3":
            menu_pantun()
        elif pilihan == "4":
            list_jamu_names()
        elif pilihan == "5":
            ketik("\nMbokSri: Matur nuwun wis nyoba Racik Misteri. Muga-Muga tambah sehat yo rek!", suara=False)
            break
        else:
            ketik("Pilih 1-5.")

# ====== Program entrypoint ======
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        ketik("\n\nMbokSri: Oke rek, kapan-kapan maneh yo. Semoga sehat!")
