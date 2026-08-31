use clap::Parser;
use serde::Deserialize;

#[derive(Parser)]
#[command(name = "jp-trans")]
#[command(about = "Translates English input to Japanese and outputs a Romaji pronunciation guide")]
struct Args {
    /// English text to translate
    #[arg(required = true)]
    text: Vec<String>,
}

#[derive(Deserialize)]
struct ResponseData {
    #[serde(rename = "translatedText")]
    translated_text: String,
}

#[derive(Deserialize)]
struct TranslationResponse {
    #[serde(rename = "responseData")]
    response_data: ResponseData,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let english_text = args.text.join(" ");

    let url = format!(
        "https://api.mymemory.translated.net/get?q={}&langpair=en|ja",
        urlencoding::encode(&english_text)
    );

    let client = reqwest::Client::new();
    let res: TranslationResponse = client.get(&url).send().await?.json().await?;
    let japanese_text = res.response_data.translated_text;

    // Convert to Romaji
    let kakasi_res = kakasi::convert(&japanese_text);

    println!("\nEnglish Input:  {}", english_text);
    
    // If kakasi returned the exact same text (meaning no Japanese script was converted)
    if kakasi_res.romaji == japanese_text {
        println!("Japanese Text:  (No translation available)");
        println!("Romaji Guide:   (No Kanji/Kana detected to convert)");
    } else {
        println!("Japanese Text:  {}", japanese_text);
        println!("Romaji Guide:   {}\n", kakasi_res.romaji);
    }

    Ok(())
}