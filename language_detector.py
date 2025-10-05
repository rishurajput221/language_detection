import time
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# ======== Config ========
URL_FILE = 'C:\\Users\\DELL\\Downloads\\idfc\\urls.txt'
OUTPUT_DIR = 'C:\\Users\\DELL\\Downloads\\idfc\\scrapped_data'
CHROME_DRIVER_PATH = 'C:\\Users\\DELL\\Downloads\\idfc\\chromedriver-win64\\chromedriver.exe'

# ======== Setup Output Folder ========
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ======== Selenium Setup ========
chrome_options = Options()
chrome_options.add_argument("--headfull")
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=chrome_options)

# ======== COUNTRY CODES (COMMON FOR ALL LANGUAGES) ========
COUNTRY_CODES = [
    '+1', '+7', '+20', '+27', '+30', '+31', '+32', '+33', '+34', '+36', '+39', '+40', '+41', '+43', '+44', '+45', '+46', '+47', '+48', '+49',
    '+51', '+52', '+53', '+54', '+55', '+56', '+57', '+58', '+60', '+61', '+62', '+63', '+64', '+65', '+66', '+81', '+82', '+84', '+86', '+90',
    '+91', '+92', '+93', '+94', '+95', '+98', '+212', '+213', '+216', '+218', '+220', '+221', '+222', '+223', '+224', '+225', '+226', '+227',
    '+228', '+229', '+230', '+231', '+232', '+233', '+234', '+235', '+236', '+237', '+238', '+239', '+240', '+241', '+242', '+243', '+244',
    '+245', '+246', '+247', '+248', '+249', '+250', '+251', '+252', '+253', '+254', '+255', '+256', '+257', '+258', '+260', '+261', '+262',
    '+263', '+264', '+265', '+266', '+267', '+268', '+269', '+290', '+291', '+297', '+298', '+299', '+350', '+351', '+352', '+353', '+354',
    '+355', '+356', '+357', '+358', '+359', '+370', '+371', '+372', '+373', '+374', '+375', '+376', '+377', '+378', '+380', '+381', '+382',
    '+383', '+385', '+386', '+387', '+389', '+420', '+421', '+423', '+500', '+501', '+502', '+503', '+504', '+505', '+506', '+507', '+508',
    '+509', '+590', '+591', '+592', '+593', '+594', '+595', '+596', '+597', '+598', '+599', '+670', '+672', '+673', '+674', '+675', '+676',
    '+677', '+678', '+679', '+680', '+681', '+682', '+683', '+684', '+685', '+686', '+687', '+688', '+689', '+690', '+691', '+692', '+850',
    '+852', '+853', '+855', '+856', '+880', '+886', '+960', '+961', '+962', '+963', '+964', '+965', '+966', '+967', '+968', '+970', '+971',
    '+972', '+973', '+974', '+975', '+976', '+977', '+992', '+993', '+994', '+995', '+996', '+998','+11', '+35818', '+1684', '+1340', '+1264', '+1268', '+1242', '+1246', '+1441', '+5993', '+1284', '+1345', '+6189164', '+6189162', 
    '+5999', '+1767', '+1809', '+1473', '+1671', '+441481', '+441624', '+1876', '+441534', '+262269', '+1664', '+1721', '+6723', '+1670', '+1787', '+211', '+1869', '+1758', '+1784', '+4779', '+1868', '+1649', '+3906698', '+390669'
]

# ================================================================
# LANGUAGE-SPECIFIC CONFIGURATION
# UNCOMMENT THE SECTION FOR YOUR TARGET LANGUAGE
# ================================================================

# # ======== FOR KANNADA - UNCOMMENT THESE LINES ========
CURRENT_LANGUAGE = "KANNADA"
UNICODE_RANGE_START = '\u0C80'
UNICODE_RANGE_END = '\u0CFF'
LANGUAGE_SPECIFIC_EXCLUDED_WORDS = {
    'NRIs','ವಿಧ*','हिंदी','मराठी','â€¦','3.79*','ಬೆಂಗಳೂರು-NCR','1.50*','1.56*','3.20*','1.23*','64.5*','Acres','1.14*','81*','1.48*','1.5*','9001:2000','ರ—ಒಂದು','IT/ITES','50ನೇ','Cr','100ನೇ','2nd','700-ಸೀಟರ್','1500+','2000+','20+','CREDAI','ICI','ICS','1,500','d','FKCCIs','CRISIL','CNBC','1k+','300+','50,000','100,000','2,520','40+','IT/','COVID','20,000+','52,000','(REITs)','REITs','(Proptech)','₹2000','2k+','90,000','1,00,00,000','EMI/','10,000','12,000','3,000','9,000','Pmsr','Pkw','Pwt','14,000','6,000','13,000','Rs.250','$2','1,000','4Ps','5,000','2,500','2,800','CNBC-TV18','1,367.40','1,350','1,350.5','1,052.50','COVID-19','FnB','Informistmedia.com','62,000','10,382','₹10,382','10,382.2','30,121','YoY','Housing.com','Y-o-Y','FY22-23','₹4,268','FY23-24','7,500','ET-ಆತಿಥ್ಯ','Q2FY2022','NCDs','FY2021-22:','FY2021-22','2,400.30','mn','sq','ft','Sq.','Ft.','FY2022-23','#Q2WithAwaaz','Pc','1,100-1,200','₹23,511','pc','35,110','26,029','#Bengaluru','buy#39;,','#Q3WithBQ','24th','FY2022-23:','Ecc','10*','(PIOs)','PIOs','NRE/NRO/FCNR','FAQs','rbi.org','NRI/PIO','NRIs/NROs','NRIs/PIOs','(FRO)/','NRIs/PROs','22,2024','investors@prestigeconstructions.com','rnt.helpdesk@linkintime.co.in','6th','umesh.salvi@ctltrustee.com','https://prestigecorporatesite.s3.ap-south-1.amazonaws.com/investors/disclosure-under-regulation-30/2024-2025-regulations.zip','ಪ್ರಕಟೀಕರಣ-2022/23','60(2)','PEPL-ಸುರಕ್ಷತೆ','FY22-23','Ft.3,540','3,508','ಬೆಂಗಳೂರು-560025','(IFA.help@idfcfirstbank.com)'
}

