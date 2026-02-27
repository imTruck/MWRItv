import requests

# لیستی از منابعی که خودشون تستر دارن و لینک‌های سالم می‌ذارن
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ir.m3u", # Iran Official
    "https://raw.githubusercontent.com/Moebius77/Persian-IPTV/master/playlist.m3u", # Persian All
    "https://raw.githubusercontent.com/ssili126/tv/main/itvlist.m3u" # Global Sports
]

def fetch():
    final_content = "#EXTM3U\n"
    print("📡 Fetching pre-validated links for mwriTV...")
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                # حذف خط اول مشترک M3U
                lines = r.text.split('\n')[1:]
                final_content += '\n'.join(lines)
                print(f"✅ Source synced: {url[:40]}...")
        except:
            print(f"❌ Failed to sync: {url[:40]}")

    with open('valid_channels.m3u', 'w') as f:
        f.write(final_content)
    print("\n✨ valid_channels.m3u is ready! No local testing needed.")

if __name__ == "__main__":
    fetch()
