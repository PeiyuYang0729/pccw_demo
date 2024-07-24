from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import urllib.request
import os,sys
import subprocess

current_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(current_path)

#open browser
driver = webdriver.Chrome()
driver.get('https://graph.baidu.com/pcpage/index?tpl_from=pc')
driver.maximize_window()

#waiting for image search box and click it
graph_xpath = "//span[@class='graph-d20-search-wrapper-camera']"
wait = WebDriverWait(driver, 10)
graph = wait.until(lambda driver: driver.find_element(by=By.XPATH, value=graph_xpath))
driver.find_element(by=By.XPATH, value=graph_xpath).click()

#waiting for file upload box and upload demo.png
file_xpath = "//input[@type='file']"
wait = WebDriverWait(driver, 10)
file = wait.until(lambda driver: driver.find_element(by=By.XPATH, value=file_xpath))
driver.find_element(by=By.XPATH, value=file_xpath).send_keys(current_path+'/demo/demo.png')

#check if the result is "相似图片" if not shown, page is not loaded correctly, end this test
similar_pic_xpath = "//div[@class='general-title-cont']"
wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, similar_pic_xpath)))
result = driver.find_element(by=By.XPATH, value=similar_pic_xpath).text
if result != '相似图片':
    #end this test
    print("Page is not loaded, test failed")
    driver.quit()
    exit()        
                 
#open configuration json file and get vaule of "visit_result"
file = open(current_path+ "/config.json", "r")
config = json.load(file)
if "visit_result" not in config:
    print("visit_result not found")
    driver.quit()
visit_result = config["visit_result"]

#get visit_result image and save it to current folder
waterfall = "//div[@class='general-waterfall']"
wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, waterfall)))
col_num = driver.find_elements(by=By.CLASS_NAME, value="general-imgcol")
col = visit_result % len(col_num)
line = int(visit_result / len(col_num))+1
img_path = "//div[@class='general-waterfall']//div[%d]//a[%d]//img" % (col, line)
img = driver.find_element(by=By.XPATH, value=img_path)
src = img.get_attribute('src')
if not os.path.exists(current_path+'/download'):
    os.makedirs(current_path+'/download')
if os.path.exists(current_path+'/download/demo.png'):
    os.remove(current_path+'/download/demo.png')
urllib.request.urlretrieve(src, current_path+'/download/demo.png')
time.sleep(2)
#close the browser
driver.quit()


#compare demo.png and downloadimg.png
#run command "python3 -m clip_score /Users/peiyu/Documents/pccw/demo /Users/peiyu/Documents/pccw/download --real_flag img --fake_flag img
result = subprocess.run(["python3", "-m", "clip_score", current_path+"/demo", current_path+"/download", "--real_flag", "img", "--fake_flag", "img"], stdout=subprocess.PIPE, text=True)
score = result.stdout.replace(' ', '').rsplit(":",1)[-1]
print(score)

#if score is over 80, the two picture is related and test passed
#if score is less than 80, the two picture is not related and test failed
if float(score) > 80:
    print("Test passed, score: ", score, "File path is", current_path+'/download/demo.png')
else:
    os.remove(current_path+'/download/demo.png')
    print("Test failed")
exit()