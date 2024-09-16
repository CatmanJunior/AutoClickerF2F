from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
waitBetweenActions = 2

# Setup WebDriver (using Chrome as an example)
driver = webdriver.Chrome()

email = "amber.gold.s11@gmail.com"
password = "f2f2023f2f!"

id_last_post = ""

def wait_for_loading_page(wait_time):
    time.sleep(wait_time)

def login(email, password):
    # Check if the login form exists
    login_element = driver.find_element(By.XPATH, "/html/body/div[4]/div[4]/div[1]/div[2]/div/div[2]/div[2]")
    login_element.click()
    
    email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    
    email_field.send_keys(email)
    password_field.send_keys(password)
    
    time.sleep(waitBetweenActions)
    
    login_button = driver.find_element(By.CSS_SELECTOR, "button[class*='_button'][class*='_primary']")
    login_button.click()
    
    print("Login successful")
    wait_for_loading_page(waitBetweenActions)

def create_post():
    global id_last_post
    wait_for_loading_page(5)
    driver.get("https://f2f.com/library/create/")
    wait_for_loading_page(waitBetweenActions)
    spam_folder_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,"/html/body/div[4]/div[2]/div/section/div[1]/div[1]/div/a/img"))
    )
    spam_folder_button.click()
    wait_for_loading_page(waitBetweenActions)

    

    wait_for_loading_page(waitBetweenActions)
    # Click the first child of the div with class "ZjJRiW_gridContainer abvcKa_grid"
    first_child = driver.find_element(By.CSS_SELECTOR, ".ZjJRiW_gridContainer.abvcKa_grid > div:first-child")
    first_child.click()

    # Wait for the new page to load
    wait_for_loading_page(waitBetweenActions)

    # Click the button that says "Volgende"
    volgende_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#content-container > div > div.abvcKa_selectionWrapper > div.abvcKa_desktopButtons > div._8HzuwW_button._8HzuwW_primary"))
    )
    volgende_button.click()

    # Wait for the next page to load
    wait_for_loading_page(waitBetweenActions)
    #at the post page (picture with "volgende" button)
    current_url = driver.current_url
    print(current_url)
    # Split the URL and get the last part
    id_last_post = current_url.split('/')[4]

    # Print the extracted part
    print(id_last_post)
    # On the new page, click "Volgende" again
    volgende_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div[3]'))
    )
    volgende_button.click()

    # A modal should now pop up, click "Volgende"
    volgende_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[3]/div[4]/div/div[2]'))
    )
    volgende_button.click()

    # Once again, click "Volgende"
    volgende_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[3]/div[3]/div/div[2]'))
    )
    volgende_button.click()
    wait_for_loading_page(waitBetweenActions)
    # Finally, click the button that says "Nu Publiceren" (adjust locator accordingly)
    nu_publiceren_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div[2]/div/div[3]/div[3]/div/div[2]'))
    )


    nu_publiceren_button.click()

    # Wait for a few seconds to ensure the action completes
    wait_for_loading_page(waitBetweenActions)

def save_id_to_file(id_last_post):
    #add the id_last_post to the end of the file
    with open("id_last_post.txt", "w") as file:
        file.write(id_last_post)
    print("id saved to file")


def remove_post(last_id):
    last_id = last_id.strip()
    wait_for_loading_page(waitBetweenActions)
    profile_button = driver.find_element(By.XPATH, "/html/body/div[4]/nav[1]/div/div/div/div")
    profile_button.click()
    wait_for_loading_page(waitBetweenActions)
    link_to_profile = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/nav/div[1]/div/div/a")
    link_to_profile.click()
    # Locate the element you are interested in (adjust the locator to fit your case)
    wait_for_loading_page(waitBetweenActions)
    elements = driver.find_elements(By.CLASS_NAME, "grid-post")
    
    for element in elements:
        #get the a element of the grid-post
        a_element = element.find_element(By.TAG_NAME, "a")
        #get the href attribute of the a element
        href = a_element.get_attribute("href")
        #find the part after "search=" in the href
        id_post = href.split("start=")[1]
        print("id_post-", id_post)
        #strip both strings to remove any whitespace
        id_post = id_post.strip()
        print("last_id-", last_id)
        print (id_post==last_id)
        
        if id_post == last_id:
            #folow the a element 
            a_element.click()
            break
    wait_for_loading_page(waitBetweenActions)
    print("current url: ", driver.current_url)
    edit_button = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div")
    edit_button.click()
    wait_for_loading_page(waitBetweenActions)
    delete_button = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[5]/div")
    delete_button.click()
    wait_for_loading_page(waitBetweenActions)
    confirm_delete_button = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/div[2]/div[2]/div/div[2]/button")
    confirm_delete_button.click()
    print("Post deleted")

