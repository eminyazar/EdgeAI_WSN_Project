# Edge AI in Wireless Sensor Networks (WSN) 📡🧠
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)<br>
A lightweight, object-oriented Python simulation framework demonstrating the impact of Edge Artificial Intelligence on Wireless Sensor Networks. 

## 📌 Overview
In traditional WSNs, sensor nodes act as "dumb" collectors, constantly transmitting raw data to a central cloud/gateway. This leads to high energy consumption (battery drain), network congestion, and high latency. 

This project flips the paradigm by deploying a **Random Forest** machine learning model directly onto the edge nodes. The nodes process environmental data (temperature and gas levels) locally, filtering out noise and only transmitting alerts when a critical anomaly is detected. 

## ✨ Key Features
* **Machine Learning at the Edge:** Uses `scikit-learn` to train and deploy lightweight models for local inference, minimizing False Positives compared to static threshold logic.
* **Energy Drain Simulation:** Mathematically models and tracks the battery life of nodes, proving that local CPU operations cost significantly less energy than RF (Radio Frequency) transmissions.
* **Realistic Network Constraints:** Simulates physical range limits, packet loss, and environmental sensor noise.
* **Rich Visualizations:** Automatically generates network topology maps and time-series energy consumption graphs using `matplotlib`.

## 📂 Project Structure
```text
EdgeAI_WSN_Project/
├── data/                  # Stores trained ML models (.pkl)
├── src/
│   ├── ai/                # Model training and testing scripts
│   ├── core/              # OOP Core classes (BaseNode, NetworkManager, Environment)
│   └── utils/             # Visualization, helpers, and logging tools
└── main.py                # Main simulation loop entry point
```
📊 Expected Results
  1. main.py<br>
       <img width="600" height="500" alt="Figure_1" src="https://github.com/user-attachments/assets/8ab404ca-d2e2-4e0d-8441-4fbbd28b1cf8" />
       <img width="600" height="500" alt="Figure_2" src="https://github.com/user-attachments/assets/7b0b4a46-2e79-4d06-a7b2-14a6d6fbabd6" />

  2. plot_comparison.py<br>
     <img width="600" height="500" alt="Ekran görüntüsü 2026-05-23 191617" src="https://github.com/user-attachments/assets/8681dc1d-8d36-458d-a622-cf534f5cd62d" />

1. Install Dependencies
   ```text
   pip install numpy scikit-learn matplotlib
   ```
  
