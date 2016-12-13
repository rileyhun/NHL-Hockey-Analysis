import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
binary = FirefoxBinary(r'C:\Users\RHun\Desktop\Tor Browser\Browser\firefox.exe')
profile = FirefoxProfile(r'C:\Users\RHun\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default')


def NHL_Teamstats_miner():

    url = 'http://www.nhl.com/stats/team?aggregate=0&gameType=2&report=teamsummary&reportType=season&seasonFrom=20002001' \
          '&seasonTo=20152016&filter=gamesPlayed,gte,1&sort=wins,points'

    browser = webdriver.Chrome()
    browser.get(url)

    hockey_stats = []
    max_pages = Select(browser.find_element_by_css_selector("select[class*='pager-select']"))
    max_pages = len(max_pages.options)

    for page in [i for i in range(1, max_pages+1)]:

                wait = WebDriverWait(browser, 10)

                Page_Options = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "select[class*='pager-select']")))
                Select(Page_Options).select_by_visible_text(str(page))

                html = browser.page_source
                soup = BeautifulSoup(html)
                table = soup.find('table', {'class': "stat-table"})
                rows = table.findAll('tr')

                for row in rows[1:-1]:
                      cols = row.findAll('td')
                      cols = [ele.text for ele in cols]
                      hockey_stats.append([ele for ele in cols if ele])

    df = pd.DataFrame(hockey_stats)
    del df[0]
    print(df)


    df.to_csv("NHL_Hockey_Team_Data (2000-2001 to 2015-2016 REGULAR).csv", index=False, header=
                        ["Team", "Season", "GP", "W", "L", "T", "OT", "P", "ROW", "P%", "GF", "GA", "S/O Wins",
                        "GF/GP", "GA/GP", "PP%", "PK%", "Shots/GP", "SA/GP", "FOW%"])

def NHL_Playerstats_miner():

    url = 'http://www.nhl.com/stats/player?aggregate=0&gameType=2&report=skatersummary&pos=S&reportType=season&season' \
          'From=20002001&seasonTo=20152016&filter=gamesPlayed,gte,1&sort=points,goals,assists'

    browser = webdriver.Firefox()
    browser.get(url)

    hockey_stats = []
    max_pages = Select(browser.find_element_by_css_selector("select[class*='pager-select']"))
    max_pages = len(max_pages.options)

    for page in [i for i in range(1, max_pages+1)]:

                wait = WebDriverWait(browser, 10)

                Page_Options = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "select[class*='pager-select']")))
                Select(Page_Options).select_by_visible_text(str(page))

                html = browser.page_source
                soup = BeautifulSoup(html)
                table = soup.find('table', {'class': "stat-table"})
                rows = table.findAll('tr')

                for row in rows[1:-1]:
                      cols = row.findAll('td')
                      cols = [ele.text for ele in cols]
                      hockey_stats.append([ele for ele in cols if ele])

    df = pd.DataFrame(hockey_stats)
    del df[0]
    print(df)


    df.to_csv("NHL_Hockey_Player_Data (1999-2000 to 2015-2016 REGULAR).csv", index=False, header=
                        ["Player", "Season", "Team", "Pos", "GP", "G", "A", "P", "+/-", "PIM", "P/GP", "PPG",
                         "PPP", "SHG", "SHP", "GWG", "OTG", "S", "S%", "TOI/GP", "Shifts/GP", "FOW%"])

def Team_stats2():

    hockey_stats = []

    browser = webdriver.Firefox()
    browser.get('http://www.hockey-reference.com/leagues/NHL_2016.html')

    for i in range(7):

        html = browser.page_source
        soup = BeautifulSoup(html)
        table = soup.find('table', {'id': "stats"})
        rows = table.findAll('tr')

        for row in rows[2:-1]:
              cols = row.findAll('td')
              cols = [ele.text for ele in cols]
              hockey_stats.append([ele for ele in cols if ele])

        browser.find_element_by_css_selector("a[class*='button2 prev']").click()

        year = 2016
        df = pd.DataFrame(hockey_stats)
        df['year'] = year - i
        df.to_csv("NHL_Hockey_Team_Stats (2010 to 2016).csv", mode='a', index=False, header=False)

