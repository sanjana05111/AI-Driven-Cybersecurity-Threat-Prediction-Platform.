import os
import random
import shutil
import time
from fastapi import HTTPException

# Try importing Scapy
try:
    from scapy.all import rdpcap, TCP, UDP, DNS
    SCAPY_AVAILABLE = True
except (ImportError, OSError):
    SCAPY_AVAILABLE = False


class PCAPService:
    def analyze(self, file_obj, filename):
        if not SCAPY_AVAILABLE:
            return self._mock_pcap()

        temp_path = f"temp_{filename}_{random.randint(1000,9999)}.pcap"

        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file_obj, buffer)

            packets = rdpcap(temp_path)

            if len(packets) == 0:
                return self._mock_pcap()

            # -------------------------------
            # BASIC STATS
            # -------------------------------
            start_time = packets[0].time
            end_time = packets[-1].time
            duration = max(end_time - start_time, 1)

            packet_rate = len(packets) / duration
            anomaly_score = min(packet_rate / 1000, 1.0)

            if anomaly_score > 0.7:
                threat_level = "Malicious"
                reason = "Abnormally high packet rate (possible DDoS or scan)"
            elif anomaly_score > 0.3:
                threat_level = "Suspicious"
                reason = "Unusual traffic burst detected"
            else:
                threat_level = "Normal"
                reason = "Traffic within expected thresholds"

            summary = {
                "packets": len(packets),
                "duration": f"{duration:.2f}s",
                "protocols": {"TCP": 0, "UDP": 0, "DNS": 0, "Other": 0},
                "suspicious": 0
            }

            timeline = []

            for p in packets:
                if p.haslayer(TCP):
                    summary["protocols"]["TCP"] += 1
                    if p[TCP].flags == "S":
                        summary["suspicious"] += 1
                elif p.haslayer(UDP):
                    summary["protocols"]["UDP"] += 1
                elif p.haslayer(DNS):
                    summary["protocols"]["DNS"] += 1
                else:
                    summary["protocols"]["Other"] += 1

                if len(timeline) < 100:
                    timeline.append({
                        "time": int(p.time),
                        "len": len(p)
                    })

            chart_data = [
                {"name": k, "value": v}
                for k, v in summary["protocols"].items()
                if v > 0
            ]

            return {
                "stats": summary,
                "chart": chart_data,
                "timeline": timeline,
                "intelligence": {
                    "packet_rate": round(packet_rate, 2),
                    "anomaly_score": round(anomaly_score, 2),
                    "threat_level": threat_level,
                    "reason": reason
                }
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PCAP Error: {str(e)}")

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _mock_pcap(self):
        return {
            "stats": {
                "packets": 0,
                "duration": "N/A",
                "protocols": {},
                "suspicious": 0
            },
            "chart": [],
            "timeline": [],
            "intelligence": {
                "packet_rate": 0,
                "anomaly_score": 0,
                "threat_level": "Normal",
                "reason": "Scapy/Npcap not available"
            }
        }


pcap_service = PCAPService()
