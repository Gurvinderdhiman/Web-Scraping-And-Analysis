# Created By : Gurvinder Dhiman
# Created Date : 9 Feb - 14 Feb 2023

# Importing all required modules and packages

import re
from nltk.tokenize import RegexpTokenizer, sent_tokenize
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from textblob import TextBlob
import pyphen
import xlsxwriter



# Filepath locations in my local storage

positiveWordsFile = r"C:\Users\user\PycharmProjects\pythonProject2\Task Submission by 14th Feb\MasterDictionary\positive-words.txt"
negativeWordsFile = r"C:\Users\user\PycharmProjects\pythonProject2\Task Submission by 14th Feb\MasterDictionary\negative-words.txt"


# Importing the input file containing all the urls

df=pd.read_csv(r'C:\Users\user\PycharmProjects\pythonProject2\Task Submission by 14th Feb\Input.csv')[['URL_ID','URL']]
df=df.iloc[0:114]
df.drop('URL_ID',axis=1)

# Getting all the urls from our input file in a list form

li = [url for url in df['URL']]

with open(r'C:\Users\user\PycharmProjects\pythonProject2\Task Submission by 14th Feb\StopWords\StopWords_Auditor.txt' ,'r') as stop_words:
    stopWords = stop_words.read().lower()
stopWordList = stopWords.split('\n')
stopWordList[-1:] = []

# Functions used for getting variables

# Calculating the Positive Score

def positive_score(text):
    numPosWords = 0
    #print(text)
    rawToken = tokenizer(text)
    for word in rawToken:
        if word in positiveWordList:
            numPosWords += 1

    sumPos = numPosWords
    return sumPos

# Calculating the Negative score
def negative_score(text):
    numNegWords=0
    rawToken = tokenizer(text)
    for word in rawToken:
        if word in negativeWordList:
            numNegWords -=1
    sumNeg = numNegWords
    sumNeg = sumNeg * -1
    return sumNeg

# Calculating the Polarity Score

def polarity_score(positiveScore, negativeScore):
    pol_score = (positiveScore - negativeScore) / ((positiveScore + negativeScore) + 0.000001)
    return pol_score


# Calculating the Average length of a sentence

def average_sentence_length(text):
    sentence_list = sent_tokenize(text)
    tokens = tokenizer(text)
    totalWordCount = len(tokens)
    totalSentences = len(sentence_list)
    average_sent = 0
    if totalSentences != 0:
        average_sent = totalWordCount / totalSentences

    average_sent_length = average_sent

    return round(average_sent_length)


# Calculating the percentage of complex word

def percentage_complex_word(text):
    tokens = tokenizer(text)
    complexWord = 0
    complex_word_percentage = 0

    for word in tokens:
        vowels = 0
        if word.endswith(('es', 'ed')):
            pass
        else:
            for w in word:
                if (w == 'a' or w == 'e' or w == 'i' or w == 'o' or w == 'u'):
                    vowels += 1
            if (vowels > 2):
                complexWord += 1
    if len(tokens) != 0:
        complex_word_percentage = complexWord / len(tokens)

    return complex_word_percentage

# Calculating the Fog Index

def fog_index(averageSentenceLength, percentageComplexWord):
    fogIndex = 0.4 * (averageSentenceLength + percentageComplexWord)
    return fogIndex


# Counting the complex words

def complex_word_count(text):
    tokens = tokenizer(text)
    complexWord = 0

    for word in tokens:
        vowels = 0
        if word.endswith(('es', 'ed')):
            pass
        else:
            for w in word:
                if (w == 'a' or w == 'e' or w == 'i' or w == 'o' or w == 'u'):
                    vowels += 1
            if (vowels > 2):
                complexWord += 1
    return complexWord

#Counting the total words

def total_word_count(text):
    tokens = tokenizer(text)
    return len(tokens)

# Counting the average words per sentence

def avg_words_per_sentence(text):
    sentences = text.split(".")
    num_words = 0
    for sentence in sentences:
        words = sentence.split()
        num_words += len(words)
    avg = num_words / len(sentences)
    return avg

# Calculating the Subjectivity Score with the help of a pre-defined python package

def subjectivity_score(text):
    blob = TextBlob(text)
    return blob.sentiment.subjectivity

# Calculating the Syllables Per Word with the help of a pre-defined python package

dic = pyphen.Pyphen(lang='en_US')

def count_syllables(word):
    return len(dic.inserted(word).split('-'))

def avg_syllables_per_word(text):
    words = text.split()
    total_syllables = sum(count_syllables(word) for word in words)
    if(len(words) == 0):
        avg = 0
    else:
        avg = total_syllables / len(words)
    return avg


# Calculating the Average Length of Words

def avg_word_length(text):
    words = text.split()
    total_length = sum(len(word) for word in words)
    if (len(words) == 0):
        avg = 0
    else:
        avg = total_length / len(words)
    return avg

