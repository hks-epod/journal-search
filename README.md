journal-search
==============

### Summary

November 2015. Some basic text mining of econ articles.

### Resources
* [AER](https://www.aeaweb.org/aer/issues.php)
* [Journal of Political Economy](http://www.jstor.org/journal/jpoliecon)
* [Econometrica](https://www.econometricsociety.org/publications/econometrica/browse)
* [Finding word stems using `nltk`](http://www.nltk.org/howto/stem.html)

### Notes

#### On scraping the journals
* AER's links to past issues are very well-structured: 
```
<a href='/articles.php?doi=10.1257/aer.' + 'i' + '.' + 'j'>
```
where `i` is years since 1910 (e.g. 2015 is `105`) and `j` is months (e.g. November is `11`, January is `1`).
* JPE is causing problems; getting HTTP errors (302 (infinite loop) and 404 (not found)). It works when a human does it. Use `selenium`?
* Econometrica's link to past issues are also very well-structured: 
```
<a href="/publications/econometrica/issue/2014/11/">November 2014 (Issue 6)</a>
```
Lovely. However, Econometrica's articles are united by `<div class="featured_paper_content">`, which is not helpful. (Since AER's articles are all united by `articles.php` being in their `<a href>`.)

#### On word stems
The array of stems that we're interested in are `['impact*', 'effect*', 'predict*', 'forecast*', 'fore*']`. We can probably use [NLTK's word stemmer (`nltk.stem`)](http://www.nltk.org/api/nltk.stem.html) to do this, and then use [`collections.Counter()`](https://docs.python.org/2/library/collections.html#collections.Counter) or somesuch for counting the words in each title/abstract.


### TODO
1. ~~`git`.~~
2. ~~Look at 2-3 top econ journals (say AER, Journal of Political Economy, and Econometrica) for the past 3-5 years (depending on how time consuming the task is)~~
  * Get JPE to work...
  * Deal with "Requested item not found" errors on Econometrica.
3. Count the number of times that the word effect (or its relatives like “impact”) appears.
4. Count the number of times that the word predict (or its relatives like prediction, predicting,predicted etc) appears.
  * NLTK root words?
5. Count the number of times that the word forecast appears (or its relatives like forecasting) appears.
6. Tally these counts by journal and by year (in excel)
7. Tally the number of articles for which we checked (so we have a denominator)
8. ~~Make `.gitignore`.~~
9. Do this for abstracts.
10. Do this for full articles?

