from django.shortcuts import render, get_object_or_404
import requests
import re
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
from .models import Record
import operator
from django.http import HttpResponse, HttpResponseRedirect


def homepage(request):
    if request.method == 'POST':
        return render(request, 'myapp/homepage.html')
    else:
        return render(request, 'myapp/homepage.html')


def myfun(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def clean_up(words_list, clean_word_list):
    common_words = ["a", "in", "to", "the", "of", "and", "of", "for", "by", "on", "is", "I", "all", "this", "with", "it", "at", "from", "or", "you",
                    "as", "your", "an", "are", "be", "that", "do", "not", "have", "one", "can", "was", "if", "we", "but", "what", "which", "there",
                    "when", "use", "their", "they", "how", "we", "were", "his", "had", "each", "said", "she", "word", "The", "And", "I m", " ", "For",
                    "Is", "we re", "We"]
    for word in words_list:
        symbols = "!@#$%^&|*()_+{}:\"<>?,./;'[]-='"
        for i in range(0, len(symbols)):
            word = word.replace(symbols[i], " ")
        word.strip()

        if '\n' in word:
            word = word.replace("\n", " ")
            word.strip()
        word.replace(" ", "")

        word = ''.join([i for i in word if not i.isdigit()])

        if (len(word) > 2 and word != ' '):
            if (word != '\n' and word not in common_words):
                clean_word_list.append(word)


def result(request):
    if request.method == 'POST':
        url = request.POST.get('inputurl')

        flag = False

        try:
            old_item = Record.objects.get(url_1=url)
        except Record.DoesNotExist:

            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.text, 'html.parser')
            data = soup.find_all(text=True)
            result = filter(myfun, data)
            temp = list(result)

            words_list = []
            for many_words in temp:
                words = many_words.split(" ")
                for each_word in words:
                    words_list.append(each_word)

            clean_word_list = []
            clean_up(words_list, clean_word_list)

            temp_word_count = {}
            for word in clean_word_list:
                if word in temp_word_count:
                    temp_word_count[word] += 1
                else:
                    temp_word_count[word] = 1

            k = []
            v = []

            i = 1

            for key, value in sorted(temp_word_count.items(), key=operator.itemgetter(1), reverse=True):
                if i <= 10:
                    print(key, value)
                    k.append(key)
                    v.append(value)
                elif i > 10:
                    break
                i += 1

            word_count = dict(zip(k, v))

            new_item = Record(url_1=url, content=word_count)
            new_item.save()
            flag = True

        if not flag:
            old_word_count = old_item.content
            old = "Data Fetched from the database!"
            old_url = old_item.url_1
            return render(request, 'myapp/freqlist.html', {'old_word_count': old_word_count, 'old': old, 'old_url': old_url})

        elif flag:
            new_data = "New url content"
            return render(request, 'myapp/freqlist.html', {'word_count': word_count, 'new_data': new_data})
