from flask import Flask

app = Flask(__name__)

@app.route('/')
def health_check():
    return 'OK'

def run_flask():
    app.run(host='0.0.0.0', port=8000)