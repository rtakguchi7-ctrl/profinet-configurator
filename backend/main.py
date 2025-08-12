from fastapi import FastAPI, Query
from typing import List
import subprocess

app = FastAPI()

@app.get("/identify")
def identify(interface: str):
    # Run profi-dcp identify command
    result = subprocess.run(["profi-dcp", "identify", "-i", interface], capture_output=True, text=True)
    return {"output": result.stdout}

@app.post("/set-ip")
def set_ip(mac: str, ip: str, subnet: str, gateway: str):
    result = subprocess.run([
        "profi-dcp", "set-ip",
        "--mac", mac,
        "--ip", ip,
        "--subnet", subnet,
        "--gateway", gateway
    ], capture_output=True, text=True)
    return {"output": result.stdout}

@app.post("/set-name")
def set_name(mac: str, name: str):
    result = subprocess.run([
        "profi-dcp", "set-name",
        "--mac", mac,
        "--name", name
    ], capture_output=True, text=True)
    return {"output": result.stdout}

@app.get("/vendor")
def get_vendor(mac: str):
    oui = mac.upper().replace(":", "")[:6]
    vendor = oui_lookup.get(oui, "Unknown Vendor")
    return {"vendor": vendor}

# Sample OUI lookup dictionary
oui_lookup = {
    "000C29": "VMware, Inc.",
    "001C23": "Siemens AG",
    "F4CE46": "Phoenix Contact",
    "D89EF3": "Beckhoff Automation",
    "0002B3": "Hirschmann Automation"
}