# ======== FOR HINDI - UNCOMMENT THESE LINES ========
# CURRENT_LANGUAGE = "HINDI"
# UNICODE_RANGE_START = '\u0900'
# UNICODE_RANGE_END = '\u097F'
# LANGUAGE_SPECIFIC_EXCLUDED_WORDS = {
#     'NRIs','ವಿಧ*','english','मराठी','â€¦','3.79*','दिल्ली-NCR','मुंबई-NCR','1.50*','1.56*','3.20*','1.23*','64.5*','Acres','1.14*','81*','1.48*','1.5*','9001:2000','IT/ITES','50वां','Cr','100वां','2nd','700-सीटर','1500+','2000+','20+','CREDAI','ICI','ICS','1,500','d','FKCCIs','CRISIL','CNBC','1k+','300+','50,000','100,000','2,520','40+','IT/','COVID','20,000+','52,000','(REITs)','REITs','(Proptech)','₹2000','2k+','90,000','1,00,00,000','EMI/','10,000','12,000','3,000','9,000','Pmsr','Pkw','Pwt','14,000','6,000','13,000','Rs.250','$2','1,000','4Ps','5,000','2,500','2,800','CNBC-TV18','1,367.40','1,350','1,350.5','1,052.50','COVID-19','FnB','दिल्ली-110001','मुंबई-400001','ಕನ್ನಡ','(IFA.help@idfcfirstbank.com)'
# }

# ======== FOR TELUGU - UNCOMMENT THESE LINES ========
# CURRENT_LANGUAGE = "TELUGU"
# UNICODE_RANGE_START = '\u0C00'
# UNICODE_RANGE_END = '\u0C7F'
# LANGUAGE_SPECIFIC_EXCLUDED_WORDS = {
#     'NRIs','ವಿಧ*','हिंदी','english','â€¦','3.79*','హైదరాబాద్-NCR','విజయవాడ-NCR','1.50*','1.56*','3.20*','1.23*','64.5*','Acres','1.14*','81*','1.48*','1.5*','9001:2000','IT/ITES','50వ','Cr','100వ','2nd','700-సీటర్','1500+','2000+','20+','CREDAI','ICI','ICS','1,500','d','FKCCIs','CRISIL','CNBC','1k+','300+','50,000','100,000','2,520','40+','IT/','COVID','20,000+','52,000','(REITs)','REITs','(Proptech)','₹2000','2k+','90,000','1,00,00,000','EMI/','10,000','12,000','3,000','9,000','Pmsr','Pkw','Pwt','14,000','6,000','13,000','Rs.250','$2','1,000','4Ps','5,000','2,500','2,800','CNBC-TV18','1,367.40','1,350','1,350.5','1,052.50','COVID-19','FnB','హైదరాబాద్-500001','(IFA.help@idfcfirstbank.com)'
# }

# ======== FOR TAMIL - UNCOMMENT THESE LINES ========
# CURRENT_LANGUAGE = "TAMIL"
# UNICODE_RANGE_START = '\u0B80'
# UNICODE_RANGE_END = '\u0BFF'
# LANGUAGE_SPECIFIC_EXCLUDED_WORDS = {
#     'NRIs','ವಿಧ*','हिंदी','english','â€¦','3.79*','சென்னை-NCR','கோவை-NCR','1.50*','1.56*','3.20*','1.23*','64.5*','Acres','1.14*','81*','1.48*','1.5*','9001:2000','IT/ITES','50வது','Cr','100வது','2nd','700-இருக்கை','1500+','2000+','20+','CREDAI','ICI','ICS','1,500','d','FKCCIs','CRISIL','CNBC','1k+','300+','50,000','100,000','2,520','40+','IT/','COVID','20,000+','52,000','(REITs)','REITs','(Proptech)','₹2000','2k+','90,000','1,00,00,000','EMI/','10,000','12,000','3,000','9,000','Pmsr','Pkw','Pwt','14,000','6,000','13,000','Rs.250','$2','1,000','4Ps','5,000','2,500','2,800','CNBC-TV18','1,367.40','1,350','1,350.5','1,052.50','COVID-19','FnB','சென்னை-600001','காப்புரிமை©','(IFA.help@idfcfirstbank.com)'
# }

