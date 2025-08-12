from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

def run_identify(interface):
    try:
        result = subprocess.run(
            ["profi-dcp", "identify", "--interface", interface],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def set_ip(mac, ip, subnet, gateway, nic):
    cmd = [
        "profi-dcp", "set-ip",
        "--mac", mac,
        "--ip", ip,
        "--subnet", subnet,
        "--gateway", gateway,
        "--interface", nic
    ]
    subprocess.run(cmd, check=True)

def set_station_name(mac, name, nic):
    cmd = [
        "profi-dcp", "set-name",
        "--mac", mac,
        "--name", name,
        "--interface", nic
    ]
    subprocess.run(cmd, check=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    identify_result = ''
    if request.method == 'POST':
        if 'search' in request.form:
            nic = request.form['nic']
            identify_result = run_identify(nic)
        else:
            mac = request.form['mac']
            station_name = request.form['station_name']
            ip_address = request.form['ip_address']
            subnet_mask = request.form['subnet_mask']
            gateway = request.form['gateway']
            nic = request.form['nic']
            try:
                set_ip(mac, ip_address, subnet_mask, gateway, nic)
                set_station_name(mac, station_name, nic)
                message = '設定を送信しました。'
            except Exception as e:
                message = f'エラー: {e}'
    return render_template('index.html', message=message, identify_result=identify_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
