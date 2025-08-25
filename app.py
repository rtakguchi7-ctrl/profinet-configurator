from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<title>DCP Web UI</title>
<h2>PROFINET Device Scanner</h2>
<form method="post">
  Interface: <select name="interface">
    <option value="eth-x4">eth-x4</option>
    <option value="eth-x5">eth-x5</option>
  </select>
  <input type="submit" name="action" value="SCAN">
</form>

{% if scanning %}
  <p><strong>スキャン中...</strong></p>
{% endif %}

{% if scan_message %}
  <p><strong>{{ scan_message }}</strong></p>
{% endif %}

{% if devices %}
  <h3>Detected PROFINET Devices</h3>
  <table border=1 style="background-color:#eef;">
    <tr><th>MAC Address</th><th>IP Address</th><th>Station Name</th><th>Vendor</th></tr>
    {% for d in devices %}
      <tr><td>{{ d.mac }}</td><td>{{ d.ip }}</td><td>{{ d.name }}</td><td>{{ d.vendor }}</td></tr>
    {% endfor %}
  </table>
{% endif %}

<h2>Configure Device</h2>
<form method="post">
  Interface: <select name="interface">
    <option value="eth-x4">eth-x4</option>
    <option value="eth-x5">eth-x5</option>
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
    scan_message = ""
    scanning = False

    if request.method == 'POST':
        interface = request.form['interface']
        action = request.form['action']

        if action == "SCAN":
            scanning = True
            output = run_dcp_command(["profi-dcp", "identify", "--interface", interface])
            devices = parse_identify_output(output)
            scan_message = "No PROFINET devices found." if not devices else ""

        elif action == "CONFIGURE":
            mac = request.form['mac']
            name = request.form['name']
            ip = request.form['ip']
            message += run_dcp_command(["profi-dcp", "set-name", "--interface", interface, "--mac", mac, "--name", name])
            message += run_dcp_command(["profi-dcp", "set-ip", "--interface", interface, "--mac", mac, "--ip", ip])

    return render_template_string(HTML_TEMPLATE, message=message, devices=devices, scan_message=scan_message, scanning=scanning)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
