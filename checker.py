import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# منابع طلایی (این لیست را هر چقدر بخواهی می‌توانی بزرگ کنی)
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ir.m3u",
    "https://raw.githubusercontent.com/Moebius77/Persian-IPTV/master/playlist.m3u"
]

def check():
    print("🚀 mwriTV Crawler started...")
    all_raw = ""
    for s in SOURCES:
        try:
            r = requests.get(s, timeout=10)
            all_raw += r.text + "\n"
        except: continue

    lines = all_raw.split('\n')
    valid = ["#EXTM3U"]
    seen = set()

    print(f"🔍 Analyzing {len(lines)//2} potential streams...")

    current_info = ""
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            current_info = line
        elif line.startswith("http") and current_info:
            if line in seen: continue
            
            try:
                # تست واقعی با دریافت هدر و شبیه‌سازی مرورگر
                headers = {'User-Agent': 'Mozilla/5.0'}
                with requests.get(line, headers=headers, timeout=4, stream=True, verify=False) as r:
                    if r.status_code == 200:
                        valid.append(current_info)
                        valid.append(line)
                        seen.add(line)
                        print(f"✅ OK: {line[:40]}...")
            except: pass
            current_info = ""

    with open('valid_channels.m3u', 'w', encoding='utf-8') as f:
        f.write("\n".join(valid))
    print(f"✨ Success! Total valid channels: {len(valid)//2}")

if __name__ == "__main__":
    check()
