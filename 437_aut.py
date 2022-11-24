import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup


def aut():
    url = "https://www.aut.ac.nz/study/study-options/engineering-computer-and-mathematical-sciences/academic-staff/information-technology-and-software-engineering-department"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    #print(soup.prettify())

    # file initialization to write
    filename = "aut.txt"
    f = open(filename, "w")

    excel_filename = "aut.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "aut"
    country = "NZ"

    garbage_emails = []
    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all profs on the dept homepage
    #d = soup.find('a')
    #print(d)
    dd=soup.find_all('a')
    #print(dd)
    # count = 0 
    # iterating for every prof
    for i in dd:
        #a = i.find('a')                     # a contains the name and the homepage of prof
        #print(a)
        if i.get('href') == None:
            continue
        link =  i.get('href')                # extracting prof page link
        #print(link)
        name = i.get_text()                 # extracting prof name
        #print(name)
        try:
            prof_resp = requests.get(link)      # requesting prof homepgae
        except:
            continue

        email = "Not Found"
        # print(name, link)
        filterandgetEmail(var, garbage_emails, name, link, email, prof_resp)


    f.close()
    f2.close()
    f3.close()
    print("Finished")





def filterandgetEmail(var, garbage_emails, name, link, email, prof_resp):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    keyword_list = ['Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 
                'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded System','Computer Organization','VLSI', 'Computer and System',
                'Distributed System', 'distributed system', 'Distributed system' ]
    flag = 1
    prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
    research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern,research_text):
            flag = 0
            if email != 'Not Found':
                f.write(link + '\n' + name + "\t"+ email + "\n")
                csvwriter.writerow([u_name, country, name, email, link])
                csvwriter2.writerow([u_name, country, name, email, link])
            else:
                new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
                for eemail in garbage_emails:
                    if eemail in new_emails:
                        new_emails.remove(eemail)
                if len(new_emails) == 0:
                    email = "Email Not Found"
                    f.write(link + '\n' + name + "\t"+ email + "\n")
                    csvwriter.writerow([u_name, country, name, email, link])
                    csvwriter2.writerow([u_name, country, name, email, link])
                else:
                    # f.write(link + '\n' + name)
                    for email in new_emails:
                        f.write(link + '\n' + name + '\t\t' + email + '\n')
                        csvwriter.writerow([u_name, country, name, email, link])
                        csvwriter2.writerow([u_name, country, name, email, link])
                    # f.write("\n") 
 

            f.write(pattern)
            f.write('\n\n')
            break

if __name__ == '__main__':
    aut()
