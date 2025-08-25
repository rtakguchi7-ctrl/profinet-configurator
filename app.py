from flask import Flask, request, render_template_string
from profi_dcp import DCPManager

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<title>DCP Web UI</title>
<h2>DCP Station Configuration</h2>
<form method=post>
  Interface: <select name="interface">
    <option value="eth-4">eth-4</option>
    <option value="eth-5">eth-5</option>
  </select><br>
  MAC Address: <input type=text name=mac><br>
  Station Name: <input type=text name=name><br>
  IP Address: <input type=text name=ip><br>
  <input type=submit value=Configure>
</form>
<p>{{ message }}</p>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        interface = request.form['interface']
        mac = request.form['mac']
        name = request.form['name']
        ip = request.form['ip']
        try:
            dcp = DCPManager(interface)
            dcp.identify(mac)
            dcp.set_station_name(mac, name)
            dcp.set_ip(mac, ip)
            message = "Configuration successful."
        except Exception as e:
            message = f"Error: {e}"
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
