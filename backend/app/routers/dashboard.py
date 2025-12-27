from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.system_service import get_system_metrics, get_network_interfaces
from app.schemas.dashboard import DashboardStats, NetworkScanResult
import asyncio
import time
import random
import subprocess

router = APIRouter()

# -------------------------------------------------
# Dashboard Stats
# -------------------------------------------------
@router.get("/stats", response_model=DashboardStats)
def dashboard_stats():
    sys = get_system_metrics()
    return {
        "global_threats": 842000 + int(time.time() % 10000),
        "active_attacks": int(sys["recv"] * 5) + random.randint(0, 10),
        "threats_blocked": 762000 + int(time.time() % 500),
        "networks_secured": len(get_network_interfaces()),
        "system_load": sys
    }

# -------------------------------------------------
# Network Scan
# -------------------------------------------------
@router.get("/network/scan", response_model=list[NetworkScanResult])
def network_scan():
    try:
        output = subprocess.check_output(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            shell=True
        ).decode("utf-8", errors="ignore")

        networks = []
        current_net = {}

        for line in output.split("\n"):
            line = line.strip()
            if line.startswith("SSID"):
                if current_net.get("ssid"):
                    current_net["signal"] = random.randint(40, 100)
                    networks.append(current_net)
                current_net = {"ssid": line.split(":", 1)[1].strip()}
            elif line.startswith("Authentication"):
                current_net["security"] = line.split(":", 1)[1].strip()

        results = []
        for n in networks:
            sec = n.get("security", "UNKNOWN").upper()
            status = "Warning"
            if "OPEN" in sec:
                status = "Danger"
            elif "WPA2" in sec or "WPA3" in sec:
                status = "Trusted"

            results.append({
                "ssid": n["ssid"],
                "security": sec,
                "signal": n.get("signal", random.randint(60, 99)),
                "status": status
            })

        if not results:
            return [
                {"ssid": "CyberSpy_Secure_HQ", "security": "WPA3-ENT", "signal": 98, "status": "Trusted"},
                {"ssid": "Guest_Access_Open", "security": "OPEN", "signal": 75, "status": "Danger"},
                {"ssid": "IoT_Smart_Fridge", "security": "WEP", "signal": 35, "status": "Danger"},
                {"ssid": "Office_Printer_Direct", "security": "WPA2-PSK", "signal": 60, "status": "Warning"},
            ]

        return results[:10]

    except Exception as e:
        print(f"Wifi scan error: {e}")
        return [
            {"ssid": "Simulation_Net_Alpha", "security": "WPA3", "signal": 90, "status": "Trusted"},
            {"ssid": "Malicious_Honeypot", "security": "OPEN", "signal": 85, "status": "Danger"},
        ]

# -------------------------------------------------
# Live WebSocket Stream (STEP 3 INTELLIGENCE)
# -------------------------------------------------
@router.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    geo_locations = ["US", "CN", "RU", "DE", "BR", "IN", "JP", "FR"]
    protocols = ["TCP", "UDP", "HTTP", "DNS", "SSH", "FTP", "SMTP", "RDP"]
    flags = ["SYN", "ACK", "FIN", "PSH", "RST", "URG", "ECE"]

    try:
        while True:
            # -------------------------------
            # Traffic Intelligence
            # -------------------------------
            packet_rate = random.randint(50, 2000)
            anomaly_score = min(packet_rate / 1500, 1.0)

            if anomaly_score > 0.7:
                threat_level = "Malicious"
            elif anomaly_score > 0.3:
                threat_level = "Suspicious"
            else:
                threat_level = "Normal"

            data = {
                "system": get_system_metrics(),
                "packet": {
                    "id": int(time.time() * 1000),
                    "type": random.choice(protocols),
                    "size": random.randint(64, 4096),
                    "source": f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
                    "flag": random.choice(flags) if random.random() > 0.3 else None,
                    "geo": random.choice(geo_locations),
                    "packet_rate": packet_rate,
                    "anomaly_score": round(anomaly_score, 2),
                    "threat_level": threat_level
                }
            }

            await websocket.send_json(data)
            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        pass
