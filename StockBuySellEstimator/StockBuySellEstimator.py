# -*- coding: utf-8 -*-
import spacy
import re
from re import sub

# Program Name: Stock Buy/Sell Estimator
# Coder: Haris
# Date: Dec 2th, 2022

# Customer class
class Customer:
	def __init__(self):
		self.customerEmail = ""
		self.customerInvestments = {}

# Function Name: processString
# Purpose: uses the 're' sub library to remove all random characters from the text file and return an
# array of string based on '<<End>>' portion of the text
def processString(docTextString):
	line = re.sub("'", "’", docTextString)
	return line.split("<<End>>")

# Function Name: processMoney
# Purpose: determine whether if used a word version of a money number from the text file
def processMoney(docTextMoney):
	numberDictionary = {
		"zero": 0,
		"one": 1,
		"two": 2,
		"three": 3,
		"four": 4,
		"five": 5,
		"six": 6,
		"seven": 7,
		"eight": 8,
		"nine": 9,
		"ten": 10,
		"eleven": 11,
		"twelve": 12,
		"thirteen": 13,
		"fourteen": 14,
		"fifteen": 15,
		"sixteen": 16,
		"seventeen": 17,
		"eighteen": 18,
		"nineteen": 19,
		"twenty" : 20,
		"thirty": 30,
		"fourty": 40,
		"fifty": 50,
		"sixty": 60,
		"seventy": 70,
		"eighty": 80,
		"ninety": 90,
		"hundred": 100,
		"thousand": 1000,
		"million": 1000000,
		"billion": 1000000000
		}
	if " " in docTextMoney:
		currencyNo = 1.0
		numberArr = docTextMoney.split()
		for numberString in numberArr:
			if numberString in numberDictionary:
				currencyNo *= numberDictionary[numberString]
			elif any(chr.isdigit() for chr in numberString):
				currencyNo *= float(sub(r'[^\d.]', '', numberString))
		return currencyNo
	else:
		return float(sub(r'[^\d.]', '', docTextMoney))

## Read the text file and process the strings
nlp = spacy.load('en_core_web_sm')
textFile = open('EmailLog.txt', mode='r', encoding='utf-8').read()
emails = processString(textFile)

customersList = []
for email in emails:
	if email != "\n":
		doc = nlp(email)
		currentCustomer = Customer()
		for token in doc:
			if(token.like_email):
				currentCustomer.customerEmail = token.text

		money = ""
		company = ""
		for ent in doc.ents:
			if ent.label_ == "ORG":
				company = ent.text
				currentCustomer.customerInvestments[company] = money
			elif ent.label_ == "MONEY":
				money = processMoney(ent.text)
		customersList.append(currentCustomer)
		
## Write and save spaCy parsed output to a text file
f = open('output.txt', mode='wt')

totalRequests = 0.0
for customer in customersList:
	customerInfo = customer.customerEmail + ": "
	isFirstInvestment = True
	counter = 1
	for investment in customer.customerInvestments:
		totalRequests += customer.customerInvestments[investment]
		if isFirstInvestment == True:
			customerInfo += '${:,.0f}'.format(customer.customerInvestments[investment]) + " to " + investment
			isFirstInvestment = False
			if counter == len(customer.customerInvestments):
				f.write(customerInfo + "\n")
			counter += 1
			
		elif counter < len(customer.customerInvestments):
			customerInfo += ", " + '${:,.0f}'.format(customer.customerInvestments[investment]) + " to " + investment
			counter += 1
		else:
			customerInfo += " and " + '${:,.0f}'.format(customer.customerInvestments[investment]) + " to " + investment + "\n"
			f.write(customerInfo)

totalLine = "\nTotal Requests: " + '${:,.2f}'.format(totalRequests)
f.write(totalLine)
f.close()

# read spaCy parsed output from a text file and display the contents onto the console
print("-------------------------------------------------")
print("|                  Project 2                    |")
print("-------------------------------------------------")
f = open('output.txt', mode='r')
for line in f:
	line = line.strip('\n')
	print(line)

f.close()

