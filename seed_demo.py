"""
Seed Script: Populates Demo Users, Sample Files, Blockchain Transactions,
Access Control Grants, and Audit Logs.
"""

import os
import io
import time
from app import create_app
from app.config import Config


def seed():
    print("==================================================")
    print("  Initializing Blockchain-Based Cloud Storage... ")
    print("==================================================")

    # Ensure clean data directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("sample_files", exist_ok=True)

    app = create_app(Config)
    db = app.db
    blockchain = app.blockchain
    storage = app.storage

    # 1. Create Sample Test Files on Disk
    sample_files_data = [
        (
            "Cloud_Security_Whitepaper.txt",
            """# Cloud Computing & Blockchain Security Whitepaper
Author: Dr. Alice Johnson
Date: 2026-10-25
Abstract:
This whitepaper analyzes the integration of cryptographic distributed ledgers with 
scalable cloud storage providers (such as Local Volumes and AWS S3). 
By computing streaming SHA-256 hashes and anchoring them inside Proof-of-Work blocks,
cloud tenants achieve tamper-proof data verification without relying blindly on third-party cloud providers.
Key Findings:
1. Merkle Trees provide logarithmic integrity checks.
2. Discretionary Access Control (DAC) tracked on-chain prevents privilege escalation.
3. Zero-knowledge proof verification ensures privacy while guaranteeing integrity.
""",
        ),
        (
            "Hospital_Medical_Records_Sample.csv",
            """RecordID,PatientName,DiagnosisCode,AttendingPhysician,EncryptedDataHash
1001,John Doe,E11.9,Dr. Smith,a8b9f71c42e88a01bf9e
1002,Jane Roe,I10,Dr. Taylor,7c6e44b910fa8d223c10
1003,Robert Green,J45.909,Dr. Alice Johnson,6f32e01b7a998c445d82
1004,Emily White,M54.5,Dr. Smith,810ad93c0042f88b9a11
""",
        ),
        (
            "Blockchain_Storage_Architecture.json",
            """{
  "system": "Blockchain-Based Cloud Storage Solutions",
  "version": "1.0.0",
  "consensus": "Proof-of-Work",
  "hashing_algorithm": "SHA-256",
  "storage_tiers": ["Local Disk Driver", "Amazon Web Services S3"],
  "security_properties": [
    "Bit-level Tamper Detection",
    "Immutable Audit Trail",
    "Discretionary Access Control (DAC)",
    "Non-repudiation"
  ]
}
""",
        ),
    ]

    for fname, content in sample_files_data:
        fpath = os.path.join("sample_files", fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
    print("[+] Sample test files written to 'sample_files/' directory.")

    # 2. Create Demo Users
    users_to_create = [
        ("alice", "alice@cloudstorage.edu", "password123", "Alice Johnson", "User"),
        ("bob", "bob@cloudstorage.edu", "password123", "Bob Smith", "User"),
        ("admin", "admin@cloudstorage.edu", "admin123", "System Administrator", "Admin"),
    ]

    created_users = {}
    for uname, email, pw, fname, role in users_to_create:
        existing = db.get_user_by_username(uname)
        if not existing:
            u = db.create_user(uname, email, pw, fname, role)
            created_users[uname] = u
            db.log_event("USER_REGISTER", u["id"], u["username"], "127.0.0.1", f"Seed account created with role {role}")
            print(f"[+] User created: {uname} ({role}) -> Wallet: {u['wallet_address'][:16]}...")
        else:
            created_users[uname] = existing
            print(f"[*] User already exists: {uname}")

    alice = created_users.get("alice")
    bob = created_users.get("bob")

    # 3. Upload and Anchor Sample Files if none exist
    existing_files = db.get_all_active_files()
    if not existing_files and alice:
        print("[+] Uploading initial sample files and mining blockchain blocks...")

        for fname, content in sample_files_data:
            stream = io.BytesIO(content.encode("utf-8"))
            storage_key, file_size, sha256_hash = storage.save(stream, fname)

            # Record on Blockchain & Mine Block
            tx_data, mined_block = blockchain.record_and_mine(
                tx_type="FILE_UPLOAD",
                file_id=None,
                file_name=fname,
                file_hash=sha256_hash,
                owner=alice["username"],
                details=f"Initial seed upload of {fname}",
                extra_data={"size": file_size, "uploader": alice["username"]},
            )

            # Save in DB
            db_file = db.create_file(
                filename=fname,
                storage_key=storage_key,
                file_size=file_size,
                mime_type="text/plain" if fname.endswith(".txt") else "application/json",
                sha256_hash=sha256_hash,
                owner_id=alice["id"],
                is_public=False,
                blockchain_tx_id=tx_data["tx_id"],
                blockchain_block_index=mined_block.index,
            )

            db.log_event(
                "FILE_UPLOAD",
                alice["id"],
                alice["username"],
                "127.0.0.1",
                f"Anchored '{fname}' in Block #{mined_block.index}",
                blockchain_tx_id=tx_data["tx_id"],
            )
            print(f"    -> Anchored '{fname}' to Block #{mined_block.index} [Tx: {tx_data['tx_id'][:12]}...]")

        # 4. Grant Alice -> Bob Access on Whitepaper
        first_file = db.get_files_by_owner(alice["id"])[0]
        if bob:
            tx_data, mined_block = blockchain.record_and_mine(
                tx_type="PERMISSION_GRANT",
                file_id=str(first_file["id"]),
                file_name=first_file["filename"],
                file_hash=first_file["sha256_hash"],
                owner=alice["username"],
                details=f"Alice granted DOWNLOAD permission to Bob",
            )
            db.grant_access(first_file["id"], bob["id"], alice["id"], "DOWNLOAD", tx_data["tx_id"])
            db.log_event(
                "ACCESS_GRANTED",
                alice["id"],
                alice["username"],
                "127.0.0.1",
                f"Access granted on '{first_file['filename']}' to bob",
                blockchain_tx_id=tx_data["tx_id"],
            )
            print(f"[+] Access Permission granted: Alice -> Bob for '{first_file['filename']}' in Block #{mined_block.index}")

    print("\n==================================================")
    print("  Seed Complete! You can now run the application.")
    print("==================================================")
    print("Demo Accounts:")
    print("  1. Alice (User)   -> Username: alice, Password: password123")
    print("  2. Bob (User)     -> Username: bob,   Password: password123")
    print("  3. Admin (Admin)  -> Username: admin, Password: admin123")
    print("==================================================")


if __name__ == "__main__":
    seed()
