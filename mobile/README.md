# Android migration roadmap

The Streamlit project is the prototype. For the actual Android app, create a Flutter project.

Recommended:
```bash
flutter create pashurakshak_mobile
cd pashurakshak_mobile
flutter pub add sqflite path geolocator camera connectivity_plus flutter_local_notifications
```

Core screens:
1. Role selection
2. Farmer dashboard
3. Vet dashboard
4. Herds
5. Add herd
6. Herd detail
7. Health check
8. Disease alert
9. Vaccination
10. Movement/GPS
11. Pharmacy
12. Orders
13. Nutrition
14. Knowledge
15. Sync center
16. Settings/language

Offline pattern:
- Every write goes to local SQLite first.
- Create a `sync_queue` row.
- When connectivity returns, push pending rows to FastAPI.
- Server responds with canonical IDs.
- Mark queue item as synced.
- Conflicts are resolved using server timestamps + audit logs.

GPS:
- Capture coordinates locally.
- Do not require a map tile to store a coordinate.
- Upload coordinates when online.
- Use PostGIS on server for geofencing/outbreak zones.

Voice:
- Add speech-to-text for local languages.
- Normalize the text into the disease NLP pipeline.
- Always show a confirmation screen before saving a health event.
