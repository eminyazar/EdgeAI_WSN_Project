import matplotlib.pyplot as plt
import matplotlib.patches as patches

class NetworkVisualizer:
    """Ağ topolojisini ve simülasyon metriklerini görselleştiren sınıf."""
    
    def __init__(self, net_manager):
        self.net = net_manager
        
    def plot_topology(self):
        """Düğümlerin konumlarını ve Gateway kapsama alanını çizer."""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # 1. Gateway'i (Merkezi) Çiz
        ax.scatter(self.net.gateway_pos[0], self.net.gateway_pos[1], 
                   c='red', marker='^', s=200, label='Gateway')
        
        # 2. Kapsama Alanını (Menzili) Çiz
        circle = patches.Circle(self.net.gateway_pos, self.net.max_range, 
                                fill=False, color='red', linestyle='--', alpha=0.5, 
                                label=f'Coverage Area (R={self.net.max_range})')
        ax.add_patch(circle)
        
        # 3. Düğümleri Çiz
        in_range_x, in_range_y = [], []
        out_range_x, out_range_y = [], []
        
        for node in self.net.nodes:
            dist = self.net.calculate_distance_to_gateway(node)
            if dist <= self.net.max_range:
                in_range_x.append(node.x)
                in_range_y.append(node.y)
            else:
                out_range_x.append(node.x)
                out_range_y.append(node.y)
                
        # Menzil içindekiler (Yeşil)
        ax.scatter(in_range_x, in_range_y, c='green', s=50, label='Connected Nodes')
        # Menzil dışındakiler (Gri)
        ax.scatter(out_range_x, out_range_y, c='gray', marker='x', s=50, label='Out of Range')
        
        ax.set_title('WSN Edge AI Topology Visualization')
        ax.set_xlabel('X coordinate')
        ax.set_ylabel('Y coordinate')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Grafiği göster
        plt.show()

    def plot_energy_history(self, energy_history):
        """Zaman içindeki enerji tüketimini çizer."""
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(energy_history) + 1), energy_history, 
                 marker='o', linestyle='-', color='b', linewidth=2)
        
        plt.title('Total Energy Consumption (Edge AI)')
        plt.xlabel('Simulation Cycle')
        plt.ylabel('Total Energy (mJ)')
        plt.grid(True, alpha=0.5)
        
        # Anomali anını işaretle (11. döngü)
        plt.axvline(x=11, color='r', linestyle='--', label='Anomaly (Fire) Start')
        plt.legend()
        
        plt.show()