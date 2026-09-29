import streamlit as st
import sqlite3
from pathlib import Path
from datetime import datetime, date

# ============================================================
# PASHURAKSHAK - SINGLE FILE VERSION
# ============================================================
# This version intentionally uses Streamlit components/native
# widgets for the interface instead of rendering HTML through
# st.markdown. This prevents HTML/CSS from appearing as code.
# ============================================================

st.set_page_config(
    page_title="PashuRakshak",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Theme
# -----------------------------
GREEN = "#176B52"
GREEN_DARK = "#0F513D"
GREEN_SOFT = "#EAF5EF"
GREEN_BORDER = "#BFDACD"
GREY = "#E7E7E7"
GREY_DARK = "#D2D2D2"
WHITE = "#FFFFFF"
TEXT = "#17352B"
MUTED = "#61756C"

# -----------------------------
# Database
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "pashurakshak.db"
IMAGE_DIR = DATA_DIR / "animal_images"
IMAGE_DIR.mkdir(exist_ok=True)


def db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def now():
    return datetime.now().isoformat(timespec="seconds")


def init_db():
    c = db()
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS herds(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            species TEXT NOT NULL,
            breed TEXT,
            count INTEGER NOT NULL,
            district TEXT,
            taluk TEXT,
            location TEXT,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS health_cases(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            herd_id INTEGER,
            affected_count INTEGER,
            status TEXT,
            notes TEXT,
            created_at TEXT,
            animal_type TEXT,
            symptoms TEXT,
            temperature REAL,
            noticed_when TEXT,
            additional_details TEXT,
            image_path TEXT,
            image_name TEXT,
            emergency INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS vaccines(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            herd_id INTEGER,
            vaccine TEXT,
            next_due TEXT,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS movements(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            herd_id INTEGER,
            from_place TEXT,
            to_place TEXT,
            lat REAL,
            lon REAL,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pharmacy TEXT,
            item TEXT,
            qty INTEGER,
            price REAL,
            payment_method TEXT,
            payment_status TEXT,
            order_status TEXT,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS pharmacies(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            district TEXT,
            phone TEXT,
            upi_id TEXT
        );

        CREATE TABLE IF NOT EXISTS updates(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            message TEXT,
            category TEXT,
            created_at TEXT
        );
        """
    )

    # Safe migration for databases created by earlier PashuRakshak versions.
    existing_columns = {row[1] for row in c.execute("PRAGMA table_info(health_cases)").fetchall()}
    migrations = {
        "animal_type": "ALTER TABLE health_cases ADD COLUMN animal_type TEXT",
        "symptoms": "ALTER TABLE health_cases ADD COLUMN symptoms TEXT",
        "temperature": "ALTER TABLE health_cases ADD COLUMN temperature REAL",
        "noticed_when": "ALTER TABLE health_cases ADD COLUMN noticed_when TEXT",
        "additional_details": "ALTER TABLE health_cases ADD COLUMN additional_details TEXT",
        "image_path": "ALTER TABLE health_cases ADD COLUMN image_path TEXT",
        "image_name": "ALTER TABLE health_cases ADD COLUMN image_name TEXT",
        "emergency": "ALTER TABLE health_cases ADD COLUMN emergency INTEGER DEFAULT 0",
    }
    for column, statement in migrations.items():
        if column not in existing_columns:
            c.execute(statement)

    if c.execute("SELECT COUNT(*) FROM pharmacies").fetchone()[0] == 0:
        c.executemany(
            """
            INSERT INTO pharmacies(name,district,phone,upi_id)
            VALUES(?,?,?,?)
            """,
            [
                ("Pashu Care Pharmacy", "Davanagere", "0000000000", "pashucare@upi"),
                ("Animal Health Store", "Bengaluru", "0000000000", "animalhealth@upi"),
                ("Veterinary Medicine Centre", "Mysuru", "0000000000", "vetcare@upi"),
            ],
        )

    if c.execute("SELECT COUNT(*) FROM updates").fetchone()[0] == 0:
        c.executemany(
            """
            INSERT INTO updates(title,message,category,created_at)
            VALUES(?,?,?,?)
            """,
            [
                (
                    "Daily Animal Health",
                    "Observe appetite, movement, breathing and behaviour every day.",
                    "Daily Care",
                    now(),
                ),
                (
                    "Clean Drinking Water",
                    "Provide clean drinking water every day.",
                    "Prevention",
                    now(),
                ),
                (
                    "Seasonal Care",
                    "Increase observation when weather conditions change.",
                    "Seasonal",
                    now(),
                ),
            ],
        )

    c.commit()
    c.close()


init_db()

# -----------------------------
# Language
# -----------------------------
LANGUAGES = [
    "English",
    "Hindi",
    "Kannada",
    "Marathi",
    "Telugu",
    "Tamil",
    "Malayalam",
    "Gujarati",
    "Bengali",
    "Punjabi",
    "Odia",
    "Assamese",
    "Nepali",
    "Urdu",
]

T = {
    "English": {
        "welcome": "Welcome to PashuRakshak",
        "tagline": "Healthy animals. Healthy families. Stronger communities.",
        "choose": "Choose your role",
        "farmer": "Livestock Owner",
        "farmer_sub": "Manage animals and herd health",
        "vet": "Veterinary Doctor",
        "vet_sub": "Monitor animal health and cases",
        "language": "Language",
        "change": "Change role",
        "herd": "Manage Herd",
        "health": "Animal Health",
        "vaccines": "Vaccination",
        "movement": "Animal Movement",
        "pharmacy": "Pharmacy",
        "nutrition": "Food & Nutrition",
        "seasonal": "Seasonal Health",
        "awareness": "Awareness",
        "updates": "Health Updates",
        "monitor": "Health Monitoring",
        "cases": "Health Cases",
        "knowledge": "Disease Knowledge",
        "animals": "Animals",
        "healthy": "Healthy",
        "attention": "Need Attention",
        "observation": "Under Observation",
        "deaths": "Deaths",
    },

    "Hindi": {
        "welcome": "पशुरक्षक में आपका स्वागत है",
        "tagline": "स्वस्थ पशु। स्वस्थ परिवार। मजबूत समुदाय।",
        "choose": "अपनी भूमिका चुनें",
        "farmer": "पशुपालक",
        "farmer_sub": "पशुओं और झुंड का प्रबंधन करें",
        "vet": "पशु चिकित्सक",
        "vet_sub": "पशु स्वास्थ्य और मामलों की निगरानी करें",
        "language": "भाषा",
        "change": "भूमिका बदलें",
        "herd": "झुंड प्रबंधन",
        "health": "पशु स्वास्थ्य",
        "vaccines": "टीकाकरण",
        "movement": "पशु आवागमन",
        "pharmacy": "फार्मेसी",
        "nutrition": "भोजन और पोषण",
        "seasonal": "मौसमी स्वास्थ्य",
        "awareness": "जागरूकता",
        "updates": "स्वास्थ्य अपडेट",
        "monitor": "स्वास्थ्य निगरानी",
        "cases": "स्वास्थ्य मामले",
        "knowledge": "रोग जानकारी",
        "animals": "पशु",
        "healthy": "स्वस्थ",
        "attention": "ध्यान आवश्यक",
        "observation": "निगरानी में",
        "deaths": "मृत्यु",
    },

    "Kannada": {
        "welcome": "ಪಶುರಕ್ಷಕ್‌ಗೆ ಸ್ವಾಗತ",
        "tagline": "ಆರೋಗ್ಯಕರ ಪ್ರಾಣಿಗಳು. ಆರೋಗ್ಯಕರ ಕುಟುಂಬಗಳು. ಬಲವಾದ ಸಮುದಾಯಗಳು.",
        "choose": "ನಿಮ್ಮ ಪಾತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "farmer": "ಪಶುಪಾಲಕ",
        "farmer_sub": "ಪ್ರಾಣಿಗಳು ಮತ್ತು ಹಿಂಡಿನ ಆರೋಗ್ಯ ನಿರ್ವಹಿಸಿ",
        "vet": "ಪಶುವೈದ್ಯರು",
        "vet_sub": "ಪ್ರಾಣಿಗಳ ಆರೋಗ್ಯ ಮತ್ತು ಪ್ರಕರಣಗಳನ್ನು ಗಮನಿಸಿ",
        "language": "ಭಾಷೆ",
        "change": "ಪಾತ್ರ ಬದಲಿಸಿ",
        "herd": "ಹಿಂಡು ನಿರ್ವಹಣೆ",
        "health": "ಪ್ರಾಣಿ ಆರೋಗ್ಯ",
        "vaccines": "ಲಸಿಕೆ",
        "movement": "ಪ್ರಾಣಿ ಚಲನೆ",
        "pharmacy": "ಫಾರ್ಮಸಿ",
        "nutrition": "ಆಹಾರ ಮತ್ತು ಪೋಷಣೆ",
        "seasonal": "ಋತುಮಾನ ಆರೋಗ್ಯ",
        "awareness": "ಜಾಗೃತಿ",
        "updates": "ಆರೋಗ್ಯ ಅಪ್‌ಡೇಟ್‌ಗಳು",
        "monitor": "ಆರೋಗ್ಯ ಮೇಲ್ವಿಚಾರಣೆ",
        "cases": "ಆರೋಗ್ಯ ಪ್ರಕರಣಗಳು",
        "knowledge": "ರೋಗ ಮಾಹಿತಿ",
        "animals": "ಪ್ರಾಣಿಗಳು",
        "healthy": "ಆರೋಗ್ಯಕರ",
        "attention": "ಗಮನ ಅಗತ್ಯ",
        "observation": "ಗಮನದಲ್ಲಿದೆ",
        "deaths": "ಸಾವುಗಳು",
    },

    "Marathi": {
        "welcome": "पशुरक्षक मध्ये आपले स्वागत आहे",
        "tagline": "निरोगी प्राणी. निरोगी कुटुंबे. मजबूत समुदाय.",
        "choose": "आपली भूमिका निवडा",
        "farmer": "पशुपालक",
        "farmer_sub": "प्राणी आणि कळपाचे आरोग्य व्यवस्थापित करा",
        "vet": "पशुवैद्यकीय डॉक्टर",
        "vet_sub": "प्राण्यांचे आरोग्य आणि प्रकरणांचे निरीक्षण करा",
        "language": "भाषा",
        "change": "भूमिका बदला",
        "herd": "कळप व्यवस्थापन",
        "health": "प्राणी आरोग्य",
        "vaccines": "लसीकरण",
        "movement": "प्राण्यांची हालचाल",
        "pharmacy": "फार्मसी",
        "nutrition": "आहार आणि पोषण",
        "seasonal": "हंगामी आरोग्य",
        "awareness": "जागरूकता",
        "updates": "आरोग्य अपडेट्स",
        "monitor": "आरोग्य निरीक्षण",
        "cases": "आरोग्य प्रकरणे",
        "knowledge": "रोग माहिती",
        "animals": "प्राणी",
        "healthy": "निरोगी",
        "attention": "लक्ष आवश्यक",
        "observation": "निरीक्षणाखाली",
        "deaths": "मृत्यू",
    },

    "Telugu": {
        "welcome": "పశురక్షక్‌కు స్వాగతం",
        "tagline": "ఆరోగ్యకరమైన జంతువులు. ఆరోగ్యకరమైన కుటుంబాలు. బలమైన సమాజాలు.",
        "choose": "మీ పాత్రను ఎంచుకోండి",
        "farmer": "పశుపోషకుడు",
        "farmer_sub": "జంతువులు మరియు మంద ఆరోగ్యాన్ని నిర్వహించండి",
        "vet": "పశువైద్యుడు",
        "vet_sub": "జంతువుల ఆరోగ్యం మరియు కేసులను పర్యవేక్షించండి",
        "language": "భాష",
        "change": "పాత్ర మార్చండి",
        "herd": "మంద నిర్వహణ",
        "health": "జంతు ఆరోగ్యం",
        "vaccines": "టీకాలు",
        "movement": "జంతువుల కదలిక",
        "pharmacy": "ఫార్మసీ",
        "nutrition": "ఆహారం మరియు పోషణ",
        "seasonal": "కాలానుగుణ ఆరోగ్యం",
        "awareness": "అవగాహన",
        "updates": "ఆరోగ్య నవీకరణలు",
        "monitor": "ఆరోగ్య పర్యవేక్షణ",
        "cases": "ఆరోగ్య కేసులు",
        "knowledge": "వ్యాధి సమాచారం",
        "animals": "జంతువులు",
        "healthy": "ఆరోగ్యకరం",
        "attention": "శ్రద్ధ అవసరం",
        "observation": "పర్యవేక్షణలో",
        "deaths": "మరణాలు",
    },

    "Tamil": {
        "welcome": "பசுரக்ஷக்கிற்கு வரவேற்கிறோம்",
        "tagline": "ஆரோக்கியமான விலங்குகள். ஆரோக்கியமான குடும்பங்கள். வலுவான சமூகங்கள்.",
        "choose": "உங்கள் பங்கைத் தேர்வு செய்யுங்கள்",
        "farmer": "கால்நடை உரிமையாளர்",
        "farmer_sub": "விலங்குகள் மற்றும் மந்தையின் ஆரோக்கியத்தை நிர்வகிக்கவும்",
        "vet": "கால்நடை மருத்துவர்",
        "vet_sub": "விலங்கு ஆரோக்கியம் மற்றும் வழக்குகளை கண்காணிக்கவும்",
        "language": "மொழி",
        "change": "பங்கை மாற்றவும்",
        "herd": "மந்தை மேலாண்மை",
        "health": "விலங்கு ஆரோக்கியம்",
        "vaccines": "தடுப்பூசி",
        "movement": "விலங்கு நகர்வு",
        "pharmacy": "மருந்தகம்",
        "nutrition": "உணவு மற்றும் ஊட்டச்சத்து",
        "seasonal": "பருவகால ஆரோக்கியம்",
        "awareness": "விழிப்புணர்வு",
        "updates": "ஆரோக்கிய புதுப்பிப்புகள்",
        "monitor": "ஆரோக்கிய கண்காணிப்பு",
        "cases": "ஆரோக்கிய வழக்குகள்",
        "knowledge": "நோய் தகவல்",
        "animals": "விலங்குகள்",
        "healthy": "ஆரோக்கியமானது",
        "attention": "கவனம் தேவை",
        "observation": "கண்காணிப்பில்",
        "deaths": "இறப்புகள்",
    },

    "Malayalam": {
        "welcome": "പശുരക്ഷക്കിലേക്ക് സ്വാഗതം",
        "tagline": "ആരോഗ്യമുള്ള മൃഗങ്ങൾ. ആരോഗ്യമുള്ള കുടുംബങ്ങൾ. ശക്തമായ സമൂഹങ്ങൾ.",
        "choose": "നിങ്ങളുടെ പങ്ക് തിരഞ്ഞെടുക്കുക",
        "farmer": "കന്നുകാലി ഉടമ",
        "farmer_sub": "മൃഗങ്ങളുടെയും കൂട്ടത്തിന്റെയും ആരോഗ്യം നിയന്ത്രിക്കുക",
        "vet": "വെറ്ററിനറി ഡോക്ടർ",
        "vet_sub": "മൃഗങ്ങളുടെ ആരോഗ്യവും കേസുകളും നിരീക്ഷിക്കുക",
        "language": "ഭാഷ",
        "change": "പങ്ക് മാറ്റുക",
        "herd": "കൂട്ടം നിയന്ത്രണം",
        "health": "മൃഗാരോഗ്യം",
        "vaccines": "വാക്സിനേഷൻ",
        "movement": "മൃഗങ്ങളുടെ നീക്കം",
        "pharmacy": "ഫാർമസി",
        "nutrition": "ഭക്ഷണവും പോഷണവും",
        "seasonal": "കാലാവസ്ഥാ ആരോഗ്യസംരക്ഷണം",
        "awareness": "ബോധവൽക്കരണം",
        "updates": "ആരോഗ്യ അപ്ഡേറ്റുകൾ",
        "monitor": "ആരോഗ്യ നിരീക്ഷണം",
        "cases": "ആരോഗ്യ കേസുകൾ",
        "knowledge": "രോഗ വിവരങ്ങൾ",
        "animals": "മൃഗങ്ങൾ",
        "healthy": "ആരോഗ്യമുള്ളത്",
        "attention": "ശ്രദ്ധ ആവശ്യമാണ്",
        "observation": "നിരീക്ഷണത്തിൽ",
        "deaths": "മരണങ്ങൾ",
    },

    "Gujarati": {
        "welcome": "પશુરક્ષકમાં આપનું સ્વાગત છે",
        "tagline": "સ્વસ્થ પ્રાણીઓ. સ્વસ્થ પરિવારો. મજબૂત સમુદાયો.",
        "choose": "તમારી ભૂમિકા પસંદ કરો",
        "farmer": "પશુપાલક",
        "farmer_sub": "પ્રાણીઓ અને ટોળાના સ્વાસ્થ્યનું સંચાલન કરો",
        "vet": "પશુચિકિત્સક",
        "vet_sub": "પ્રાણીઓના સ્વાસ્થ્ય અને કેસોનું નિરીક્ષણ કરો",
        "language": "ભાષા",
        "change": "ભૂમિકા બદલો",
        "herd": "ટોળું વ્યવસ્થાપન",
        "health": "પ્રાણી આરોગ્ય",
        "vaccines": "રસીકરણ",
        "movement": "પ્રાણી હલનચલન",
        "pharmacy": "ફાર્મસી",
        "nutrition": "ખોરાક અને પોષણ",
        "seasonal": "મોસમી આરોગ્ય",
        "awareness": "જાગૃતિ",
        "updates": "આરોગ્ય અપડેટ્સ",
        "monitor": "આરોગ્ય દેખરેખ",
        "cases": "આરોગ્ય કેસ",
        "knowledge": "રોગની માહિતી",
        "animals": "પ્રાણીઓ",
        "healthy": "સ્વસ્થ",
        "attention": "ધ્યાન જરૂરી",
        "observation": "નિરીક્ષણ હેઠળ",
        "deaths": "મૃત્યુ",
    },

    "Bengali": {
        "welcome": "পশুরক্ষকে স্বাগতম",
        "tagline": "সুস্থ প্রাণী। সুস্থ পরিবার। শক্তিশালী সমাজ।",
        "choose": "আপনার ভূমিকা বেছে নিন",
        "farmer": "পশুপালক",
        "farmer_sub": "পশু ও পশুপালের স্বাস্থ্য পরিচালনা করুন",
        "vet": "পশু চিকিৎসক",
        "vet_sub": "পশুর স্বাস্থ্য ও কেস পর্যবেক্ষণ করুন",
        "language": "ভাষা",
        "change": "ভূমিকা পরিবর্তন করুন",
        "herd": "পশুপাল ব্যবস্থাপনা",
        "health": "পশুর স্বাস্থ্য",
        "vaccines": "টিকাদান",
        "movement": "পশুর চলাচল",
        "pharmacy": "ফার্মেসি",
        "nutrition": "খাদ্য ও পুষ্টি",
        "seasonal": "মৌসুমি স্বাস্থ্য",
        "awareness": "সচেতনতা",
        "updates": "স্বাস্থ্য আপডেট",
        "monitor": "স্বাস্থ্য পর্যবেক্ষণ",
        "cases": "স্বাস্থ্য সংক্রান্ত কেস",
        "knowledge": "রোগের তথ্য",
        "animals": "পশু",
        "healthy": "সুস্থ",
        "attention": "মনোযোগ প্রয়োজন",
        "observation": "পর্যবেক্ষণে",
        "deaths": "মৃত্যু",
    },

    "Punjabi": {
        "welcome": "ਪਸ਼ੂਰਕਸ਼ਕ ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ",
        "tagline": "ਤੰਦਰੁਸਤ ਪਸ਼ੂ। ਤੰਦਰੁਸਤ ਪਰਿਵਾਰ। ਮਜ਼ਬੂਤ ਭਾਈਚਾਰੇ।",
        "choose": "ਆਪਣੀ ਭੂਮਿਕਾ ਚੁਣੋ",
        "farmer": "ਪਸ਼ੂ ਪਾਲਕ",
        "farmer_sub": "ਪਸ਼ੂਆਂ ਅਤੇ ਝੁੰਡ ਦੀ ਸਿਹਤ ਸੰਭਾਲੋ",
        "vet": "ਪਸ਼ੂ ਡਾਕਟਰ",
        "vet_sub": "ਪਸ਼ੂਆਂ ਦੀ ਸਿਹਤ ਅਤੇ ਕੇਸਾਂ ਦੀ ਨਿਗਰਾਨੀ ਕਰੋ",
        "language": "ਭਾਸ਼ਾ",
        "change": "ਭੂਮਿਕਾ ਬਦਲੋ",
        "herd": "ਝੁੰਡ ਪ੍ਰਬੰਧਨ",
        "health": "ਪਸ਼ੂ ਸਿਹਤ",
        "vaccines": "ਟੀਕਾਕਰਨ",
        "movement": "ਪਸ਼ੂਆਂ ਦੀ ਆਵਾਜਾਈ",
        "pharmacy": "ਫਾਰਮੇਸੀ",
        "nutrition": "ਭੋਜਨ ਅਤੇ ਪੋਸ਼ਣ",
        "seasonal": "ਮੌਸਮੀ ਸਿਹਤ",
        "awareness": "ਜਾਗਰੂਕਤਾ",
        "updates": "ਸਿਹਤ ਅੱਪਡੇਟ",
        "monitor": "ਸਿਹਤ ਨਿਗਰਾਨੀ",
        "cases": "ਸਿਹਤ ਮਾਮਲੇ",
        "knowledge": "ਬਿਮਾਰੀ ਦੀ ਜਾਣਕਾਰੀ",
        "animals": "ਪਸ਼ੂ",
        "healthy": "ਤੰਦਰੁਸਤ",
        "attention": "ਧਿਆਨ ਦੀ ਲੋੜ",
        "observation": "ਨਿਗਰਾਨੀ ਹੇਠ",
        "deaths": "ਮੌਤਾਂ",
    },

    "Odia": {
        "welcome": "ପଶୁରକ୍ଷକକୁ ସ୍ୱାଗତ",
        "tagline": "ସୁସ୍ଥ ପଶୁ। ସୁସ୍ଥ ପରିବାର। ଶକ୍ତିଶାଳୀ ସମୁଦାୟ।",
        "choose": "ଆପଣଙ୍କ ଭୂମିକା ବାଛନ୍ତୁ",
        "farmer": "ପଶୁପାଳକ",
        "farmer_sub": "ପଶୁ ଏବଂ ଗୋଠର ସ୍ୱାସ୍ଥ୍ୟ ପରିଚାଳନା କରନ୍ତୁ",
        "vet": "ପଶୁ ଚିକିତ୍ସକ",
        "vet_sub": "ପଶୁ ସ୍ୱାସ୍ଥ୍ୟ ଏବଂ ମାମଲା ନିରୀକ୍ଷଣ କରନ୍ତୁ",
        "language": "ଭାଷା",
        "change": "ଭୂମିକା ବଦଳାନ୍ତୁ",
        "herd": "ଗୋଠ ପରିଚାଳନା",
        "health": "ପଶୁ ସ୍ୱାସ୍ଥ୍ୟ",
        "vaccines": "ଟିକାକରଣ",
        "movement": "ପଶୁ ଗତିବିଧି",
        "pharmacy": "ଫାର୍ମାସି",
        "nutrition": "ଖାଦ୍ୟ ଏବଂ ପୋଷଣ",
        "seasonal": "ଋତୁକାଳୀନ ସ୍ୱାସ୍ଥ୍ୟ",
        "awareness": "ସଚେତନତା",
        "updates": "ସ୍ୱାସ୍ଥ୍ୟ ଅଦ୍ୟତନ",
        "monitor": "ସ୍ୱାସ୍ଥ୍ୟ ନିରୀକ୍ଷଣ",
        "cases": "ସ୍ୱାସ୍ଥ୍ୟ ମାମଲା",
        "knowledge": "ରୋଗ ସୂଚନା",
        "animals": "ପଶୁ",
        "healthy": "ସୁସ୍ଥ",
        "attention": "ଧ୍ୟାନ ଆବଶ୍ୟକ",
        "observation": "ନିରୀକ୍ଷଣରେ",
        "deaths": "ମୃତ୍ୟୁ",
    },

    "Assamese": {
        "welcome": "পশুৰক্ষকলৈ স্বাগতম",
        "tagline": "সুস্থ পশু। সুস্থ পৰিয়াল। শক্তিশালী সমাজ।",
        "choose": "আপোনাৰ ভূমিকা বাছনি কৰক",
        "farmer": "পশুপালক",
        "farmer_sub": "পশু আৰু জাকৰ স্বাস্থ্য পৰিচালনা কৰক",
        "vet": "পশু চিকিৎসক",
        "vet_sub": "পশুৰ স্বাস্থ্য আৰু ঘটনাসমূহ নিৰীক্ষণ কৰক",
        "language": "ভাষা",
        "change": "ভূমিকা সলনি কৰক",
        "herd": "জাক পৰিচালনা",
        "health": "পশুৰ স্বাস্থ্য",
        "vaccines": "টিকাকৰণ",
        "movement": "পশুৰ চলাচল",
        "pharmacy": "ফাৰ্মাচী",
        "nutrition": "খাদ্য আৰু পুষ্টি",
        "seasonal": "ঋতুভিত্তিক স্বাস্থ্য",
        "awareness": "সজাগতা",
        "updates": "স্বাস্থ্য আপডেট",
        "monitor": "স্বাস্থ্য নিৰীক্ষণ",
        "cases": "স্বাস্থ্যৰ ঘটনা",
        "knowledge": "ৰোগৰ তথ্য",
        "animals": "পশু",
        "healthy": "সুস্থ",
        "attention": "মনোযোগৰ প্ৰয়োজন",
        "observation": "নিৰীক্ষণত",
        "deaths": "মৃত্যু",
    },

    "Nepali": {
        "welcome": "पशुरक्षकमा स्वागत छ",
        "tagline": "स्वस्थ पशु। स्वस्थ परिवार। बलियो समुदाय।",
        "choose": "आफ्नो भूमिका छान्नुहोस्",
        "farmer": "पशुपालक",
        "farmer_sub": "पशु र बथानको स्वास्थ्य व्यवस्थापन गर्नुहोस्",
        "vet": "पशु चिकित्सक",
        "vet_sub": "पशुको स्वास्थ्य र केसहरू निगरानी गर्नुहोस्",
        "language": "भाषा",
        "change": "भूमिका परिवर्तन गर्नुहोस्",
        "herd": "बथान व्यवस्थापन",
        "health": "पशु स्वास्थ्य",
        "vaccines": "खोप",
        "movement": "पशु आवागमन",
        "pharmacy": "फार्मेसी",
        "nutrition": "खाना र पोषण",
        "seasonal": "मौसमी स्वास्थ्य",
        "awareness": "सचेतना",
        "updates": "स्वास्थ्य अपडेट",
        "monitor": "स्वास्थ्य निगरानी",
        "cases": "स्वास्थ्य केसहरू",
        "knowledge": "रोग जानकारी",
        "animals": "पशुहरू",
        "healthy": "स्वस्थ",
        "attention": "ध्यान आवश्यक",
        "observation": "निगरानीमा",
        "deaths": "मृत्यु",
    },

    "Urdu": {
        "welcome": "پشورکشک میں خوش آمدید",
        "tagline": "صحت مند جانور۔ صحت مند خاندان۔ مضبوط معاشرے۔",
        "choose": "اپنا کردار منتخب کریں",
        "farmer": "مویشی پالنے والا",
        "farmer_sub": "جانوروں اور ریوڑ کی صحت کا انتظام کریں",
        "vet": "ویٹرنری ڈاکٹر",
        "vet_sub": "جانوروں کی صحت اور کیسز کی نگرانی کریں",
        "language": "زبان",
        "change": "کردار تبدیل کریں",
        "herd": "ریوڑ کا انتظام",
        "health": "جانوروں کی صحت",
        "vaccines": "ویکسینیشن",
        "movement": "جانوروں کی نقل و حرکت",
        "pharmacy": "فارمیسی",
        "nutrition": "خوراک اور غذائیت",
        "seasonal": "موسمی صحت",
        "awareness": "آگاہی",
        "updates": "صحت کی تازہ معلومات",
        "monitor": "صحت کی نگرانی",
        "cases": "صحت کے کیسز",
        "knowledge": "بیماری کی معلومات",
        "animals": "جانور",
        "healthy": "صحت مند",
        "attention": "توجہ درکار",
        "observation": "نگرانی میں",
        "deaths": "اموات",
    },
}



if "language" not in st.session_state:
    st.session_state.language = "English"

if "role" not in st.session_state:
    st.session_state.role = None

if "page" not in st.session_state:
    st.session_state.page = "home"


def L(key):
    return T[st.session_state.language].get(
        key,
        T["English"].get(key, key),
    )


# -----------------------------
# CSS
# -----------------------------
st.markdown(
    f"""
    <style>
    :root {{
        --pr-green: {GREEN};
        --pr-green-dark: {GREEN_DARK};
        --pr-green-soft: {GREEN_SOFT};
        --pr-border: {GREEN_BORDER};
        --pr-grey: {GREY};
        --pr-grey-dark: {GREY_DARK};
        --pr-white: #FFFFFF;
        --pr-text: {TEXT};
        --pr-muted: {MUTED};
    }}

    /* ---------- Global page ---------- */
    html, body, [class*="css"] {{
        color: var(--pr-text) !important;
    }}

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stHeader"] {{
        background: #FFFFFF !important;
    }}

    .block-container {{
        max-width: 1150px !important;
        padding-top: 28px !important;
        background: #FFFFFF !important;
    }}

    h1, h2, h3, h4, h5, h6,
    p, label, span {{
        color: var(--pr-text);
    }}

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {{
        background: #FFFFFF !important;
        border-right: 1px solid var(--pr-border) !important;
    }}

    [data-testid="stSidebar"] * {{
        color: var(--pr-text) !important;
    }}

    /* ---------- Every normal Streamlit button ---------- */
    [data-testid="stButton"] > button {{
        background: var(--pr-green) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--pr-green) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-height: 44px !important;
        box-shadow: none !important;
    }}

    [data-testid="stButton"] > button *,
    [data-testid="stButton"] > button p,
    [data-testid="stButton"] > button span {{
        color: #FFFFFF !important;
    }}

    [data-testid="stButton"] > button:hover,
    [data-testid="stButton"] > button:focus,
    [data-testid="stButton"] > button:active {{
        background: var(--pr-green-dark) !important;
        color: #FFFFFF !important;
        border-color: var(--pr-green-dark) !important;
    }}

    [data-testid="stButton"] > button:hover *,
    [data-testid="stButton"] > button:focus *,
    [data-testid="stButton"] > button:active * {{
        color: #FFFFFF !important;
    }}

    /* ---------- Square role buttons ---------- */
    .role-holder [data-testid="stButton"] > button {{
        background: var(--pr-green) !important;
        color: #FFFFFF !important;
        border: 2px solid var(--pr-green) !important;
        border-radius: 22px !important;
        width: 210px !important;
        height: 210px !important;
        min-height: 210px !important;
        max-height: 210px !important;
        margin: auto !important;
        white-space: pre-wrap !important;
        font-size: 16px !important;
        line-height: 1.45 !important;
        box-shadow: 0 8px 25px rgba(23,107,82,.12) !important;
    }}

    .role-holder [data-testid="stButton"] > button *,
    .role-holder [data-testid="stButton"] > button p,
    .role-holder [data-testid="stButton"] > button span {{
        color: #FFFFFF !important;
    }}

    .role-holder [data-testid="stButton"] > button:hover {{
        background: var(--pr-green-dark) !important;
        border-color: var(--pr-green-dark) !important;
    }}

    /* ---------- Feature cards ---------- */
    .feature-holder [data-testid="stButton"] > button {{
        background: var(--pr-green-soft) !important;
        color: var(--pr-green) !important;
        border: 1px solid var(--pr-border) !important;
        border-radius: 17px !important;
        min-height: 105px !important;
        white-space: pre-wrap !important;
        font-size: 15px !important;
        line-height: 1.4 !important;
        box-shadow: none !important;
    }}

    .feature-holder [data-testid="stButton"] > button *,
    .feature-holder [data-testid="stButton"] > button p,
    .feature-holder [data-testid="stButton"] > button span {{
        color: var(--pr-green) !important;
    }}

    .feature-holder [data-testid="stButton"] > button:hover {{
        background: var(--pr-green) !important;
        color: #FFFFFF !important;
        border-color: var(--pr-green) !important;
    }}

    .feature-holder [data-testid="stButton"] > button:hover *,
    .feature-holder [data-testid="stButton"] > button:hover p,
    .feature-holder [data-testid="stButton"] > button:hover span {{
        color: #FFFFFF !important;
    }}

    /* ---------- Metrics ---------- */
    [data-testid="stMetric"] {{
        background: #FFFFFF !important;
        border: 1px solid var(--pr-border) !important;
        border-radius: 15px !important;
        padding: 14px !important;
        box-shadow: none !important;
    }}

    [data-testid="stMetricValue"] {{
        color: var(--pr-green) !important;
    }}

    [data-testid="stMetricLabel"] {{
        color: var(--pr-muted) !important;
    }}

    /* ---------- Inputs / selects ---------- */
    input,
    textarea {{
        background: #FFFFFF !important;
        color: var(--pr-text) !important;
        border-color: var(--pr-border) !important;
    }}

    input::placeholder,
    textarea::placeholder {{
        color: #7A7A7A !important;
    }}

    [data-baseweb="select"] > div {{
        background: #FFFFFF !important;
        color: var(--pr-text) !important;
        border-color: var(--pr-border) !important;
    }}

    [data-baseweb="select"] *,
    [data-baseweb="select"] span {{
        color: var(--pr-text) !important;
    }}

    [role="listbox"],
    [data-baseweb="menu"] {{
        background: #FFFFFF !important;
        color: var(--pr-text) !important;
    }}

    [role="option"] {{
        background: #FFFFFF !important;
        color: var(--pr-text) !important;
    }}

    [role="option"]:hover,
    [aria-selected="true"] {{
        background: var(--pr-green-soft) !important;
        color: var(--pr-green) !important;
    }}

    /* ---------- Forms ---------- */
    [data-testid="stForm"] {{
        background: #FFFFFF !important;
        border-color: var(--pr-border) !important;
    }}

    [data-testid="stFormSubmitButton"] > button {{
        background: var(--pr-green) !important;
        color: #FFFFFF !important;
        border-color: var(--pr-green) !important;
    }}

    [data-testid="stFormSubmitButton"] > button * {{
        color: #FFFFFF !important;
    }}

    /* ---------- Expanders ---------- */
    [data-testid="stExpander"] {{
        background: #FFFFFF !important;
        border: 1px solid var(--pr-border) !important;
        border-radius: 14px !important;
    }}

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary:hover {{
        background: var(--pr-green-soft) !important;
        color: var(--pr-green) !important;
    }}

    [data-testid="stExpander"] summary * {{
        color: var(--pr-green) !important;
    }}

    /* ---------- Alerts / messages ---------- */
    [data-testid="stAlert"] {{
        background: var(--pr-green-soft) !important;
        border: 1px solid var(--pr-border) !important;
        color: var(--pr-text) !important;
    }}

    [data-testid="stAlert"] * {{
        color: var(--pr-text) !important;
    }}

    /* ---------- Code / preformatted areas ----------
       If Streamlit renders anything in a code-style surface,
       it is grey instead of black. Text remains readable. */
    [data-testid="stCodeBlock"],
    [data-testid="stCodeBlock"] pre,
    pre,
    code {{
        background: var(--pr-grey) !important;
        color: var(--pr-text) !important;
        border-color: var(--pr-grey-dark) !important;
    }}

    /* ---------- Data tables ---------- */
    [data-testid="stDataFrame"],
    [data-testid="stDataFrame"] iframe {{
        background: #FFFFFF !important;
    }}

    /* ---------- Remove dark Streamlit surfaces ---------- */
    [data-testid="stDecoration"],
    [data-testid="stToolbar"] {{
        background: transparent !important;
    }}

    /* ---------- Custom information cards ---------- */
    .green-info {{
        background: var(--pr-green-soft);
        border: 1px solid var(--pr-border);
        border-radius: 16px;
        padding: 18px;
        margin: 10px 0;
    }}

    .green-info h4 {{
        color: var(--pr-green) !important;
        margin: 0 0 8px 0;
    }}

    .green-info p {{
        color: var(--pr-text) !important;
        margin: 0;
    }}

    /* ---------- Mobile ---------- */
    @media(max-width:800px) {{
        .role-holder [data-testid="stButton"] > button {{
            width: 175px !important;
            height: 175px !important;
            min-height: 175px !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Helpers
# -----------------------------
def go(page):
    st.session_state.page = page
    st.rerun()


def reset_role():
    st.session_state.role = None
    st.session_state.page = "home"
    st.rerun()


def records(sql, params=()):
    c = db()
    rows = c.execute(sql, params).fetchall()
    c.close()
    return [dict(r) for r in rows]


def stats():
    c = db()
    animals = c.execute("SELECT COALESCE(SUM(count),0) FROM herds").fetchone()[0]
    diseased = c.execute(
        """
        SELECT COALESCE(SUM(affected_count),0)
        FROM health_cases
        WHERE status IN ('Suspected','Confirmed by Vet')
        """
    ).fetchone()[0]
    observation = c.execute(
        """
        SELECT COALESCE(SUM(affected_count),0)
        FROM health_cases
        WHERE status='Under Observation'
        """
    ).fetchone()[0]
    deaths = c.execute(
        """
        SELECT COALESCE(SUM(affected_count),0)
        FROM health_cases
        WHERE status='Deceased'
        """
    ).fetchone()[0]
    c.close()
    healthy = max(0, animals - diseased - observation - deaths)
    return animals, healthy, diseased, observation, deaths


def show_table(data):
    if not data:
        st.info("No records available yet.")
        return
    st.dataframe(data, use_container_width=True, hide_index=True)


def delete_record(table, record_id):
    """Delete one user-created record and clean up attached health-case photos."""
    c = db()
    if table == "health_cases":
        row = c.execute("SELECT image_path FROM health_cases WHERE id=?", (int(record_id),)).fetchone()
        if row and row[0]:
            image_file = BASE_DIR / row[0]
            try:
                if image_file.exists():
                    image_file.unlink()
            except OSError:
                pass
    c.execute(f"DELETE FROM {table} WHERE id=?", (int(record_id),))
    c.commit()
    c.close()


def delete_section(table, title, label="Record"):
    """Provide an explicit confirmation-based delete control for user-created records."""
    rows = records(f"SELECT * FROM {table} ORDER BY id DESC")
    if not rows:
        return

    st.markdown(f"### 🗑️ {title}")
    choices = {
        row["id"]: row for row in rows
    }
    selected_id = st.selectbox(
        f"Select {label} to delete",
        list(choices.keys()),
        format_func=lambda rid: f"{label} #{rid}",
        key=f"delete_select_{table}",
    )
    confirm = st.checkbox(
        "I understand that this record will be permanently deleted.",
        key=f"delete_confirm_{table}",
    )
    if st.button(
        f"Delete {label} #{selected_id}",
        type="secondary",
        disabled=not confirm,
        key=f"delete_button_{table}",
    ):
        delete_record(table, selected_id)
        st.success(f"{label} #{selected_id} deleted successfully.")
        st.rerun()


def card(title, text, icon="🌿"):
    st.markdown(
        f"""
        <div class="green-info">
            <h4>{icon} {title}</h4>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def emergency_alert(title, details):
    """Show a prominent emergency warning without making an autonomous diagnosis."""
    st.markdown(
        f"""
        <div style="
            border: 2px solid #C62828;
            background: #FFF3F3;
            border-radius: 14px;
            padding: 16px 18px;
            margin: 12px 0 18px 0;
        ">
            <div style="color:#B71C1C; font-size:20px; font-weight:800;">🚨 {title}</div>
            <div style="color:#4A1F1F; margin-top:8px; line-height:1.55;">{details}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# Language selector
# -----------------------------
with st.sidebar:
    language = st.selectbox(
        L("language"),
        LANGUAGES,
        index=LANGUAGES.index(st.session_state.language),
    )

if language != st.session_state.language:
    st.session_state.language = language
    st.rerun()

with st.sidebar:
    st.caption(f"{len(LANGUAGES)} languages available")


# ============================================================
# HOME / ROLE SELECTION
# ============================================================
if st.session_state.role is None:

    st.markdown(
        f"""
        <div style="
            color:{GREEN};
            font-size:13px;
            font-weight:800;
            letter-spacing:2px;
            margin-bottom:8px;
        ">
            PASHURAKSHAK
        </div>
        """,
        unsafe_allow_html=True,
    )

    # IMPORTANT:
    # This hero is a Streamlit HTML component, not markdown.
    # Therefore it cannot become a markdown code block.
    st.components.v1.html(
        f"""
        <div style="
            background:{GREEN};
            border-radius:24px;
            padding:38px 42px;
            box-sizing:border-box;
            font-family:Arial,sans-serif;
            min-height:245px;
        ">
            <div style="
                color:#BDE4D0;
                font-size:12px;
                font-weight:800;
                letter-spacing:1.8px;
            ">
                PASHURAKSHAK
            </div>

            <div style="
                color:#FFFFFF;
                font-family:Georgia,serif;
                font-size:38px;
                font-weight:700;
                line-height:1.2;
                margin-top:12px;
            ">
                {L("welcome")}
            </div>

            <div style="
                color:#FFFFFF;
                font-size:17px;
                line-height:1.6;
                margin-top:13px;
            ">
                {L("tagline")}
                <span style="font-size:28px;margin-left:8px;">🐄</span>
            </div>
        </div>
        """,
        height=275,
        scrolling=False,
    )

    st.markdown(f"## {L('choose')}")
    st.write("")

    left, farmer_col, gap, vet_col, right = st.columns(
        [1, 2.2, 0.35, 2.2, 1]
    )

    with farmer_col:
        st.markdown('<div class="role-holder">', unsafe_allow_html=True)
        farmer_clicked = st.button(
            f"👨‍🌾\n\n{L('farmer')}\n\n{L('farmer_sub')}",
            key="role_farmer",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with vet_col:
        st.markdown('<div class="role-holder">', unsafe_allow_html=True)
        vet_clicked = st.button(
            f"🩺\n\n{L('vet')}\n\n{L('vet_sub')}",
            key="role_vet",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if farmer_clicked:
        st.session_state.role = "farmer"
        st.session_state.page = "farmer_home"
        st.rerun()

    if vet_clicked:
        st.session_state.role = "vet"
        st.session_state.page = "vet_home"
        st.rerun()

    st.stop()


# ============================================================
# HEADER
# ============================================================
top1, top2 = st.columns([5, 1])

with top1:
    role_name = L("farmer") if st.session_state.role == "farmer" else L("vet")
    st.markdown(
        f"""
        <div style="
            color:{GREEN};
            font-size:13px;
            font-weight:800;
            letter-spacing:2px;
        ">PASHURAKSHAK</div>
        <h1 style="color:{TEXT};margin-top:4px;">{role_name}</h1>
        """,
        unsafe_allow_html=True,
    )

with top2:
    if st.button(L("change"), use_container_width=True):
        reset_role()


animals, healthy, diseased, observation, deaths = stats()

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric(L("animals"), animals)
m2.metric(L("healthy"), healthy)
m3.metric(L("attention"), diseased)
m4.metric(L("observation"), observation)
m5.metric(L("deaths"), deaths)


# ============================================================
# FARMER
# ============================================================
if st.session_state.role == "farmer":

    features = [
        ("🐄", L("herd"), "herds"),
        ("🩺", L("health"), "health"),
        ("💉", L("vaccines"), "vaccines"),
        ("📍", L("movement"), "movement"),
        ("💊", L("pharmacy"), "pharmacy"),
        ("🥬", L("nutrition"), "nutrition"),
        ("🌦️", L("seasonal"), "seasonal"),
        ("📢", L("awareness"), "awareness"),
        ("🔔", L("updates"), "updates"),
    ]

    cols = st.columns(3, gap="medium")

    for i, (icon, label, page) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                '<div class="feature-holder">',
                unsafe_allow_html=True,
            )
            clicked = st.button(
                f"{icon}\n\n{label}",
                key=f"farmer_feature_{page}",
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
            if clicked:
                go(page)

    st.write("")

    if st.session_state.page == "farmer_home":
        st.subheader("Recent Health Records")
        show_table(
            records(
                """
                SELECT *
                FROM health_cases
                ORDER BY id DESC
                LIMIT 10
                """
            )
        )

    elif st.session_state.page == "herds":
        st.subheader(L("herd"))

        with st.form("add_herd"):
            a, b, c = st.columns(3)
            species = a.selectbox(
                "Animal Type",
                ["Cattle", "Buffalo", "Goat", "Sheep", "Pig", "Poultry", "Other"],
            )
            breed = b.text_input("Breed")
            count = c.number_input(
                "Number of Animals",
                min_value=1,
                value=5000,
                step=1,
            )

            a, b, c = st.columns(3)
            district = a.text_input("District")
            taluk = b.text_input("Taluk")
            location = c.text_input("Village / Location")

            save = st.form_submit_button(
                "Add Herd",
                use_container_width=True,
            )

            if save:
                cdb = db()
                cdb.execute(
                    """
                    INSERT INTO herds(
                        species,breed,count,district,taluk,location,created_at
                    )
                    VALUES(?,?,?,?,?,?,?)
                    """,
                    (
                        species,
                        breed,
                        int(count),
                        district,
                        taluk,
                        location,
                        now(),
                    ),
                )
                cdb.commit()
                cdb.close()
                st.success("Herd saved successfully.")
                st.rerun()

        st.subheader("Registered Herds")
        show_table(records("SELECT * FROM herds ORDER BY id DESC"))
        delete_section("herds", "Delete Herd", "Herd")

    elif st.session_state.page == "health":
        st.subheader(L("health"))

        # Step 1 — Choose the animal
        st.markdown("### Step 1 — Choose an animal")

        animal_type = st.selectbox(
            "Choose an animal",
            [
                "Cow",
                "Buffalo",
                "Goat",
                "Sheep",
                "Pig",
                "Poultry",
                "Other",
            ],
            index=0,
        )

        # Step 2 — Select symptoms
        st.markdown("### Step 2 — What have you noticed?")
        st.caption(
            "Pick every sign you can see. It is okay if you are not sure."
        )

        symptom_options = [
            "Fever / feels hot",
            "Eating much less / not eating",
            "Very weak / lying down",
            "Difficulty breathing",
            "Skin lumps, scabs, or pox-like marks",
            "Mouth sores, drooling, or foot lesions",
            "Limping / cannot walk normally",
            "Nose or eye discharge",
            "Diarrhoea / loose droppings",
            "Sudden fall in milk production",
            "Swollen, hot, or painful udder",
            "Bleeding / sudden death in herd",
            "Vomiting / repeated retching",
            "Severe itching, hair loss, or skin irritation",
            "Sudden unusual behaviour, fits, or head tilt",
            "Belly pain, rolling, or swollen stomach",
        ]

        selected_symptoms = []

        symptom_cols = st.columns(2)
        for i, symptom in enumerate(symptom_options):
            with symptom_cols[i % 2]:
                if st.checkbox(
                    symptom,
                    key=f"health_symptom_{i}",
                ):
                    selected_symptoms.append(symptom)

        # Additional details box
        additional_details = st.text_area(
            "Additional details",
            placeholder=(
                "Example: drinking less water than usual, "
                "started after grazing, or any other detail you noticed."
            ),
            height=90,
        )

        # Photo evidence
        st.markdown("### 📷 Add a photo (optional)")
        st.caption(
            "You can upload a clear photo of the animal, wound, skin change, eye, mouth, hoof, udder, or other visible problem. "
            "A photo is saved with the health case when you save it."
        )

        photo_mode = st.radio(
            "Photo source",
            ["Upload a photo", "Take a photo with camera"],
            horizontal=True,
            key="health_photo_mode",
        )

        health_image = None
        if photo_mode == "Upload a photo":
            health_image = st.file_uploader(
                "Choose an image",
                type=["jpg", "jpeg", "png", "webp"],
                key="health_image_upload",
                help="Use a clear, well-lit photo. Avoid including unnecessary personal information in the image.",
            )
        else:
            health_image = st.camera_input(
                "Take a photo",
                key="health_camera_input",
            )

        if health_image is not None:
            st.image(
                health_image,
                caption="Photo attached to this health check",
                width=420,
            )
            st.caption("The current version stores the photo with the health case. AI image identification will be connected in the next stage.")

        # Step 3 — Helpful details
        st.markdown("### Step 3 — A few helpful details")

        temp_col, noticed_col = st.columns(2)

        with temp_col:
            temperature = st.number_input(
                "Temperature, if you know it (°F)",
                min_value=80.0,
                max_value=115.0,
                value=None,
                step=0.1,
                format="%.1f",
                placeholder="Example: 104",
            )

        with noticed_col:
            noticed_when = st.selectbox(
                "When did you first notice it?",
                [
                    "Today",
                    "Yesterday",
                    "2–3 days ago",
                    "4–7 days ago",
                    "More than a week ago",
                    "Not sure",
                ],
            )

        emergency_found = []

        if st.button("Check Health", use_container_width=True):
            # Combine the structured symptom selections with the free-text details
            # so the existing health-sign matching can still work.
            selected_text = " ".join(selected_symptoms)
            combined_text = f"{selected_text} {additional_details}".lower()

            # Emergency warning signs are intentionally broad safety triggers.
            # They do not diagnose a disease; they tell the user to seek prompt
            # veterinary attention when serious signs are present.
            emergency_signs = [
                "difficulty breathing",
                "bleeding / sudden death in herd",
                "very weak / lying down",
                "sudden unusual behaviour, fits, or head tilt",
                "sudden death",
                "severe breathing",
                "cannot breathe",
                "unconscious",
                "collapse",
                "seizure",
                "fits",
                "heavy bleeding",
            ]

            emergency_found = [
                sign for sign in emergency_signs
                if sign in combined_text
            ]

            if emergency_found:
                emergency_alert(
                    "Emergency health alert",
                    "Serious warning signs were selected. Please contact a veterinarian or nearby veterinary service immediately. Keep the animal calm and separated from the rest of the herd if this can be done safely. Do not give medicines unless a veterinarian advises you.",
                )
                st.warning(
                    "Emergency signs detected: "
                    + ", ".join(emergency_found)
                )

            possible = []

            if any(
                x in combined_text
                for x in [
                    "mouth sore",
                    "salivation",
                    "drooling",
                    "foot lesion",
                    "foot sore",
                    "lameness",
                    "blister",
                ]
            ):
                possible.append("Foot-and-Mouth Disease")

            if any(
                x in combined_text
                for x in [
                    "skin lump",
                    "skin lumps",
                    "nodule",
                    "nodules",
                    "skin lesion",
                    "scabs",
                    "pox-like",
                ]
            ):
                possible.append("Lumpy Skin Disease")

            if animal_type in ["Goat", "Sheep"] and any(
                x in combined_text
                for x in [
                    "diarrhea",
                    "diarrhoea",
                    "nasal discharge",
                    "nose discharge",
                    "cough",
                    "weak",
                ]
            ):
                possible.append("PPR")

            if any(
                x in combined_text
                for x in [
                    "panting",
                    "heavy breathing",
                    "heat stress",
                    "excessive sweating",
                    "feels hot",
                    "fever",
                ]
            ):
                possible.append("Heat Stress")

            if possible:
                card(
                    "Health signs to discuss",
                    ", ".join(possible),
                    "🩺",
                )
            else:
                card(
                    "Health status",
                    "No specific health pattern was found from the selected observations.",
                    "🌿",
                )

            if temperature is not None:
                st.info(
                    f"Recorded temperature: {temperature:.1f} °F • "
                    f"First noticed: {noticed_when}"
                )
            else:
                st.info(
                    f"Temperature: Not provided • "
                    f"First noticed: {noticed_when}"
                )

            if additional_details.strip():
                st.caption(f"Additional details: {additional_details.strip()}")

            st.subheader("Care & Precautions")

            precautions = [
                "Keep the affected animal under observation.",
                "Provide clean drinking water.",
                "Keep housing and feeding areas clean.",
                "Avoid unnecessary movement of visibly sick animals.",
                "Watch appetite, movement, breathing and behaviour.",
                "Contact a veterinary professional if symptoms continue or worsen.",
            ]

            for p in precautions:
                card("Care", p, "✓")

        st.divider()
        st.subheader("Record Health Case")

        with st.form("health_case"):
            a, b, c = st.columns(3)
            herd_id = a.number_input("Herd ID", min_value=1, value=1)
            affected = b.number_input(
                "Affected Animals",
                min_value=1,
                value=1,
            )
            status = c.selectbox(
                "Status",
                [
                    "Suspected",
                    "Under Observation",
                    "Confirmed by Vet",
                    "Recovered",
                    "Deceased",
                ],
            )
            notes = st.text_area("Notes")

            save = st.form_submit_button(
                "Save Health Case",
                use_container_width=True,
            )

            if save:
                cdb = db()
                image_path = None
                image_name = None

                if health_image is not None:
                    original_name = getattr(health_image, "name", "animal_photo.jpg")
                    suffix = Path(original_name).suffix.lower() or ".jpg"
                    safe_name = f"health_case_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}{suffix}"
                    destination = IMAGE_DIR / safe_name
                    destination.write_bytes(health_image.getbuffer())
                    image_path = str(destination.relative_to(BASE_DIR))
                    image_name = original_name

                cdb.execute(
                    """
                    INSERT INTO health_cases(
                        herd_id, affected_count, status, notes, created_at,
                        animal_type, symptoms, temperature, noticed_when,
                        additional_details, image_path, image_name, emergency
                    )
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        int(herd_id),
                        int(affected),
                        status,
                        notes,
                        now(),
                        animal_type,
                        ", ".join(selected_symptoms),
                        float(temperature) if temperature is not None else None,
                        noticed_when,
                        additional_details.strip(),
                        image_path,
                        image_name,
                        1 if emergency_found else 0,
                    ),
                )
                cdb.commit()
                cdb.close()
                st.success("Health case saved.")
                st.rerun()

        show_table(records("SELECT * FROM health_cases ORDER BY id DESC"))
        delete_section("health_cases", "Delete Health Case", "Health Case")

    elif st.session_state.page == "vaccines":
        st.subheader(L("vaccines"))

        with st.form("vaccine"):
            a, b, c = st.columns(3)
            herd_id = a.number_input("Herd ID", min_value=1, value=1)
            vaccine = b.text_input("Vaccine", value="FMD")
            due = c.date_input("Next Due Date", value=date.today())

            save = st.form_submit_button(
                "Save Vaccination",
                use_container_width=True,
            )

            if save:
                cdb = db()
                cdb.execute(
                    """
                    INSERT INTO vaccines(
                        herd_id,vaccine,next_due,created_at
                    )
                    VALUES(?,?,?,?)
                    """,
                    (int(herd_id), vaccine, str(due), now()),
                )
                cdb.commit()
                cdb.close()
                st.success("Vaccination saved.")
                st.rerun()

        show_table(records("SELECT * FROM vaccines ORDER BY next_due"))
        delete_section("vaccines", "Delete Vaccination Record", "Vaccination")

    elif st.session_state.page == "movement":
        st.subheader(L("movement"))

        with st.form("movement"):
            herd_id = st.number_input("Herd ID", min_value=1, value=1)

            a, b = st.columns(2)
            from_place = a.text_input("From")
            to_place = b.text_input("To")

            a, b = st.columns(2)
            lat = a.number_input("Latitude", value=14.4644, format="%.6f")
            lon = b.number_input("Longitude", value=75.9218, format="%.6f")

            save = st.form_submit_button(
                "Save Movement",
                use_container_width=True,
            )

            if save:
                cdb = db()
                cdb.execute(
                    """
                    INSERT INTO movements(
                        herd_id,from_place,to_place,lat,lon,created_at
                    )
                    VALUES(?,?,?,?,?,?)
                    """,
                    (
                        int(herd_id),
                        from_place,
                        to_place,
                        lat,
                        lon,
                        now(),
                    ),
                )
                cdb.commit()
                cdb.close()
                st.success("Movement saved.")
                st.rerun()

        show_table(records("SELECT * FROM movements ORDER BY id DESC"))
        delete_section("movements", "Delete Movement Record", "Movement")

    elif st.session_state.page == "pharmacy":
        st.subheader(L("pharmacy"))

        pharmacies = records(
            "SELECT * FROM pharmacies ORDER BY name"
        )

        if pharmacies:
            names = [p["name"] for p in pharmacies]
            selected_name = st.selectbox("Pharmacy", names)
            pharmacy = next(
                p for p in pharmacies if p["name"] == selected_name
            )

            card(
                pharmacy["name"],
                f"{pharmacy['district']} • Phone: {pharmacy['phone']} • UPI: {pharmacy['upi_id']}",
                "💊",
            )

            with st.form("medicine_order"):
                item = st.text_input("Medicine / Item")
                qty = st.number_input(
                    "Quantity",
                    min_value=1,
                    value=1,
                )
                price = st.number_input(
                    "Estimated Amount",
                    min_value=0.0,
                    value=0.0,
                    step=10.0,
                )
                payment = st.selectbox(
                    "Payment Method",
                    [
                        "UPI / Online Payment",
                        "Cash on Delivery",
                    ],
                )

                order = st.form_submit_button(
                    "Place Order",
                    use_container_width=True,
                )

                if order:
                    if not item.strip():
                        st.error("Please enter the medicine or item.")
                    else:
                        payment_status = (
                            "Payment Pending"
                            if payment.startswith("UPI")
                            else "Pay on Delivery"
                        )

                        cdb = db()
                        cdb.execute(
                            """
                            INSERT INTO orders(
                                pharmacy,item,qty,price,
                                payment_method,payment_status,
                                order_status,created_at
                            )
                            VALUES(?,?,?,?,?,?,?,?)
                            """,
                            (
                                selected_name,
                                item,
                                int(qty),
                                float(price),
                                payment,
                                payment_status,
                                "Placed",
                                now(),
                            ),
                        )
                        cdb.commit()
                        cdb.close()

                        st.success(
                            "Order saved. An actual online payment gateway is not connected in this local prototype."
                        )
                        st.rerun()

        st.subheader("Order History")
        show_table(records("SELECT * FROM orders ORDER BY id DESC"))
        delete_section("orders", "Delete Order", "Order")

    elif st.session_state.page == "nutrition":
        st.subheader(L("nutrition"))

        for icon, title, text in [
            ("🌾", "Balanced Feed", "Provide suitable feed according to animal type, age and production stage."),
            ("💧", "Clean Water", "Provide clean drinking water every day."),
            ("🧂", "Minerals", "Use suitable mineral supplementation when recommended."),
            ("🌿", "Roughage", "Provide suitable roughage or forage."),
            ("🥬", "Green Feed", "Provide suitable clean green fodder."),
        ]:
            card(title, text, icon)

    elif st.session_state.page == "seasonal":
        st.subheader(L("seasonal"))

        season = st.selectbox(
            "Season",
            ["Summer", "Monsoon", "Winter"],
        )

        data = {
            "Summer": [
                "Heat stress",
                "Dehydration",
                "Water hygiene",
                "Increased insect activity",
            ],
            "Monsoon": [
                "Wet housing",
                "Water contamination",
                "Parasite exposure",
                "Skin and foot problems",
            ],
            "Winter": [
                "Respiratory problems",
                "Cold stress",
                "Poor ventilation",
                "Reduced water intake",
            ],
        }

        for item in data[season]:
            card(item, "Increase regular observation and seek veterinary advice when unusual symptoms appear.", "🌦️")

    elif st.session_state.page == "awareness":
        st.subheader(L("awareness"))

        awareness = [
            ("Clean housing", "Keep animal housing and feeding areas clean.", "🧼"),
            ("Safe water", "Provide clean drinking water every day.", "💧"),
            ("Separate affected animals", "Where practical, keep visibly affected animals away from healthy animals.", "🐄"),
            ("Vaccination", "Maintain appropriate vaccination schedules with veterinary guidance.", "💉"),
            ("Daily observation", "Watch changes in appetite, movement, breathing and behaviour.", "👀"),
        ]

        for title, text, icon in awareness:
            card(title, text, icon)

    elif st.session_state.page == "updates":
        st.subheader(L("updates"))

        for item in records(
            "SELECT * FROM updates ORDER BY id DESC"
        ):
            card(
                item["title"],
                item["message"],
                "🔔",
            )


# ============================================================
# VETERINARY SIDE
# ============================================================
else:

    features = [
        ("📊", L("monitor"), "monitor"),
        ("🩺", L("cases"), "cases"),
        ("💉", L("vaccines"), "vet_vaccines"),
        ("📍", L("movement"), "vet_movement"),
        ("📚", L("knowledge"), "knowledge"),
        ("🌦️", L("seasonal"), "vet_seasonal"),
        ("📢", L("awareness"), "vet_awareness"),
    ]

    cols = st.columns(3, gap="medium")

    for i, (icon, label, page) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                '<div class="feature-holder">',
                unsafe_allow_html=True,
            )
            clicked = st.button(
                f"{icon}\n\n{label}",
                key=f"vet_feature_{page}",
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
            if clicked:
                go(page)

    st.write("")

    if st.session_state.page == "vet_home":
        st.subheader("Recent Health Cases")
        show_table(
            records(
                """
                SELECT *
                FROM health_cases
                ORDER BY id DESC
                LIMIT 15
                """
            )
        )

    elif st.session_state.page == "monitor":
        st.subheader(L("monitor"))

        card(
            "Health Activity",
            "Health cases recorded in PashuRakshak are available here for monitoring and follow-up.",
            "🟢",
        )

        # Surface emergency notes entered by farmers/field staff for the veterinary team.
        recent_cases = records("SELECT * FROM health_cases ORDER BY id DESC LIMIT 50")
        emergency_case_terms = [
            "difficulty breathing", "bleeding", "sudden death", "fits",
            "seizure", "collapse", "unconscious", "cannot breathe",
            "heavy bleeding",
        ]
        emergency_cases = []
        for case in recent_cases:
            notes_text = str(case.get("notes", "")).lower()
            if any(term in notes_text for term in emergency_case_terms):
                emergency_cases.append(case)

        if emergency_cases:
            emergency_alert(
                "Emergency cases need attention",
                f"{len(emergency_cases)} recent health case(s) contain serious warning signs in their notes. Review the cases below and arrange prompt veterinary follow-up.",
            )
            show_table(emergency_cases)
        else:
            st.success("No emergency warning signs were flagged in the recent case notes.")

        st.subheader("Health Cases")
        show_table(recent_cases)

        st.subheader("Registered Herds")
        show_table(records("SELECT * FROM herds ORDER BY id DESC"))

        st.subheader("Animal Movement")
        show_table(records("SELECT * FROM movements ORDER BY id DESC"))

    elif st.session_state.page == "cases":
        st.subheader(L("cases"))
        show_table(records("SELECT * FROM health_cases ORDER BY id DESC"))
        delete_section("health_cases", "Delete Health Case", "Health Case")

    elif st.session_state.page == "vet_vaccines":
        st.subheader(L("vaccines"))
        show_table(records("SELECT * FROM vaccines ORDER BY next_due"))
        delete_section("vaccines", "Delete Vaccination Record", "Vaccination")

    elif st.session_state.page == "vet_movement":
        st.subheader(L("movement"))
        show_table(records("SELECT * FROM movements ORDER BY id DESC"))
        delete_section("movements", "Delete Movement Record", "Movement")

    elif st.session_state.page == "knowledge":
        st.subheader(L("knowledge"))

        disease_info = [
            ("FMD", "Monitor fever, mouth lesions, excessive salivation and lameness."),
            ("Lumpy Skin Disease", "Monitor fever and characteristic skin nodules or lesions."),
            ("PPR", "Monitor fever, nasal or mouth discharge, digestive signs and respiratory signs."),
            ("Heat Stress", "Watch for panting, weakness and other signs associated with excessive heat."),
        ]

        for title, text in disease_info:
            with st.expander(f"🩺 {title}"):
                card(title, text, "🩺")

    elif st.session_state.page == "vet_seasonal":
        st.subheader(L("seasonal"))

        season = st.selectbox(
            "Season",
            ["Summer", "Monsoon", "Winter"],
            key="vet_season",
        )

        data = {
            "Summer": [
                "Heat stress",
                "Dehydration",
                "Increased insect activity",
                "Water management",
            ],
            "Monsoon": [
                "Wet housing",
                "Water contamination",
                "Parasite exposure",
                "Skin and foot problems",
            ],
            "Winter": [
                "Respiratory problems",
                "Cold stress",
                "Ventilation",
                "Water intake",
            ],
        }

        for item in data[season]:
            card(
                item,
                "Increase regular observation and follow local veterinary guidance.",
                "🌦️",
            )

    elif st.session_state.page == "vet_awareness":
        st.subheader(L("awareness"))

        awareness = [
            ("Clean housing", "Maintain clean feeding, drinking and housing areas.", "🧼"),
            ("Clean water", "Ensure animals have access to clean drinking water.", "💧"),
            ("Movement control", "Avoid unnecessary movement of affected animals.", "🚧"),
            ("Vaccination", "Follow appropriate vaccination schedules with veterinary guidance.", "💉"),
            ("Regular observation", "Monitor changes in feeding, movement, breathing and behaviour.", "👀"),
        ]

        for title, text, icon in awareness:
            card(title, text, icon)
