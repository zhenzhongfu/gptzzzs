from http.server import BaseHTTPRequestHandler
from datetime import datetime

import os
import urllib.request
import json
import random
import urlparse

finnlp_file = "../2synonyms.json"

percentToChange = float(50)
collection = int(2)
ignore_quotes = True

def toHuman(content, percentToChange, collection, ignore_quotes):
    try:
        newWords = ""
        f = open(finnlp_file)
        synonyms = json.load(f)
        print("Loaded file ")
        
        words = content.split(" ")
        num_words = int(len(words) * percentToChange / 100)
        chosen_indices = random.sample(range(len(words)), num_words)

        quotation_count = 0
        for i in range(len(words)):
            if "\"" in words[i]:
                quotation_count += words[i].count("\"")

            if i in chosen_indices and (quotation_count % 2 == 0 or not ignore_quotes):
                word = words[i]
                endswith = ""
                if word.endswith((".", ",", "!", "'", "?", ":", ";")):
                    endswith = word[len(word) - 1]
                    word = word[:-1]

                if len(word) > 3 and word in synonyms.keys() and len(synonyms[word]) != 0:
                    word = random.choice(synonyms[word])

                    newWords = "{}{}{}".format(newWords, word, endswith)
                if i != len(words) - 1:
                    newWords = "{}{}".format(newWords, " ")
            else:
                newWords = "{}{}".format(newWords, words[i])
                if i != len(words) - 1:
                    newWords = "{}{}".format(newWords, " ")
        return newWords
    except Exception as e:
        print("\033[0;31;40mFailed to load synonyms file\033[0m")
        print(e)
        exit()

content ="John F. Kennedy, who served as the 35th President of the United States from 1961 until his assassination in 1963, is widely considered as one of the best Presidents in American history. He was a charismatic leader who inspired and united the nation, particularly during the Civil Rights Movement. Kennedy's speeches, such as his inaugural address in which he famously said Ask not what your country can do for you, ask what you can do for your country, and his famous Moon speech in which he challenged the nation to put a man on the moon within a decade, are still remembered and quoted today. Additionally, Kennedy's foreign policy was marked by a strong commitment to peace and diplomacy, as exemplified by the Cuban Missile Crisis, where his cool and steady leadership helped to defuse a potentially catastrophic conflict with the Soviet Union. Overall, JFK's legacy as a visionary leader who inspired a generation and left a lasting impact on the world continues to make him one of the most beloved Presidents in American history."
result = toHuman(content, 20, 2, True)
print(content)
print(result)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        data=parsed_path.query[1]
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).encode())
        return