# Finding the personal pronouns

def find_personal_pronouns(text):
    personal_pronouns = re.findall(r"\b(I|me|you|he|him|she|her|it|we|us|they|them)\b", text, re.IGNORECASE)
    return personal_pronouns

# Creating a workbook

workbook = xlsxwriter.Workbook(r'C:\Users\user\PycharmProjects\pythonProject2\Task Submission by 14th Feb\Output Data Structure.xlsx')

# Adding a worksheet in a workbook

worksheet = workbook.add_worksheet()

# Initializing the row value by 0
row = 0
# Initializing the column value by 0
column = 0
# Initializing the particular column value by 37 as per the needs of task
i=37

# giving header name to every column in the workbook file
worksheet.write(row, column, "URL_ID")
column += 1
worksheet.write(row, column, "URL")
column += 1
worksheet.write(row, column, "POSITIVE SCORE")
column += 1
worksheet.write(row, column, "NEGATIVE SCORE")
column += 1
worksheet.write(row, column, "POLARITY SCORE")
column += 1
worksheet.write(row, column, "SUBJECTIVITY SCORE")
column += 1
worksheet.write(row, column, "AVG SENTENCE LENGTH")
column += 1
worksheet.write(row, column, "PERCENTAGE OF COMPLEX WORDS")
column += 1
worksheet.write(row, column, "FOG INDEX")
column += 1
worksheet.write(row, column, "AVG NUMBER OF WORDS PER SENTENCE")
column += 1
worksheet.write(row, column, "COMPLEX WORD COUNT")
column += 1
worksheet.write(row, column, "WORD COUNT")
column += 1
worksheet.write(row, column, 'SYLLABLE PER WORD')
column += 1
worksheet.write(row, column, "PERSONAL PRONOUNS")
column += 1
worksheet.write(row, column, "AVG WORD LENGTH")

# Incrementing the row value by 1
row += 1

# For loop which runs on all the urls stored in a list named (li)

for url in li:
    column = 0
    page = requests.get(url)
    content = requests.get(url).content

    soup = bs(page.content,'html.parser')
    title = soup.find('h1', class_='entry-title')   # Extracting only the title part

    soup = bs(page.content, 'html.parser')
    desc = soup.find('div', class_='td-post-content') # Extracting only the article text part

    # Condition handling the null values

    if title is None and desc is None:
        text = ""
    else:
        text = title.text + ' ' + desc.text

    # Tokenizer (tokenizing all the text)

    def tokenizer(text):
        text = text.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        filtered_words = list(filter(lambda token: token not in stopWordList, tokens))
        return filtered_words

    # getting the positive words

    with open(positiveWordsFile,'r') as posfile:
        positivewords=posfile.read().lower()
    positiveWordList=positivewords.split('\n')

    # getting the negative words

    with open(negativeWordsFile ,'r') as negfile:
        negativeword=negfile.read().lower()
    negativeWordList=negativeword.split('\n')

    # getting all variables

    positiveScore = positive_score(text)
    negativeScore = negative_score(text)
    averageSentenceLength = average_sentence_length(text)
    percentageComplexWord = percentage_complex_word(text)
    polarityScore = polarity_score(positiveScore, negativeScore)
    fogIndex = fog_index(averageSentenceLength, percentageComplexWord)
    complexWordCount = complex_word_count(text)
    totalWordCount = total_word_count(text)
    avgWordsPerSentence = avg_words_per_sentence(text)
    subjectivityScore = subjectivity_score(text)
    syllablesPerWord = avg_syllables_per_word(text)
    avgWordLength = avg_word_length(text)
    findPersonalPronouns = find_personal_pronouns(text)


    # writing the values in the workbook file

    worksheet.write(row, column, i)
    column += 1
    worksheet.write(row, column, url)
    column += 1
    worksheet.write(row, column, positiveScore)
    column += 1
    worksheet.write(row, column, negativeScore)
    column += 1
    worksheet.write(row, column, polarityScore)
    column += 1
    worksheet.write(row, column, subjectivityScore)
    column += 1
    worksheet.write(row, column, averageSentenceLength)
    column += 1
    worksheet.write(row, column, percentageComplexWord)
    column += 1
    worksheet.write(row, column, fogIndex)
    column += 1
    worksheet.write(row, column, avgWordsPerSentence)
    column += 1
    worksheet.write(row, column, complexWordCount)
    column += 1
    worksheet.write(row, column, totalWordCount)
    column += 1
    worksheet.write(row, column, syllablesPerWord)
    column += 1
    worksheet.write(row, column,str(findPersonalPronouns))
    column += 1
    worksheet.write(row, column, avgWordLength)
    column += 1
    row += 1
    i += 1

# Closing the workbook file after inserting all the values
workbook.close()