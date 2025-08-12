from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

def run_identify(ip_address):
    try:
        result = subprocess.run(
            ["profi-dcp", "identify", "--ip-address", ip_address],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    result = ''
    if request.method == 'POST':
        if 'search' in request.form:
            ip_address = request.form['ip_address']
            result = run_identify(ip_address)
        elif 'configure' in request.form:
            mac = request.form['mac']
            station_name = request.form['station_name']
            ip_address = request.form['ip_address']
            subnet_mask = request.form['subnet_mask']
            gateway = request.form['gateway']
            try:
                subprocess.run([
                    "profi-dcp", "set-ip",
                    "--mac", mac,
                    "--ip", ip_address,
                    "--subnet", subnet_mask,
                    "--gateway", gateway
                ], check=True)
                subprocess.run([
                    "profi-dcp", "set-name",
                    "--mac", mac,
                    "--name", station_name
                ], check=True)
                message = '設定を送信しました。'
            except subprocess.CalledProcessError as e:
                message = f'エラー: {e.stderr}'
    return render_template('index.html', message=message, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
