import os
import random
import string
import math
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants
PASSWORD_LENGTH = 12
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20

# Initialize Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--window-size=500,500")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    clear_screen()
    print("************************************")
    print("*   RAG - Roblox Account Generator  *")
    print("************************************")
    print("1. Create New Roblox Account")
    print("2. Credits")
    print("3. Exit")
    print("\nChoose an option (1-3): ")

def generate_username(base_word: str, random_string_length: int) -> str:
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=random_string_length))
    username = base_word + random_string
    if USERNAME_MIN_LENGTH <= len(username) <= USERNAME_MAX_LENGTH:
        return username
    else:
        return None

def generate_password(password_type: str = "random") -> str:
    if password_type == "random":
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=PASSWORD_LENGTH))
    elif password_type == "fixed":
        return input("Enter the fixed password: ")
    else:
        print("Invalid choice. Generating random password by default.")
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=PASSWORD_LENGTH))

def select_random_birthdate(driver):
    Select(driver.find_element(By.ID, "MonthDropdown")).select_by_index(random.randrange(1, 12))
    Select(driver.find_element(By.ID, "DayDropdown")).select_by_index(random.randrange(1, 28))
    Select(driver.find_element(By.ID, "YearDropdown")).select_by_index(random.randrange(19, 25))

def create_account():
    clear_screen()

    base_word = input("Enter the base word for the username: ")
    while True:
        try:
            random_string_length = int(input("Enter the length of the random string to append: "))
            if random_string_length <= 0:
                print("Please enter a number greater than 0.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    username = generate_username(base_word, random_string_length)
    if username:
        password_choice = input("Would you like to generate a random password or use a fixed password? (random/fixed): ").strip().lower()
        password = generate_password(password_choice)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get('https://roblox.com/')
        
        select_random_birthdate(driver)
        
        driver.find_element(By.ID, "signup-username").send_keys(username)
        driver.find_element(By.ID, "signup-password").send_keys(password)
        
        random_gender = random.choice(["MaleButton", "FemaleButton"])
        driver.find_element(By.ID, random_gender).click()
        signup_button = driver.find_element(By.ID, "signup-button")
        while True:
            if signup_button.is_enabled():
                signup_button.click()
                break

        try:
            WebDriverWait(driver, math.inf).until(EC.url_to_be('https://www.roblox.com/home?nu=true'))

            with open('accounts.txt', 'a') as f:
                f.write(username + ':' + password + '\n')

            driver.close()
            return True
        except:
            return False

    else:
        print(f"\nError: The generated username '{username}' is not valid.")
        print(f"Usernames should be between {USERNAME_MIN_LENGTH} and {USERNAME_MAX_LENGTH} characters long.")

def credits():
    clear_screen()
    print("\nCredits:")
    print("RAG - Roblox Account Generator was created by alipade.")
    print("Thanks for using my program!")

def main():
    while True:
        display_menu()

        try:
            choice = int(input())
        except ValueError:
            print("\nInvalid input! Please enter a number between 1 and 3.")
            input("Press Enter to continue...")
            continue

        if choice == 1:
            create_account()
            input("Press Enter to return to the main menu...")
        elif choice == 2:
            credits()
            input("Press Enter to return to the main menu...")
        elif choice == 3:
            clear_screen()
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1 and 3.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
