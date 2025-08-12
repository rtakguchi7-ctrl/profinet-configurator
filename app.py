from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        mac = request.form['mac']
        station_name = request.form['station_name']
        ip_address = request.form['ip_address']
        subnet_mask = request.form['subnet_mask']
        gateway = request.form['gateway']
        nic = request.form['nic']

        try:
            subprocess.run([
                "profi-dcp", "set-ip",
                "--mac", mac,
                "--ip", ip_address,
                "--subnet", subnet_mask,
                "--gateway", gateway,
                "--interface", nic
            ], check=True)

            subprocess.run([
                "profi-dcp", "set-name",
                "--mac", mac,
                "--name", station_name,
                "--interface", nic
            ], check=True)

            message = '設定を送信しました。'
        except subprocess.CalledProcessError as e:
            message = f'エラー: {e}'

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
