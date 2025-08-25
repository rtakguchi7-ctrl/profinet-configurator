from flask import Flask, request, render_template_string
import subprocess

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

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        interface = request.form['interface']
        mac = request.form['mac']
        name = request.form['name']
        ip = request.form['ip']

        # Run identify
        message += run_dcp_command(["profi-dcp", "identify", "--interface", interface])

        # Set station name
        message += run_dcp_command(["profi-dcp", "set-name", "--interface", interface, "--mac", mac, "--name", name])

        # Set IP address
        message += run_dcp_command(["profi-dcp", "set-ip", "--interface", interface, "--mac", mac, "--ip", ip])

    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
