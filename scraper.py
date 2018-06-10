import requests
import sys
from bs4 import BeautifulSoup

def get_result (usn): 
    url_form = "http://results.rvce.edu.in/" #Login Page URL 
    url_result = "http://results.rvce.edu.in/viewresult2.php" #Results Display page url that accepts the post request
    session = requests.session()
    page = session.get(url_form)
    soup = BeautifulSoup(page.text, 'html.parser') #converts raw html to a structured bs4 object 
    captcha = soup.find_all('label')[1].get_text() 
    answer = int(captcha[8]) + int (captcha[12]) #solves captcha on login page
    creds = {'usn' : usn, 'captcha' : answer}
    response = session.post(url_result, data = creds)
    result_soup = BeautifulSoup(response.text, 'html.parser') #converts raw html of results page to bs4 object
    flag = result_soup.find('table') #validation results that do not exist 
    msg = flag.find_all('td')[1].text
    if msg == "Result Not Found":
        return "400"
    name = result_soup.find('td', attrs={ 'data-title': 'NAME' }) #structures the results table 
    sgpa = result_soup.find('td', attrs={ 'data-title': 'SGPA' })
    grades = (result_soup.find_all('tbody')[1]).find_all('tr')
    subject_grades = ""
    grd = {}
    for grade in grades:
        course = grade.find('td', attrs={ 'data-title': 'COURSE NAME'})
        gr = grade.find('td', attrs={ 'data-title': 'GRADE'})
        if course is not None
            grd[course.text] = gr.text
    res = {"usn" : usn , "name" : name.text, "sgpa" : sgpa.text ,"grades" : grd}     
    return res







