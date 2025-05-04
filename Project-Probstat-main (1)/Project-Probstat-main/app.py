from flask import Flask, render_template, request
from collections import Counter
import pandas as pd
import os

data = pd.read_csv(os.path.join('tes.csv'))
data.columns = data.columns.str.strip()

app = Flask(__name__)

def filter_players_by_game(game):
    filtered_data = data[data['game'] == game]
    if filtered_data.empty:
        return [], []
    players = []
    for idx, row in enumerate(filtered_data.iterrows(), start=1):
        _, row_data = row
        players.append({
            'no': idx,
            'nama': row_data['name'],
            'lokasi': row_data['location'],
            'gender': row_data['gender'],
            'usia': row_data['age']
        })
    ages = filtered_data['age'].tolist()
    return players, ages

def calculate_stats(ages):
    if not ages:
        return {
            'mean': None,
            'median': None,
            'mode': None,
            'min': None,
            'max': None,
            'total': 0,
            'sorted_ages': [],
            'std_dev': None,
            'range': None,
            'mid_range': None,
            'q1': None,
            'q2': None,
            'q3': None,
            'iqr': None
        }
    
    # Manual calculation without using NumPy
    sorted_ages = sorted(ages)
    n = len(sorted_ages)
    
    # Mean calculation
    total = sum(sorted_ages)
    mean = round(total / n, 2)
    
    # Median calculation
    if n % 2 == 0:
        median = round((sorted_ages[n//2 - 1] + sorted_ages[n//2]) / 2, 2)
    else:
        median = round(sorted_ages[n//2], 2)
    
    # Mode calculation
    freq = Counter(sorted_ages)
    max_freq = max(freq.values())
    mode = [k for k, v in freq.items() if v == max_freq][0]
    
    # Min and Max
    min_age = min(sorted_ages)
    max_age = max(sorted_ages)
    
    # Range calculations
    range_val = max_age - min_age
    mid_range = round((min_age + max_age) / 2, 2)
    
    # Standard deviation calculation
    variance_sum = sum((x - mean) ** 2 for x in sorted_ages)
    std_dev = round((variance_sum / n) ** 0.5, 2)
    
    # Quartile calculations
    def calculate_percentile(data, p):
        # Calculate the position
        position = (n - 1) * (p / 100)
        floor_position = int(position)
        ceil_position = floor_position + 1
        
        if ceil_position >= n:
            return data[floor_position]
        
        # Interpolate if position is not an integer
        if floor_position == position:
            return data[floor_position]
        else:
            return data[floor_position] + (data[ceil_position] - data[floor_position]) * (position - floor_position)
    
    q1 = round(calculate_percentile(sorted_ages, 25), 2)
    q2 = round(calculate_percentile(sorted_ages, 50), 2)
    q3 = round(calculate_percentile(sorted_ages, 75), 2)
    iqr = round(q3 - q1, 2)
    
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
        'q1': q1,
        'q2': q2,
        'q3': q3,
        'iqr': iqr
    }
    return stats

@app.route('/', methods=['GET', 'POST'])
def home():
    players = None
    stats = None
    game = None
    if request.method == 'POST':
        game = request.form['game']
        players, ages = filter_players_by_game(game)
        stats = calculate_stats(ages)
    return render_template('index1.html', players=players, stats=stats, game=game)

if __name__ == '__main__':
    app.run(debug=True)