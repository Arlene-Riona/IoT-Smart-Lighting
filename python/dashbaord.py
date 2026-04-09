import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# --- Configuration ---
PORT = 'COM3'        # change to your port from Arduino IDE
BAUD_RATE = 9600
MAX_POINTS = 60      # show last 60 seconds on graph

# --- Data Storage ---
times       = deque(maxlen=MAX_POINTS)
ldr_values  = deque(maxlen=MAX_POINTS)
brightness  = deque(maxlen=MAX_POINTS)
pir_values  = deque(maxlen=MAX_POINTS)
energy      = deque(maxlen=MAX_POINTS)

# --- Open Serial ---
try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {PORT}")
except:
    print(f"Could not connect to {PORT} - check your port!")
    exit()

# --- Setup Figure ---
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Smart IoT Lighting Dashboard', fontsize=16, fontweight='bold')

ax_ldr        = axes[0, 0]  # top left
ax_brightness = axes[0, 1]  # top right
ax_pir        = axes[1, 0]  # bottom left
ax_energy     = axes[1, 1]  # bottom right

def calculate_brightness(ldr):
    return 255 - (ldr / 1023.0 * 255)

def update(frame):
    # --- Read Serial Line ---
    try:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            return
        
        values = line.split(',')
        if len(values) != 4:
            return

        # --- Parse Values ---
        currentTime  = int(values[0])
        ldrValue     = int(values[1])
        pirValue     = int(values[2])
        timeLedIsOn  = int(values[3])
        brightnessVal = calculate_brightness(ldrValue)

        # --- Store Values ---
        times.append(currentTime)
        ldr_values.append(ldrValue)
        brightness.append(brightnessVal if pirValue == 1 else 0)
        pir_values.append(pirValue)
        energy.append(timeLedIsOn)

        # --- Plot 1: LDR Value ---
        ax_ldr.clear()
        ax_ldr.plot(list(times), list(ldr_values), color='orange', linewidth=2)
        ax_ldr.set_title('Natural Light Level (LDR)')
        ax_ldr.set_ylabel('LDR Value (0-1023)')
        ax_ldr.set_xlabel('Time (seconds)')
        ax_ldr.set_ylim(0, 1023)
        ax_ldr.fill_between(list(times), list(ldr_values), alpha=0.3, color='orange')

        # --- Plot 2: Brightness ---
        ax_brightness.clear()
        ax_brightness.plot(list(times), list(brightness), color='yellow', linewidth=2)
        ax_brightness.set_title('LED Brightness Level')
        ax_brightness.set_ylabel('Brightness (0-255)')
        ax_brightness.set_xlabel('Time (seconds)')
        ax_brightness.set_ylim(0, 255)
        ax_brightness.fill_between(list(times), list(brightness), alpha=0.3, color='yellow')

        # --- Plot 3: PIR Occupancy ---
        ax_pir.clear()
        pir_color = 'green' if pirValue == 1 else 'red'
        pir_text  = 'OCCUPIED' if pirValue == 1 else 'EMPTY'
        ax_pir.set_facecolor(pir_color)
        ax_pir.text(0.5, 0.5, pir_text,
                   horizontalalignment='center',
                   verticalalignment='center',
                   transform=ax_pir.transAxes,
                   fontsize=24,
                   fontweight='bold',
                   color='white')
        ax_pir.set_title('Room Occupancy (PIR)')
        ax_pir.set_xticks([])
        ax_pir.set_yticks([])

        # --- Plot 4: Energy Counter ---
        ax_energy.clear()
        ax_energy.plot(list(times), list(energy), color='blue', linewidth=2)
        ax_energy.set_title('Total Energy Usage (LED on time)')
        ax_energy.set_ylabel('Seconds LED was ON')
        ax_energy.set_xlabel('Time (seconds)')
        ax_energy.fill_between(list(times), list(energy), alpha=0.3, color='blue')

        plt.tight_layout()

    except Exception as e:
        print(f"Error reading data: {e}")

# --- Run Animation ---
ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
plt.tight_layout()
plt.show()

# --- Close Serial on Exit ---
ser.close()