# ======== FOR GUJARATI - UNCOMMENT THESE LINES ========
# CURRENT_LANGUAGE = "GUJARATI"
# UNICODE_RANGE_START = '\u0A80'
# UNICODE_RANGE_END = '\u0AFF'
# LANGUAGE_SPECIFIC_EXCLUDED_WORDS = {
#     'NRIs','ವಿಧ*','हिंदी','english','â€¦','3.79*','અમદાવાદ-NCR','સુરત-NCR','1.50*','1.56*','3.20*','1.23*','64.5*','Acres','1.14*','81*','1.48*','1.5*','9001:2000','IT/ITES','50મું','Cr','100મું','2nd','700-સીટ','1500+','2000+','20+','CREDAI','ICI','ICS','1,500','d','FKCCIs','CRISIL','CNBC','1k+','300+','50,000','100,000','2,520','40+','IT/','COVID','20,000+','52,000','(REITs)','REITs','(Proptech)','₹2000','2k+','90,000','1,00,00,000','EMI/','10,000','12,000','3,000','9,000','Pmsr','Pkw','Pwt','14,000','6,000','13,000','Rs.250','$2','1,000','4Ps','5,000','2,500','2,800','CNBC-TV18','1,367.40','1,350','1,350.5','1,052.50','COVID-19','FnB','અમદાવાદ-380001'
# }

# ======== FOR MARATHI - UNCOMMENT THESE LINES ========
# CURRENT_LANGUAGE = "MARATHI"
# UNICODE_RANGE_START = '\u0900'
# UNICODE_RANGE_END = '\u097F'
# LANGUAGE_SPECIFIC_EXCLUDED_WORDS = {
#     'NRIs','ವಿಧ*','हिंदी','english','â€¦','3.79*','मुंबई-NCR','पुणे-NCR','1.50*','1.56*','3.20*','1.23*','64.5*','Acres','1.14*','81*','1.48*','1.5*','9001:2000','IT/ITES','50वे','Cr','100वे','2nd','700-आसन','1500+','2000+','20+','CREDAI','ICI','ICS','1,500','d','FKCCIs','CRISIL','CNBC','1k+','300+','50,000','100,000','2,520','40+','IT/','COVID','20,000+','52,000','(REITs)','REITs','(Proptech)','₹2000','2k+','90,000','1,00,00,000','EMI/','10,000','12,000','3,000','9,000','Pmsr','Pkw','Pwt','14,000','6,000','13,000','Rs.250','$2','1,000','4Ps','5,000','2,500','2,800','CNBC-TV18','1,367.40','1,350','1,350.5','1,052.50','COVID-19','FnB','मुंबई-400001'
# }

# ======== FOR MALAYALAM - UNCOMMENT THESE LINES ========
# CURRENT_LANGUAGE = "MALAYALAM"
# UNICODE_RANGE_START = '\u0D00'
# UNICODE_RANGE_END = '\u0D7F'
# LANGUAGE_SPECIFIC_EXCLUDED_WORDS = {
#     'NRIs','Type*','Online','Portals','© 2025','©2025','ವಿಧ*','हिंदी','english','â€¦','3.79*','കൊച്ചി-NCR','തിരുവനന്തപുരം-NCR','1.50*','1.56*','3.20*','1.23*','64.5*','Acres','1.14*','81*','1.48*','1.5*','9001:2000','IT/ITES','50ാം','Cr','100ാം','2nd','700-സീറ്റ്','1500+','2000+','20+','CREDAI','ICI','ICS','1,500','d','FKCCIs','CRISIL','CNBC','1k+','300+','50,000','100,000','2,520','40+','IT/','COVID','20,000+','52,000','(REITs)','REITs','(Proptech)','₹2000','2k+','90,000','1,00,00,000','EMI/','10,000','12,000','3,000','9,000','Pmsr','Pkw','Pwt','14,000','6,000','13,000','Rs.250','$2','1,000','4Ps','5,000','2,500','2,800','CNBC-TV18','1,367.40','1,350','1,350.5','1,052.50','COVID-19','FnB','കൊച്ചി-682001'
# }

