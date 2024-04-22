from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re

def get_top_result(keyword):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    headers = {'User-Agent': user_agent}
    url = f"https://www.google.com/search?q={keyword}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 

        soup = BeautifulSoup(response.content, 'html.parser')

        top_result = soup.find('div', class_='g') 
        if top_result:
            top_link = top_result.find('a')
            if top_link:
            
                return top_link['href'] 

    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")

    return None

def scrape_website_text(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')

        text = '\n\n'.join([p.get_text() for p in paragraphs])

        return text
    else:
        print("Failed to fetch the page. Status code:", response.status_code)
        return None

def remove_symbol_numbers(text):
    # Remove symbols in the form [numbers]
    clean_text = re.sub(r'\[\d+\]', '', text)
    return clean_text

def save_text_to_html(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('<!DOCTYPE html>\n<html>\n<head>\n<title>Scraped Text</title>\n')
        file.write('<style>\n')
        file.write('body { font-family: Arial, sans-serif; }\n')
        file.write('.content { max-width: 800px; margin: 0 auto; padding: 20px; }\n')
        file.write('</style>\n')
        file.write('</head>\n<body>\n')

        file.write('<div class="content">\n')
        file.write(text)
        file.write('\n</div>\n')

        file.write('</body>\n</html>')




def index(request):
    return render(request,'index.html')

def result(request):
    keyword=request.POST.get('keyword')
    
    url = get_top_result(keyword)
    website_text = scrape_website_text(url)

    if website_text:
        # Remove symbol numbers from the scraped text
        cleaned_text = remove_symbol_numbers(website_text)

        # Save the cleaned text to an HTML file
        save_text_to_html(cleaned_text, 'templates/scraped_text.html')
        print("Scraped text saved to 'scraped_text.html'")
    else:
        print("Failed to fetch website text.")
    
    return render(request,'scraped_text.html',)

