## Cook County Deeds

I was condo shopping in Chicago a couple of years ago and wanted to evaluate historic condo prices / trends before making an offer. Zillow Zestimates looked inconsistent and seemed to deteriorate in quality the more concentrated the location got. It was obvious from a few examples that price dynamics were very building-specific. It seemed Zillow was using stuff around the buildings instead of looking at the buildings in isolation. I was planning on living near the Loop so using Zillow Zestimates would not work.

Furthermore, price histories were available for individual properties on websites like Zillow and Redfin but the thought of manually aggregating all the price histories of a 200+ unit building made me cringe. Good thing we have public records!

This is just a python script that pulls data from http://cookrecorder.com/.

To use this script simply provide a range of property pins to get_pins_data, get your df, and take it from there!

### Get set up

- Set up an anaconda environment with environment.yml
- Requires chrome.
- Download latest version of chromedriver (or whichever version you require if not using the latest chrome) and put the .exe in your script directory.