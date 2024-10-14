from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from LuciferBanker'

if __name__ == "__main__":
    # Ensure Flask listens on the correct port, in this case, 8080
    port = int(os.getenv("PORT", 8080))  # Default to 8080 if no PORT is set
    app.run(host="0.0.0.0", port=port)
