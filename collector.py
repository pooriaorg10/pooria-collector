import requests
import base64
import urllib.parse
import random
import os
from typing import List, Set

# .لیستی از جاویدنامان خیزش زن، زندگی، آزادی و آبان ۹۸. این لیست برای یادبود این عزیزان استفاده شده است
JAVID_NAMAN: List[str] = [
    # --- جاویدنامان خیزش زن، زندگی، آزادی ---
    "مهسا امینی", "نیکا شاکرمی", "سارینا اسماعیل‌زاده", "حدیث نجفی", "مینو مجیدی", "غزاله چلابی",
    "حنانه کیا", "محسن شکاری", "مجیدرضا رهنورد", "محمدمهدی کرمی", "سید محمد حسینی", "کیان پیرفلک",
    "خدیجه نقدی", "جواد حیدری", "فرشته احمدی", "رضا شهپرنیا", "عرفان زمانی", "یلدا آقافضلی",
    "ابوالفضل آدینه‌زاده", "اسرا پناهی", "محسن قیصری", "حمیدرضا روحی", "آیلار حقی", "سپهر مقصودی",
    "مهدی زارع اشکذری", "دنیا فرهادی", "آرشیا امامقلی‌زاده", "نگین عبدالمالکی", "مهرشاد شهیدی",
    "سارینا ساعدی", "کومار درافتاده", "بهناز افشاری", "آرمین صیادی", "امیرحسین شمس", "دانیال پابندی",
    "عرفان خزایی", "شیرین علیزاده", "فواد محمدی", "پویا شیدا", "مهرگان زحمتکش", "سیاوش محمودی",
    "پدرام آذرنوش", "علی روزبهانی", "مهدی حضرتی", "آرمان عمادی", "میلاد سعیدیان‌جو", "آیدا رستمی",
    "علی سیدی", "امیرمهدی فرخی‌پور", "سمانه نیک‌نام", "اسماعیل دزوار", "فریدون محمودی", "رضا لطفی",
    "زکریا خیال", "مومن زندکریمی", "صدرالدین لیتانی", "عاطفه نعامی", "آرنیکا قائم مقامی",
    "محمدحسن ترکمان", "مبین میرزایی", "جواد موسوی", "آیدین درویش", "متین نصرتی", "سینا نادری",
    "عرفان کاکایی", "اسماعیل مولودی", "آرین مریدی", "سینا ملایری", "امید حسنی", "آرین خوش‌گواریان",
    "روزبه خادمیان", "رضا کاظمی", "حمید گلی", "محمد حاجی‌رسول‌پور", "شمال خدیری‌پور", "ابراهیم میرزایی",
    "نسرین قادری", "آرمان اکبری", "پوریا احمدی", "محمدامین هاشمی", "امیر فلاحت‌دوست", "میلاد خوشکام",
    "هومن عبداللهی", "امیرمحمد رحیمی", "شورش نیکنام", "محمدحسین کمندلو", "محمود احمدی", "حمیدرضا براهویی",
    "محمد اقبال شهنوازی", "محمد ریگی", "عمر شهنوازی", "سامر هاشم‌زهی", "متین قنبرزهی", "جابر شیروزهی",

    # --- جاویدنامان آبان ۹۸ ---
    "پویا بختیاری", "نیکتا اسفندانی", "نوید بهبودی", "فرزاد انصاری‌فر", "ارشام ابراهیمی", "ابراهیم کتابدار",
    "پژمان قلی‌پور", "مهدی نکویی", "آذر میرزاپور", "منوچهر رضایی", "محسن جعفرپناه", "امیررضا عبداللهی",
    "رضا معظمی", "امیرحسین صادقی", "سعید زینبی", "علیرضا نوری", "محمد حشم‌دار", "مهرداد معین‌فر",
    "وحید دامور", "برهان منصوری", "کمال فرجی", "حمید رسولی", "محمدجواد عابدی", "جواد بابایی",
    "مهدی پازوکی", "علی رحمانی", "مسعود رضوی", "امیر الوندی‌مهر", "آرش کهزادی", "ناصر رضایی",
    "رضا حسن‌وند", "آرمین قادری", "امیر شاملو", "حسین قدمی", "میلاد محبوبی", "بهمن جعفری",
    "محمد ملکی", "میثم احمدی", "فرهاد مجدم", "علی قیصری", "مهدی دالوند", "پوریا ناصرخانی"
]


