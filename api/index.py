from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

import os
import urllib
import json
import random
import urlparse
import io,shutil
import cgi

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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):

        parsed_path = urlparse.urlparse(self.path)
        print(self.path)
        #data=parsed_path.query[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).encode())
        return

    def do_POST(self):
        form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD':'POST',
        'CONTENT_TYPE':self.headers['Content-Type'],
        })

        content = ""
        result = ""
        for field in form.keys():
            if field == "text":
                content = form[field].value
                result = toHuman(content, 60, 2, False)
                break

        enc = "UTF-8"
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=%s" % enc)
        self.end_headers()
        #self.wfile.write('Client: %s\n' % str(self.client_address))
        #self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write("{\"text\":\""+content+"\"}")
