Scraper acting unexpectedly for different timeranges passed
### Description
I came across something very off with scraper when using it to scrape files that only have a `%Y` in the pattern of interest.

For example, I'm currently looking at scraping files from this pattern, and it works fine for this timerange.

```python

>>> file_pattern_ngdc = ("https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/goes-xrs-report_%Y.txt")
>>> file_scraper_ngdc = scraper.Scraper(file_pattern_ngdc)


>>> trange = TimeRange("2013-01-01", "2013-12-31")
>>> file_scraper_ngdc.filelist(trange)
['https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/goes-xrs-report_2013.txt']
```
But like if I slightly change the date (it shouldn't matter right - its should only look at 2013?) this returns nothing, whereas it should return the same file.
```python
>>> trange = TimeRange("2013-05-01", "2013-12-31")
>>> file_scraper_ngdc.filelist(trange)
[]

```
am I going mad? I think this is a bug withing scraper



again more of a need for #4888
