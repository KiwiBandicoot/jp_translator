import argparse
import sys
import ctranslate2
import pykakasi
import transformers


def main():
  parser = argparse.ArgumentParser(
      description="Offline English to Japanese Romaji CLI"
  )
  parser.add_argument("text", nargs="+", help="English text to translate")
  args = parser.parse_args()

  english_text = " ".join(args.text).strip()
  if not english_text:
    print("Error: Please provide English text to translate.")
    sys.exit(1)

  # 1. Load local tokenizer and ctranslate2 neural model
  model_dir = "opus-mt-en-jap-ct2"
  try:
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        "Helsinki-NLP/opus-mt-en-jap"
    )
    translator = ctranslate2.Translator(model_dir, device="cpu")
  except Exception as e:
    print(f"Error loading local model: {e}")
    print(
        "Ensure you ran: ct2-transformers-converter --model"
        " Helsinki-NLP/opus-mt-en-jap --output_dir opus-mt-en-jap-ct2"
    )
    sys.exit(1)

  # 2. Local Neural Translation (CPU-bound, no network requests)
  source_tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(english_text))
  results = translator.translate_batch([source_tokens])
  target_tokens = results[0].hypotheses[0]
  japanese_text = tokenizer.decode(
      tokenizer.convert_tokens_to_ids(target_tokens)
  )

  # 3. Local Kanji/Kana to Romaji conversion
  kks = pykakasi.kakasi()
  result = kks.convert(japanese_text)

  romaji_tokens = [
      item.get("hepburn") or item.get("orig", "") for item in result
  ]
  romaji_text = " ".join(romaji_tokens).strip()

  print(f"\nEnglish Input:  {english_text}")
  print(f"Japanese Text:  {japanese_text}")
  print(f"Romaji Guide:   {romaji_text}\n")


if __name__ == "__main__":
  main()