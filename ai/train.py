import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from src.environment import SensorEnvironment

def generate_training_data(samples=1000):
    env = SensorEnvironment(noise_level=1.2)
    X, y = [], []

    print("[TRAIN] Veri seti oluşturuluyor...")
    for _ in range(samples):
        # Normal veri üret
        env.is_anomaly_active = False
        read = env.get_sensor_reading()
        X.append([read["temperature"], read["gas_level"]])
        y.append(0) # Normal

        # Anomali verisi üret
        env.is_anomaly_active = True
        read = env.get_sensor_reading()
        X.append([read["temperature"], read["gas_level"]])
        y.append(1) # Anomali/Yangın

        #zorlu senaryo: Gürültülü ama normal veri
        X.append([np.random.uniform(56.0, 65.0), np.random.uniform(80.0, 110.0)])
        y.append(0)

    return np.array(X), np.array(y)

def train_and_save_model():
    X, y = generate_training_data()
    
    # Random Forest Modelini Oluştur
    # n_estimators=5: TinyML kısıtları için modeli küçük tutuyoruz.
    model = RandomForestClassifier(n_estimators=5, max_depth=3)
    model.fit(X, y)
    
    # Modeli 'data' klasörüne kaydet
    with open('data/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("[TRAIN] Model eğitildi ve 'data/model.pkl' olarak kaydedildi!")

if __name__ == "__main__":
    train_and_save_model()