import time
import math
import json
import requests

from selenium import webdriver

url = "http://localhost:8080"
headers = {
    'Content-Type': 'application/json',
}
driver = webdriver.Chrome(executable_path="chromedriver.exe")

def Add_Singlerecord(natid):
    payload = "{ \"birthday\": \"01011960\", \"gender\": \"m\", \"name\": \"test1\", \"natid\": \"" + natid + "\", \"salary\": \""+str(salary)+"\", \"tax\": \""+str(tax)+"\"}"
    response = requests.request("POST", url + "/calculator/insert", headers=headers, data=payload)
    return response

def Multiplerecord(natid1,natid2,natid3,natid4,natid5):
    payload = "[{\"birthday\": \"01011961\", \"gender\": \"m\", \"name\": \"test2\", \"natid\": \"" + natid1 + "\", \"salary\": \"3000\", \"tax\": \"2950\"},{\"birthday\": \"01011962\", \"gender\": \"f\", \"name\": \"test3\", \"natid\": \"" + natid2 + "\", \"salary\": \"7000\", \"tax\": \"100\"},{\"birthday\": \"01011961\", \"gender\": \"m\", \"name\": \"test2\", \"natid\": \"" + natid3 + "\", \"salary\": \"6000\", \"tax\": \"100\"},{\"birthday\": \"01011961\", \"gender\": \"m\", \"name\": \"test2\", \"natid\": \"" + natid4 + "\", \"salary\": \"6000\", \"tax\": \"100\"},{\"birthday\": \"01011961\", \"gender\": \"m\", \"name\": \"test2\", \"natid\": \"" + natid5 + "\", \"salary\": \"6000\", \"tax\": \"100\"}]"
    response = requests.request("POST", url + "/calculator/insertMultiple", headers=headers, data=payload)
    return response

driver.get('http://localhost:8080')
driver.maximize_window()

SCROLL_PAUSE_TIME =0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

natid = "S1234566D"
salary = 5107
tax = 100
print("Add Single record:")
# insert success case
resp = Add_Singlerecord(natid)
time.sleep(2)
Clk_RefreshTaxReliefTable = driver.find_element_by_css_selector('#contents > button.btn.btn-primary')
Clk_RefreshTaxReliefTable.click()
if resp.status_code == 202:
    print("Testpass- Single record inserted successfully")
else:
    print("TestFail- Single record not inserted")
time.sleep(2)
print("\n")
print("Retrieve tax relief Check:")
getTaxRelief_resp =requests.get( url + "/calculator/taxRelief")
TaxRelief= json.loads(getTaxRelief_resp.text)[0]['relief']
print("Retrieve tax relief from database: "+str(TaxRelief))
Calculate_TaxRelief = (salary-tax)*0.367;
print ("Before truncate : " + str(Calculate_TaxRelief))
truncateval = math.trunc(Calculate_TaxRelief*100)/100
print ("After truncate : " + str(truncateval))

round_val=math.ceil(truncateval)
print ("After Round : " + str(round_val))

if TaxRelief==round_val:
    print ("TaxRelief Amount Round value is correct")
else:
    print ("TaxRelief Amount Round value is not correct. Expected value: "+str(round_val)+", But Actual value is: "+str(TaxRelief))
if TaxRelief==truncateval:
    print ("TaxRelief Amount Truncate value is correct")
else:
    print ("TaxRelief Amount Truncate value is not correct. Expected value: "+str(truncateval)+", But Actual value is: "+str(TaxRelief))
time.sleep(2)
print("\n")
print("Check Natid MASKED FROM 5TH CHARACTER ONWARDS :")
# Check NATID IS MASK
natid_mask="S123$$t$$"
singlerecord_natidmask_chk= json.loads(getTaxRelief_resp.text)[0]['natid']

i=4
strcheck="T"
while i < (len(singlerecord_natidmask_chk)-1):
    if singlerecord_natidmask_chk[i]!="$":
        strcheck="F"
        break
    i+=1

if strcheck=="T":
    print ("This natid id masked successfully with $ sign from 5th character")
else:
    print ("This natid id mask is incorrect")

Clk_RefreshTaxReliefTable = driver.find_element_by_css_selector('#contents > button.btn.btn-primary')
Clk_RefreshTaxReliefTable.click()
time.sleep(2)
print("\n")
print("Check Single duplicate Insert:")
# Check duplicate record
resp = Add_Singlerecord(natid)
if resp.status_code == 202:
    print("Error: TestFail-Allowing to insert same natid")
time.sleep(2)
print("\n")
#iNSERT mULTIPLE RECORD
print("Add Multiple records:")
AddMultiplerecord =['S1234567A','S2234567B','S3334567C','S4434567D','S5534567E']
resp=Multiplerecord(AddMultiplerecord[0],AddMultiplerecord[1],AddMultiplerecord[2],AddMultiplerecord[3],AddMultiplerecord[4])
if resp.status_code == 202:
    print("Testpass- Multiple record inserted successfully")
else:
    print("TestFail- Multiple record not inserted")
time.sleep(2)
Clk_RefreshTaxReliefTable = driver.find_element_by_css_selector('#contents > button.btn.btn-primary')
Clk_RefreshTaxReliefTable.click()
time.sleep(2)
print("\n")
#AC5- tax relief amout is more than 0.00 but less than 50.00, the final tax relief amount should be 50.00 check
print("tax relief amout is more than 0.00 but less than 50.00 check:")
getTaxRelief_resp =requests.get( url + "/calculator/taxRelief")
TaxRelief= json.loads(getTaxRelief_resp.text)[2]['relief']
if TaxRelief == "50.00":
    print("TestPass - The final tax relief amount is 50.00")
else:
    print("Test Fail-  Tax Relief amount should be 50.00.")

#UPLOAD CSV CHECK
print("Upload Csv with 5 records:")
time.sleep(5)
uploadcsv=driver.find_element_by_css_selector("#contents > div.input-group.mb-3 > div.custom-file > input")
uploadcsv.send_keys("new_hero3.csv")
Clk_RefreshTaxReliefTable = driver.find_element_by_css_selector('#contents > button.btn.btn-primary')
Clk_RefreshTaxReliefTable.click()
time.sleep(5)
print("Uploaded csv file with 5 records successfully")
print("\n")
#DISPENSE NOW TEST

Dispense_title="Dispense!!"
print("Dispense Tax relief:")
time.sleep(2)
Clk_DispenseNow = driver.find_element_by_css_selector('#contents > a.btn.btn-danger.btn-block')
Clk_DispenseNow.click()
getdispense_pagetitle = driver.title

if getdispense_pagetitle ==Dispense_title:
    print("Test pass: Cash Dispensed")
else:
    print("Test Fail: Cash is not dispensed ")
time.sleep(5)
driver.close()
