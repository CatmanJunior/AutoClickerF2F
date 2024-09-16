from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

wait_between_actions = 2
driver = webdriver.Chrome()

# Replace credentials with secure inputs or environment variables in production
email = "amber.gold.s11@gmail.com"
password = "f2f2023f2f!"
id_last_post = ""

# Helper function for waiting
def wait_for_loading_page(wait_time):
    time.sleep(wait_time)

# Helper function for clicking elements with explicit waits
def click_element(by, value, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()

# Helper function for finding elements
def find_element(by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

# Login function
def login(email, password):
    click_element(By.XPATH, "/html/body/div[4]/div[4]/div[1]/div[2]/div/div[2]/div[2]")  # Click login button
    find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(email)
    find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)
    click_element(By.CSS_SELECTOR, "button[class*='_button'][class*='_primary']")  # Click login
    print("Login successful")
    wait_for_loading_page(wait_between_actions)

# Create post function
def create_post():
    global id_last_post
    driver.get("https://f2f.com/library/create/")
    wait_for_loading_page(5)
    click_element(By.XPATH, "/html/body/div[4]/div[2]/div/section/div[1]/div[1]/div/a/img")  # Click spam folder button

    # Click first child element of grid container
    click_element(By.CSS_SELECTOR, ".ZjJRiW_gridContainer.abvcKa_grid > div:first-child")
    click_element(By.CSS_SELECTOR, "#content-container > div > div.abvcKa_selectionWrapper > div.abvcKa_desktopButtons > div._8HzuwW_button._8HzuwW_primary")
    wait_for_loading_page(2)
    # Capture post ID from URL
    id_last_post = driver.current_url.split('/')[4]
    print(f"ID of last post: {id_last_post}")

    # Sequence of "Volgende" button clicks
    for xpath in [
        '/html/body/div[4]/div[2]/div/div/div[2]/div[3]',
        '//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[3]/div[4]/div/div[2]',
        '//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[3]/div[3]/div/div[2]'
    ]:
        click_element(By.XPATH, xpath)
    wait_for_loading_page(2)
    print("Ready to publish post")    
    # Click "Nu Publiceren"
    publish_button = find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div[2]/div/div[3]/div[3]/div/div[2]')
    print({publish_button.text})
    publish_button.click()
    print("Post published")
    wait_for_loading_page(5)

# Save ID to file
def save_id_to_file(id_last_post):
    with open("id_last_post.txt", "w") as file:
        file.write(id_last_post)
    print("ID saved to file")

# Remove post
def remove_post(last_id):
    last_id = last_id.strip()
    click_element(By.XPATH, "/html/body/div[4]/nav[1]/div/div/div/div")  # Click profile
    click_element(By.XPATH, "/html/body/div[4]/div[2]/div/nav/div[1]/div/div/a")  # Click link to profile

    elements = driver.find_elements(By.CLASS_NAME, "grid-post")
    for element in elements:
        a_element = element.find_element(By.TAG_NAME, "a")
        id_post = a_element.get_attribute("href").split("start=")[1].strip()
        if id_post == last_id:
            a_element.click()
            break
    
    click_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div")  # Edit button
    click_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[5]/div")  # Delete button
    click_element(By.XPATH, "/html/body/div[4]/div[1]/div/div[2]/div[2]/div/div[2]/button")  # Confirm delete
    print("Post deleted")

# Scrolling helper function
def scroll_down_in_steps(total_scroll, step_size=1000, delay=1):
    current_scroll_position = 0
    while current_scroll_position <= total_scroll:
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
        time.sleep(delay)
        current_scroll_position += step_size

# Get first post on explore
def get_first_post_on_explore():
    driver.get("https://f2f.com/explore/")
    wait_for_loading_page(wait_between_actions)
    first_post = driver.find_elements(By.CLASS_NAME, "FqVJUq_post")[0].find_element(By.TAG_NAME, "a")
    id_post = first_post.get_attribute("href").split("start=")[1]

    # Handle ID logging logic
    try:
        with open("id_newestpost.txt", "r") as file:
            latest_id_post_file = file.read()
    except FileNotFoundError:
        with open("id_newestpost.txt", "w") as file:
            file.write(f"{id_post},{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            return
    
    if id_post != latest_id_post_file:
        with open("id_newestpost.txt", "a") as file:
            file.write(f"{id_post},{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        print("New post found")
    else:
        print("No new post")

# Log creator details to a JSON file
json_data = {}
with open("creators.json", "r") as file:
    json_data = json.load(file)

def log_creator(creator, position):
    json_data.setdefault(creator, []).append(position)

def save_creators_to_json_file():
    with open("creators.json", "w") as file:
        json.dump(json_data, file)

def log_position_to_file(post_id, position):
    with open("position.txt", "a") as file:
        file.write(f"{post_id} {time.time()} {position}\n")

def get_id_from_file():
    with open("id_last_post.txt", "r") as file:
        return file.read()

def look_for_post_on_explore(last_id):
    """
    Looks for posts on the explore page and logs information if the post with the given last_id is found.
    Also logs creator information if a post by 'miss_lucypussy' is found.
    """
    driver.get("https://f2f.com/explore/")
    wait_for_loading_page(wait_between_actions)

    # Scroll down to load more posts if needed (adjust the total_scroll value as necessary)
    scroll_down_in_steps(total_scroll=12000)

    # Find all posts on the explore page
    elements = driver.find_elements(By.CLASS_NAME, "FqVJUq_post")
    target_creator = "miss_lucypussy"
    creator_list = []
    new_post_list = []

    # Iterate over posts and check for target creator and the latest post ID
    for i, element in enumerate(elements, start=1):
        a_element = element.find_element(By.TAG_NAME, "a")
        href = a_element.get_attribute("href")

        # Extract creator and post ID from the href
        creator = href.split("/")[3]
        id_post = href.split("start=")[1].strip()

        print(f"id_post- {id_post} - {id_post == last_id} - {creator} - {creator == target_creator}")

        # Log positions of the posts by the target creator
        if creator == target_creator:
            creator_list.append([id_post, i])
            print(f"Creator Post found at position: {i}")

        # Log positions of posts matching the last post ID
        if id_post == last_id:
            new_post_list.append([id_post, i])
            print(f"Latest Post found at position: {i}")

    # Log creator information and post IDs
    for creator in creator_list:
        log_position_to_file(creator[0], time.time(), creator[1])
        log_creator(creator[0], creator[1])
        
    for new_post in new_post_list:
        log_position_to_file(new_post[0], time.time(), new_post[1])

    # Save the updated creator list to the JSON file
    save_creators_to_json_file()
    print("Logged to file successfully.")


if __name__ == "__main__":
    driver.get("https://f2f.com")
    driver.maximize_window()
    time.sleep(3)
    login(email, password)
    wait_for_loading_page(wait_between_actions)

    while True:
        create_post()
        save_id_to_file(id_last_post)
        get_first_post_on_explore()
        look_for_post_on_explore(id_last_post)
        
        # Loop to repeatedly check for new posts
        for i in range(12):
            time.sleep(10)
            get_first_post_on_explore()
            print(f"Waited {i * 10} seconds")
        
        look_for_post_on_explore(id_last_post)
        remove_post(id_last_post)
