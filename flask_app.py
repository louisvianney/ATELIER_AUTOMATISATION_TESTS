from flask import Flask, jsonify, render_template
from tester.runner import execute_run
from storage import save_run, list_runs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html', runs=list_runs())

@app.route('/run')
def run():
    result = execute_run()
    save_run(result)
    return jsonify(result)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', runs=list_runs())

@app.route('/health')
def health():
    runs = list_runs(limit=1)
    last = runs[0] if runs else None
    return jsonify({
        "status": "ok",
        "last_run": last["timestamp"] if last else None,
        "last_error_rate": last["error_rate"] if last else None
    })

if __name__ == "__main__":
    app.run(debug=True)