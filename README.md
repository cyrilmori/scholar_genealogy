# Scholar genealogy

Simple library with utility functions to scrape researcher genealogy from ArXiv. From a researcher name, ArXiv is scraped for papers where he is the last author and, in those same papers, the first authors are taken as "descendants" (PhD students or post-docs) who were supervized by him.

The main function to be used is:
```
get_descendant_generations(main_author, main_author_id=0, desc_list=[], relation_list=[], n_gens=1, save=True)
```
where the only important arguments are ```main_author``` (a string indicating the name of the main researcher to be scraped) and ```n_gens``` (an integer for the number of generations of descendants to be scraped). The other arguments are mostly used for recursivity of the function.

Note that the script takes a while to run and is limited by a delay of 3s which is required by the terms of use of the ArXiv API. It is thus recomended to used ```n_gens < 4```.


### Future improvements

- Implement CLI
- Import multiple tree files at once
- Check overlaps between several genealogy trees
