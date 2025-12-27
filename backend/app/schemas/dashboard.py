from pydantic import BaseModel
from typing import Dict, List


class SystemLoad(BaseModel):
    cpu: float
    memory: float
    recv: float
    sent: float


class DashboardStats(BaseModel):
    global_threats: int
    active_attacks: int
    threats_blocked: int
    networks_secured: int
    system_load: Dict[str, float]


class NetworkScanResult(BaseModel):
    ssid: str
    security: str
    signal: int
    status: str
