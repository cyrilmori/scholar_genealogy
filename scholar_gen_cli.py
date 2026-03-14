import argparse
from scrape_gen import *

def main(command_line=None):
    parser = argparse.ArgumentParser(
        prog='Scholar Genealogy',
        description='Uses ArXiv API to generate genealogy trees for reserachers with publications.'
    )
    subparsers = parser.add_subparsers(dest='action')

    #
    # Scrape and save genealogy tree
    #
    scrape = subparsers.add_parser(
        'scrape',
        help = 'Scrape an author\'s descendants.'
    )
    scrape.add_argument('name', type=str, help = 'Full name of the main author.')
    scrape.add_argument('generations', type=int, help = 'Number of generations to scrape (advised <4).')
    scrape.add_argument('-np', '--no_print', action='store_true', help = 'Do not print the final scraped genealogy tree.')
    scrape.add_argument('-ns', '--no_save', action='store_true', help = 'Do not save the scraped data.')
    
    #
    # List saved genealogy trees
    #
    list = subparsers.add_parser(
        'list',
        help = 'List and index all saved genealogy trees associated to a given author.'
    )
    list.add_argument('name', help = 'Full name of the main author.')
    
    #
    # Print a saved genealogy tree
    #
    load = subparsers.add_parser(
        'load',
        help = 'Load and print a previously scraped author\'s descendants.'
    )
    load.add_argument('name', help = 'Full name of the main author.')
    load.add_argument('-f', '--file', help = 'File index of the file (found by using the list command). Default is the most recent file.', default=-1)
    
    args = parser.parse_args(command_line)
    interface = Interface()
    match args.action:
        case 'scrape':
            interface.scrape(args.name, args.generations, args.no_print, args.no_save)
        case 'list':
            interface.list_files(args.name)
        case 'load':
            interface.load(args.name, args.file)





if __name__ == "__main__":
    main()