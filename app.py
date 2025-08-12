from flask import Flask, request, render_template
from profi_dcp import DCPClient

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
            client = DCPClient(interface=nic)
            client.set_ip(mac, ip_address, subnet_mask, gateway)
            client.set_station_name(mac, station_name)
            message = '設定を送信しました。'
        except Exception as e:
            message = f'エラー: {e}'

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
