import urllib.request as re
import urllib.error as er

import string


def prompt_for_input():
    print("Which text file would you like to open?")
    try:
        filename = input("> ")
    except:
        print("Please provide a filename.")
        return prompt_for_input()
    return filename



def find_title_and_url(line):
    line = line.strip()
    comma_position = line.find(",")
    try: 
        while line[comma_position +1] == " ":
            comma_position = line.find(",", comma_position + 1)
    except:
        title = "title not available"
        url = "URL not available"
        return title, url
    title = line[0:comma_position]
    url = line[comma_position + 1:]
    return title, url


def get_url(url):
    """takes a url string as input, makes a HTTP GET request to the URL and returns a string with content.
    Decoding from: http://stackoverflow.com/questions/18897029/read-csv-file-from-url-into-python-3-x-csv-error-iterator-should-return-str
    """
    try:
        response = re.urlopen(url)
        content = response.read()
    except(er.URLError):
        content = ' '
        print("The URL is not functional: " + url)
    except:
        content = ' '
        print("The  url ({}) was not in the expected format.".format(url))
    try:
        content = content.decode('utf-8')
    except:
        print("could not decode")
    return content


def filter_data(content):
    """
    Method to filter non alphabets. Returns a list of words
    adapted from lab slides
    """
    list_of_words = content.split()
    try:
        list_of_words = [''.join([char for char in word if char in string.ascii_letters]).lower() for word in list_of_words]
    except:
        return list_of_words
    list_of_words = [word for word in list_of_words if word.isalpha()]
    return list_of_words



def add_to_dict(dict, list_of_words, total_num_books, book_index):
    for word in list_of_words:
        if word in dict:
            dict[word][book_index] = dict[word][book_index] + 1
        else:
            dict[word] = []
            x = 0
            while x < total_num_books:
                dict[word].append(0)
                x += 1
            dict[word][book_index] = 1
    return dict


def get_query():
    try:
        query = input("Search term? ")
        return query
    except:
        print("Please try again.")
        return get_query()


def assess_input(word):
    terminate = False
    catalog = False
    titles = False
    if word == "<terminate>":
        terminate = True
    if word == "<catalog>":
        catalog = True
    if word == "<titles>":
        titles = True
    return terminate, catalog, titles



def get_results(word, Titles, Words, Books, total_num_books):
    book_index = 0
    i = 1
    while book_index < total_num_books:
        try:
            if Words[word][book_index] == 0:
                book_index += 1
                continue
        except:
            print("The word {} does not appear in any books in the library".format(word))
            return
        else:
            new_list = list(Words[word])
            while new_list != []:
                new_current = max(new_list)
                if new_current == 0:
                    return
                position = 0
                reached_end = False
                while not reached_end:
                    if position +1 == total_num_books:
                        if Words[word][position] != new_current:
                            reached_end = True
                            break
                    try:
                        while Words[word][position] != new_current and position + 1 <= total_num_books:
                            position += 1
                            if position + 1 >= total_num_books:
                                reached_end = True
                    except:
                        break

                    if Words[word][position] == new_current:
                        title = Titles[position]
                        print("{}. The word {} appears {} {} in {} (link: {}) ".format(i, word, new_current, get_times(new_current), title, Books[title][1]))
                        i += 1
                        new_list.remove(new_current)
                        if new_list == []:
                           return
                        else:
                            new_current = max(new_list)
                            if new_current == 0:
                                return
                        if position + 1 < total_num_books:
                            position += 1
                        else:
                            reached_end == True
                            break
            return



def print_catalog(Books, total_num_books):
    i = 0
    while i < total_num_books:
        for key, value in Books.items():
            if value[0] == i:
                print("'{}' : {}".format(key, value))
        i += 1


def print_titles(Titles):
    for title in Titles:
        print (title)


def get_times(int):
    if int == 1:
        return "time"
    else:
        return "times"


def main():
    filename = prompt_for_input()
    if filename == "<terminate>":
        return
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except:
        print("Sorry, could not find the file.")
        return main()
    if lines == []:
        print("The file seems to be empty.")
        return main()
    Books = {}
    Titles = []
    total_num_books = 0
    Words = {}
    for line in lines:
        if "http://" not in line: 
            continue
        title, url = find_title_and_url(line)
        if title in Titles:
            continue
        Titles.append(title)
        Books[title] = [total_num_books, url]
        total_num_books += 1
    for key, value in Books.items():
        book_index = value[0]
        url = value[1]
        content = get_url(url)
        list_of_words = filter_data(content)
        Words = add_to_dict(Words, list_of_words, total_num_books, book_index)
    while True:
        query = get_query()
        terminate, catalog, titles = assess_input(query)
        if terminate:
            return
        if catalog:
            print_catalog(Books, total_num_books)
            continue
        elif titles:
            print_titles(Titles)
            continue
        else:
            result = get_results(query, Titles, Words, Books, total_num_books)
    return

main()
