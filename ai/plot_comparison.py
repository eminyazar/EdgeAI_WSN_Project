import os
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Python'ın 'src' klasörünü bulabilmesi için yol ayarı
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from src.environment import SensorEnvironment

def load_model():
    """Eğitilmiş ML modelini yükler."""
    model_path = os.path.join(root_dir, 'data', 'model.pkl')
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    return None

def old_threshold_logic(temp, gas):
    """Geleneksel eşik değeri mantığı (Akılsız Düğüm)"""
    return temp > 55 or gas > 300

def run_and_plot_comparison(test_samples=600):
    model = load_model()
    if model is None: 
        print("[ERROR] Model not found! Please run 'python -m ai.train' first.")
        return

    print(f"\n[SIMULATION] performing test start with {test_samples} samples ...")

    correct_model, correct_threshold = 0, 0
    false_alarms_model, false_alarms_threshold = 0, 0
    
    # 1. TEST VERİSİ ÜRETİMİ VE TAHMİN
    for i in range(test_samples):
        # 1/3 Normal, 1/3 Gerçek Yangın, 1/3 Kavurucu Yaz Sıcağı (Tuzak Senaryo)
        if i < test_samples // 3:
            temp, gas = np.random.uniform(20, 30), np.random.uniform(70, 90)
            actual_label = 0
        elif i < (test_samples // 3) * 2:
            temp, gas = np.random.uniform(60, 80), np.random.uniform(350, 450)
            actual_label = 1
        else: 
            # Tuzak: Sadece sıcaklık yüksek, gaz düşük. (Yangın yok)
            temp, gas = np.random.uniform(56.0, 65.0), np.random.uniform(80.0, 110.0)
            actual_label = 0

        # AI Kararı
        model_pred = int(model.predict([[temp, gas]])[0])
        # Geleneksel Karar
        threshold_pred = 1 if old_threshold_logic(temp, gas) else 0
        
        # Sonuçları Kaydet
        if model_pred == actual_label: correct_model += 1
        if model_pred == 1 and actual_label == 0: false_alarms_model += 1
            
        if threshold_pred == actual_label: correct_threshold += 1
        if threshold_pred == 1 and actual_label == 0: false_alarms_threshold += 1

    model_acc = (correct_model / test_samples) * 100
    thresh_acc = (correct_threshold / test_samples) * 100

    # 2. MATPLOTLIB İLE GÖRSELLEŞTİRME
    print("[GRAPH] Rendering results...")
    
    labels = ['Accuracy (%)', 'False Alarms\n(Excessive Energy Consumption)']
    edge_ai_scores = [model_acc, false_alarms_model]
    classic_scores = [thresh_acc, false_alarms_threshold]

    x = np.arange(len(labels))  # Etiket konumları
    width = 0.35  # Barların genişliği

    fig, ax = plt.subplots(figsize=(9, 6))
    
    # Barları Çiz
    rects1 = ax.bar(x - width/2, edge_ai_scores, width, label='Edge AI (Random Forest)', color='#2ca02c')
    rects2 = ax.bar(x + width/2, classic_scores, width, label='Classic (If/Else)', color='#d62728')

    # Eksenleri ve Başlıkları Ayarla
    ax.set_ylabel('Score / Count', fontsize=12)
    ax.set_title('Edge AI vs Classic Sensor Networks: Error and Performance Analysis', fontsize=14, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.legend(fontsize=11)

    # Barların üzerine tam sayısal değerleri yazdır
    ax.bar_label(rects1, padding=3, fmt='%.1f', fontsize=11, fontweight='bold')
    ax.bar_label(rects2, padding=3, fmt='%.1f', fontsize=11, fontweight='bold')

    # Görsel Düzenlemeler
    fig.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.show()

if __name__ == "__main__":
    run_and_plot_comparison()