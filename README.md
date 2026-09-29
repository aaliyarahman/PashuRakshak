# 🐄 PashuRakshak — Offline-First Livestock Health MVP

PashuRakshak is a prototype for livestock owners/farmers and veterinarians focused on:

- Bulk herd/batch management instead of forcing farmers to register every animal individually
- Offline local SQLite storage
- Symptom/NLP-style triage
- Health cases and affected-subset tracking
- Vaccination register
- Movement/migration logs with GPS-ready fields
- Cached pharmacy directory and order workflow
- Farmer and veterinarian roles
- Multilingual UI foundation
- District/taluk-ready data model
- Disease/outbreak workflow foundation

## 1. Install

### Windows
```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open:
http://localhost:8501

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## 2. Folder structure

```text
PashuRakshak/
├── app.py
├── db.py
├── nlp_engine.py
├── i18n.py
├── utils.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── pashurakshak.db        # created automatically
└── mobile/
    └── README.md               # Android roadmap
```

## 3. Why bulk herds solve the 5,000-animal problem

A herd can be represented as:
- species = Goat
- breed = Osmanabadi
- count = 5000
- location = village/taluk/district

If 17 animals become sick, create a health case:
- herd_id = 1
- affected_count = 17
- status = Suspected

Later, the production system can assign temporary animal IDs only to the 17 affected animals. This is much more practical than entering 5,000 animals individually.

## 4. Offline design

Core operations do not require internet:
- add/view herds
- create health cases
- vaccination records
- movement logs
- local symptom triage
- cached pharmacy directory
- dashboard totals

Online-only features should be treated as sync layers:
- cloud synchronization
- government data feeds
- live maps
- SMS/WhatsApp notifications
- online pharmacy inventory
- payment gateway
- remote veterinarian consultations

## 5. Production architecture

Recommended next version:

Mobile:
- Flutter
- SQLite/Drift
- background sync queue
- GPS
- camera
- local notifications
- multilingual ARB files

Backend:
- FastAPI
- PostgreSQL/PostGIS
- Redis/Celery for jobs
- object storage for images
- JWT/OAuth2
- role-based access

AI/NLP:
- symptom entity extraction
- multilingual text normalization
- approved disease knowledge graph
- risk scoring
- optional image model for lesions/skin signs
- veterinarian-in-the-loop review

Important: AI must provide triage/risk support, not autonomous diagnosis or prescription.

## 6. Android conversion

Do NOT try to turn Streamlit itself into the final Android architecture.

Use Streamlit as the hackathon/local prototype.

Then rebuild the mobile UI in Flutter while keeping the same backend/data model.

Suggested flow:

```text
Flutter Android App
        │
        ├── Local SQLite (offline)
        │
        ├── GPS / Camera / Notifications
        │
        └── Sync Queue
                │
                ▼
             FastAPI
                │
        PostgreSQL/PostGIS
                │
        ├── Vet dashboard
        ├── disease analytics
        ├── pharmacy
        └── government integrations
```

## 7. Payment

The MVP records an order as "Pending Payment".

For production, use a licensed payment provider and server-side verification. Never store card/UPI credentials yourself. Payment should be attempted only when connectivity is available.

## 8. Disease safety

The built-in NLP module only finds symptom patterns. It does not confirm a disease.

A production release needs:
- veterinary authority review
- validated disease rules/models
- medicine and dosage governance
- vaccination schedule governance
- antimicrobial stewardship
- audit logs
- emergency/outbreak escalation rules

## 9. Data/statistics

Do not hard-code invented government statistics.

Import official datasets into a separate analytics layer with:
- source
- publication year
- district
- taluk/block
- species
- breed
- population
- shelter counts
- disease events
- timestamp

The Maharashtra Animal Husbandry Department publishes livestock census material, including the 20th Livestock Census and breed-wise reports.

## 10. Suggested hackathon demo

Demo with:
1. 5,000 goats entered as one batch
2. 17 goats reported with symptoms
3. offline NLP flags a high-attention pattern
4. create a suspected case
5. isolate/monitor workflow
6. show vaccination status
7. log movement to a grazing area
8. show vet dashboard
9. show district/taluk analytics
10. create pharmacy order
11. switch language
12. turn off internet and repeat core operations

## 11. Future modules

- QR/RFID/ear-tag support
- camera-based lesion screening
- voice-first farmer interface
- IVR/SMS fallback
- satellite/geo-risk layers
- weather-linked disease risk
- outbreak heatmaps
- herd-level reproduction/productivity
- feed/nutrition planning
- shelter management
- mortality reporting
- insurance/claim evidence
- veterinary appointment scheduling
- government vaccination campaign planning
