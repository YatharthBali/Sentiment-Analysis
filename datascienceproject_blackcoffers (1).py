# -*- coding: utf-8 -*-
"""DataScienceProject_BlackCoffers.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ug9ExJ5aMynlmM0oTt2RCWWNlGa5qYHL
"""

import pandas as pd #used this library to read excel file
import requests# used this library to get permission from the particular websites to fetch the text
from bs4 import BeautifulSoup#used this library for getting the response from the library
import xml.etree.ElementTree as ET#used to pass xml

df=pd.read_excel('Input.xlsx')#used to read the excel file

df.head()#will dispay the top 5 rows of the excel sheet

def fetch_article_data(url):#defined a function


    response = requests.get(url)#request the webpage for data gather
    response.raise_for_status()  # Check for HTTP errors

    soup = BeautifulSoup(response.content, 'html.parser')#will response to data that html will return

    title_element = soup.find('h1')  # used to find the title as its generally denoted by h1 tag
    title = title_element.text.strip() if title_element else None#we remove the extra spaceand if it is not found in excel then it will return none

    text_elements = soup.find_all('p')  # used to find all text in excel
    text = '\n'.join([p.text.strip() for p in text_elements])#join the next line of paragraph and remove the space

    return title, text#this will return the title and text found for every particular url

# Read URLs from an Excel file
df = pd.read_excel('Input.xlsx') # Read the Excel file using pandas
urls = df['URL'].tolist() # Extract URLs from the 'URL' column

# Process each URL
results = []
for url in urls:#for loop will keep running till 147 times
    title, text = fetch_article_data(url)#here we ae calling the functions and the return statement values will be stored in title and text here
    if title and text:
        results.append({'url': url, 'title': title, 'text': text})#if it is found then it will append and store in dictionary
        print(f"Successfully fetched data for: {url}")
    else:
        print(f"Failed to fetch data for: {url}")




for result in results:#for every loop this will run too and will mention each url,title and text
    print("URL:", result['url'])
    print("Title:", result['title'])
    print("Text:", result['text'])
    print("-" * 30)

count_success = 0  # i have used to check the count so that if out of 147 url if anyone is missed then i have to perform another operation

for url in urls:
    title, text = fetch_article_data(url)
    if title and text:
        results.append({'url': url, 'title': title, 'text': text})
        print(f"Successfully fetched data for: {url}")
        print("Title:", title)
        print("Text:", text)
        print("-" * 30)
        count_success += 1

# Print the total count after the loop
print(f"Successfully extracted data for {count_success} URLs.")#successfully i got 147 count here

print("\033[94mDATA EXTRACTION IS DONE TILL THIS POINT , NOW TIME FOR ANALYSIS\033[0m")

!pip install textblob nltk

from textblob import TextBlob#nlp library and used for sentimental analysis
import nltk
nltk.download('punkt')#used to break text to sentences
nltk.download('averaged_perceptron_tagger')# will convert each word in a sentence and coreect it gramatically

def analyze_text(text):
    blob = TextBlob(text)#will hold the text and help in analysis
    words = blob.words#will extract every particular word
    sentences = blob.sentences#will extract every particular sentence

    #Positive Score
    positive_score = blob.sentiment.polarity if blob.sentiment.polarity > 0 else 0

    #Negative Score
    negative_score = -blob.sentiment.polarity if blob.sentiment.polarity < 0 else 0

    #Polarity Score
    polarity_score = blob.sentiment.polarity

    #Subjectivity Score
    subjectivity_score = blob.sentiment.subjectivity

    #Avg Sentence Length
    avg_sentence_length = sum(len(sentence.words) for sentence in sentences) / len(sentences) if sentences else 0

    #Percentage of Complex Words
    complex_word_count = sum(1 for word in words if len(word) > 6)
    percentage_complex_words = (complex_word_count / len(words)) * 100 if words else 0

    #Fog Index
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    #Avg Number of Words per Sentence
    avg_words_per_sentence = avg_sentence_length

    #Word Count
    word_count = len(words)

    #Syllable per Word
    def count_syllables(word):
        vowels = "aeiouy"
        count = 0
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        return count

    syllable_count = sum(count_syllables(word) for word in words)
    syllables_per_word = syllable_count / word_count if word_count else 0

    #Personal Pronouns
    personal_pronouns = ["I", "me", "my", "mine", "we", "us", "our", "ours", "you", "your", "yours", "he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs"]
    personal_pronoun_count = sum(1 for word in words if word.lower() in personal_pronouns)

    #Avg Word Length
    avg_word_length = sum(len(word) for word in words) / word_count if word_count else 0

    return {
        'Positive Score': positive_score,
        'Negative Score': negative_score,
        'Polarity Score': polarity_score,
        'Subjectivity Score': subjectivity_score,
        'Avg Sentence Length': avg_sentence_length,
        'Percentage of Complex Words': percentage_complex_words,
        'Fog Index': fog_index,
        'Avg Number of Words per Sentence': avg_words_per_sentence,
        'Complex Word Count': complex_word_count,
        'Word Count': word_count,
        'Syllable per Word': syllables_per_word,
        'Personal Pronouns': personal_pronoun_count,
        'Avg Word Length': avg_word_length
    }

results = []
for url in urls:
    title, text = fetch_article_data(url)
    if title and text:
        analysis = analyze_text(text)
        result = {'url': url, 'title': title, 'text': text}
        result.update(analysis) # Add analysis results to the dictionary
        results.append(result)
        print(f"Successfully fetched and analyzed data for: {url}")
    else:
        print(f"Failed to fetch data for: {url}")

# Create a DataFrame from the results and save to Excel
df_output = pd.DataFrame(results)
df_output.to_excel("Output_Analysis.xlsx", index=False)#final output file name