# لیست لینک‌های سابسکریپشن شما
SUB_LINKS: List[str] = [
    "https://raw.githubusercontent.com/liketolivefree/kobabi/main/sub.txt",
    "https://farsonline24.ir/",
    "https://info.farsonline24.ir",
    "https://manager.farsonline24.ir",
    "https://office.farsonline24.ir/",
    "http://sabapardaziran.ir/download/sub?target=V2Ray",
    "https://raw.githubusercontent.com/arshiacomplus/v2rayExtractor/main/vless.html"
]

# نام فایل خروجی در پوشه configs
OUTPUT_FILENAME: str = "configs/proxy_configs.txt"

# اضافه کردن هدر برای اینکه درخواست‌ها طبیعی‌تر به نظر برسند
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_configs_from_sub(url: str) -> List[str]:
    """کانفیگ‌ها را از یک لینک سابسکریپشن دانلود و استخراج می‌کند."""
    try:
        print(f"در حال دریافت کانفیگ از: {url}")
        response = requests.get(url, timeout=20, headers=HEADERS)
        response.raise_for_status()
        
        content = response.text
        decoded_content = ""
        
        try:
            missing_padding = len(content) % 4
            if missing_padding:
                content += '=' * (4 - missing_padding)
            decoded_content = base64.b64decode(content).decode('utf-8')
        except Exception:
            decoded_content = content

        configs = [line.strip() for line in decoded_content.splitlines() if line.strip()]
        print(f"تعداد {len(configs)} کانفیگ از این لینک پیدا شد.")
        return configs
        
    except requests.exceptions.RequestException as e:
        print(f"خطا در دریافت لینک {url}: {e}")
        return []
    except Exception as e:
        print(f"خطایی ناشناخته در پردازش لینک {url}: {e}")
        return []

def main():
    """تابع اصلی برنامه"""
    if not JAVID_NAMAN:
        print("لیست نام‌ها خالی است. برنامه متوقف شد.")
        return

    shuffled_names = JAVID_NAMAN[:]
    random.shuffle(shuffled_names)
    print("\nترتیب نام‌ها به صورت تصادفی برای این اجرا مشخص شد.")
    
    all_configs: List[str] = []
    for link in SUB_LINKS:
        all_configs.extend(get_configs_from_sub(link))
    
    print(f"\nمجموعاً {len(all_configs)} کانفیگ (با احتساب موارد تکراری) پیدا شد.")
    
    unique_configs: Set[str] = set(all_configs)
    print(f"تعداد {len(unique_configs)} کانفیگ منحصر به فرد یافت شد.")
    
    if not unique_configs:
        print("هیچ کانفیگی برای پردازش وجود ندارد. خروج.")
        return

    renamed_configs: List[str] = []
    sorted_unique_configs = sorted(list(unique_configs))
    
    for i, config in enumerate(sorted_unique_configs):
        if '#' in config:
            base_link = config.split('#')[0]
        else:
            base_link = config
        
        name_index = i % len(shuffled_names)
        javid_nam = shuffled_names[name_index]
        
        # جایگزینی تمام فاصله‌ها با خط تیره
        name_without_spaces = javid_nam.replace(" ", "-")
        new_name = f"POORIA-{name_without_spaces}"
        
        encoded_name = urllib.parse.quote(new_name)
        new_link = f"{base_link}#{encoded_name}"
        renamed_configs.append(new_link)
        
    final_config_str = "\n".join(renamed_configs)
    final_b64_config = base64.b64encode(final_config_str.encode('utf-8')).decode('utf-8')
    
    try:
        # ایجاد پوشه configs در صورتی که وجود نداشته باشد
        os.makedirs(os.path.dirname(OUTPUT_FILENAME), exist_ok=True)

        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write(final_b64_config)
        print(f"\nیادشان گرامی. {len(renamed_configs)} کانفیگ در فایل '{OUTPUT_FILENAME}' ذخیره شد.")
    except IOError as e:
        print(f"خطا در نوشتن فایل خروجی: {e}")

if __name__ == "__main__":
    main()
