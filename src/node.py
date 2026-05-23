import uuid
import time
import os
import pickle

class BaseNode:
    """
    Tüm ağ düğümleri için temel sınıf (Abstract Base).
    Kimlik, konum ve enerji yönetimini sağlar.
    """
    def __init__(self, x=0, y=0, initial_energy=1000.0):
        self.node_id = str(uuid.uuid4())[:8]  # Benzersiz kısa ID
        self.x = x
        self.y = y
        self.energy = initial_energy  # Birim: milli-Joule (mJ)
        self.is_alive = True

    def consume_energy(self, amount, task_name="Task"):
        """Enerji tüketimi simülasyonu."""
        if not self.is_alive:
            return False
        
        self.energy -= amount
        if self.energy <= 0:
            self.energy = 0
            self.is_alive = False
            print(f"[NODE {self.node_id}] ENERJİ BİTTİ - Çevrimdışı.")
        return self.is_alive

class SensorNode(BaseNode):
    """
    Edge AI yeteneklerine sahip Akıllı Sensör Düğümü.
    """
    def __init__(self, environment, x=0, y=0, initial_energy=5000.0):
        super().__init__(x, y, initial_energy)
        self.environment = environment
        
        # Enerji Tüketim Katsayıları (Örnek değerler)
        self.costs = {
            "sensing": 0.5,      # Veri okuma maliyeti
            "inference": 2.5,    # Edge AI (Yerel işlem) maliyeti
            "transmit": 15.0     # RF ile veri gönderme maliyeti (EN YÜKSEK!)
        }
        
        self.sent_packets_count = 0
        self.model = self.load_ai_model()

    def load_ai_model(self):
        """Eğitilmiş AI modelini yükler (örneğin, Random Forest)."""
        model_path = 'data/model.pkl'
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        return None
    
    def edge_ai_decision(self, data):
        if self.model:
            features = [[data["temperature"], data["gas_level"]]]
            prediction = self.model.predict(features)
            return bool(prediction[0])

    def run_cycle(self):
        """Düğümün bir simülasyon döngüsünde yaptığı işlemler."""
        if not self.is_alive:
            return None

        start_time = time.time()

        # 1. Sensing (Algılama)
        self.consume_energy(self.costs["sensing"], "Sensing")
        data = self.environment.get_sensor_reading()

        # 2. Edge AI Inference (Yerel İşlem)
        # Burası AI modelinin karar verdiği yer.
        self.consume_energy(self.costs["inference"], "Inference")
        is_critical = self.edge_ai_decision(data)

        # 3. Communication (Haberleşme Kararı)
        # SADECE kritik bir durum varsa veriyi gönder (Edge AI Tasarrufu!)
        if is_critical:
            self.transmit_data(data)
            return {"status": "ALERT", "node": self.node_id, "data": data}
        
        end_time = time.time()
        processing_duration = (end_time - start_time) * 1000  # ms cinsinden

        return {"status": "SUCCESS", "duration_ms": round(processing_duration, 4)}


    def transmit_data(self, data):
        """Veriyi RF üzerinden Gateway'e gönderir."""
        if self.consume_energy(self.costs["transmit"], "Transmit"):
            self.sent_packets_count += 1
            # Gerçek bir sistemde burada radyo modülü (LoRa/Zigbee) tetiklenir.