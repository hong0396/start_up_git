import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast
from functools import reduce

# https://www.nasdaq.com/screening/company-list.aspx
def get_code():
	nasdaq=pd.read_csv("https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download")
	nyse=pd.read_csv("https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download")
	amex=pd.read_csv("https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download")
	code=nasdaq.append(nyse,ignore_index =True).append(amex,ignore_index =True)
	code.rename(columns={"Symbol":"code","IPOyear":"year"}, inplace =True)
	return code
get_code()	



