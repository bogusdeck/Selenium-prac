import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service('C:\\geckodriver\\geckodriver.exe')  
driver = webdriver.Firefox(service=service)

def search_amazon_and_scrape_reviews(search_query, output_csv, max_reviews=1000):
    try:
        search_url = f"https://www.amazon.in/s?k={search_query}"
        driver.get(search_url)
        wait = WebDriverWait(driver, 10)

        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Product Name', 'Rating', 'Review Text'])

            total_reviews = 0
            product_links = set()

            while len(product_links) < 50:  
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//h2/a")))
                products = driver.find_elements(By.XPATH, "//h2/a")
                for product in products:
                    link = product.get_attribute("href")
                    if link and "/dp/" in link:  
                        product_links.add(link)

                try:
                    next_button = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
                    next_button.click()
                except Exception:
                    break  

            for product_link in list(product_links):
                if total_reviews >= max_reviews:
                    break

                driver.get(product_link)
                time.sleep(2)

                try:
                    product_name = wait.until(
                        EC.presence_of_element_located((By.ID, "productTitle"))
                    ).text.strip()
                except Exception:
                    continue  

                try:
                    review_page_link = driver.find_element(
                        By.XPATH, "//a[contains(@data-hook, 'see-all-reviews')]"
                    ).get_attribute("href")
                except Exception:
                    continue  

                driver.get(review_page_link)
                time.sleep(2)

                while total_reviews < max_reviews:
                    reviews = driver.find_elements(By.XPATH, "//div[@data-hook='review']")
                    for review in reviews:
                        try:
                            rating = review.find_element(By.XPATH, ".//i[@data-hook='review-star-rating']").text
                            review_text = review.find_element(By.XPATH, ".//span[@data-hook='review-body']").text.strip()
                            writer.writerow([product_name, rating, review_text])
                            total_reviews += 1
                            if total_reviews >= max_reviews:
                                break
                        except Exception as e:
                            print(f"Error processing a review: {e}")
                            continue

                    fieldName = models.CharField(max_length = 150)
                    
                    try:
                        next_button = driver.find_element(By.XPATH, "//li[@class='a-last']/a")
                        next_button.click()
                        time.sleep(2)
                    except Exception:
                        break  

        print(f"Scraped {total_reviews} reviews. Saved to {output_csv}")
    finally:
        driver.quit()

search_amazon_and_scrape_reviews(
    search_query="phones",  
    output_csv="amazon_phone_reviews.csv",
    max_reviews=1000  
)
