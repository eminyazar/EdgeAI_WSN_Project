import os
import pickle
import numpy as np
from src.environment import SensorEnvironment

def load_model():
    """Eğitilmiş modeli yükler."""
    model_path = 'data/model.pkl'
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    else:
        print("[HATA] Model bulunamadı! Lütfen önce ai/train.py dosyasını çalıştırın.")
        return None

def old_threshold_logic(temp, gas):
    """Eski, akıllı olmayan sistemin karar mekanizması (If/Else)"""
    return temp > 55 or gas > 300

def run_performance_test(test_samples=600):
    model = load_model()
    if model is None: return

    print("\n--- YZ Modeli vs Klasik Kural (If/Else) Testi Başlıyor ---")
    
    correct_model, correct_threshold = 0, 0
    false_alarms_model, false_alarms_threshold = 0, 0
    
    for i in range(test_samples):
        # Veriyi üçe bölüyoruz: Normal, Yangın ve ZORLU (Yaz Sıcağı)
        if i < test_samples // 3:
            # Normal
            temp, gas = np.random.uniform(20, 30), np.random.uniform(70, 90)
            actual_label = 0
        elif i < (test_samples // 3) * 2:
            # Gerçek Yangın
            temp, gas = np.random.uniform(60, 80), np.random.uniform(350, 450)
            actual_label = 1
        else:
            # ZORLU SENARYO: Kavurucu Yaz Günü
            temp, gas = np.random.uniform(56.0, 65.0), np.random.uniform(80.0, 110.0)
            actual_label = 0 # Yangın YOK!

        # Tahminler
        model_pred = int(model.predict([[temp, gas]])[0])
        threshold_pred = 1 if old_threshold_logic(temp, gas) else 0
        
        # Doğruluk Kontrolü
        if model_pred == actual_label: correct_model += 1
        if model_pred == 1 and actual_label == 0: false_alarms_model += 1
            
        if threshold_pred == actual_label: correct_threshold += 1
        if threshold_pred == 1 and actual_label == 0: false_alarms_threshold += 1

    # Metrikleri Hesapla
    model_accuracy = (correct_model / test_samples) * 100
    threshold_accuracy = (correct_threshold / test_samples) * 100
    
    print("\n=== TEST SONUÇLARI ===")
    print(f"Yapay Zeka (Random Forest) Doğruluğu: %{model_accuracy:.2f}")
    print(f"Klasik Kural (If/Else) Doğruluğu:     %{threshold_accuracy:.2f}")
    print("-" * 40)
    print(f"YZ Yanlış Alarm Sayısı:     {false_alarms_model}")
    print(f"Klasik Yanlış Alarm Sayısı: {false_alarms_threshold}")
    print("-" * 40)
    
    if model_accuracy > threshold_accuracy:
        print("[KANIT] Yapay Zeka, sensör gürültülerini filtrelemeyi öğrenmiş!")
        print("Geleneksel yöntem çok fazla 'Yanlış Alarm' verip enerjiyi boşa harcarken, Edge AI sistemi ağı koruyor.")
    else:
        print("[BİLGİ] Veri çok temiz olduğu için her iki yöntem de benzer çalışıyor.")

if __name__ == "__main__":
    run_performance_test()