import os, io, json
from datetime import datetime
from .scrape_genealogy import format_author, get_descendant_generations, tree_from_file


class Interface:

    def __init__(self):
        return 0

    #
    # Scrape
    #

    def scrape(self, name, generations, no_print=False, no_save=False):
        desc_list, relation_list = get_descendant_generations(format_author(name), n_gens=generations, save=(not no_save))
        if not no_print:
            tree_from_file(format_author(name), save=False)

    #
    # List
    #
    def list_files(self, name):
        base_path = '.\\saved_results\\'
        files = os.listdir(base_path)
        filtered_files = list(filter(lambda string: format_author(name) in string, files))
        for i in range(len(filtered_files)):
            print(str(i) + ':\t' + filtered_files[i])

    #
    # Load
    #
    def load(self, name, file=-1):
        tree_from_file(format_author(name), fileindex=file, save=False)
