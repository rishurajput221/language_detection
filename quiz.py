import time
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# ======== Config ========
LOGIN_URL = "https://www.idfcfirstacademy.com/"
COURSE_URL = "https://www.idfcfirstacademy.com/hindi/courses"
PHONE = "9267907384"
URL_FILE = "url1.txt"
OUTPUT_DIR = 'quiz_language_validation'
CHROME_DRIVER_PATH = 'C:\\Users\\DELL\\Downloads\\idfc\\chromedriver-win64\\chromedriver.exe'

# ======== Setup Output Folder ========
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ======== COUNTRY CODES ========
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
    '+972', '+973', '+974', '+975', '+976', '+977', '+992', '+993', '+994', '+995', '+996', '+998'
]

# ======== LANGUAGE CONFIGURATION (HINDI) ========
CURRENT_LANGUAGE = "HINDI"
UNICODE_RANGE_START = '\u0900'
UNICODE_RANGE_END = '\u097F'

LANGUAGE_SPECIFIC_EXCLUDED_WORDS = {
    'NRIs','english','मराठी','3.79*','दिल्ली-NCR','मुंबई-NCR','1.50*','1.56*','3.20*','1.23*','64.5*','Acres','1.14*','81*','1.48*','1.5*','9001:2000','IT/ITES','50वां','Cr','100वां','2nd','700-सीटर','1500+','2000+','20+','CREDAI','ICI','ICS','1,500','d','FKCCIs','CRISIL','CNBC','1k+','300+','50,000','100,000','2,520','40+','IT/','COVID','20,000+','52,000','(REITs)','REITs','(Proptech)','₹2000','2k+','90,000','1,00,00,000','EMI/','10,000','12,000','3,000','9,000','Pmsr','Pkw','Pwt','14,000','6,000','13,000','Rs.250','$2','1,000','4Ps','5,000','2,500','2,800','CNBC-TV18','1,367.40','1,350','1,350.5','1,052.50','COVID-19','FnB','दिल्ली-110001','मुंबई-400001','(IFA.help@idfcfirstbank.com)','RR','Rishabh','Rajput'
}

COMMON_EXCLUDED_WORDS = {
    'www.prestigeconstructions.com', 'properties@prestigeconstructions.com',
    'name*', 'mobile*', 'email*', 'your', 'ok', 'english',
    'board', 'meeting', 'notice', '2016', '2017', '2018', '2019', '2020', 
    '2021', '2022', '2023', '2024', '2025','www', 'http', 'https', 'com', 'org', 'in', 'net', 'co',
    'email', 'mobile', 'phone', 'contact', 'address', 'name','FAQs','Date','Schedule','Time','Number','First','Last'
}

EXCLUDED_WORDS = LANGUAGE_SPECIFIC_EXCLUDED_WORDS.union(COMMON_EXCLUDED_WORDS)
EXCLUDED_WORDS_LOWER = {word.lower() for word in EXCLUDED_WORDS}

# ======== VALIDATION FUNCTIONS ========

def is_numeric_with_comma_and_asterisk(word):
    clean = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    return bool(re.match(r'^\d{1,3}(,\d{3})*(\.\d+)?\*?$', clean)) or \
           bool(re.match(r'^\d+\.\d+\*$', clean)) or \
           bool(re.match(r'^\d+\*$', clean))

def is_email_address(word):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, word))

def is_decimal_or_hyphenated_number(word):
    clean = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    if re.match(r'^\d+\.\d+$', clean):
        return True
    if re.match(r'^\d+(-\d+)+$', clean):
        return True
    if re.match(r'^\d{4}-\d{2,4}$', clean):
        return True
    return False

def is_hashtag_content(word):
    return word.startswith('#') and len(word) > 1

def is_slash_separated_content(word):
    if '/' in word and not any(UNICODE_RANGE_START <= ch <= UNICODE_RANGE_END for ch in word):
        parts = word.split('/')
        return all(len(part) <= 8 and part.replace('-', '').replace('_', '').isalnum() for part in parts if part)
    return False

def is_currency_amount(word):
    currency_pattern = r'^[₹$£€¥][\d,]+(\.\d{1,2})?$|^Rs\.[\d,]+(\.\d{1,2})?$'
    return bool(re.match(currency_pattern, word))

def is_country_code(word):
    clean_word = word.strip('#.,!?()[]{}:;©"\'“”’%©')
    return clean_word in COUNTRY_CODES

