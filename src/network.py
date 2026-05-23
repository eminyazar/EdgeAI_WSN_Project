import math

class NetworkManager:
    """
    Ağ topolojisini, haberleşme menzilini ve veri trafiğini yöneten sınıf.
    Düğümler ile Gateway (Ağ Geçidi) arasındaki köprüdür.
    """
    def __init__(self, gateway_x=50, gateway_y=50, max_range=40):
        self.nodes = []
        self.gateway_pos = (gateway_x, gateway_y)
        self.max_range = max_range  # RF iletişim menzili (birim mesafe)
        
        # Ağ Genel İstatistikleri (Sunum için metrikler)
        self.total_received_alerts = 0
        self.dropped_packets = 0

    def add_node(self, node):
        """Ağa yeni bir sensör düğümü ekler."""
        self.nodes.append(node)

    def calculate_distance_to_gateway(self, node):
        r"""
        Düğümün Gateway'e olan uzaklığını hesaplar.
        Öklid Mesafesi: $$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$
        """
        dist = math.sqrt((node.x - self.gateway_pos[0])**2 + 
                         (node.y - self.gateway_pos[1])**2)
        return dist

    def simulate_cycle(self):
        """Tüm ağın bir zaman dilimindeki hareketini simüle eder."""
        cycle_alerts = []
        
        for node in self.nodes:
            if not node.is_alive:
                continue
            
            # Düğüm kendi iç döngüsünü (Sensing + AI) çalıştırır
            report = node.run_cycle()
            
            # Eğer Edge AI bir tehlike tespit edip mesaj gönderdiyse
            if report and report["status"] == "ALERT":
                distance = self.calculate_distance_to_gateway(node)
                
                # RF Menzil Kontrolü: Düğüm Gateway'e yeterince yakın mı?
                if distance <= self.max_range:
                    self.total_received_alerts += 1
                    cycle_alerts.append(report)
                    print(f"[AĞ] Mesaj Alındı! Düğüm: {node.node_id}, Mesafe: {round(distance, 2)}")
                else:
                    self.dropped_packets += 1
                    print(f"[AĞ] !!! KAYIP PAKET !!! Düğüm {node.node_id} menzil dışında ({round(distance, 2)})")
        
        return cycle_alerts

    def report_status(self):
        """Ağın genel sağlık durumunu özetler."""
        alive_nodes = [n for n in self.nodes if n.is_alive]
        total_energy = sum(n.energy for n in alive_nodes)
        
        print("\n--- AĞ DURUM RAPORU ---")
        print(f"Aktif Düğüm Sayısı: {len(alive_nodes)} / {len(self.nodes)}")
        print(f"Toplam Kalan Enerji: {round(total_energy, 2)} mJ")
        print(f"Başarıyla Alınan Uyarılar: {self.total_received_alerts}")
        print(f"Menzil Nedeniyle Kaybolan Paketler: {self.dropped_packets}")
        print("-----------------------\n")