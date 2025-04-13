from flask import Flask, render_template, request
import random
from collections import Counter
import numpy as np

app = Flask(__name__)

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

locations = ['Jakarta', 'Bandung', 'Surabaya', 'Medan', 'Yogyakarta', 'Bali', 'Makassar', 'Palembang', 'Balikpapan', 'Semarang']
genders = ['Laki-laki', 'Perempuan']

def generate_players(game):
    names = game_players[game]
    players = []
    ages = []
    for i, name in enumerate(names, start=1):
        usia = random.randint(17, 35)
        pemain = {
            'no': i,
            'nama': name,
            'lokasi': random.choice(locations),
            'gender': random.choice(genders),
            'usia': usia
        }
        players.append(pemain)
        ages.append(usia)
    return players, ages

def calculate_stats(ages):
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

@app.route('/', methods=['GET', 'POST'])
def home():
    players = None
    stats = None
    game = None
    if request.method == 'POST':
        game = request.form['game']
        players, ages = generate_players(game)
        stats = calculate_stats(ages)
    return render_template('index.html', players=players, stats=stats, game=game)

if __name__ == '__main__':
    app.run(debug=True)