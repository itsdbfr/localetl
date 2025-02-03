#Amazon Review Scraping, Transformation and Loading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#Uncomment these if you do not have them downloaded

# nltk.download('punkt')
# nltk.download('stopwords')

import random
import time

import pandas as pd
import openpyxl


options = webdriver.ChromeOptions()

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

randomNumber = random.randint(1, 4)

#Enter your url here
url = ("https://www.amazon.com/SPANX-Seamless-Higher-Power-Shorty/product-reviews/B0CYV8NRQ2/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1")

driver.get(url)
time.sleep(randomNumber)

username = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div[2]/div[1]/form/div/div/div/div[1]/input[1]')
continueButton = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div[2]/div[1]/form/div/div/div/div[2]/span/span/input')

# Enter your username and password here
userid = 'username'
passkey = 'password'

username.send_keys(userid)
driver.execute_script("arguments[0].click();", continueButton)

time.sleep(randomNumber)

password = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div/form/div/div[1]/input')
signInButton = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div/form/div/div[2]/span/span/input')

time.sleep(randomNumber)


password.send_keys(passkey)
driver.execute_script("arguments[0].click();", signInButton)

productReviews = []
i = 1

#Make the limit for i the number of pages you want to take reviews from
reviewPages = 1
while i <= reviewPages:
    time.sleep(randomNumber)
    
    x = 0
    while x <= 10:
        
        productReviewElements = driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/ul[1]/li[" + str(x + 1) + "]/span/div/div/div[4]/span/span")
        
        for productReview in productReviewElements:
            productReviews.append(productReview.text)
            print(productReview.text)
            
        x+=1

    time.sleep(randomNumber)

    if i != 1:
        driver.execute_script("window.scrollTo(5, document.body.scrollHeight);")
        nextPageButton = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div/span/div/ul/li[2]/a')
        
        
        
        driver.execute_script("arguments[0].click();", nextPageButton)
    else:
        print("You're done scraping this product.")
    i += 1
    
driver.quit()
    
#This section removes stop words and organizes terms used in the review by frequency of appearance

allWords = ''.join(productReviews)
    
tokens = nltk.word_tokenize(allWords)

stopWords = stopwords.words('english')

wordsLowerCase = [w.lower() for w in tokens]
wordsNoPunctuation = [w for w in wordsLowerCase if w.isalpha()]
wordsNoStopWords = [w for w in wordsNoPunctuation if w not in stopWords]

frequency = FreqDist(wordsNoStopWords)
sortedFrequency = sorted(frequency.items(),key = lambda k:k[1], reverse = True)

wordFrequencyDf = pd.DataFrame(sortedFrequency, columns = ['Keyword','Frequency'])
#Enter the location where you wish to save the excel here
frequencyDataLocation = '/Users/example/Desktop/wordFrequencyOutput.xlsx'
wordFrequencyDf.to_excel(frequencyDataLocation)
print('Word Frequency Data Save Completed')

#This section scores each review in terms of the sentiments expressed (neutral, negative, positive) and gives it an overall score

sentimentAnalyzer = SentimentIntensityAnalyzer()

reviewSentiment = []

for review in productReviews:
    sentimentScore = sentimentAnalyzer.polarity_scores(review)
    review = review.replace('\\n', '')
    row = [review, sentimentScore['compound'], sentimentScore['neg'], sentimentScore['neu'], sentimentScore['pos']]
    reviewSentiment.append(row)

sentimentDf = pd.DataFrame(reviewSentiment, columns = ['Review Content','Overall Score','Negative Score','Neutral Score','Positive Score'])
#Enter the location where you wish to save the excel here
sentimentDfLocation = '/Users/example/Desktop/sentimentScoreOutput.xlsx'
sentimentDf.to_excel(sentimentDfLocation)
print('Sentiment Data Save Completed')





    


    
    

    