def Find_Player_Stats_HR():

    url = 'http://www.hockey-reference.com/players/'

    browser = webdriver.Firefox()
    browser.get(url)

    index_of_letters = list('ayz')

    for page in index_of_letters:

                wait = WebDriverWait(browser, 10)

                browser.get('http://www.hockey-reference.com/players/' + str(page) + '/')

                browser.implicitly_wait(3)

                Toggle_off_nonnhl = wait.until(EC.visibility_of_element_located((
                    By.CSS_SELECTOR, "span[id*='all_players_toggle_non_nhl']")))
                Toggle_off_nonnhl.click()

                html = browser.page_source
                soup = BeautifulSoup(html)
                soup_to_string = str(soup)
                soup_to_string = soup_to_string.split('<div id="footer"')[0]

                links_on_page = re.findall('<a href="/players/'+str(page)+'/.*\.html.*</a>', soup_to_string)
                links_on_page = [x.split('<a href="')[1].split('">')[0] for x in links_on_page][5:-2]

                player_attributes = []

                for i in links_on_page:
                    browser.implicitly_wait(3)
                    browser.get('http://www.hockey-reference.com' + i)
                    html = browser.page_source
                    soup = BeautifulSoup(html)
                    soup_string = str(soup).split('itemtype="http://schema.org/Person">')[1]

                    Name = soup_string.split('itemprop="name">')[1].split('</h1>')[0].strip(" ")
                    if '<strong>Position</strong>' not in soup_string:
                        Position ="NA"
                    else: Position = soup_string.split('<strong>Position</strong>: ')[1].split(" ")[0].strip(" ")
                    if '<span data-birth' not in soup_string:
                        Birth_Date = "NA"
                    else:
                        Birth_Date = soup_string.split('<span data-birth="')[1].split('"')[0].strip(" ")

                    if '<span itemprop="height">' not in soup_string:
                        Height = "NA"
                    else:
                        Height = soup_string.split('<span itemprop="height">')[1].split("</span>")[0].strip(" ") + " ft"

                    if '<span itemprop="weight">' not in soup_string:
                        Weight = "NA"
                    else:
                        Weight = soup_string.split('<span itemprop="weight">')[1].split("</span>")[0].strip(" ")

                    attr_data = [Name, Position, Birth_Date, Height, Weight]
                    player_attributes.append(attr_data)
                    print(player_attributes)


                df = pd.DataFrame(player_attributes)
                df.to_csv('player_attributes-2.csv', header= ['Name', 'Position', 'Birth_Date', 'Height', 'Weight'],
                            mode='a', index=False)

                browser.get('http://www.hockey-reference.com/players/')


def Find_Player_Stats_DB():

    url = 'http://www.hockeydb.com/ihdb/players/player_let.html'

    browser = webdriver.Firefox()
    browser.get(url)

    index_of_letters = list('bcdefghijklmnopqrstuvwxyz')
    for page in index_of_letters:

                wait = WebDriverWait(browser, 10)

                Page_Options = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href*='player_ind_"
                                                                            + str(page)+".html']")))
                Page_Options.click()

                html = browser.page_source
                soup = BeautifulSoup(html)
                soup_to_string = str(soup)

                links_on_page = re.findall('<a href="/ihdb/stats/pdisplay.php\?pid=.*</a>', soup_to_string)
                links_on_page = [x.split('<a href="')[1].split('">')[0] for x in links_on_page]

                player_attributes = []

                for i in links_on_page:

                    browser.get('http://www.hockeydb.com' + i)
                    html = browser.page_source
                    soup = BeautifulSoup(html)

                    Name = str(soup).split('itemprop="name">')[1].split('</h1>')[0].strip(" ")
                    if '<div class="v1-1">' not in str(soup):
                        Position ="NA"
                    else: Position = str(soup).split('<div class="v1-1">')[1].split(" ")[0].strip("\n")
                    if 'Born' not in str(soup):
                        Birth_Date = "NA"
                    else:
                        Birth_Date = str(soup).split('Born')[1].split('--')[0].strip(" ")

                    if 'Height' not in str(soup):
                        Height = "NA"
                    else:
                        Height = str(soup).split('Height')[1].split("--")[0].strip(" ")

                    if "Weight" not in str(soup):
                        Weight = "NA"
                    else:
                        Weight = str(soup).split("Weight")[1].split("<")[0].strip(" ")

                    attr_data = [Name, Position, Birth_Date, Height, Weight]
                    player_attributes.append(attr_data)


                    browser.quit()

                df = pd.DataFrame(player_attributes)
                df.to_csv('player_attributes.csv', header= ['Name', 'Position', 'Birth_Date', 'Height', 'Weight'],
                            mode='a', index=False)

Find_Player_Stats_HR()