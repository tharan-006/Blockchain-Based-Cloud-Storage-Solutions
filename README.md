# Blockchain-Based Cloud Storage Solutions

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask_3.1-black.svg)](https://flask.palletsprojects.com/)
[![Consensus](https://img.shields.io/badge/Consensus-Proof--of--Work_(SHA--256)-cyan.svg)]()
[![Tests](https://img.shields.io/badge/Tests-10%2F10_Passing-brightgreen.svg)]()
[![Storage](https://img.shields.io/badge/Storage-Local_%2B_AWS_S3-orange.svg)]()

> **Cloud Computing Subject Final Project**  
> An enterprise-grade, secure cloud storage platform that allows users to upload, store, download, and share files with immutable cryptographic blockchain anchoring and SHA-256 integrity verification.

---

## 1. Executive Summary & Objective

In traditional cloud storage architectures (e.g., centralized object stores), tenants must blindly trust the cloud provider not to alter, corrupt, or leak their data. Furthermore, malicious insiders or external attackers with administrative database access can silently tamper with file contents without leaving verifiable cryptographic traces.

**Blockchain-Based Cloud Storage Solutions** solves this fundamental trust issue using a **dual-tier decentralized architecture**:
1. **Tier 1 (Storage Layer):** High-throughput object storage (Local filesystem driver for development/prototyping, with a native plug-and-play adapter for **Amazon Web Services S3**).
2. **Tier 2 (Integrity & Access Ledger):** A cryptographic **Proof-of-Work Blockchain** that records immutable SHA-256 file fingerprints, timestamps, ownership attributions, and Access Control List (ACL) permission grants/revocations.

---

## 2. System Architecture Diagram

```
+=========================================================================================================+
|                                    CLIENT APPLICATION / WEB INTERFACE                                    |
|             [Upload / Download]          [Verify Integrity]          [Grant / Revoke ACL]               |
+=========================================================================================================+
                                                     |
                                                     v
+=========================================================================================================+
|                                      APPLICATION BACKEND (FLASK REST)                                   |
|   - Authentication & Salted PBKDF2 Password Hashing        - Role-Based & Discretionary Access Control  |
|   - Streaming Chunked SHA-256 Hash Engine                  - Security Audit Event Logging Engine        |
+=========================================================================================================+
                       /                                                         \
                      /                                                           \
                     v                                                             v
+===========================================+             +===============================================+
|        TIER 1: CLOUD OBJECT STORAGE       |             |         TIER 2: CRYPTOGRAPHIC LEDGER          |
|  - StorageBackend Abstraction Driver      |             |  - Proof-of-Work Blockchain Engine            |
|  - Local File Storage (Active Prototype)  |             |  - Linked Blocks with Nonce & Target Diff.     |
|  - AWS S3 Object Storage (AWS SDK boto3)  |             |  - Merkle Tree Root Calculation per Block     |
|  - Raw Byte Storage (Payloads)            |             |  - Immutable File SHA-256 Fingerprints & ACL  |
+===========================================+             +===============================================+
                     |                                                             |
                     \_____________________________   _____________________________/
                                                   \ /
                                                    v
                             +==============================================+
                             |       INTEGRITY VERIFICATION ENGINE          |
                             |  Storage Hash == Blockchain Anchor Hash?     |
                             |  [MATCH]   --> 100% Authentic & Intact       |
                             |  [MISMATCH]--> Security Alert: Tampered!     |
                             +==============================================+
```

---

## 3. Core Features & Capabilities

### 1. User Authentication & Cryptographic Identity
- User registration, login, logout, and salted `PBKDF2:SHA256` password hashing.
- Each registered user receives a deterministic cryptographic public identity (Ethereum-style address `0x...`) derived from their credentials to sign file ownership and permissions.
- Role-Based Access Control (**Admin** vs. **User**).

### 2. Multi-Format File Upload & Cloud Storage
- Supports any file type (PDFs, DOCX, TXT, Images, ZIP archives, CSV, JSON, code files) up to 100 MB.
- Memory-efficient streaming reads in 64 KB chunks—prevents memory exhaustion on large files.
- Modular `StorageBackend` abstraction:
  - `LocalStorageBackend` (Active zero-dependency prototype stored in `uploads/`).
  - `S3StorageBackend` (Amazon Web Services S3 object storage driver using `boto3`).

### 3. Cryptographic Blockchain Ledger Engine
- Real Python cryptographic blockchain with:
  - **Proof-of-Work (PoW):** Solves mathematical nonce puzzles meeting target difficulty (`000...`).
  - **Block Hash Chaining:** `Block.hash = SHA256(index + timestamp + merkle_root + previous_hash + nonce)`.
  - **Merkle Trees:** Pairwise SHA-256 transaction aggregation ensuring any modified transaction breaks the block header.
  - **Mempool:** Staging area for pending transactions with manual or automatic block mining.
  - **JSON Ledger Persistence:** Stored in `data/blockchain_ledger.json`.

### 4. Bit-Level File Integrity Verification
- Re-reads stored files on demand and calculates real-time SHA-256 digests.
- Queries the blockchain ledger for the original anchor block.
- **Match:** Confirms file authenticity and highlights block index.
- **Mismatch:** Triggers a security alert (`TAMPER_ALERT`) and logs unauthorized modification to the audit trail.

### 5. Access Control Lists (ACL) & Sharing
- File owners can grant/revoke granular permissions (`DOWNLOAD` or `READ`) to other registered users.
- Every permission grant or revocation is recorded as an immutable transaction on the blockchain (`PERMISSION_GRANT` / `PERMISSION_REVOKE`).

### 6. Academic Tamper Demonstration Suite
- Built specifically for Cloud Computing course demonstrations:
  - **File Tamper Simulator:** Injects unauthorized byte alteration into physical storage files. Clicking "Verify Integrity" immediately exposes the SHA-256 mismatch!
  - **Block Tamper Simulator:** Alters transaction data inside an existing mined block. Clicking "Audit Ledger Integrity" flags the exact block index where the cryptographic chain link broke.
  - **Heal / Restore:** Restores clean states with one click for repeatable grading tests.

### 7. Interactive Visual Blockchain Explorer
- Shows the complete cryptographic chain from Genesis Block (#0) to latest.
- Block cards display Block #, Timestamp, Nonce, Merkle Root, Previous Hash, and Current Hash.
- **Inspect Block Modal:** Allows inspecting transaction payloads and raw block JSON.

### 8. Enterprise Dashboard & Visual Analytics
- Real-time stat cards: Total Files Stored, Cloud Storage Used (KB/MB), Blockchain Blocks Mined, On-Chain Transactions.
- Visual file category breakdown (Documents, Images, Code/Data, Archives).
- Blockchain Health Status Banner.

### 9. Comprehensive Security Audit Trail
- Logs all uploads, downloads, integrity checks, access grants, deletions, and tamper attempts.
- Searchable and filterable by event type.
- **Export to CSV:** Direct 1-click download of the entire security audit trail.

---

## 4. Technology Disclosure: Real vs. Simulated Components

In accordance with project requirements to clearly distinguish simulated features from real integrations:

| Component | Architecture Type | Implementation Details |
| :--- | :--- | :--- |
| **File Hashing (SHA-256)** | **100% Real Cryptography** | Standard cryptographic SHA-256 digests calculated over streaming file buffers. Bit-level sensitive. |
| **Blockchain Engine** | **100% Real PoW Engine** | Real local Proof-of-Work consensus engine with target difficulty, chained block hashes, Merkle root trees, and JSON persistence. |
| **Password Security** | **100% Real Security** | Salted `PBKDF2:SHA256` password hashing via Werkzeug security. |
| **Storage Layer** | **Hybrid / Modular** | Local filesystem storage backend is fully implemented and active by default. AWS S3 driver is fully implemented in `app/storage/s3_storage.py` and activates automatically when credentials are provided in `.env`. |
| **Cryptographic Identity** | **Deterministic Simulation** | Ethereum-style addresses (`0x...`) derived deterministically via SHA-256 of user identity for transparent attribution. |

---

## 5. Technology Stack

- **Backend:** Python 3.10+, Flask 3.1, Werkzeug
- **Database:** SQLite 3 (Thread-safe, zero external database setup required)
- **Frontend:** HTML5, Modern CSS3 (Dark Blue & Clean White Enterprise Theme), Vanilla JavaScript, Bootstrap 5.3, Bootstrap Icons, Google Fonts (Plus Jakarta Sans & JetBrains Mono)
- **Object Storage:** Local filesystem storage driver + AWS S3 SDK (`boto3`)
- **Testing:** Pytest 8.0+

---

## 6. Directory Structure

```
cloud 4/
├── app/
│   ├── __init__.py               # Flask application factory & context processors
│   ├── config.py                 # Application configuration & env loader
│   ├── models.py                 # SQLite database schema (Users, Files, ACL, Audit)
│   ├── blockchain/
│   │   ├── __init__.py
│   │   ├── block.py              # Block model (index, merkle_root, proof, prev_hash)
│   │   ├── merkle.py             # Binary Merkle Tree implementation
│   │   └── blockchain.py         # PoW mining, chain validation, and persistence
│   ├── storage/
│   │   ├── __init__.py           # Storage factory
│   │   ├── base.py               # Abstract StorageBackend interface
│   │   ├── local_storage.py      # Local file persistence with chunked hashing
│   │   └── s3_storage.py         # AWS S3 object storage driver (boto3)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py               # Login, Register, Logout, Profile
│   │   ├── dashboard.py          # Dashboard metrics & file distribution
│   │   ├── files.py              # Upload, Download, Share, Tamper simulation
│   │   ├── integrity.py          # Real-time SHA-256 verification against blockchain
│   │   ├── blockchain_view.py    # Blockchain visual explorer & chain audit
│   │   └── audit.py              # Audit logs & CSV export
│   ├── static/
│   │   ├── css/style.css         # Custom dark blue & white responsive theme
│   │   ├── js/main.js            # Clipboard copy, toast notifications, search
│   │   ├── js/files.js           # Drag & drop upload, verification modal, ACL
│   │   ├── js/blockchain.js      # Block inspector & raw JSON viewer
│   │   └── img/logo.svg          # Custom SVG emblem & branding
│   └── templates/
│       ├── base.html             # Layout with dark blue sidebar & navbar
│       ├── index.html            # Landing / Welcome page
│       ├── architecture.html     # System Architecture & Academic Specification
│       ├── dashboard.html        # Main dashboard with cards and charts
│       ├── profile.html          # Cryptographic wallet identity & quota
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── files/
│       │   ├── list.html         # Files repository with actions & tamper tool
│       │   └── shared.html       # Files shared with current user
│       ├── blockchain/
│       │   └── explorer.html     # Visual block stream & chain health
│       └── audit/
│           └── logs.html         # Audit trail table with filters & CSV export
├── data/                         # Local database & persisted blockchain state
│   ├── app.db                    # SQLite database
│   └── blockchain_ledger.json    # Persisted blockchain ledger
├── uploads/                      # Uploaded cloud storage directory
├── sample_files/                 # Pre-configured test files for evaluation
├── tests/
│   ├── test_blockchain.py        # Tests for PoW, Merkle roots, chain validity
│   ├── test_storage.py           # Tests for storage, chunked hashing, and tamper
│   ├── test_access_control.py    # Tests for authentication and ACL enforcement
│   ├── test_api.py               # Tests for Flask route integration
│   └── verify_live.py            # End-to-end HTTP validation script
├── run.py                        # Server launch script (python run.py)
├── seed_demo.py                  # Seed script with demo accounts & sample files
├── requirements.txt              # Project dependencies
├── .env.example                  # Environment configuration template
└── README.md                     # Comprehensive project documentation
```

---

## 7. Installation & Quick Start Guide

### Step 1: Clone or Navigate to the Project Directory
```bash
cd "c:\Users\Tharan\OneDrive\Desktop\cloud 4"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Seed Demo Accounts & Sample Files
This command initializes the SQLite database, generates sample test files in `sample_files/`, uploads them, computes SHA-256 hashes, and mines the initial Proof-of-Work blockchain blocks:
```bash
python seed_demo.py
```

### Step 4: Run the Application
```bash
python run.py
```

Open your browser and navigate to:
**`http://127.0.0.1:5000`**

---

## 8. Demo User Accounts

The seeding script automatically provisions three accounts:

| Role | Username | Password | Email | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Researcher (Owner)** | `alice` | `password123` | `alice@cloudstorage.edu` | Uploads files, manages ACLs, tests tampering. |
| **Engineer (Collaborator)** | `bob` | `password123` | `bob@cloudstorage.edu` | Receives shared files, tests download & verification. |
| **Security Administrator** | `admin` | `admin123` | `admin@cloudstorage.edu` | Global audit log review, blockchain ledger inspection. |

*(Note: The login page includes 1-click **Quick Test Account** buttons to immediately populate credentials for grading!)*

---

## 9. Running the Test Suite

Execute the automated test suite covering blockchain consensus, Merkle trees, chunked hashing, access control, and API endpoints:

```bash
python -m pytest tests/ -v
```

Expected output:
```
tests/test_access_control.py::test_user_creation_and_auth PASSED
tests/test_access_control.py::test_access_control_rules PASSED
tests/test_api.py::test_public_routes PASSED
tests/test_api.py::test_user_registration_and_flow PASSED
tests/test_blockchain.py::test_genesis_block PASSED
tests/test_blockchain.py::test_mine_block PASSED
tests/test_blockchain.py::test_merkle_tree PASSED
tests/test_blockchain.py::test_tamper_detection PASSED
tests/test_storage.py::test_storage_save_and_hash PASSED
tests/test_storage.py::test_storage_tamper_and_restore PASSED
============================= 10 passed in 3.97s =============================
```

To run end-to-end live HTTP endpoint verification:
```bash
python tests/verify_live.py
```

---

## 10. Step-by-Step Evaluator Walkthrough

1. **Sign In as Alice:**
   - Go to `http://127.0.0.1:5000/login` and click **Alice (Researcher)**, then click **Authenticate & Enter**.
2. **Explore the Dashboard:**
   - Observe the live metric cards (Total Files, Cloud Storage Used, Blockchain Blocks Mined).
   - View the visual **Storage Distribution** breakdown and the **Cryptographic Ledger Integrity: 100% Valid** badge.
3. **Verify File Integrity:**
   - Navigate to **My Files** in the sidebar.
   - Click the green **Verify** button on `Cloud_Security_Whitepaper.txt`.
   - A modal appears showing real-time SHA-256 calculation: active storage hash matches the immutable blockchain anchor in Block #1.
4. **Demonstrate Tamper Detection (Academic Test):**
   - In **My Files**, click the orange **<i class="bi bi-bug"></i>** (Tamper) icon next to a file.
   - The file on disk is altered with unauthorized bytes.
   - Now click **Verify** on that file: the modal immediately flags **TAMPERING DETECTED: HASH MISMATCH** in red!
   - Click the blue **Restore** icon to heal the file back to its pristine state.
5. **Inspect Blockchain Blocks:**
   - Navigate to **Blockchain Explorer** in the sidebar.
   - View the chained sequence of blocks from Genesis (#0) to latest.
   - Click **Inspect Block** to examine the block's raw JSON, Merkle Root, Nonce, and transaction records.
6. **Simulate Blockchain Tamper:**
   - In the **Blockchain Explorer**, click **Alter Block #1**.
   - Click **Audit Ledger Integrity**: the status immediately changes to **Cryptographic Tamper Alert: Chain Link Broken!**
   - Click **Restore Clean State** to re-heal the ledger.
7. **View Security Audit Trail:**
   - Navigate to **Audit Trail** in the sidebar.
   - Filter by event type (`FILE_UPLOAD`, `FILE_VERIFY`, `TAMPER_DETECTED`).
   - Click **Export Audit Trail (CSV)** to download the audit log spreadsheet.
8. **View System Architecture:**
   - Click **Architecture Specs** in the sidebar to review the full technical design and data flow diagrams.

---

## 11. AWS S3 Cloud Storage Integration (Optional)

To switch the storage backend from Local Disk to **Amazon Web Services S3**:
1. Copy `.env.example` to `.env`.
2. Configure your AWS S3 bucket credentials:
   ```env
   STORAGE_PROVIDER=s3
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=us-east-1
   AWS_S3_BUCKET_NAME=your-bucket-name
   ```
3. Restart `python run.py`. The top navbar and system status will automatically indicate `AWS S3 Cloud Storage (Active)`.