def is_target_language(word):
    for ch in word:
        if UNICODE_RANGE_START <= ch <= UNICODE_RANGE_END:
            continue
        elif ch in [' ', '-', '?','!',',', '.', '(', ')', '“','/', '”','_', '"', "'","`", '’', ':', ';', '।','|','1','2','3','4','5','6','7','8','9','0','+','*','@']:
            continue
        elif ch in ['\u200C', '\u200D']:
            continue
        elif ch in ['\u00A0', '\u2009', '\u2010', '\u2011', '\u2013', '\u2014', '\u2015', '\u2018', '\u2019', '\u201C', '\u201D']:
            continue
        else:
            return False
    return True

def is_excluded_word(word):
    if word.lower() in EXCLUDED_WORDS_LOWER:
        return True
    clean_word = word.strip('#.,!?()[]{}:;©"\'“”’%©').lower()
    if clean_word in EXCLUDED_WORDS_LOWER:
        return True
    return False

def should_exclude_word(word):
    if not word or word.isdigit() or re.fullmatch(r'\W+', word):
        return True
    if is_numeric_with_comma_and_asterisk(word):
        return True
    if is_country_code(word):
        return True
    if is_excluded_word(word):
        return True
    if is_email_address(word):
        return True
    if is_decimal_or_hyphenated_number(word):
        return True
    if is_hashtag_content(word):
        return True
    if is_slash_separated_content(word):
        return True
    if is_currency_amount(word):
        return True
    return False

def extract_and_validate_content(driver):
    """Extract text and find non-target language words"""
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    page_title = ""
    title_tag = soup.find('title')
    if title_tag:
        page_title = title_tag.get_text().strip()
    
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
        
        if not is_target_language(word):
            non_target_language_words.append(word)
    
    return text, non_target_language_words

def validate_page_content(driver, quiz_idx, validation_count, accumulated_words, accumulated_text):
    """Validate current page content and accumulate results"""
    try:
        current_url = driver.current_url
        text, non_target_words = extract_and_validate_content(driver)
        
        # Accumulate unique non-target words
        accumulated_words.update(non_target_words)
        
        # Accumulate text content
        accumulated_text.append(f"\n{'='*80}\nVALIDATION #{validation_count} - URL: {current_url}\n{'='*80}\n{text}")
        
        print(f"    Validation #{validation_count}: Found {len(non_target_words)} non-{CURRENT_LANGUAGE} words on current page")
        
        return len(non_target_words)
        
    except Exception as e:
        print(f"    Error in validation #{validation_count}: {e}")
        return 0

def save_quiz_results(quiz_idx, initial_url, accumulated_text, accumulated_words):
    """Save accumulated validation results to file"""
    if accumulated_words:
        filename = f'Fail-quiz{quiz_idx}.txt'
        status = "FAIL"
    else:
        filename = f'Pass-quiz{quiz_idx}.txt'
        status = "PASS"
    
    file_path = os.path.join(OUTPUT_DIR, filename)
    with open(file_path, 'w', encoding='utf-8') as f_out:
        f_out.write(f"STATUS: {status}\n")
        f_out.write(f"INITIAL URL: {initial_url}\n")
        f_out.write(f"LANGUAGE: {CURRENT_LANGUAGE}\n")
        f_out.write(f"TOTAL VALIDATIONS PERFORMED: {len(accumulated_text)}\n")
        f_out.write("=" * 80 + "\n\n")
        
        # Write all accumulated text from all validations
        for text_block in accumulated_text:
            f_out.write(text_block + "\n\n")
        
        f_out.write("\n\n" + "=" * 80)
        if accumulated_words:
            f_out.write(f"\nALL NON-{CURRENT_LANGUAGE} WORDS DETECTED ACROSS ENTIRE QUIZ ({len(accumulated_words)} unique words):\n")
            f_out.write("=" * 80 + "\n")
            f_out.write('\n'.join(sorted(accumulated_words)))
        else:
            f_out.write(f"\n✅ NO NON-{CURRENT_LANGUAGE} WORDS DETECTED IN ENTIRE QUIZ")
    
    return status, len(accumulated_words)

