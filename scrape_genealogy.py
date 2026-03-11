import os, io, json
from datetime import datetime
import time
from bs4 import BeautifulSoup
import feedparser
from treelib import Tree

CATEGORY = 'quant-ph'
MAX_STUDENT_PER_PAPER = 1
SAVE_PATH = '.\\saved_results\\'


def format_author(string):
    formatted = '_'.join(string.split()).lower()
    return formatted


def get_articles_from_author(author, max_results = 1000, category=CATEGORY):
    if ' ' in author:
        author = format_author(author)
    base_url = 'http://export.arxiv.org/api/query?search_query='
    rss_request = base_url + 'au:' + author
    rss_request += '+AND+cat:' + category
    rss_request += '&start=0&max_results=' + str(max_results)
    d = feedparser.parse(rss_request)
    article_list = d.entries
    return article_list


def same_author(string1, string2):
    same_initial = lambda w1, w2: w1[0].lower() == w2[0].lower()
    def equivalent_words(w1, w2):
        if len(w1) == len(w2):
            return w1.lower() == w2.lower()
        else:
            if len(w1) > len(w2):
                w1, w2 = w2, w1
            return len(w1)==2 and w1[1]=='.' and same_initial(w1, w2)

    if string1.lower() == string2.lower():  # If strings are identitical this is simple
        return True
    split1, split2 = string1.split(), string2.split()
    if split1[-1].lower() == split2[-1].lower():  # Check for identical last names
        split1.pop()
        split2.pop()
        if len(split1) == len(split2):  # if same number of words
            flag_same = True
            for word1, word2 in zip(split1, split2):
                flag_same = flag_same and (word1[0].lower() == word2[0].lower())
            return flag_same
        else:  # if different number of words
            if len(split1) > len(split2):  # check that split1 has fewer words
                split1, split2 = split2, split1
            i1, i2 = 0, 0
            while i1 < len(split1) and i2 < len(split2):
                if equivalent_words(split1[i1], split2[i2]):
                    i1, i2 = i1+1, i2+1
                else:
                    i2 += 1
            if i1 == len(split1):
                return True
    return False


def add_authors_from_article(article, author_list=[], max_authors=MAX_STUDENT_PER_PAPER):
    if not 0<=max_authors<=len(article['authors']):
        max_authors = len(article['authors'])
    for i in range(max_authors):
        author = article['authors'][i]
        name = author['name']
        if sum(list(map(lambda w: same_author(name, w), author_list))) == 0:
            author_list.append(name)
    return author_list


def add_authors_all(article_list, author_list=[], max_authors=MAX_STUDENT_PER_PAPER):
    for article in article_list:
        author_list = add_authors_from_article(article, author_list, max_authors)
    return author_list


def add_descendants(author, desc_list=[]):
    def supervisor(author, article):
        list_authors = article['authors']
        return same_author(author, list_authors[-1]['name'])
    
    article_list = get_articles_from_author(author)
    time.sleep(5)
    supervised_articles = list(filter(lambda art: supervisor(author, art), article_list))
    desc_list = add_authors_all(supervised_articles, desc_list)
    return desc_list


def get_all_descendants(main_author, main_author_id=0, desc_list=[], relation_list=[], save=True):
    # Not to be used for authors which have too many descendants
    if not desc_list:
        desc_list.append(main_author)
        relation_list = [[0,0]]
        main_author_id = 0
    initial_len = len(desc_list)
    desc_list = add_descendants(main_author, desc_list)
    relation_list += [[main_author_id, i] for i in range(initial_len, len(desc_list))]
    for i in range(initial_len, len(desc_list)):
        desc = desc_list[i]
        print(i, desc)
        desc_list, relation_list = get_all_descendants(desc, i, desc_list, relation_list, save=False)
    if save:
        save_json(main_author, {'desc_list': desc_list, 'relation_list': relation_list})
        print('Saved scraped data.')
    return desc_list, relation_list


def get_descendant_generations(main_author, main_author_id=0, desc_list=[], relation_list=[], n_gens=1, save=True):
    if not desc_list:
        desc_list.append(main_author)
        relation_list = [[0,0]]
        main_author_id = 0
    if n_gens > 0:
        initial_len = len(desc_list)
        desc_list = add_descendants(main_author, desc_list)
        relation_list += [[main_author_id, i] for i in range(initial_len, len(desc_list))]
        for i in range(initial_len, len(desc_list)):
            desc = desc_list[i]
            print(i, desc)
            desc_list, relation_list = get_descendant_generations(desc, i, desc_list, relation_list, n_gens=n_gens-1, save=False)
        if save:
            save_json(main_author, {'desc_list': desc_list, 'relation_list': relation_list})
            print('Saved scraped data.')
    return desc_list, relation_list


def save_json(author, author_dict):
    timestamp = datetime.now().strftime('_%Y-%m-%d_%H-%M-%S')
    json_file = SAVE_PATH + format_author(author) + timestamp + '.json'
    with io.open(json_file, 'w', encoding='utf-8') as f:
        json.dump(author_dict, f, ensure_ascii=False, indent=4, sort_keys=True)


def read_json(author):
    list_files = os.listdir(SAVE_PATH)
    json_file = ''
    for file in list_files:
        if format_author(author) in file:
            json_file = file
    try:
        with io.open(SAVE_PATH + json_file, 'r', encoding='utf-8') as f:
            author_dict = json.load(f)
        return author_dict
    except:
        raise ValueError('Author name has not been scraped previously!')


def tree_from_file(author, save=True):
    author_dict = read_json(author)
    desc_list = author_dict['desc_list']
    relation_list = author_dict['relation_list']
    tree = Tree()
    for name, relation in zip(desc_list, relation_list):
        if relation[0] == relation[1]:
            tree.create_node(name, format_author(name))
        else:
            tree.create_node(name, format_author(name), parent=format_author(desc_list[relation[0]]))
    if save:
        timestamp = datetime.now().strftime('_%Y-%m-%d_%H-%M-%S')
        tree.save2file('.\\trees\\' + author + '_' + timestamp + '.txt', line_type='ascii-em')
    tree.show()





if __name__ == '__main__':
    main_author = ''
    descendants, relations = get_descendant_generations(main_author, n_gens=3)
    print(descendants)
    print(relations)
    tree_from_file(main_author)

