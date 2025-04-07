import pyrealsense2 as rs
import time
import csv
from datetime import datetime

# Intervallzeiten in Sekunden
intervals = [60, 180, 300, 600, 1200, 1800, 2700, 3600]

# RealSense-Device starten
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline_profile = pipeline.start(config)
print("RealSense-Stream gestartet...")

# Device holen und Sensoren abrufen
device = pipeline_profile.get_device()
sensors = device.query_sensors()

# Temperaturfähigen Sensor finden (typischerweise der erste oder zweite)
temperature_sensor = None
for sensor in sensors:
    if sensor.supports(rs.option.asic_temperature):
        temperature_sensor = sensor
        break

if not temperature_sensor:
    raise RuntimeError("Kein Sensor mit Temperaturmessung gefunden.")

# CSV-Datei vorbereiten
csv_filename = "realsense_temperature_log.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Asic Temp (°C)", "Projector Temp (°C)"])

start_time = time.time()
next_interval_index = 0

try:
    while next_interval_index < len(intervals):
        frames = pipeline.wait_for_frames()  # holen, damit der Stream läuft

        elapsed = time.time() - start_time
        if elapsed >= intervals[next_interval_index]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            asic_temp = temperature_sensor.get_option(rs.option.asic_temperature)
            projector_temp = temperature_sensor.get_option(rs.option.projector_temperature)
            if asic_temp > 60:
                break
            if projector_temp > 50:
                break

            # CSV schreiben
            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, round(asic_temp, 2), round(projector_temp, 2)])
                print(f"[{timestamp}] ASIC: {asic_temp:.2f} °C | Projektor: {projector_temp:.2f} °C")

            next_interval_index += 1

        time.sleep(0.5)

finally:
    pipeline.stop()
    print("RealSense-Stream gestoppt.")
