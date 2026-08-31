import sys
import argparse
import urllib.parse
import requests
import pykakasi

def main():
    parser = argparse.ArgumentParser(description="English to Japanese Romaji CLI")
    parser.add_argument("text", nargs="+", help="English text to translate")
    args = parser.parse_args()

    english_text = " ".join(args.text)
    encoded_text = urllib.parse.quote(english_text)
    url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair=en|ja"

    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        japanese_text = data.get("responseData", {}).get("translatedText", "")
    except Exception as e:
        print(f"Error fetching translation: {e}")
        sys.exit(1)

    kks = pykakasi.kakasi()
    result = kks.convert(japanese_text)

    # Extract hepburn transliteration
    romaji_list = [item["hepburn"] for item in result if item["hepburn"]]
    romaji_text = " ".join(romaji_list)

    println_output(english_text, japanese_text, romaji_text)

def println_output(english, japanese, romaji):
    print(f"\nEnglish Input:  {english}")
    print(f"Japanese Text:  {japanese}")
    print(f"Romaji Guide:   {romaji}\n")

if __name__ == "__main__":
    main()