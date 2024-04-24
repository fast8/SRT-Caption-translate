import requests
import pysrt
import concurrent.futures
from bs4 import BeautifulSoup

def remove_tags(text):
    # 使用 BeautifulSoup 去除标签
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    text = text.replace(r"{\an8}", "")
    # print(text)
    return text

def translate_line(text, source_lang, target_lang):
    text = remove_tags(text)
    data = {
        "q": text,
        "source": source_lang,
        "target": target_lang
    }
    response = requests.post("http://127.0.0.1:9911/translate", json=data)
    result = response.json()
    if "error" in result:
        return text  # 如果发生错误，则保持原文本不变
    else:
        return result["translatedText"]

def translate_subtitle(input_file, output_file, source_lang='en', target_lang='zh', max_workers=5):
    subs = pysrt.open(input_file, encoding='utf-8')

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for sub in subs:
            future = executor.submit(translate_line, sub.text, source_lang, target_lang)
            futures.append((future, sub))
            
        
        for future, sub in futures:
            translated_text = future.result()
            print(translated_text)
            sub.text = translated_text

    subs.save(output_file, encoding='utf-8')

if __name__ == "__main__":
    input_file = input('input:')
    output_file = input('output:')
    translate_subtitle(input_file, output_file)