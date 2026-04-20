import requests
import time
import math

# Configuration
PHI = (1 + math.sqrt(5)) / 2
H = 2 / (PHI ** 3)          # Helical operator ≈ 0.472
T_45 = 1 / 4.5              # ≈ 0.222 s
OMEGA0 = 1.0                # Base amplitude - scale as needed (0.1-5 μJ/cm² range)

def get_sr_power():
    # Replace with your actual SR data source (public API or local station)
    # Example placeholder - adapt to real magnetometer feed
    try:
        response = requests.get("https://your-sr-api.example.com/power/4.5hz")
        data = response.json()
        return data.get("power", 0.0)
    except:
        return 0.0  # fallback

def compute_n_local(sr_power, baseline=1.0, threshold=2.0):
    normalized = max(0, (sr_power - baseline) / threshold)
    return 0.05 * normalized

# Main loop - run while driving
while True:
    sr_power = get_sr_power()
    n_local = compute_n_local(sr_power)
    
    k = 0  # increment per pulse
    omega_k = OMEGA0 * (PHI**k / math.sqrt(5)) * H * n_local
    phase = math.cos(math.pi * time.time() / (2 * T_45))
    
    # Send to AWG (adapt to your hardware API)
    print(f"k={k} | N_local={n_local:.4f} | Ω_k={omega_k:.4f} | phase={phase:.4f}")
    
    time.sleep(0.01)  # adjust timing as needed
