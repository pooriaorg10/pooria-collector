import urllib.request
import urllib.error
import urllib.parse
import base64
import os
import concurrent.futures
from typing import List, Set

# لیست لینک‌های سابسکریپشن
SUB_LINKS: List[str] = [
    "https://raw.githubusercontent.com/liketolivefree/kobabi/main/sub.txt",
    "https://farsonline24.ir/",
    "https://info.farsonline24.ir",
    "https://manager.farsonline24.ir",
    "https://office.farsonline24.ir/",
    "http://sabapardaziran.ir/download/sub?target=V2Ray",
    "https://raw.githubusercontent.com/arshiacomplus/v2rayExtractor/main/vless.html"
]

OUTPUT_FILENAME: str = "configs/proxy_configs.txt"

def get_configs_from_sub(url: str) -> List[str]:
    """دانلود کانفیگ‌ها با استفاده از کتابخانه استاندارد (بدون نیاز به نصب requests)"""
    try:
        # تنظیم هدر برای جلوگیری از بلاک شدن
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        # تایم‌اوت کوتاه (۱۰ ثانیه) برای سرعت بیشتر
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            
        decoded_content = ""
        try:
            missing_padding = len(content) % 4
            if missing_padding:
                content += '=' * (4 - missing_padding)
            decoded_content = base64.b64decode(content).decode('utf-8')
        except Exception:
            decoded_content = content

        return [line.strip() for line in decoded_content.splitlines() if line.strip()]
        
    except Exception:
        return []

def main():
    all_configs: List[str] = []
    
    # استفاده از ThreadPool برای دانلود همزمان تمام لینک‌ها (افزایش شدید سرعت)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(get_configs_from_sub, SUB_LINKS)
        for result in results:
            all_configs.extend(result)
    
    unique_configs: Set[str] = set(all_configs)
    
    if not unique_configs:
        return

    renamed_configs: List[str] = []
    sorted_unique_configs = sorted(list(unique_configs))
    
    # تغییر نام کانفیگ‌ها طبق فرمت درخواستی
    for i, config in enumerate(sorted_unique_configs):
        if '#' in config:
            base_link = config.split('#')[0]
        else:
            base_link = config
        
        new_name = f"POORIAREDiran{i+1}"
        encoded_name = urllib.parse.quote(new_name)
        renamed_configs.append(f"{base_link}#{encoded_name}")
        
    final_config_str = "\n".join(renamed_configs)
    final_b64_config = base64.b64encode(final_config_str.encode('utf-8')).decode('utf-8')
    
    try:
        os.makedirs(os.path.dirname(OUTPUT_FILENAME), exist_ok=True)
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write(final_b64_config)
    except IOError:
        pass

if __name__ == "__main__":
    main()
