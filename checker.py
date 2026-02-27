import requests
import urllib3
import concurrent.futures

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# منابع عظیم و جامع (شامل ایران، ورزش، اخبار و جهانی)
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ir.m3u", # صدا و سیما و استانی
    "https://raw.githubusercontent.com/Moebius77/Persian-IPTV/master/playlist.m3u", # GEM و فارسی خارجی
    "https://raw.githubusercontent.com/iptv-org/iptv/master/categories/sports.m3u", # ورزش کل دنیا
    "https://raw.githubusercontent.com/iptv-org/iptv/master/categories/news.m3u", # اخبار کل دنیا
    "https://raw.githubusercontent.com/iptv-org/iptv/master/categories/movies.m3u", # فیلم و سینما
    "https://iptv-org.github.io/iptv/languages/fas.m3u" # تمامی شبکه‌های فارسی‌زبان موجود
]

def check_link(item):
    info, url = item
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        with requests.get(url, headers=headers, timeout=5, stream=True, verify=False) as r:
            if r.status_code == 200:
                return (info, url)
    except: pass
    return None

def run_ultimate_check():
    print("🌍 mwriTV: Fetching thousands of channels...")
    all_raw = ""
    for s in SOURCES:
        try:
            r = requests.get(s, timeout=15)
            all_raw += r.text + "\n"
        except: print(f"⚠️ Failed to sync: {s[:40]}")

    lines = all_raw.split('\n')
    tasks = []
    current_info = ""
    seen_urls = set()

    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            current_info = line
        elif line.startswith("http") and current_info:
            if line not in seen_urls:
                tasks.append((current_info, line))
                seen_urls.add(line)
            current_info = ""

    print(f"🔍 Analyzing {len(tasks)} channels using Multi-threading...")
    valid_channels = ["#EXTM3U"]

    # استفاده از چند پردازشی برای بالا بردن سرعت تست (Multi-threading)
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(check_link, tasks))

    for res in results:
        if res:
            valid_channels.append(res[0])
            valid_channels.append(res[1])

    with open('valid_channels.m3u', 'w', encoding='utf-8') as f:
        f.write("\n".join(valid_channels))
    
    print(f"✨ SUCCESS! mwriTV Database Updated: {len(valid_channels)//2} Live Channels Found.")

if __name__ == "__main__":
    run_ultimate_check()
