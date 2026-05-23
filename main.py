import random
from src.environment import SensorEnvironment
from src.node import SensorNode
from src.network import NetworkManager
from utils.visualizer import NetworkVisualizer

def run_simulation():
    # 1. Başlatma (Initialization)
    print("--- Edge AI WSN is Running ---\n")
    
    # Dünyayı yarat
    env = SensorEnvironment(base_temp=24.0, base_gas=80.0, noise_level=0.8)
    
    # Ağ yöneticisini kur (Gateway merkezde: 50,50)
    net_manager = NetworkManager(gateway_x=50, gateway_y=50, max_range=60)
    
    # 2. Düğümleri Oluştur ve Sahaya Dağıt
    NODE_COUNT = 20
    for i in range(NODE_COUNT):
        rand_x = random.uniform(0, 100)
        rand_y = random.uniform(0, 100)
        
        # Her bir düğüme çevreyi ve konumunu tanıt
        node = SensorNode(environment=env, x=rand_x, y=rand_y, initial_energy=2000.0)
        net_manager.add_node(node)
    
    print(f"[SYSTEM] {NODE_COUNT} nodes successfully deployed.\n")

    # 3. Simülasyon Döngüsü (Simulation Loop)
    TOTAL_CYCLES = 30
    energy_history = []  # Enerji tüketimini takip etmek için
    
    for cycle in range(1, TOTAL_CYCLES + 1):
        print(f"--- Cycle {cycle} ---")
        
        # Simülasyonun yarısında bir felaket tetikle!
        if cycle == 11:
            env.trigger_anomaly()
        
        # Ağdaki tüm düğümleri çalıştır
        alerts = net_manager.simulate_cycle()
        
        current_total_energy = sum(n.energy for n in net_manager.nodes if n.is_alive)
        energy_history.append(current_total_energy)

        # Eğer bu döngüde bir uyarı alındıysa ekrana bas
        if alerts:
            print(f" >> In this cycle, {len(alerts)} nodes sent CRITICAL alerts!")
        else:
            print(" >> Normal Status: No data transmission (Energy saving achieved).")
            
        # Her 10 döngüde bir ara rapor ver
        if cycle % 10 == 0:
            net_manager.report_status()

    # 4. Final Raporu
    print("\n=== SIMULATION COMPLETED ===")
    net_manager.report_status()
    print("Edge AI prevented unnecessary data traffic and extended network lifespan.")

    # SİMÜLASYON BİTTİKTEN SONRA GRAFİKLERİ ÇİZ
    print("\n[GRAPHS] Graphical visualization is starting. Please close the opened windows to proceed.")
    viz = NetworkVisualizer(net_manager)
    viz.plot_topology() # Önce haritayı çizer
    viz.plot_energy_history(energy_history) # Sonra enerji grafiğini çizer

if __name__ == "__main__":
    run_simulation()