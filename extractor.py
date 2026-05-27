import re
from urllib.parse import urlparse

def extract_features(url):
    features = {}
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc.lower()
        path = parsed_url.path.lower()
    except:
        hostname = ""
        path = ""

    # 1. Base Lexical Features
    features['url_length'] = len(url)
    features['dot_count'] = hostname.count('.')
    features['has_at_symbol'] = 1 if '@' in url else 0
    features['hyphen_count'] = url.count('-')
    
    ip_pattern = r'^(?:\d{1,3}\.){3}\d{1,3}$'
    features['is_ip_address'] = 1 if re.match(ip_pattern, hostname) else 0
    features['digit_count'] = sum(c.isdigit() for c in url)
    
    # 2. Suspicious Keywords Tracker
    suspicious_keywords = [
        'login', 'verify', 'update', 'secure', 'account', 'banking', 
        'signin', 'paypal', 'amazon', 'apple', 'microsoft', 'netflix'
    ]
    features['suspicious_word_count'] = sum(1 for word in suspicious_keywords if word in url.lower())
    
    # 3. Structural Dimensions
    features['double_slash_path'] = 1 if '//' in path else 0
    features['hostname_length'] = len(hostname)
    features['path_length'] = len(path)
    
    # 4. URL Shortener Tracker
    shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd', 'buff.ly']
    features['is_shortened'] = 1 if any(s in hostname for s in shorteners) else 0

    # 5. Brand Impersonation (Combosquatting) Detection
    brands = {'paypal': 'paypal.com', 'google': 'google.com', 'apple': 'apple.com', 
              'microsoft': 'microsoft.com', 'netflix': 'netflix.com', 'amazon': 'amazon.com'}
    
    brand_spoof = 0
    for brand, official_domain in brands.items():
        if brand in url.lower():
            if not hostname.endswith(official_domain):
                brand_spoof = 1
                break
                
    features['brand_impersonation'] = brand_spoof

    return features