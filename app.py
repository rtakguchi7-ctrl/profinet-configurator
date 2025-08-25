from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<title>DCP Web UI</title>
<h2>PROFINET Device Scanner</h2>
<form method="post">
  Interface: <select name="interface">
    <option value="eth-4">eth-4</option>
    <option value="eth-5">eth-5</option>
  </select>
  <input type="submit" name="action" value="SCAN">
</form>

{% if devices %}
  <h3>Detected PROFINET Devices</h3>
  <table border=1>
    <tr><th>MAC Address</th><th>IP Address</th><th>Station Name</th><th>Vendor</th></tr>
    {% for d in devices %}
      <tr><td>{{ d.mac }}</td><td>{{ d.ip }}</td><td>{{ d.name }}</td><td>{{ d.vendor }}</td></tr>
    {% endfor %}
  </table>
{% endif %}

<h2>Configure Device</h2>
<form method="post">
  Interface: <select name="interface">
    <option value="eth-4">eth-4</option>
    <option value="eth-5">eth-5</option>
  </select><br>
  MAC Address: <input type=text name=mac><br>
  Station Name: <input type=text name=name><br>
  IP Address: <input type=text name=ip><br>
  <input type="submit" name="action" value="CONFIGURE">
</form>
<pre>{{ message }}</pre>
'''

def run_dcp_command(args):
    try:
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"

def parse_identify_output(output):
    devices = []
    for block in output.strip().split("\n\n"):
        lines = block.splitlines()
        mac, ip, name, vendor = "", "", "", ""
        for line in lines:
            if "MAC" in line:
                mac = line.split()[-1]
            elif "IP" in line:
                ip = line.split()[-1]
            elif "Station Name" in line:
                name = line.split()[-1]
            elif "Vendor" in line or "Manufacturer" in line:
                vendor = line.split(":")[-1].strip()
        if mac:
            devices.append({"mac": mac, "ip": ip, "name": name, "vendor": vendor})
    return devices

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    devices = []
    if request.method == 'POST':
        interface = request.form['interface']
        action = request.form['action']

        if action == "SCAN":
            output = run_dcp_command(["profi-dcp", "identify", "--interface", interface])
            devices = parse_identify_output(output)

        elif action == "CONFIGURE":
            mac = request.form['mac']
            name = request.form['name']
            ip = request.form['ip']
            message += run_dcp_command(["profi-dcp", "set-name", "--interface", interface, "--mac", mac, "--name", name])
            message += run_dcp_command(["profi-dcp", "set-ip", "--interface", interface, "--mac", mac, "--ip", ip])

    return render_template_string(HTML_TEMPLATE, message=message, devices=devices)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