# ======== COMMON EXCLUDED WORDS (FOR ALL LANGUAGES) ========
COMMON_EXCLUDED_WORDS = {
    'â€"', 'â€œ', 'â€', 
    '(OBSOLETE)','appartment','Appartment',
    'www.prestigeconstructions.com', 'properties@prestigeconstructions.com',
    'name*', 'mobile*', 'email*', 'your', 'ok', 'english','ಕನ್ನಡ','मराठी',
    'board', 'meeting', 'notice', '2016', '2017', '2018', '2019', '2020', 
    '2021', '2022', '2023', '2024', '2025','www', 'http', 'https', 'com', 'org', 'in', 'net', 'co',
    'email', 'mobile', 'phone', 'contact', 'address', 'name','हिन्दी','தமிழ்','മലയാളം','తెలుగు','ગુજરાતી','FAQs','Date','Schedule','Time','Number','First','Last','Project*',"Location", "Property","Type","Source*", "Plot", "Apartment", "Villas", "Source", "Hoarding", "Radio", "Newspaper", "Magazine", "WhatsApp", "Google", "Facebook", "Instagram", "LinkedIn", "Online Portals", "External","Ahmed","nagar",'Afghanistan','Aland','Albania','Algeria','American','Minor','Outlying','Islands','Samoa','Virgin','Andorra','Angola','Anguilla','Antarctica','Antigua','and','Barbuda','Argentina','Armenia','Aruba','Australia','Austria','Azerbaijan','Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bermuda','Bhutan','Bolivia','Bonaire','Sint','Eustatius','Saba','Bosnia','Herzegovina','Botswana','Bouvet','Brazil','British','Indian','Ocean','Territory','Brunei','Darussalam','Bulgaria','Burkina','Faso','Burundi','Cambodia','Cameroon','Canada','Cape','Verde','Cayman','Central','African','Republic','Chad','Chile','China','Christmas','Island','Cocos','Keeling','Colombia','Comoros','Congo','Cook','Costa','Rica','Cote',"d'Ivoire",'country','Croatia','Cuba','Curaçao','Cyprus','Czech','Democratic','of','the','Denmark','Djibouti','Dominica','Dominican','Ecuador','Egypt','El','Salvador','Equatorial','Guinea','Eritrea','Estonia','Ethiopia','Falkland','Faroe','Fiji','Finland','France','French','Guyana','Polynesia','Southern','Territories','Gabon','Gambia','Georgia','Germany','Ghana','Gibraltar','Greece','Greenland','Grenada','Guadeloupe','Guam','Guatemala','Guernsey','Guinea-Bissau','Haiti','Heard','McDonald','Honduras','Hong','Kong','Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland','Isle','Of','Man','Israel','Italy','Jamaica','Japan','Jersey','Jordan','Kazakhstan','Kenya','Kiribati','Kuwait','Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho','Liberia','Libya','Liechtenstein','Lithuania','Luxembourg','Macau','Madagascar','Malawi','Malaysia','Maldives','Mali','Malta','Marshall','Martinique','Mauritania','Mauritius','Mayotte','Mexico','Micronesia','Moldova','Monaco','Mongolia','Montenegro','Montserrat','Morocco','Mozambique','Myanmar','Namibia','Nauru','Nepal','Netherlands','Antilles','New','Caledonia','Zealand','Nicaragua','Niger','Nigeria','Niue','Norfolk','North','Korea','Macedonia','Northern','Mariana','Norway','Oman','Pakistan','Palau','Palestine','State','Panama','Papua','Guinea','Paraguay','Peru','Philippines','Pitcairn','Poland','Portugal','Puerto','Rico','Qatar','South','Sudan','Reunion','Romania','Russian','Federation','Rwanda','Saint','Barthélemy','Kitts','Nevis','Martin','Samoa','San','Marino','Sao','Tome','Principe','Saudi','Arabia','Senegal','Serbia','Montenegro','Seychelles','Sierra','Leone','Singapore','Maarten','Slovakia','Slovenia','Solomon','Somalia','Africa','Georgia','Sandwich','Korea','Spain','Sri','Lanka','St.','Helena','Lucia','Pierre','Miquelon','Vincent','Suriname','Svalbard','Sweden','Switzerland','Syria','Taiwan','Tajikistan','Tanzania','Thailand','The','Kingdom','Eswatini','Türkiye','Timor-Leste','Togo','Tokelau','Tonga','Trinidad,Tobago','Tunisia','Turkmenistan','Turksh','Caicosin','Tuvalu','Uganda','Ukraine','United','Arab','Emirates','States','America','Uruguay','Uzbekistan','Vanuatu','Vatican','City','Venezuela','Vietnam','Wallis','Futuna','West','Sahara','Yemen','Zambia','Zimbabwe',"कॉपीराइट©",'Type*','Online','Portals'
}

# Combine language-specific and common excluded words
EXCLUDED_WORDS = LANGUAGE_SPECIFIC_EXCLUDED_WORDS.union(COMMON_EXCLUDED_WORDS)
EXCLUDED_WORDS_LOWER = {word.lower() for word in EXCLUDED_WORDS}

# ======== ADDON FUNCTIONS (COMMON FOR ALL LANGUAGES) ========

def is_numeric_with_comma_and_asterisk(word):
    """Check for numeric values with commas and asterisks (e.g., 1,234*, 5.67*, 1,000)"""
    clean = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    return bool(re.match(r'^\d{1,3}(,\d{3})*(\.\d+)?\*?$', clean)) or \
           bool(re.match(r'^\d+\.\d+\*$', clean)) or \
           bool(re.match(r'^\d+\*$', clean))

