from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import pathlib
import requests
import re

#### Set up the initial connection
url = 'https://randomwalksbooth.org'
driver = webdriver.Safari()
driver.get(url)
headers = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

#### Go through each location and add to Raw Data
locations = driver.find_elements('tag name', 'a')
raw_data_frame = pd.DataFrame(columns= ['rw_destination','rw_destination2' ,'email', 'hometown', 'undergrad_college'
                                        , 'undergrad_major', 'work_experience', 'booth_concentrations'
                                        , 'random_walk_1y', 'hobbies', 'fun_facts'])


for index, location in enumerate(locations):
    link = location.get_attribute('href')
    # exclude the email address + top-line links + family RW page
    if 'private' not in link:
        continue
    # clean up the link to extract the location
    clean_location = (re.findall(r'int\-(.+?)\.htm',link) or re.findall(r'dom\-(.+?)\.htm',link))[0]
    # click on the link and get the HTML of that page
    driver.get(link)
    result = requests.get(link, headers= headers).text
    # scrape the relevant data - the second table on the page has the trip leader data
    # within that table all after the first row contain data about a particular leader
    soup = BeautifulSoup(result, features= 'html.parser')
    trip_leader_overall = soup.findChildren('table')[1]
    each_leader_info = trip_leader_overall.findChildren('tr')[1:]
    # go through each leader and export details (stored in p)
    for row in each_leader_info:
        temp = [location, clean_location]
        cells = row.findChildren('p')
        for cell in cells:
            value = cell.string
            if value is None:
                continue
            else:
                temp.append(value)
        # add final data to dataframe
        # for initial version, skip leaders who don't have complete data
        try:
            raw_data_frame.loc[raw_data_frame.shape[0]] = temp
        except ValueError:
            print('skipping leader, missing information from: ' + clean_location)
    driver.back()

driver.quit()


# Manually add in rows for the leaders with missing information
raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                               'PuertoRicoCouples', 
                                               'E-mail: julieannemorand@gmail.com', 
                                               'Hometown: Windsor, Canada', 
                                               'Undergrad College: University  of Waterloo', 
                                               'Undergrad Major: Environment  and Business', 
                                               'Work Experience: Public Company/Financial Institutions Insurance Examiner', 
                                               'Booth Concentrations: None',
                                               '2022 Random Walk: Croatia (with Ravi)', 
                                               'Hobbies: Cooking, working out, hosting  parties, going to sports games, podcasts', 
                                               'Fun Facts: I am learning French and am always looking for people to practice  with! ']


raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                               'PuertoRicoCouples', 
                                               'E-mail:  anor@chicagobooth.edu', 
                                               'Hometown:  Moscow,  Russia', 
                                               'Undergrad  College: Russian  State University of oil and gas'
                                               , 'Undergrad  Major: Chemical  Engineering'
                                               , 'Work  Experience: AgTech'
                                               , 'Booth Concentrations: None'
                                               , '2022  Random Walk: Iceland'
                                               , 'Hobbies:  Running/hiking/gym;  coffee making; cooking (currently - Ramsay’s Masterclass) '
                                               , 'Fun  Facts:  haven’t  had a permanent home for 12 months while traveling across the US before Booth']

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                               'CostaRicaCouples'
                                               , ' E-mail: emma@steyaert.com'
                                               , 'Hometown: Austin,  Texas'
                                               , 'Undergrad College: The  University of Texas at Austin'
                                               , 'Undergrad Major: International  Relations, Government'
                                               , 'Work Experience: Political  campaigns | Civic tech | UChicago Harris School of Policy Policy  MPP 2023'
                                               , 'Booth Concentrations: None'
                                               , '2022 Random Walk: Greece  Couples'
                                               , 'Hobbies: Â\xa0cooking, reading, trying out new restaurants  in Chicago, watching movies, thrifting, hiking, planning elaborately themed  events'
                                               , 'Fun Facts: I always carry a deck of cards | I love  crossword puzzles | I still do the Wordle every day | I have a *comprehensive*  list of the best restaurants in Chicago ']

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                               'Cyprus'
                                               , 'E-mail: aahuja2@chicagobooth.edu'
                                               , 'Hometown: Dublin,  CA Â\xa0(Not Ireland)'
                                               , 'Undergrad College: UC  Berkeley (Go Bears!)'
                                               , 'Undergrad Major: Business  Administration'
                                               , 'Work Experience: Consulting'
                                               , 'Booth Concentrations: Finance,  Strategic Management'
                                               , '2022 Random Walk: South  Africa'
                                               ,None
                                               ,None]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                              'Greece'
                                              , 'E-mail: asingh26@chicagobooth.edu'
                                              , 'Hometown:  Naperville, IL'
                                              , 'Undergrad College:  University of Michigan'
                                              , 'Undergrad Majors:  Computer Science'
                                              , 'Work Experience:  Software Engineer in Algo Trading'
                                              , 'Booth Concentrations:  Finance'
                                              , '2022 Random Walk:  South Africa'
                                              , 'Hobbies:Â\xa0 Triathlons, Single-Origin Pour Over  Coffee,  Live Music (#BoothTakesOverCoachella),  Architecture, Mountaineering, Reading about the old times and writing about the  new'
                                              , 'Fun Facts:  (1)  Born in India, (2) Have been stung by a String Ray but never a Bee/Wasp, (3)  Been to 200+ concerts, (4) I caught an egg thrown at me in Columbus before a  Michigan/OSU football game, (5) I give unofficial tours of the UChicago campus  (ask me for one when we’re back from Greece!)'
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                              'Greece'
                                              , 'Hometown:Â\xa0 Harrisburg,  Pennsylvania'
                                              , 'Undergrad College:Â\xa0 Georgetown  University #HoyaSaxa'
                                              , 'Undergrad Majors:  Marketing & International Business'
                                              , "Work Experience:  Luxury Products at L'OrÃ©al USA"
                                              , 'Booth Concentrations:  Finance and Behavioral Science (probably)'
                                              , '2022 Random Walk:  Turkey'
                                              , 'Hobbies:Â\xa0 Cooking way too much food and still  be stressed that people will leave hungry, the New York Times Tuesday  Crossword, Yuengling Lager, Formula 1 Racing, the Pennsylvania Farm Show,  making sure everyone knows Harrisburg is the capital of Pennsylvania, the New  York City Subway System, being an aunt, and Italian Variety Shows', 'Fun Facts:  (1) I  won a handwriting competition (2) Italian was my first language (3) I have  never eaten Subway (4) I have been paid to write Instagram Captions for people  (5) LancÃ´me named a mascara set after me'
                                              , None]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                              'India'
                                              , 'E-mail: andrew.song@chicagobooth.edu'
                                              , 'Hometown: San  Ramon, CA '
                                              , 'Undergrad College: UC  Berkeley (Cal)'
                                              , 'Undergrad Major: Molecular  Biology, Spanish'
                                              , 'Work Experience: Pharma  consulting (Pre-Booth) to Healthcare Investment Banking (Post-Booth)'
                                              , 'Booth Concentrations: Finance,  Accounting, Entrepreneurship'
                                              , '2022 Random Walk: Egypt  :]'
                                              , 'Hobbies: Soccer,  Golf, Snowboarding, BBQ/Smoking Meats, Eating, Mixology, Traveling, Music  Festivals, all things Bay Area'
                                              , 'Fun Facts: Â\xa0Broke  my wrist in Chicago last year. Have not yet contracted COVID. I collect  Jordans, backpacks, and earphones/headphones. Never been to India before :]'
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                              'India'
                                              , 'E-mail: lpurcell@chicagobooth.edu'
                                              , 'Hometown: Atlanta,  GA'
                                              , 'Undergrad College: Georgia  Tech (but I also did a 1-year Master’s  at UVA - wahoowa!)'
                                              , 'Undergrad Major: Economics  and History (lol - don’t ask me why I went to Tech for that)'
                                              , 'Work Experience: EM  at McKinsey (I’ll go back after Booth, but am recruiting for Tech for this  summer)'
                                              , 'Booth Concentrations: Marketing,  Behavioral Science, Strategic Management'
                                              , '2022 Random Walk: Egypt  (with this whole crew!)'
                                              , 'Hobbies: Â\xa0Cocktails,  celebrity gossip podcasts, workout classes, Tiktok (only viewing, no posting), my perfect  and adorable puppy Phoebe, thrifting, going to Foxtrot (iykyk)'
                                              , 'Fun Facts: I’m trying to visit every US National  Park (I’m at 10/63 currently), I drink at least 1 matcha latte a day, I learned  how to golf really only for the aesthetic'
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                              'Italy'
                                              , None
                                              , 'Hometown:  Army brat, longest I’ve lived somewhere is 4 years. '
                                              , 'Undergrad College: West  Point'
                                              , 'Undergrad Major: Systems  Engineering'
                                              , 'Work Experience: Army  Engineer Officer'
                                              , 'Booth Concentrations: Strategy,  International Business'
                                              , '2022 Random Walk: Ecuador  (Couples) '
                                              , 'Hobbies:  Playing  with my dog, outdoor activities, watching Boston sports teams, movies, travel  Â\xa0'
                                              , 'Fun Facts: (1) Only mentioned that I climbed  Mt. Kilimanjaro in 5/6 consulting interviews (2) Ran the Honolulu Marathon  without anyÂ\xa0 train-up (3) Near encyclopedic knowledge of  Fast and Furious franchise'
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                              'Japan2'
                                              , 'E-mail: ogutierr@chicagobooth.edu'
                                              , 'Hometown: State  of Mexico, Mexico'
                                              , 'Undergrad College: Tec  de Monterrey'
                                              , 'Undergrad Major: Sustainable  Development Engineering'
                                              , 'Work Experience: Consulting  (McKinsey), CPG (ABInbev,  P&G)'
                                              , 'Booth Concentrations: Business  Analytics, Marketing Management, Econometrics & Statistics'
                                              , '2022 Random Walk: Thailand'
                                              , 'Hobbies: Â\xa0Karaoke Night, Swimming, Yachting, Going to  the movies, watching reality TV, eating out, hiking.'
                                              , 'Fun Facts: I’m  allergic to camels, I don’t drink coffee and I’ve never tried KFC. I’m always  sorted in Slytherin in those HP quizzes, and I once had lunch with Jennifer  Lawrence'
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                              'Morocco'
                                              , 'E-mail: estelle.esson@chicagobooth.edu'
                                              , 'Hometown: Basking  Ridge, NJ'
                                              , 'Undergrad College: Villanova  School of Business'
                                              , 'Undergrad Major(s / Minors): Finance,  Data Analytics, International Business / Accounting, French (Jack of all  tradesâ\x80¦ Master of none)'
                                              , 'Work Experience: Fixed  Income Product Strategy at PIMCO (No, Alec and I did not coordinate  this)'
                                              , 'Booth Concentrations: Finance  and Strategic Management? #ABC'
                                              , '2022 Random Walk: Guatemala!  Happy to talk about the PTSD-inducing experience that was hiking this volcano â\x86\x92  â\x86\x92 â\x86\x92'
                                              , 'Hobbies: Weightlifting, food (preparation,  consumption, documentationâ\x80¦ whole nine yards), inserting a SpongeBob reference  into any remotely opportune moment, having overly animated facial expressions  and reactions to everything (poker 🤝  me), skiing, losing at chess, ordering  late night and PTFOing before it arrives'
                                              , 'Fun Facts: (1) I grew up training to be a  professional ballerina and have the calves to prove it (2) I’ve traveled to  over 50 countries, including Morocco! (3) Last summer I married my freshman  year study abroad crush who coincidentally became my co-worker post-grad'
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                              'Mystery'
                                              , 'E-mail: tvaradha@chicagobooth.edu'
                                              , 'Hometown: Houston, TX (s/o Yonce)'
                                              , 'Undergrad College: Rice  University'
                                              , 'Undergrad Major: Computer  Science'
                                              , 'Work Experience: Solution  Engineer @ Oracle'
                                              , 'Booth Concentrations: Strategy  & ?? don’t know for sure yet! still trying  things out'
                                              , '2022 Random Walk: Mystery!!!!  (Morocco)'
                                              , 'Hobbies: Binge-reading  fantasy books, dancing, sports for  exercise! softball, volleyball, climbing, badminton (plz note I’m not  necessarily good at them ), tackling Kyle Austin into lakes'
                                              , 'Fun Facts: I  was a huggies diaper model! looking to pivot careers. I’ve visited Beyonce’s  childhood home and shaken her dad’s hand. Our Booth cohort won 1st place in a  pie-eating contest'
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                              'Mystery'
                                              , 'E-mail: kaustin2@chicagubooth.edu'
                                              , 'Hometown: Pittsburgh,  PA'
                                              , 'Undergrad College: Northwestern'
                                              , None
                                              , 'Work Experience: IBM  Consulting '
                                              , 'Booth Concentrations: Entrepreneurship  & Finance'
                                              , '2022 Random Walk: Mystery  (Morocco)'
                                              , 'Hobbies: :  Performing  and watching stand-upÂ\xa0 comedy,  Snowboarding,  music  festivals, being pushed into lakes by Tanvi and fighting the malevolent force  that is “The Bean”'
                                              , 'Fun Facts: :  I gave my high school graduation speech (and they still let me graduate). I ran  a marathon and haven’t run more than 2 miles (at a time) since.'
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                              'SloveniaCouples'
                                              , 'E-mail: katie.obrien@chicagobooth.edu'
                                              , 'Hometown: Colorado  Springs, CO'
                                              , 'Undergrad College: University  of Colorado Denver, Grad College: Florida  Institute of Technology'
                                              , 'Undergrad Major: Psychology, Grad Major: Aviation  Human Factors'
                                              , 'Work Experience: User  Experience Researcher before booth (Boeing, Spectrum and AWS) pivoting to Tech  Product Management'
                                              , 'Booth Concentrations: Entrepreneurship,  Strategic Management & Behavioral Sciences'
                                              , None
                                              , 'Hobbies: Love  baking, DIY activities like crocheting or house renovations, and anything  outdoors (mountain biking, hiking, camping, etc.). '
                                              , 'Fun Facts: My  husband loves spicy food but I’m an absolute wimp when it comes to spice. I  taught a blues dance workshop in South Korea (love social dancing), and I’ve  been to 44 of the 50 states.'
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                              'SouthAfrica'
                                              , 'E-mail: arjunbharadwaj@chicagobooth.edu'
                                              , 'Hometown: Chennai, India'
                                              , 'Undergrad College: SRM  University, Grad College:  Clemson University '
                                              , 'Undergrad Major: Chemical  Engineering, Grad Major:  Environmental Engineering'
                                              , 'Work Experience: Climate  and Environmental Consulting'
                                              , 'Booth Concentrations: Strategy  and Operation (I think!)'
                                              , None
                                              , 'Hobbies: Â\xa0Nerding out on Water and Sustainability, watching reruns of ‘The Office’,  playing Badminton in racquetball courts, and watching an annoying amount of  sports every week (GGMU!).'
                                              , 'Fun Facts: (1) I’ve  hiked four 14’ers in the last five years. (2) I successfully created a chemical  reactor to produce methane (but shut down the whole lab in the process) (3)  I’ve driven across the US twice and camped in 13 National Parks. (4) I grew up  with 8 cats and dogs, so I am a cat-dog person.'
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                             'SouthAfrica'
                                             , 'E-mail: rkoneru@chicagobooth.edu'
                                             , 'Hometown: Alpharetta, GA'
                                             , 'Undergrad College: University  of Georgia (Go Dawgs!!) '
                                             , 'Undergrad Major: MIS  & Finance'
                                             , 'Work Experience: Consulting  & Tech'
                                             , 'Booth Concentrations: Finance, Entrepreneurship, & Strategic  Management'
                                             , '2022 Random Walk: Chile'
                                             , 'Hobbies: Photography,  kickboxing,  board-games, tennis, badminton, & watching  way too many tv shows'
                                             , 'Fun Facts: (1) I’ve been to about 30  countries, but this random walk will be my first trip toÂ\xa0 South Africa! (2)Â\xa0  I’ve never broken a bone (hope  to keep it this way) (3) I’m lowkey scared of dogs, but  it’s still one of my goals to eventually get a golden  retriever or goldendoodle because they are so  adorable/lovable!! (4) I pretty much had perfect  attendance from 1st to 12th grade (really  went downhill after thatâ\x80¦)'
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                             'Spain2'
                                             , 'E-mail: lgarciae@chicagobooth.edu'
                                             , 'Hometown: Mexico  City, MX'
                                             , 'Undergrad College: Â\xa0ITAM (Mexico)'
                                             , 'Undergrad Major: International  Relations'
                                             , 'Work Experience: Financial  services'
                                             , 'Booth Concentrations: Â\xa0Business Analytics| Finance'
                                             , '2022 Random Walk: Cyprus'
                                             , 'Hobbies: Â\xa0Swimming, traveling, theatre, mixology,  finding the best tacos and margaritas in Chicago (still better in my place)'
                                             , "Fun Facts: (1) I  haven't missed a TNDC, '(2) I had my first ski lesson in  the 2022 ski trip (3) I was a  pre-olympic swimmer"
                                              ]

raw_data_frame.loc[raw_data_frame.shape[0]] = [None,
                                             'Turkey'
                                             , 'E-mail: aquattro@chicagobooth.edu'
                                             , 'Hometown:  Providence, RI'
                                             , 'Undergrad College:  Northwestern University (I wisened up for my MBA)'
                                             , 'Undergrad Majors:  Economics'
                                             , 'Work Experience:  Strategy Consulting'
                                             , 'Booth Concentrations: Marketing  and Business Analytics'
                                             , '2022 Random Walk:  Cyprus '
                                             , 'Hobbies: Skiing  (on all forms of water apparently), wine making but mostly just drinking it,  watching Peyton & Eli’s Manning-cast, grating more cheese on my meals than  the waiters have patience for, running the beer pong table, and seizing every  opportunity to be on a boat as possible (re: Turkey Boat Party)'
                                             , 'Fun Facts: Have  never gone more than 24 hours without some form of gluten, spent multiple years  growing up in Japan, came with a twin sister to help make life decisions, ran  with the bulls in Pamplona'
                                              ]


# # Export the data
raw_data_frame.to_csv('raw_uncleaned_data.csv')