def automate_quiz_with_validation():
    """Main function combining quiz automation and dynamic language validation"""
    
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=chrome_options)
    
    pass_count = 0
    fail_count = 0
    total_non_target_words = 0
    
    try:
        # Step 1: Login
        print("=" * 80)
        print("LOGGING IN TO ACADEMY")
        print("=" * 80)
        
        driver.get(LOGIN_URL)
        time.sleep(5)
        
        login_button = driver.find_element(By.XPATH, "//li[normalize-space()='Login']")
        login_button.click()
        
        phone_input = driver.find_element(By.XPATH, "//input[@name='mobile_email']")
        phone_input.send_keys(PHONE)
        
        submit_button = driver.find_element(By.XPATH, "//*[@id='root']/div/div/div/form/button")
        submit_button.click()
        
        print("Waiting for OTP entry (70 seconds)...")
        time.sleep(70)
        
        # Step 2: Navigate to courses
        driver.get(COURSE_URL)
        time.sleep(3)
        
        # Step 3: Read quiz URLs
        with open(URL_FILE, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        
        print("\n" + "=" * 80)
        print(f"PROCESSING {len(urls)} QUIZ URLs WITH DYNAMIC VALIDATION")
        print("=" * 80)
        
        # Step 4: Process each quiz with continuous validation
        for idx, url in enumerate(urls, start=1):
            print(f"\n{'='*80}")
            print(f"Quiz {idx}/{len(urls)}: {url}")
            print('='*80)
            
            accumulated_words = set()
            accumulated_text = []
            validation_count = 0
            
            try:
                # Navigate to quiz
                driver.get(url)
                time.sleep(3)
                
                # Validation #1: Initial page
                print("  Validating initial quiz page...")
                validation_count += 1
                validate_page_content(driver, idx, validation_count, accumulated_words, accumulated_text)
                
                # Start quiz
                quiz_button = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "button.quiz-btn.Inter-600"))
                )
                quiz_button.click()
                time.sleep(3)
                
                # Validation #2: After starting quiz
                validation_count += 1
                print("  Validating after quiz start...")
                validate_page_content(driver, idx, validation_count, accumulated_words, accumulated_text)
                
                question_number = 1
                quiz_active = True
                
                while quiz_active:
                    time.sleep(2)
                    
                    print(f"  Question {question_number}: Selecting Option 1")
                    
                    # Validation: Current question page
                    validation_count += 1
                    print(f"  Validating question {question_number} page...")
                    validate_page_content(driver, idx, validation_count, accumulated_words, accumulated_text)
                    
                    # Find all options
                    options = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='react-fa-options-div ']"))
                    )
                    
                    # Always select FIRST option
                    options[0].click()
                    time.sleep(1)
                    
                    # Click Next
                    next_button = driver.find_element(By.XPATH, "//button[@class='react-fa-next-btn active']")
                    next_button.click()
                    time.sleep(2)
                    
                    # Validation: After selecting answer
                    validation_count += 1
                    print(f"  Validating after answer selection...")
                    validate_page_content(driver, idx, validation_count, accumulated_words, accumulated_text)
                    
                    # Click Continue
                    continue_button = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "//button[@class='react-fa-next-btn  active']"))
                    )
                    continue_button.click()
                    time.sleep(3)
                    
                    # Check for Submit button (quiz end)
                    submit_buttons = driver.find_elements(By.CSS_SELECTOR, ".react-fa-btn.take-quizzes-again-btn")
                    
                    if submit_buttons:
                        # Validation: Final results page
                        validation_count += 1
                        print(f"  Validating final results page...")
                        validate_page_content(driver, idx, validation_count, accumulated_words, accumulated_text)
                        
                        submit_buttons[0].click()
                        print(f"  Quiz completed! Total validations: {validation_count}")
                        quiz_active = False
                    else:
                        # Continue to next question
                        try:
                            next_btn = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, "button:nth-child(1)"))
                            )
                            time.sleep(2)
                            next_btn.click()
                            question_number += 1
                        except:
                            quiz_active = False
                
                # Save accumulated results
                status, word_count = save_quiz_results(idx, url, accumulated_text, accumulated_words)
                
                print(f"  Final Status: {status} - {word_count} unique non-{CURRENT_LANGUAGE} words across all pages")
                
                if status == "PASS":
                    pass_count += 1
                else:
                    fail_count += 1
                    total_non_target_words += word_count
                
            except Exception as e:
                print(f"  Error processing quiz: {e}")
                # Save whatever we collected
                if accumulated_text or accumulated_words:
                    save_quiz_results(idx, url, accumulated_text, accumulated_words)
                fail_count += 1
        
        # Final Summary
        print("\n" + "=" * 80)
        print("FINAL SUMMARY")
        print("=" * 80)
        print(f"Total Quizzes: {len(urls)}")
        print(f"PASS (Pure {CURRENT_LANGUAGE}): {pass_count}")
        print(f"FAIL (Contains non-{CURRENT_LANGUAGE}): {fail_count}")
        print(f"Total unique non-{CURRENT_LANGUAGE} words: {total_non_target_words}")
        print("=" * 80)
        
    except Exception as e:
        print(f"Critical error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    automate_quiz_with_validation()