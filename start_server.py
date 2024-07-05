# start_server.py
from Server import app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')