def scroll_down_in_steps(driver, total_scroll, step_size=1000, delay=1):
    current_scroll_position = 0
    while current_scroll_position <= total_scroll:
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
        time.sleep(delay)  # Wait for lazy loading to happen
        current_scroll_position += step_size

def get_first_post_on_explore():
    driver.get("https://f2f.com/explore/")
    wait_for_loading_page(waitBetweenActions)
    elements = driver.find_elements(By.CLASS_NAME, "FqVJUq_post")
    a_element = elements[0].find_element(By.TAG_NAME, "a")
    href = a_element.get_attribute("href")
    id_post = href.split("start=")[1]
    #read the id of the first post from the file
    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    try:
        with open("id_newestpost.txt", "r") as file:
            latest_id_post_file = file.read()
    except:
        with open("id_newestpost.txt", "w") as file:
            
            file.write(f"{id_post},{timenow}\n")
            return
    #TODO: Split the string at the comma and get the last element
    if id_post == latest_id_post_file:
        print("No new post")
    else:
        print("New post")
        with open("id_newestpost.txt", "a") as file:
            file.write(f"{id_post},{timenow}\n")

def look_for_post_on_explore(last_id):
    driver.get("https://f2f.com/explore/")
    wait_for_loading_page(waitBetweenActions)
    #scroll all the way down to load all the posts, to position 127668
    # Scroll down to 120,000 pixels in steps of 1000 pixels
    scroll_down_in_steps(driver, 12000)
    elements = driver.find_elements(By.CLASS_NAME, "FqVJUq_post")
    name = "miss_lucypussy"
    creator_list = []
    new_post_list = []
    for i, element in enumerate(elements, start=1):
        #get the a element of the grid-post
        a_element = element.find_element(By.TAG_NAME, "a")
        href = a_element.get_attribute("href")
        #split at the / and get the first element
        creator = href.split("/")[3]
        #find the part after "search=" in the href
        id_post = href.split("start=")[1]
        print(f"id_post- {id_post} - {id_post==last_id} - {creator} - {creator==name}")
        log_creator(creator, i)
        if creator == name:
            creator_list.append([id_post, i])
            print("Creator Post found at position: ", i)

        if id_post == last_id:
            new_post_list.append([id_post, i])
            print("Latest Post found at position: ", i)

    for creator in creator_list:
        log_position_to_file(creator[0], time.time(), creator[1])
    for new_post in new_post_list:
        log_position_to_file(new_post[0], time.time(), new_post[1])
    save_creators_to_json_file()
    print("Logged to file")        


json_data = {}
with open("creators.json", "r") as file:
    json_data = json.load(file)

#create a json file with a list of creators each with list of positions, a function thats adds a new creator to the list if it is not already there, and a new position to the list of positions of that creator
def log_creator(creator, position):
    if creator in json_data:
        json_data[creator].append(position)
    else:
        json_data[creator] = [position]

def save_creators_to_json_file():
    with open("creators.json", "w") as file:
        json.dump(json_data, file)

def log_position_to_file(postid, time, position):
    #append the postid, time and position to the end of the file
    with open("position.txt", "a") as file:
        file.write(f"{postid} {time} {position}\n")


def get_id_from_file():
    with open("id_last_post.txt", "r") as file:
        return file.read()

if __name__ == "__main__":
    
    # Visit the website
    driver.get("https://f2f.com")

    # Maximize the browser window
    driver.maximize_window()

    # Wait for the page to load
    time.sleep(3)
    login(email, password)
    wait_for_loading_page(waitBetweenActions)
    while True:
        create_post()
        save_id_to_file(id_last_post)
        id_last_post = get_id_from_file()
        get_first_post_on_explore()
        look_for_post_on_explore(id_last_post)
        for i in range(12):
            time.sleep(10)
            get_first_post_on_explore()
            print (f"waited {i*10} seconds")
        look_for_post_on_explore(id_last_post)
        remove_post(id_last_post)

    




