import requests
import pandas as pd
import os

def upload_file_with_token(file_path, folder_id, token):
    url = "https://store1.gofile.io/contents/uploadfile"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    files = {
        "file": open(file_path, "rb")
    }
    data = {
        "folderId": folder_id
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    response.raise_for_status()  # Memeriksa apakah permintaan berhasil

    return response.json()

def download_image(image_url):
    response = requests.get(image_url, stream=True)
    response.raise_for_status()  # Memeriksa apakah permintaan berhasil
    return response.content

def main():
    csv_file_path = 'bumble_data_clean.csv'  # Ganti dengan path ke file CSV lokal Anda
    folder_id = 'c037159f-36cb-4372-b0a3-7f049d89c8da'  # Ganti dengan folder ID Anda
    token = '7hbw4ERMXGzuFHtxGVtWjILkmjrYwVtf'  # Ganti dengan token Anda

    # Membaca CSV dari file lokal
    df = pd.read_csv(csv_file_path)

    # Iterasi melalui kolom image_link dan unggah setiap gambar ke gofile.io
    for idx, row in df.iterrows():
        image_url = row['Image_link']
        image_data = download_image(image_url)
        
        # Simpan gambar sementara untuk diunggah
        temp_image_path = f"temp_image_{idx}.jpg"
        with open(temp_image_path, 'wb') as f:
            f.write(image_data)

        # Unggah gambar ke gofile.io
        result = upload_file_with_token(temp_image_path, folder_id, token)
        print(f"Gambar {idx} diunggah dengan hasil: {result}")

        # Hapus gambar sementara setelah diunggah
        os.remove(temp_image_path)

if __name__ == "__main__":
    main()