def is_email_address(word):
    """Check if word is an email address"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, word))

def is_decimal_or_hyphenated_number(word):
    """Check for decimal numbers or numbers with hyphens (e.g., 3.14, 1-2-3, 2020-21)"""
    clean = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    if re.match(r'^\d+\.\d+$', clean):
        return True
    if re.match(r'^\d+(-\d+)+$', clean):
        return True
    if re.match(r'^\d{4}-\d{2,4}$', clean):
        return True
    return False

def is_hashtag_content(word):
    """Check for hashtag content (e.g., #Bengaluru, #Q2WithAwaaz)"""
    return word.startswith('#') and len(word) > 1

def is_slash_separated_content(word):
    """Check for content with forward slashes (e.g., IT/ITES, NRE/NRO/FCNR)"""
    if '/' in word and not any(UNICODE_RANGE_START <= ch <= UNICODE_RANGE_END for ch in word):
        parts = word.split('/')
        return all(len(part) <= 8 and part.replace('-', '').replace('_', '').isalnum() for part in parts if part)
    return False

def is_complex_abbreviation(word):
    """Check for complex abbreviations with numbers and special chars (e.g., FY22-23, Q2FY2022)"""
    clean = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    if re.match(r'^FY\d{2,4}-\d{2,4}:?$', clean, re.IGNORECASE):
        return True
    if re.match(r'^Q\d+FY\d{4}$', clean, re.IGNORECASE):
        return True
    if re.match(r'^[A-Z]{1,4}\d+[A-Z]*\d*$', clean):
        return True
    return False

def is_currency_amount(word):
    """Check for currency amounts (e.g., ₹2000, $2, Rs.250)"""
    currency_pattern = r'^[₹$£€¥][\d,]+(\.\d{1,2})?$|^Rs\.[\d,]+(\.\d{1,2})?$'
    return bool(re.match(currency_pattern, word))

def is_percentage_or_multiplier(word):
    """Check for percentages or multipliers (e.g., 64.5%, 10*, 1.5x)"""
    clean = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    return bool(re.match(r'^\d+(\.\d+)?[%*x]$', clean, re.IGNORECASE))

def is_country_code(word):
    clean_word = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    return clean_word in COUNTRY_CODES

def is_technical_code(word):
    """Check for technical codes and identifiers"""
    clean = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    if re.match(r'^\d{4}:\d{4}$', clean):
        return True
    if re.match(r'^[A-Z]{2,6}\d+[A-Z]*$', clean):
        return True
    return False

# ======== LANGUAGE DETECTION FUNCTION (DYNAMIC BASED ON SELECTED LANGUAGE) ========
def is_target_language(word):
    """Check if word contains only target language characters and common punctuation"""
    for ch in word:
        if UNICODE_RANGE_START <= ch <= UNICODE_RANGE_END:
            continue
        elif ch in [' ', '-', ',', '.', '(', ')', '“', '”', '"', "'","`", '’', ':', ';', '।','|',
                    '1','2','3','4','5','6','7','8','9','0','+','*','@']:
            continue
        elif ch in ['\u200C', '\u200D']:
            continue
        elif ch in ['\u00A0', '\u2009', '\u2010', '\u2011', '\u2013', '\u2014', '\u2015', '\u2018', '\u2019', '\u201C', '\u201D']:
            continue
        else:
            return False
    return True

def is_target_language_with_special_chars(word):
    """Enhanced target language detection that allows words with #, -, /"""
    clean_word = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    
    if any(char in clean_word for char in ['#', '-', '/']):
        parts = re.split(r'[#\-/]+', clean_word)
        target_lang_parts = 0
        total_parts = 0
        
        for part in parts:
            if part.strip():
                total_parts += 1
                if is_target_language(part.strip()):
                    target_lang_parts += 1
        
        if total_parts > 0 and target_lang_parts / total_parts >= 0.5:
            return True
    
    return is_target_language(clean_word)

# ======== Legacy functions ========
def is_numeric_with_symbols(word):
    clean = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    return re.fullmatch(r'\d+([\-/.]\d+)*', clean) is not None

def is_target_language_compound(word):
    """Check compound target language words separated by / or -"""
    parts = re.split(r'[/\-]', word)
    for part in parts:
        clean_part = part.strip('#.,!?()[]{}:;©"\'“”’%©')
        if not clean_part or not is_target_language(clean_part):
            return False
    return True

def is_uppercase_acronym(word):
    clean = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    return clean.isupper() and len(clean) <= 6

def is_excluded_word(word):
    if word.lower() in EXCLUDED_WORDS_LOWER:
        return True
    
    clean_word = word.strip('#.,!?()[]{}:;©"\'“”’%©').lower()
    if clean_word in EXCLUDED_WORDS_LOWER:
        return True
    
    for excluded in EXCLUDED_WORDS:
        if '.' in excluded and excluded.lower() in word.lower():
            return True
    
    return False

# ======== ENHANCED EXCLUSION FUNCTION ========
def should_exclude_word(word):
    """Master function to check if a word should be excluded using all patterns"""
    if not word or word.isdigit() or re.fullmatch(r'\W+', word):
        return True
    
    if is_numeric_with_symbols(word):
        return True
    if is_country_code(word):
        return True
    if is_uppercase_acronym(word):
        return True
    if is_excluded_word(word):
        return True
    if is_numeric_with_comma_and_asterisk(word):
        return True
    if is_email_address(word):
        return True
    if is_decimal_or_hyphenated_number(word):
        return True
    if is_hashtag_content(word):
        return True
    if is_slash_separated_content(word):
        return True
    if is_complex_abbreviation(word):
        return True
    if is_currency_amount(word):
        return True
    if is_percentage_or_multiplier(word):
        return True
    if is_technical_code(word):
        return True
    
    return False

# ======== NEW: PAGE SCROLLING FUNCTION ========
def scroll_page_smoothly(driver, scroll_pause_time=0.5, pixels_per_scroll=1600):
    """
    Scroll through the entire page SLOWLY to trigger lazy-loaded content
    
    Args:
        driver: Selenium WebDriver instance
        scroll_pause_time: Time to pause between scrolls (default 3 seconds - INCREASED)
        pixels_per_scroll: Number of pixels to scroll each time (default 1600 - SMALLER for slower)
    
    Returns:
        bool: True if scrolling completed successfully
    """
    print("  📜 Starting SLOW page scroll to load all content...")
    time.sleep(5)
    
    try:
        # Get total page height
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        current_position = 0
        scroll_step = 0
        
        print(f"  📏 Page height: {total_height}px, Viewport: {viewport_height}px")
        print(f"  🐌 Scrolling {pixels_per_scroll}px at a time with {scroll_pause_time}s pauses")
        
        while current_position < total_height:
            scroll_step += 1
            
            # Scroll by small increment
            current_position += pixels_per_scroll
            driver.execute_script(f"window.scrollTo({{top: {current_position}, behavior: 'smooth'}});")
            
            # Wait for content to load
            time.sleep(scroll_pause_time)
            
            # Check if new content was loaded (page height increased)
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            progress_percentage = min(100, (current_position / total_height) * 100)
            print(f"    ↓ Scroll step {scroll_step}: Position {current_position}px / {new_height}px ({progress_percentage:.1f}%)")
            
            # Update total height if page grew
            if new_height > total_height:
                print(f"    🆕 Page expanded: {total_height}px → {new_height}px")
                total_height = new_height
            
            # Safety limit: max 50 scrolls (increased for slower scrolling)
            if scroll_step >= 50:
                print(f"  ⚠️ Max scroll limit reached (50 scrolls)")
                break
        
        print(f"  ✅ Reached bottom of page after {scroll_step} scroll(s)")
        
        # Scroll back to top SLOWLY
        print("  ↑ Scrolling back to top slowly...")
        current_position = driver.execute_script("return window.pageYOffset")
        
        while current_position > 0:
            current_position = max(0, current_position - pixels_per_scroll)
            driver.execute_script(f"window.scrollTo({{top: {current_position}, behavior: 'smooth'}});")
            time.sleep(0.5)  # Faster on way back up
        
        time.sleep(0.5)
        print("  ✅ Scrolled back to top")
        
        return True
        
    except Exception as e:
        print(f"  ⚠️ Error during scrolling: {e}")
        return False


def scroll_page_in_steps(driver, num_steps=10, pause_time=3):
    """
    Alternative: Scroll page in equal steps SLOWLY (more controlled)
    
    Args:
        driver: Selenium WebDriver instance
        num_steps: Number of scroll steps (default 10 - INCREASED)
        pause_time: Pause between each step (default 3 seconds - INCREASED)
    """
    print(f"  📜 Scrolling page SLOWLY in {num_steps} steps...")
    
    try:
        # Get total page height
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        
        print(f"  📏 Page height: {total_height}px, Viewport: {viewport_height}px")
        print(f"  🐌 Pausing {pause_time}s between each step")
        
        # Calculate scroll step size
        step_size = total_height / num_steps
        
        for step in range(1, num_steps + 1):
            scroll_to = int(step_size * step)
            
            # Use smooth scrolling behavior
            driver.execute_script(f"window.scrollTo({{top: {scroll_to}, behavior: 'smooth'}});")
            
            progress = (step / num_steps) * 100
            print(f"    ↓ Step {step}/{num_steps}: Scrolled to {scroll_to}px ({progress:.0f}%)")
            
            time.sleep(pause_time)
            
            # Check if page height changed (new content loaded)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height > total_height:
                print(f"    🆕 Page expanded: {total_height}px → {new_height}px")
                total_height = new_height
                # Recalculate step size
                step_size = total_height / num_steps
        
        # Scroll back to top SLOWLY
        
        return True
        
    except Exception as e:
        print(f"  ⚠️ Error during step scrolling: {e}")
        return False

# ======== NEW: TRANSLATION WAIT FUNCTIONS ========
def wait_for_translation_complete(driver, target_language_range_start, target_language_range_end, max_wait=120):
    """
    Wait for page translation to complete by checking if target language content appears
    
    Args:
        driver: Selenium WebDriver instance
        target_language_range_start: Unicode start range
        target_language_range_end: Unicode end range
        max_wait: Maximum seconds to wait (default 120)
    
    Returns:
        bool: True if translation detected, False if timeout
    """
    print(f"  ⏳ Waiting for {CURRENT_LANGUAGE} translation to complete...")
    
    start_time = time.time()
    check_interval = 5
    last_target_lang_count = 0
    stable_count = 0
    
    while (time.time() - start_time) < max_wait:
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            for script in soup(["script", "style"]):
                script.extract()
            
            text = soup.get_text(separator=' ')
            text = re.sub(r'\s+', ' ', text).strip()
            
            target_lang_char_count = 0
            total_alpha_chars = 0
            
            for char in text:
                if char.isalpha() or (target_language_range_start <= char <= target_language_range_end):
                    total_alpha_chars += 1
                    if target_language_range_start <= char <= target_language_range_end:
                        target_lang_char_count += 1
            
            if total_alpha_chars > 0:
                target_lang_percentage = (target_lang_char_count / total_alpha_chars) * 100
                
                print(f"  📊 {CURRENT_LANGUAGE} content: {target_lang_percentage:.1f}% ({target_lang_char_count}/{total_alpha_chars} chars)")
                
                if target_lang_percentage > 70:
                    if abs(target_lang_char_count - last_target_lang_count) < 50:
                        stable_count += 1
                        if stable_count >= 2:
                            elapsed = time.time() - start_time
                            print(f"  ✅ Translation complete! ({elapsed:.1f}s)")
                            return True
                    else:
                        stable_count = 0
                    
                    last_target_lang_count = target_lang_char_count
            
            time.sleep(check_interval)
            
        except Exception as e:
            print(f"  ⚠️ Error checking translation: {e}")
            time.sleep(check_interval)
    
    elapsed = time.time() - start_time
    print(f"  ⏱️ Translation wait timeout after {elapsed:.1f}s")
    return False


def wait_for_page_load_and_translation(driver, max_wait=120, enable_scroll=True, scroll_method="smooth"):
    """
    Combined function: Wait for initial page load + scrolling + translation
    
    Args:
        driver: Selenium WebDriver instance
        max_wait: Maximum seconds to wait for translation
        enable_scroll: Whether to scroll page (default True)
        scroll_method: "smooth" for dynamic scrolling or "steps" for fixed steps
    """
    try:
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("  ✅ Page DOM loaded")
    except TimeoutException:
        print("  ⚠️ Page load timeout, continuing anyway...")
    
    time.sleep(3)
    
    # NEW: Scroll the page if enabled
    if enable_scroll:
        if scroll_method == "smooth":
            scroll_page_smoothly(driver, scroll_pause_time=2)
        elif scroll_method == "steps":
            scroll_page_in_steps(driver, num_steps=5, pause_time=2)
        else:
            print(f"  ⚠️ Unknown scroll method: {scroll_method}, skipping scroll")
    
    translation_complete = wait_for_translation_complete(
        driver, 
        UNICODE_RANGE_START, 
        UNICODE_RANGE_END, 
        max_wait
    )
    
    return translation_complete

# ======== Read URLs ========
with open(URL_FILE, 'r', encoding='utf-8') as f:
    urls = [line.strip() for line in f if line.strip()]

non_target_language_urls = []
total_non_target_language_words = 0
pass_count = 0
fail_count = 0

print(f"🚀 STARTING {CURRENT_LANGUAGE} LANGUAGE PROCESSING")
print(f"📝 Unicode Range: {UNICODE_RANGE_START} - {UNICODE_RANGE_END}")
print("=" * 80)

# ======== Process Each URL ========
for idx, url in enumerate(urls, start=1):
    try:
        print(f"\n{'='*80}")
        print(f"Processing URL {idx}/{len(urls)}")
        print(f"URL: {url}")
        print('='*80)
        
        # Clear cookies before loading
        driver.delete_all_cookies()
        
        driver.get(url)
        
        # NEW: Use smart wait with scrolling instead of static sleep
        # Options: enable_scroll=True/False, scroll_method="smooth"/"steps"
        translation_success = wait_for_page_load_and_translation(
            driver, 
            max_wait=120, 
            enable_scroll=True,      # Set to False to disable scrolling
            scroll_method="smooth"   # Use "smooth" or "steps"
        )
        
        if not translation_success:
            print(f"  ⚠️ WARNING: Translation may be incomplete")
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        page_title = ""
        title_tag = soup.find('title')
        if title_tag:
            page_title = title_tag.get_text().strip()
            print(f"  📄 Page title: {page_title}")

        for script in soup(["script", "style"]):
            script.extract()

        if title_tag:
            title_tag.extract()

        text = soup.get_text(separator=' ')
        text = re.sub(r'\s+', ' ', text).strip()

        words = text.split()
        non_target_language_words = []
        
        title_words = []
        if page_title:
            title_words = [word.strip('#.,!?()[]{}:;©"\'“”’%©').lower() for word in page_title.split()]

        for word in words:
            word = word.strip()
            
            if should_exclude_word(word):
                continue
            
            clean_word_lower = word.strip('#.,!?()[]{}:;©"\'“”’%©').lower()
            if clean_word_lower in title_words:
                continue
            
            if not is_target_language_with_special_chars(word):
                non_target_language_words.append(word)

        if non_target_language_words:
            filename = f'Fail-url{idx}.txt'
            status = "FAIL ❌"
            non_target_language_urls.append((url, len(non_target_language_words)))
            total_non_target_language_words += len(non_target_language_words)
            fail_count += 1
        else:
            filename = f'Pass-url{idx}.txt'
            status = "PASS ✅"
            pass_count += 1

        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, 'w', encoding='utf-8') as f_out:
            f_out.write(f"STATUS: {status}\n")
            f_out.write(f"URL: {url}\n")
            f_out.write(f"LANGUAGE: {CURRENT_LANGUAGE}\n")
            f_out.write(f"UNICODE RANGE: {UNICODE_RANGE_START} - {UNICODE_RANGE_END}\n")
            f_out.write(f"TRANSLATION STATUS: {'Complete' if translation_success else 'Incomplete/Timeout'}\n")
            f_out.write("=" * 80 + "\n\n")
            
            sentences = re.split(r'(?<=[।.!?])\s+', text)
            for sentence in sentences:
                cleaned = sentence.strip()
                if cleaned:
                    f_out.write(cleaned + '\n')

            f_out.write("\n\n" + "=" * 80)
            if non_target_language_words:
                f_out.write(f"\nNon-{CURRENT_LANGUAGE} Words Detected ({len(non_target_language_words)} words):\n")
                f_out.write("=" * 80 + "\n")
                f_out.write('\n'.join(non_target_language_words))
            else:
                f_out.write(f"\n✅ NO NON-{CURRENT_LANGUAGE} WORDS DETECTED - PURE {CURRENT_LANGUAGE} CONTENT")
            
            if page_title:
                f_out.write(f"\n\nPage Title (excluded from analysis): {page_title}")

        print(f"  {status} - Found {len(non_target_language_words)} non-{CURRENT_LANGUAGE} words")
        print(f"  Saved as: {filename}")

    except Exception as e:
        print(f"❌ Error processing {url}: {e}")
        error_filename = f'Fail-url{idx}.txt'
        error_file_path = os.path.join(OUTPUT_DIR, error_filename)
        with open(error_file_path, 'w', encoding='utf-8') as f_out:
            f_out.write(f"STATUS: FAIL ❌ (ERROR)\n")
            f_out.write(f"URL: {url}\n")
            f_out.write(f"LANGUAGE: {CURRENT_LANGUAGE}\n")
            f_out.write("=" * 80 + "\n\n")
            f_out.write(f"ERROR OCCURRED: {str(e)}\n")
        fail_count += 1

