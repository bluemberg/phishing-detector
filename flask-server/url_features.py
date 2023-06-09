import re
import socket
import Levenshtein

HINTS = ['wp', 'login', 'includes', 'admin', 'content', 'site', 'images', 'js', 'alibaba', 'css', 'myaccount', 'dropbox', 'themes', 'plugins', 'signin', 'view']

allbrand_txt = open("allbrands.txt", "r")

def __txt_to_list(txt_object):
    list = []
    for line in txt_object:
        list.append(line.strip())
    txt_object.close()
    return list

allbrand = __txt_to_list(allbrand_txt)

def url_length(url): # column: length_url
    return len(url)

def having_ip_address(url): # column: ip
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)|'  # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        '[0-9a-fA-F]{7}', url)  # Ipv6
    if match:
        return 1
    else:
        return 0

def count_dots(hostname): # column: nb_dots
    return hostname.count('.')

def count_hyphens(base_url): # column: nb_hyphens
    return base_url.count('-')

def count_at(base_url): # column: nb_at
    return base_url.count('@')

def count_exclamation(base_url): # column: nb_qm
    return base_url.count('?')

def count_and(base_url): # column: nb_and
    return base_url.count('&')

def count_equal(base_url): # column: nb_eq
    return base_url.count('=')

def count_underscore(base_url): # column: nb_underscore
    return base_url.count('_')

def count_tilde(full_url): # column: nb_tilde
    if full_url.count('~')>0:
        return 1
    return 0

def count_percentage(base_url): # column: nb_percent
    return base_url.count('%')

def count_slash(full_url): # column: nb_slash
    return full_url.count('/')

def count_star(url): # column: nb_star
    return url.count('*')

def count_colon(url): # column: nb_colon
    return url.count(':')

def count_comma(base_url): # column: nb_comma
    return base_url.count(',')

def count_semicolumn(url): # column: nb_semicolumn
    return url.count(';')

def count_dollar(base_url): # column: nb_dollar
    return base_url.count('$')

def count_space(base_url): # column: nb_space
    return base_url.count(' ')+base_url.count('%20')

def check_www(words_raw): # column: nb_www
        count = 0
        for word in words_raw:
            if not word.find('www') == -1:
                count += 1
        return count

def check_com(words_raw): # column: nb_com
        count = 0
        for word in words_raw:
            if not word.find('com') == -1:
                count += 1
        return count

def count_double_slash(full_url): # column: nb_dslash
    list=[x.start(0) for x in re.finditer('//', full_url)]
    if list[len(list)-1]>6:
        return 1
    else:
        return 0
    return full_url.count('//')

def count_http_token(url_path): # column: http_in_path
    return url_path.count('http')

def https_token(scheme): # column: https_token
    if scheme == 'https':
        return 0
    return 1

def ratio_digits(hostname): # column: ratio_digits_host
    return len(re.sub("[^0-9]", "", hostname))/len(hostname)

def punycode(url): # column: punycode
    if url.startswith("http://xn--") or url.startswith("http://xn--"):
        return 1
    else:
        return 0

def port(url): # column: port
    if re.search("^[a-z][a-z0-9+\-.]*://([a-z0-9\-._~%!$&'()*+,;=]+@)?([a-z0-9\-._~%]+|\[[a-z0-9\-._~%!$&'()*+,;=:]+\]):([0-9]+)",url):
        return 1
    return 0

def tld_in_path(tld, path): # column: tld_in_path
    if path.lower().count(tld)>0:
        return 1
    return 0

def tld_in_subdomain(tld, subdomain): # column: tld_in_subdomain
    if subdomain.count(tld)>0:
        return 1
    return 0

def abnormal_subdomain(url): # column: abnormal_subdomain
    if re.search('(http[s]?://(w[w]?|\d))([w]?(\d|-))',url):
        return 1
    return 0

def count_subdomain(url): # column: nb_subdomains
    if len(re.findall("\.", url)) == 1:
        return 1
    elif len(re.findall("\.", url)) == 2:
        return 2
    else:
        return 3

