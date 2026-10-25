"""
Application Entry Point for Blockchain-Based Cloud Storage Solutions.
Run with: python run.py
"""

import sys
from app import create_app
from app.config import Config

app = create_app(Config)

if __name__ == "__main__":
    if "--seed" in sys.argv:
        from seed_demo import seed
        seed()

    port = int(Config.DEBUG and 5000 or 5000)
    print("==================================================================")
    print("  * Blockchain-Based Cloud Storage Solutions (Cloud Computing)")
    print("  * Running on http://127.0.0.1:5000")
    print("  * Storage Driver: " + app.storage.provider_name)
    print("  * Blockchain Consensus: Proof-of-Work (SHA-256)")
    print("==================================================================")
    app.run(host="127.0.0.1", port=port, debug=Config.DEBUG)
