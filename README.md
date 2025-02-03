This Python script scrapes review text of a specified product listed on Amazon. Using NLTK, the script measures word frequency and sentiment scores, outputting two separate xlsx files. I designed this with the intention of 
emulating an ETL solution. As I do not have a database to upload to or extract data from, I've used my discretion to find alternatives. 

Things to note:

1. Amazon updates HTML tags frequently. HTML tags may not be consistent from one URL to another. As such, you may enocunter a "NoSuchElementException".
   Inspect the element on the webpage, copy the full XPATH and update the script accordingly.

2. Uncomment the following if you do not have them downloaded:
   # nltk.download('punkt')
   # nltk.download('stopwords')

3. Remember to enter the URL you wish to scrape reviews from and your Amazon username and password.
   
4. Set the number of pages you want to scrape review text from. 
