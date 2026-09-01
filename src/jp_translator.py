import sys
import argparse
import requests
import pykakasi

def main():
    parser = argparse.ArgumentParser(description="English to Japanese Romaji CLI")
    parser.add_argument("text", nargs="+", help="English text to translate")
    args = parser.parse_args()

    english_text = " ".join(args.text)
    
    # Original endpoint setup using requests params for clean formatting
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": english_text,
        "langpair": "en|ja"
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # 1. Primary endpoint check
        japanese_text = data.get("responseData", {}).get("translatedText", "").strip()
        
        # 2. Fallback to alternative matches if primary translation returns empty
        if not japanese_text and "matches" in data:
            for match in data["matches"]:
                translation = match.get("translation", "").strip()
                if translation:
                    japanese_text = translation
                    break
                    
        if not japanese_text:
            print("Error: Could not retrieve a valid translation from MyMemory.")
            sys.exit(1)

    except Exception as e:
        print(f"Error fetching translation: {e}")
        sys.exit(1)

    kks = pykakasi.kakasi()
    result = kks.convert(japanese_text)

    # Extract hepburn transliteration safely
    romaji_list = [item["hepburn"] for item in result if item.get("hepburn")]
    romaji_text = " ".join(romaji_list)

    println_output(english_text, japanese_text, romaji_text)

def println_output(english, japanese, romaji):
    print(f"\nEnglish Input:  {english}")
    print(f"Japanese Text:  {japanese}")
    print(f"Romaji Guide:   {romaji}\n")

if __name__ == "__main__":
    main()