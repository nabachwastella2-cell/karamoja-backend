from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage (Render free tier resets on redeploy)
ledger = []
blocks = []
shipments = []
audits = []
escrows = []

AUTH_TOKEN = "12345"

def require_auth(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token != AUTH_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def add_ledger(actor, event, metadata):
    ledger.append({
        "timestamp": datetime.utcnow().isoformat(),
        "actor": actor,
        "event": event,
        "metadata": metadata
    })

@app.route("/api/block/create", methods=["POST"])
@require_auth
def create_block():
    data = request.get_json()
    blocks.append(data)
    add_ledger("REGULATOR", "BLOCK_CREATED", data)
    return jsonify({"message": "Block created", "block": data})

@app.route("/api/shipment/create", methods=["POST"])
@require_auth
def create_shipment():
    data = request.get_json()
    shipments.append(data)
    add_ledger("MINER", "SHIPMENT_CREATED", data)
    return jsonify({"message": "Shipment created", "shipment": data})

@app.route("/api/audit/create", methods=["POST"])
@require_auth
def create_audit():
    data = request.get_json()
    audits.append(data)
    add_ledger("AUDITOR", "AUDIT_RECORDED", data)
    return jsonify({"message": "Audit recorded", "audit": data})

@app.route("/api/escrow/create", methods=["POST"])
@require_auth
def create_escrow():
    data = request.get_json()
    escrows.append(data)
    add_ledger("BANK", "ESCROW_CREATED", data)
    return jsonify({"message": "Escrow created", "escrow": data})

@app.route("/api/ledger", methods=["GET"])
@require_auth
def get_ledger():
    return jsonify({"ledger": ledger})

@app.route("/", methods=["GET"])
def home():
    return "Karamoja Gold Supply Chain API is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