driver.quit()

print("\n" + "=" * 80)
print(f"FINAL SUMMARY REPORT - {CURRENT_LANGUAGE}")
print("=" * 80)
print(f"Total URLs processed: {len(urls)}")
print(f"✅ PASS (Pure {CURRENT_LANGUAGE}): {pass_count}")
print(f"❌ FAIL (Contains non-{CURRENT_LANGUAGE}): {fail_count}")
print(f"Total non-{CURRENT_LANGUAGE} words found: {total_non_target_language_words}")
print(f"Unicode Range Used: {UNICODE_RANGE_START} - {UNICODE_RANGE_END}")
print("=" * 80)

print("\n📁 FILE NAMING CONVENTION:")
print(f"• Pass-url{{number}}.txt = Contains only {CURRENT_LANGUAGE} content")
print(f"• Fail-url{{number}}.txt = Contains non-{CURRENT_LANGUAGE} words")
print("=" * 80)

print("\n📊 DETAILED RESULTS:")
if pass_count > 0:
    print(f"\n✅ PASSED URLs ({pass_count}):")
    pass_urls = []
    for idx, url in enumerate(urls, start=1):
        filename = f'Pass-url{idx}.txt'
        if os.path.exists(os.path.join(OUTPUT_DIR, filename)):
            pass_urls.append(f"Pass-url{idx}.txt")
    
    for filename in pass_urls[:10]:
        print(f"  • {filename}")
    if len(pass_urls) > 10:
        print(f"  ... and {len(pass_urls) - 10} more")

