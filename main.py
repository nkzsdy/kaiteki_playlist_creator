from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import re
#import gkeepapi

# scraping
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--lang=ja')

driver = webdriver.Chrome(options=options)
driver.get('https://www4.nhk.or.jp/kaiteki/')

wait = WebDriverWait(driver, 10)

on_air_date = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="ProgramContents"]/div/div[1]/div[2]/time')))
on_air_date = on_air_date.get_attribute('datetime')
print(on_air_date)

program_title = wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'program-title')))
program_title = program_title.text
print(program_title)

playlist = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="ProgramContents"]/div/div[2]/p[2]')))
playlist = playlist.text

song_metadata_str = ''
song_metadata_array = []
song_length_pattern = re.compile('^（\d分\d+秒）$')
song_media_standard_number_pattern = re.compile('^＜.+＞$')

for line in playlist.splitlines():
    if len(line) == 0 or line == playlist[-1]:
        song_metadata_array.append(song_metadata_str)
        song_metadata_str = ''
        continue

    if song_length_pattern.match(line) or song_media_standard_number_pattern.match(line):
        continue

    song_metadata_str += line

for item in song_metadata_array:
    print(item)

driver.quit()

# TODO: create Google Keep note
# なんかgkeepapiの不具合でうまくいかないのでkeep使うか再検討
