import time
import requests
import random
import string
from ayarlar import TOKEN

# --- AYARLAR ---
DISCORD_API = "https://discord.com/api/v9/users/@me/pomelo-attempt"
HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

DELAY = 3

CHARS = string.ascii_lowercase + string.digits  # harf + rakam

def generate_random_name(length=4):
    return ''.join(random.choice(CHARS) for _ in range(length))

def save_to_file(username):
    with open("approved.txt", "a", encoding="utf-8") as f:
        f.write(f"{username}\n")

def check_username(username):
    """Kullanıcı adının dolu/boş durumunu kontrol eder"""
    try:
        res = requests.post(DISCORD_API, headers=HEADERS, json={"username": username})

        if res.status_code == 429:
            retry = res.json().get("retry_after", 10)
            print(f"\nRATE LIMIT! {retry} saniye bekleniyor...")
            time.sleep(retry + 2)
            return None  # tekrar dene sinyali

        if res.status_code == 200:
            return res.json().get("taken") is False

        print(f"Hata: {res.status_code}")
        return False

    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        time.sleep(5)
        return None

def prefix_bruteforce(prefix):
    """İlk 3 haneye göre 10 farklı deneme yapar"""
    print(f"→ Prefix modu: {prefix}*** deneniyor")

    tried = set()
    attempts = 0

    while attempts < 10:
        char = random.choice(CHARS)
        if char in tried:
            continue

        tried.add(char)
        attempts += 1

        username = prefix + char
        print(f"  Deneniyor: {username}...", end=" ", flush=True)

        result = check_username(username)

        if result is None:
            continue

        if result:
            print("BULDUM! Kaydediliyor...")
            save_to_file(username)
            return True
        else:
            print("Dolu.")

        time.sleep(DELAY)

    print("→ Prefix tutmadı, normale devam ediliyor.")
    return False

def auto_checker():
    print("Sniper Başlatıldı")

    tested_names = set()

    while True:
        username = generate_random_name(4)

        if username in tested_names:
            continue

        tested_names.add(username)
        print(f"Deneniyor: {username}...", end=" ", flush=True)

        result = check_username(username)

        if result is None:
            continue

        if result:
            print("BULDUM!")

            save_to_file(username)

            prefix = username[:3]
            prefix_bruteforce(prefix)

        else:
            print("Dolu.")

        time.sleep(DELAY)

if __name__ == "__main__":
    auto_checker()