if fail_count > 0:
    print(f"\n❌ FAILED URLs ({fail_count}):")
    for entry in non_target_language_urls[:10]:
        idx = urls.index(entry[0]) + 1
        print(f"  • Fail-url{idx}.txt | Non-{CURRENT_LANGUAGE} words: {entry[1]}")
    if len(non_target_language_urls) > 10:
        print(f"  ... and {len(non_target_language_urls) - 10} more")

print("\n" + "=" * 80)
print("🔍 ENHANCED FEATURES ACTIVE:")
print("✓ Smart translation detection (waits for actual translation)")
print("✓ Intelligent page scrolling (loads lazy content)")
print("✓ Dynamic wait times (5-120 seconds based on translation progress)")
print("✓ Translation stability check (ensures content stopped changing)")
print("✓ Real-time translation percentage monitoring")
print("✓ Automatic scroll to bottom and back to top")
print("✓ Numeric with commas and asterisks filtering")
print("✓ Email address detection and exclusion") 
print("✓ Decimal and hyphenated number filtering")
print("✓ Hashtag content exclusion")
print("✓ Slash-separated content filtering")
print("✓ Complex abbreviation detection")
print("✓ Currency amount filtering")
print("✓ Percentage and multiplier exclusion")
print("✓ Technical code detection")
print(f"✓ Enhanced {CURRENT_LANGUAGE} detection with special characters")
print(f"✓ {CURRENT_LANGUAGE} Unicode range support ({UNICODE_RANGE_START}–{UNICODE_RANGE_END})")
print("✓ ZWNJ/ZWJ character support for proper Indian language rendering")
print("✓ Unicode formatting character support")
print("✓ Cookie clearing before each page load")
print("=" * 80)

print("\n📌 Hindi Actiavte")
print("   Unicode Range: \\u0C00 - \\u0C7F")
print("=" * 80)