import argparse

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
    scrape.add_argument('name', help = 'Full name of the main author.')
    scrape.add_argument('-np', '--no_print', action='store_true', help = 'Do not print the final scraped genealogy tree.')
    scrape.add_argument('-ns', '--no_save', action='store_true', help = 'Do not save the scraped data.')
    
    #
    # List saved genealogy trees
    #
    list = subparsers.add_parser(
        'list',
        help = 'List and index all saved genealogy trees associated to a given author.'
    )
    load.add_argument('name', help = 'Full name of the main author.')
    
    #
    # Print a saved genealogy tree
    #
    load = subparsers.add_parser(
        'load',
        help = 'Load and print a previously scraped author\'s descendants.'
    )
    load.add_argument('name', help = 'Full name of the main author.')
    load.add_argument('-f', '--file', help = 'File index of the file (found by using the list command). Default is the most recent file.')
    
    args = parser.parse_args(command_line)
    # interface = Interface()
    match args.action:
        case 'scrape':
            return 0
        case 'list':
            return 0
        case 'load':
            return 0





if __name__ == "__main__":
    main()