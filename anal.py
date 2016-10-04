"""Anal text analysis program."""
from __future__ import print_function
import sys, os, re, operator, string
import requests, validators
from bs4 import BeautifulSoup

import common

def main():
    """Main function"""

    if len(sys.argv) != 2:
        print(common.USAGE)
        sys.exit()
    if sys.argv[1] in ['-h', '--help']:
        print(common.FULL_HELP)
        sys.exit()

    is_url = True
    path = sys.argv[1]

    try:
        validators.url(path)
    except validators.util.ValidationFailure:
        is_url = False

    if not is_url:
        is_file = os.path.isfile(path)
    if not is_url and not is_file:
        print(common.FULL_HELP)
        sys.exit()

    print('Analyzing {}...'.format(path))

    if is_url:
        r = requests.get(path)
        soup = BeautifulSoup(r.text, 'html.parser')
        for kill in soup(["script", "style"]):
            kill.extract()
        text = soup.get_text(separator=' ').lower()

    # remove punctuation, double and triple spaces
    text = ''.join(ch for ch in text if ch not in common.EXCLUDE).encode('utf-8').strip()
    text = ' '.join(part for part in text.split('  '))
    text = ' '.join(part for part in text.split('   '))

    # split into individual words and remove common words
    text_words = text.split(' ')
    text_words = [w for w in text_words if w not in common.COMMON_WORDS]

    word_count = len(text_words)
    frequency = {}
    for word in text_words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    sorted_freq = sorted(frequency.items(), key=operator.itemgetter(1), reverse=True)
    for word in sorted_freq[:common.FREQ_RESULTS]:
        if isinstance(word[0], str):
            print("{} ---> {}".format(word[0], str(frequency[word[0]])))
        elif isinstance(word[0], unicode):
            print('{}?'.format(word[0]))


if __name__ == "__main__":
    main()
