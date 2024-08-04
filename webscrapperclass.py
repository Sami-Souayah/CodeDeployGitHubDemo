from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import csv


class webscraper():
        def __init__(self, req, filename, state, date1, date2):
              self.req = req
              self.req = req.upper()
              self.filename = filename
              self.state = state
              self.date1 = date1
              self.date2 = date2
              self.completion=False
              self.divisor = 0
        
              chromeoptions = Options()
              chromeoptions.add_argument("--headless")
                
              self.driver = webdriver.Chrome(options=chromeoptions)

              self.driver.get("https://wonder.cdc.gov/vaers.html")

              self.driver.implicitly_wait(10)

              button1F = self.driver.find_element(by=By.XPATH, value="//*[@id='closeBtn']")
              self.driver.execute_script("arguments[0].click();", button1F)

              test = self.driver.find_element(by=By.XPATH, value="//*[@id='vaers-buttons2']/input")
              self.driver.execute_script("arguments[0].click();", test)
              
              if self.req:
                      print("VAC HIT")
                      self.selectorvac()
              if self.state:
                     print("STATE HIT")
                     self.selectorstate()
              if self.date1:
                      print("DATE HIT")
                      self.selectordate()
              self.searcher()


                
                
        

        def searcher(self):
                if ".csv" not in self.filename:
                    self.filename+=".csv"
                with open (self.filename, 'w', newline='') as file:
                                writer = csv.writer(file)
                                send = self.driver.find_element(by=By.XPATH, value="//*[@id='wonderform']/table/tbody/tr/td/div[3]/input[1]")
                                self.driver.execute_script("arguments[0].click();", send)

                                results2 = self.driver.find_element(by=By.XPATH, value="//*[@id='wonderform']/table/tbody/tr/td/div[3]/div/table[3]/tbody")
                                results3 = results2.find_elements(by=By.TAG_NAME, value="tr")


                                statename = self.driver.find_element(by=By.XPATH, value="//*[@id='wonderform']/table/tbody/tr/td/div[3]/div/table[9]/tbody/tr[3]/td")
                                vacname = self.driver.find_element(by=By.XPATH, value="//*[@id='wonderform']/table/tbody/tr/td/div[3]/div/table[9]/tbody/tr[4]/td")
                                writer.writerow(["Vaccine name:", vacname.text])
                                writer.writerow(["State name:", statename.text])
                                writer.writerow(["\n"])
                                writer.writerow(["Symptoms", " Number of events"])

                                self.divisor=len(results3)
                                print("Rows found:", self.divisor)
                                row=0
                                percent=0
                                for k in results3:
                                        row+=1
                                        name = k.find_element(by=By.TAG_NAME, value="th")
                                        elements = k.find_elements(by=By.TAG_NAME, value="td")
                                                                        
                                        for m in range(len(elements)):
                                                if m%2==0:
                                                    percent=(row/self.divisor)*100
                                                    percent = int(percent)
                                                    percent=str(percent)+"%"
                                                    print(percent,"completed. (Row", row, "done)")
                                                    writer.writerow([name.text, elements[m].text])
                                self.driver.back()
                                self.completion=True
                                closeall = self.driver.find_element(by=By.XPATH, value="//*[@id='finder-buttons-D8.V14']/input[3]")
                                self.driver.execute_script("arguments[0].click();", closeall)
                
                self.driver.quit()
        def accessor(self):
                if self.completion==True:
                        return True
                else:
                        return False
        def selectorvac(self):
                vaccine = self.driver.find_element(by=By.NAME, value="F_D8.V14")
                vaccine2 = vaccine.find_elements(by=By.TAG_NAME, value="option")
                select = Select(self.driver.find_element(by=By.XPATH, value="//*[@id='codes-D8.V14']"))

                count=0
                hit = False
                indxcount = 0
                for i in vaccine2:
                        if count==0:
                                select.deselect_by_index(0)
                        print("Comparing", self.req, "to", i.text)
                        if self.req in i.text:
                                select.select_by_index(indxcount)
                                count+=1
                                hit=True
                                if "All Vaccine" in i.text:
                                        break
                                if "UKNOWN VACCINES" in i.text:
                                        break
                        if "UNKNOWN VACCINES" in i.text and hit==False:
                                self.driver.close()
                                return False
                        indxcount+=1
        def selectorstate(self):
                state = self.driver.find_element(by=By.NAME, value="V_D8.V12")
                self.state2 = state.find_elements(by=By.TAG_NAME, value="option")
                select = Select(self.driver.find_element(by=By.XPATH, value="//*[@id='SD8.V12']"))

                count=0
                indxcount=0
                hit=False
                for i in self.state2:
                        if count==0:
                                select.deselect_by_index(1)
                        print("Comparing", self.state, "to", i.text)
                        if self.state in i.text:
                                select.select_by_index(indxcount)
                                count+=1
                                hit=True
                                if "All Location" in i.text:
                                        break
                                if "Unknown" in i.text and hit==False:
                                        self.driver.close()
                                        return False
                        indxcount+=1
        def selectordate(self):
                date = self.driver.find_element(by=By.NAME, value="F_D8.V3")
                date2 = date.find_elements(by=By.TAG_NAME, value="option")
                select = Select(self.driver.find_element(by=By.XPATH, value="//*[@id='codes-D8.V3']"))
                if int(self.date1) > int(self.date2):
                      return False
                if self.date1 == "" and self.date2=="":
                        self.result3 = "Invalid"
                        return
                self.result3 = ""
                count=0
                hit = False
                on = False
                indxcount = 0
                for i in date2:
                        if count==0:
                                select.deselect_by_index(0)
                        if hit!=True:
                                print(f"Comparing start date {self.date1} to {i.text}")
                        if hit==True and on==True:
                                print(f"Comparing end date {self.date2} to {i.text}. {i.text} selected")
                        if hit==True and on==False:
                                print(f"Comparing end date {self.date2} to {i.text}.")
                        if int(self.date2)<1980 and indxcount==1 and int(self.date1) < 1980:
                                print("WEIRD HIT")
                                return
                        if self.date1 in i.text:
                                select.select_by_index(indxcount)
                                count+=1
                                if self.date2!="":
                                        on=True
                                hit=True
                                if "All Dates" in i.text:
                                        break
                                if "Unknown Date" in i.text:
                                        break
                        if self.date2 in i.text:
                                select.select_by_index(indxcount)
                                count+=1
                                break
                        if on==True:
                                select.select_by_index(indxcount)
                                count+=1
                        if "Unknown Date" in i.text and hit==False:
                                self.driver.close()
                                return False

                        indxcount+=1
        def stategetter(self, inpt):

                self.result=""
                state2 = ["All Locations", "The United States/Territories/Unknown", "Alabama",
"Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", 
"Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
"Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", 
"North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
"Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "American Samoa", "Baker Island", 
"Federated States of Micronesia", "Guam", "Howland Island", "Jarvis Island", "Johnston Atoll", "Kingman Reef", "Marshall Islands", 
"Midway Islands", "Navassa Island", "Northern Mariana Islands", "Palmyra Atoll", "Puerto Rico", "Virgin Islands", "Wake Island", 
"Foreign", "Unknown"]
                for i in state2:
                        if inpt == "":
                                self.result=""
                                return
                        if inpt in i or inpt in i.lower():
                                self.result=i
                                return
                        if inpt == "NONE":
                                self.result=""
                                return
                self.result="Invalid"
        def dategetter(self, date1, date2):
                self.result3 = date1
                self.result4 = date2
                if date1=="" and date2=="":
                        self.result3 = ""
                        self.result4 = ""
                        return
                if len(date1)!= 4:
                        self.result3="Invalid start date"
                if len(date2)!=4:
                        self.result4 = "Invalid end date"
                if date2=="":
                        self.result4 = "Invalid end date"
                if date1=="":
                        self.result3 = "Invalid start date"
                if int(date1)>int(date2):
                        self.result3 = "Invalid start date"
                        self.result4 = "Invalid end date"
                if int(date1)>2024 or int(date2) > 2024:
                        self.result3 = "Invalid start date"
                        self.result4 = "Invalid end date"
                
               
        def accessor2(self):
                return self.result
        def accessor3(self):
                return self.result3
        def accessor4(self):
                return self.result4
        def accessor5(self):
                divisor = self.divisor
                return divisor
       