import streamlit as st
import requests
import os
import random
import string
import uuid
import time

def read_random_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        random_index = random.randint(0, len(lines) - 1)
        random_line = lines[random_index].strip()
        return random_line

def clean_cookies(cookies):
    cleaned_cookies = ''.join(filter(lambda x: x in string.printable, cookies))
    return cleaned_cookies

def generate_random_uuid():
    # Generate a UUID version 4
    random_uuid = uuid.uuid4()
    return str(random_uuid)

def main(session_id, manual_input, manual_sleep_time):
    cookies_file_path = 'vcookie.txt'

    if not os.path.exists(cookies_file_path):
        st.error("File cookie tidak ditemukan: vcookie.txt")
        return

    while True:
        cookie = read_random_line(cookies_file_path)
        cookie = clean_cookies(cookie)

        json_data = {
            'uuid': generate_random_uuid(),
            'ver': 1,
        }

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
            "Client-Info": "os=2;platform=9;scene_id=17",
            "Content-Type": "application/json",
            "Cookie": cookie,
            "Sec-Ch-Ua": '"Not_A Brand";v="99", "Chromium";v="88"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/88.0.4324.150 Safari/537.36"
        }

        response = requests.post(
            f'https://live.shopee.co.id/api/v1/session/{session_id}/join',  # Gunakan input sesi pengguna
            headers=headers,
            json=json_data,
        )

        response_json = response.json()
        if 'data' in response_json and 'session' in response_json['data']:
            st.text("Permintaan berhasil dikirim.")
        else:
            st.text("Gagal mengirim permintaan.")

        # Memutuskan waktu tidur berdasarkan masukan pengguna
        if manual_input == "ya":
            st.write(f"Menunggu {manual_sleep_time} detik sebelum mengirim permintaan berikutnya...")
            time.sleep(manual_sleep_time)
        else:
            random_sleep_time = random.randint(5, 8)  # Waktu tidur antara 5 hingga 8 detik
            st.write(f"Menunggu {random_sleep_time} detik sebelum mengirim permintaan berikutnya...")
            time.sleep(random_sleep_time)

def main_streamlit():
    st.title("Shopee API Client")

    session_id = st.text_input("Masukkan ID sesi:")
    manual_input = st.radio("Apakah Anda ingin menggunakan waktu tidur manual?", ("Ya", "Tidak"))
    manual_sleep_time = None

    if manual_input == "Ya":
        manual_sleep_time = st.number_input("Masukkan waktu tidur manual (dalam detik):")

    if st.button("Kirim Permintaan"):
        main(session_id, manual_input.lower(), manual_sleep_time)

if __name__ == "__main__":
    main_streamlit()
