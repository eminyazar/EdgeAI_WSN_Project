import numpy as np
from datetime import datetime

class SensorEnvironment:
    """
    Fiziksel dünyayı ve sensör veri üretimini simüle eden sınıf.
    OOP prensiplerine uygun olarak 'Sensing' sorumluluğunu üstlenir.
    """
    
    def __init__(self, base_temp=22.0, base_gas=100.0, noise_level=0.5):
        # Temel çevresel değerler
        self.base_temp = base_temp
        self.base_gas = base_gas
        self.noise_level = noise_level
        
        # Simülasyon durumu
        self.is_anomaly_active = False
        self.anomaly_start_time = None

    def get_sensor_reading(self):
        """
        Sensör düğümleri için anlık 'kirli' (gürültülü) veri üretir.
        """
        # Normal şartlar altında veri üretimi (Gaussian Noise eklenmiş)
        temp_noise = np.random.normal(0, self.noise_level)
        gas_noise = np.random.normal(0, self.noise_level * 5) # Gaz daha dalgalıdır
        
        current_temp = self.base_temp + temp_noise
        current_gas = self.base_gas + gas_noise

        # Eğer bir anomali (yangın vb.) tetiklendiyse değerleri dramatik artır
        if self.is_anomaly_active:
            current_temp += 40.0 + np.random.uniform(5, 15)
            current_gas += 300.0 + np.random.uniform(50, 100)

        return {
            "temperature": round(current_temp, 2),
            "gas_level": round(current_gas, 2),
            "timestamp": datetime.now().isoformat()
        }

    def trigger_anomaly(self):
        """Simülasyonda bir tehlike durumu (yangın/sızıntı) başlatır."""
        print("\n[ENV] !!! ANOMALİ TETİKLENDİ (Örn: Yangın Başladı) !!!")
        self.is_anomaly_active = True
        self.anomaly_start_time = datetime.now()

    def reset_environment(self):
        """Çevreyi normal değerlerine döndürür."""
        self.is_anomaly_active = False
        print("[ENV] Çevre normale döndü.")