def prefix_suffix(url): # column: prefix_suffix
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        return 1
    else:
        return 0 

def shortening_service(full_url): # column: shortening_service
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      full_url)
    if match:
        return 1
    else:
        return 0

def path_extension(url_path): # column: path_extension
    if url_path.endswith('.txt'):
        return 1
    return 0

def count_redirection(page): # column: nb_redirection
    return len(page.history)

def count_external_redirection(page, domain): # column: nb_external_redirection
    count = 0
    if len(page.history) == 0:
        return 0
    else:
        for i, response in enumerate(page.history,1):
            if domain.lower() not in response.url.lower():
                count+=1          
            return count

def length_word_raw(words_raw): # column: length_words_raw
    return len(words_raw)

def char_repeat(words_raw): # column: char_repeat
    
        def __all_same(items):
            return all(x == items[0] for x in items)

        repeat = {'2': 0, '3': 0, '4': 0, '5': 0}
        part = [2, 3, 4, 5]

        for word in words_raw:
            for char_repeat_count in part:
                for i in range(len(word) - char_repeat_count + 1):
                    sub_word = word[i:i + char_repeat_count]
                    if __all_same(sub_word):
                        repeat[str(char_repeat_count)] = repeat[str(char_repeat_count)] + 1
        return  sum(list(repeat.values()))

def shortest_word_length(words_raw): # column: shortest_words_raw, shortest_word_host, shortest_word_path
    if len(words_raw) ==0:
        return 0
    return min(len(word) for word in words_raw)

def longest_word_length(words_raw): # column: longest_words_raw, longest_word_host, longest_word_path
    if len(words_raw) ==0:
        return 0
    return max(len(word) for word in words_raw)

def average_word_length(words_raw): # column: average_words_raw, average_word_host, average_word_path
    if len(words_raw) ==0:
        return 0
    return sum(len(word) for word in words_raw) / len(words_raw)

def phish_hints(url_path): # column: phish_hints
    count = 0
    for hint in HINTS:
        count += url_path.lower().count(hint)
    return count

def domain_in_brand(domain): # column: domain_in_brand
        
    if domain in allbrand:
        return 1
    else:
        return 0
 
def domain_in_brand1(domain): # column: domain_in_brand
    for d in allbrand:
        if len(Levenshtein.editops(domain.lower(), d.lower()))<2:
            return 1
    return 0

def brand_in_path(domain,path): # column: brand_in_subdomain, brand_in_path
    for b in allbrand:
        if '.'+b+'.' in path and b not in domain:
            return 1
    return 0

suspecious_tlds = ['fit','tk', 'gp', 'ga', 'work', 'ml', 'date', 'wang', 'men', 'icu', 'online', 'click', # Spamhaus
        'country', 'stream', 'download', 'xin', 'racing', 'jetzt',
        'ren', 'mom', 'party', 'review', 'trade', 'accountants', 
        'science', 'work', 'ninja', 'xyz', 'faith', 'zip', 'cricket', 'win',
        'accountant', 'realtor', 'top', 'christmas', 'gdn', # Shady Top-Level Domains
        'link', # Blue Coat Systems
        'asia', 'club', 'la', 'ae', 'exposed', 'pe', 'go.id', 'rs', 'k12.pa.us', 'or.kr',
        'ce.ke', 'audio', 'gob.pe', 'gov.az', 'website', 'bj', 'mx', 'media', 'sa.gov.au' # statistics
        ]

def suspecious_tld(tld): # column: suspecious_tld
   if tld in suspecious_tlds:
        return 1
   return 0

def statistical_report(url, domain): # column: statistical_report
    url_match=re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',url)
    try:
        ip_address=socket.gethostbyname(domain)
        ip_match=re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                           '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                           '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                           '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                           '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                           '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',ip_address)
        if url_match or ip_match:
            return 1
        else:
            return 0
    except:
        return 2