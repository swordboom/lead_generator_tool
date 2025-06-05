import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# -----------------------------
# CONFIGURATION
# -----------------------------
HUNTER_API_KEY = 'fb0bde6824555a52d38be1f38e274577a6a6a425'

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------
def validate_email(email):
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data'].get('result', 'unknown')
    return 'error'

def get_tech_stack(domain):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(f"https://{domain}")
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tech_stack = set()

        meta_generator = soup.find('meta', attrs={'name': 'generator'})
        if meta_generator:
            tech_stack.add(meta_generator.get('content'))

        for script in soup.find_all('script', src=True):
            src = script['src'].lower()
            if 'cloudflare' in src:
                tech_stack.add('Cloudflare')
            if 'bootstrap' in src:
                tech_stack.add('Bootstrap')
            if 'react' in src:
                tech_stack.add('React')
            if 'vue' in src:
                tech_stack.add('Vue.js')
            if 'angular' in src:
                tech_stack.add('Angular')
            if 'jquery' in src:
                tech_stack.add('jQuery')
            if 'next' in src:
                tech_stack.add('Next.js')
            if 'tailwind' in src:
                tech_stack.add('Tailwind CSS')

        for link in soup.find_all('link', href=True):
            href = link['href'].lower()
            if 'bootstrap' in href:
                tech_stack.add('Bootstrap')
            if 'font-awesome' in href or 'fontawesome' in href:
                tech_stack.add('Font Awesome')

        driver.quit()
        return ', '.join(sorted(tech_stack)) if tech_stack else 'Unknown'

    except Exception as e:
        driver.quit()
        print(f"❌ Error scraping tech stack for {domain}: {e}")
        return 'Error'

def score_linkedin_activity(linkedin_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(linkedin_url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        followers = soup.find(text=lambda x: 'followers' in x.lower())
        if followers:
            number = ''.join([c for c in followers if c.isdigit()])
            return int(number)
        return 0
    except:
        return 0

# -----------------------------
# MAIN PIPELINE
# -----------------------------
def enrich_leads(rows):
    enriched_rows = []

    for row in rows:
        domain = row.get('Domain', '')
        try:
            response = requests.get(
                "https://api.hunter.io/v2/domain-search",
                params={"domain": domain, "api_key": HUNTER_API_KEY}
            )
            response.raise_for_status()
            data = response.json()

            emails = data.get('data', {}).get('emails', [])
            first_email = emails[0]['value'] if emails else 'N/A'
            email_validation = validate_email(first_email) if first_email != 'N/A' else 'N/A'
            tech_stack = get_tech_stack(domain)

            row['Email Valid'] = email_validation
            row['Tech Stack'] = tech_stack
            if 'LinkedIn URL' in row and row['LinkedIn URL']:
                linkedin_url = row['LinkedIn URL']
                engagement_score = score_linkedin_activity(linkedin_url)
                row['Engagement Score'] = engagement_score
            else:
                row['Engagement Score'] = len(emails) * 10

        except Exception as e:
            row['Email Valid'] = 'error'
            row['Tech Stack'] = 'N/A'
            row['Engagement Score'] = 0
            print(f"❌ Failed for domain {domain}: {str(e)}")

        enriched_rows.append(row)
        time.sleep(1)  # optional throttle

    return enriched_rows
# -----------------------------