from flask import Flask, render_template, request
from collections import Counter
import os
import csv

app = Flask(__name__)

# Direktori data (buat jika belum ada)
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Fungsi untuk membaca data dari CSV
def load_player_data(game_name):
    try:
        csv_path = os.path.join(data_dir, f"{game_name.lower().replace(' ', '_')}_players.csv")
        players = []
        ages = []
        
        # Jika file CSV belum ada, buat file kosong yang akan diproses nanti
        if not os.path.exists(csv_path):
            return [], []
            
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader, start=1):
                player = {
                    'no': i,
                    'nama': row['nama'],
                    'lokasi': row['lokasi'],
                    'gender': row['gender'],
                    'usia': int(row['usia'])
                }
                players.append(player)
                ages.append(int(row['usia']))
                
        return players, ages
    except Exception as e:
        print(f"Error loading data: {e}")
        return [], []

def calculate_stats(ages):
    if not ages:
        return None
        
    # Urutkan data usia untuk memudahkan perhitungan
    sorted_ages = sorted(ages)
    n = len(sorted_ages)
    
    # Hitung frekuensi untuk modus
    freq = Counter(sorted_ages)
    
    # Hitung statistik dasar
    mean = round(sum(sorted_ages) / n, 2)
    median = sorted_ages[n//2] if n % 2 else (sorted_ages[n//2 - 1] + sorted_ages[n//2]) / 2
    mode = [k for k, v in freq.items() if v == max(freq.values())][0]  # Mendapatkan nilai modus pertama jika ada beberapa
    min_age = min(sorted_ages)
    max_age = max(sorted_ages)
    
    # Hitung standar deviasi
    variance = sum((x - mean) ** 2 for x in sorted_ages) / n
    std_dev = round(variance ** 0.5, 2)
    
    # Hitung range dan mid range
    range_val = max_age - min_age
    mid_range = round((min_age + max_age) / 2, 2)
    
    # Hitung kuartil
    q1_pos = n // 4
    q2_pos = n // 2
    q3_pos = q1_pos * 3
    
    # Untuk menangani kasus genap dan ganjil
    q1 = sorted_ages[q1_pos] if n % 4 else (sorted_ages[q1_pos-1] + sorted_ages[q1_pos]) / 2
    q2 = median  # Q2 sama dengan median
    q3 = sorted_ages[q3_pos] if n % 4 else (sorted_ages[q3_pos-1] + sorted_ages[q3_pos]) / 2
    
    # Hitung interquartile range (IQR)
    iqr = q3 - q1
    
    # Kembalikan hasil sebagai dictionary
    stats = {
        'mean': mean,
        'median': median,
        'mode': mode,
        'min': min_age,
        'max': max_age,
        'total': n,
        'sorted_ages': sorted_ages,
        'std_dev': std_dev,
        'range': range_val,
        'mid_range': mid_range,
        'q1': round(q1, 2),
        'q2': round(q2, 2),
        'q3': round(q3, 2),
        'iqr': round(iqr, 2)
    }
    return stats

# Membuat file CSV jika belum ada (hanya dilakukan sekali di awal)
def create_sample_csv_files():
    # Data pemain lengkap (15 pemain per game) dengan nama lengkap
    game_players = {
        'Free Fire': [
            'Ahmad Fauzi', 'Budi Santoso', 'Citra Dewi', 'Dian Anggraeni', 'Eko Prasetyo',
            'Fitriani Wulandari', 'Gunawan Setiawan', 'Hana Lestari', 'Irfan Maulana', 'Jasmine Putri',
            'Kevin Kurniawan', 'Lia Rahmawati', 'Maman Suherman', 'Nina Permata', 'Oscar Wijaya'
        ],
        'PUBG': [
            'Pandu Setiawan', 'Qonita Zahra', 'Rizky Ramadhan', 'Siti Nurhaliza', 'Taufik Hidayat',
            'Umar Abdullah', 'Vina Melinda', 'Wahyu Pratama', 'Xavier Tan', 'Yuni Shara',
            'Zulkifli Hasan', 'Aisyah Rahman', 'Bambang Sutejo', 'Cindy Claudia', 'Dodi Kurniawan'
        ],
        'Mobile Legends': [
            'Erika Sutanto', 'Fajar Ramadan', 'Guntur Soekarno', 'Hesti Purwanti', 'Indra Lesmana',
            'Joko Widodo', 'Kartika Sari', 'Luna Maya', 'Muhammad Ali', 'Nadia Karina',
            'Oki Setiana', 'Prabowo Subianto', 'Queen Hasna', 'Rafi Ahmad', 'Susi Susanti'
        ]
    }
    
    # Lokasi berbeda untuk setiap kategori game
    game_locations = {
        'Free Fire': [
            'Jakarta', 'Bandung', 'Surabaya', 'Medan', 'Bogor',
            'Tangerang', 'Depok', 'Semarang', 'Solo', 'Yogyakarta',
            'Malang', 'Denpasar', 'Makassar', 'Palembang', 'Padang'
        ],
        'PUBG': [
            'Balikpapan', 'Banjarmasin', 'Manado', 'Pontianak', 'Lampung',
            'Pekanbaru', 'Jambi', 'Bengkulu', 'Bandar Lampung', 'Samarinda',
            'Jayapura', 'Sorong', 'Ambon', 'Ternate', 'Kupang'
        ],
        'Mobile Legends': [
            'Aceh', 'Medan', 'Batam', 'Tanjung Pinang', 'Padang Sidempuan',
            'Bukittinggi', 'Dumai', 'Tanjung Balai', 'Binjai', 'Sibolga',
            'Mataram', 'Bima', 'Kediri', 'Madiun', 'Probolinggo'
        ]
    }
    
    genders = ['Laki-laki', 'Perempuan']
    
    # Definisikan usia dan gender tetap untuk konsistensi data
    player_data = {
        'Free Fire': [
            {'usia': 19, 'gender': 'Laki-laki'},
            {'usia': 22, 'gender': 'Laki-laki'},
            {'usia': 25, 'gender': 'Perempuan'},
            {'usia': 18, 'gender': 'Perempuan'},
            {'usia': 27, 'gender': 'Laki-laki'},
            {'usia': 21, 'gender': 'Perempuan'},
            {'usia': 24, 'gender': 'Laki-laki'},
            {'usia': 20, 'gender': 'Perempuan'},
            {'usia': 26, 'gender': 'Laki-laki'},
            {'usia': 23, 'gender': 'Perempuan'},
            {'usia': 29, 'gender': 'Laki-laki'},
            {'usia': 17, 'gender': 'Perempuan'},
            {'usia': 30, 'gender': 'Laki-laki'},
            {'usia': 19, 'gender': 'Perempuan'},
            {'usia': 28, 'gender': 'Laki-laki'}
        ],
        'PUBG': [
            {'usia': 23, 'gender': 'Laki-laki'},
            {'usia': 18, 'gender': 'Perempuan'},
            {'usia': 25, 'gender': 'Laki-laki'},
            {'usia': 22, 'gender': 'Perempuan'},
            {'usia': 31, 'gender': 'Laki-laki'},
            {'usia': 27, 'gender': 'Laki-laki'},
            {'usia': 19, 'gender': 'Perempuan'},
            {'usia': 24, 'gender': 'Laki-laki'},
            {'usia': 20, 'gender': 'Laki-laki'},
            {'usia': 29, 'gender': 'Perempuan'},
            {'usia': 21, 'gender': 'Laki-laki'},
            {'usia': 26, 'gender': 'Perempuan'},
            {'usia': 35, 'gender': 'Laki-laki'},
            {'usia': 17, 'gender': 'Perempuan'},
            {'usia': 28, 'gender': 'Laki-laki'}
        ],
        'Mobile Legends': [
            {'usia': 21, 'gender': 'Perempuan'},
            {'usia': 24, 'gender': 'Laki-laki'},
            {'usia': 19, 'gender': 'Laki-laki'},
            {'usia': 27, 'gender': 'Perempuan'},
            {'usia': 22, 'gender': 'Laki-laki'},
            {'usia': 30, 'gender': 'Laki-laki'},
            {'usia': 20, 'gender': 'Perempuan'},
            {'usia': 26, 'gender': 'Perempuan'},
            {'usia': 32, 'gender': 'Laki-laki'},
            {'usia': 18, 'gender': 'Perempuan'},
            {'usia': 29, 'gender': 'Laki-laki'},
            {'usia': 25, 'gender': 'Laki-laki'},
            {'usia': 23, 'gender': 'Perempuan'},
            {'usia': 33, 'gender': 'Laki-laki'},
            {'usia': 17, 'gender': 'Perempuan'}
        ]
    }
    
    # Buat CSV untuk setiap game
    for game, names in game_players.items():
        csv_path = os.path.join(data_dir, f"{game.lower().replace(' ', '_')}_players.csv")
        
        # Skip jika file sudah ada
        if os.path.exists(csv_path):
            continue
            
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['nama', 'lokasi', 'gender', 'usia']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for i, name in enumerate(names):
                player_info = player_data[game][i]
                # Gunakan lokasi yang spesifik untuk game ini
                lokasi = game_locations[game][i]
                
                writer.writerow({
                    'nama': name,
                    'lokasi': lokasi,
                    'gender': player_info['gender'],
                    'usia': player_info['usia']
                })

@app.route('/', methods=['GET', 'POST'])
def home():
    # Pastikan file CSV dibuat di awal
    create_sample_csv_files()
    
    players = None
    stats = None
    game = None
    
    if request.method == 'POST':
        game = request.form['game']
        players, ages = load_player_data(game)
        stats = calculate_stats(ages)
    
    return render_template('index.html', players=players, stats=stats, game=game)

if __name__ == '__main__':
    app.run(debug=True)