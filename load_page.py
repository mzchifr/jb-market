# import scrapy
import datetime
import json
import random
import time

import loguru
import pandas as pd
import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=selenium")
driver = webdriver.Chrome(options=options)
# driver.get(
#     "https://www.linkedin.com/jobs/search/?currentJobId=3546678491&keywords=data%20scientist&refresh=true"
# )
start_url = "https://www.linkedin.com/jobs/search/?currentJobId=3546678491&keywords=data%20scientist&refresh=true"


def wait_till_get_element(driver, by, value, timeout: float = 2) -> WebElement:
    return WebDriverWait(driver, timeout).until(lambda x: x.find_element(by, value))


def find_total_job_pages(driver, url):
    driver.get(url)
    page_selectors = driver.find_element(
        By.CLASS_NAME, "artdeco-pagination__pages--number"
    )
    last_page = int(page_selectors.find_elements(By.TAG_NAME, "li")[-1].text)
    return last_page


def scrape_job_page(driver, url):
    loguru.logger.info("Scrapping {}", url)
    driver.get(url)

    jobs = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")
    for job in jobs:
        job.click()
        # time.sleep(random.randint(1, 2))
        time.sleep(2)
        job.click()
        icon_src = job.find_element(By.TAG_NAME, "img").get_attribute("src")

        try:
            detail_page = wait_till_get_element(
                driver, By.CLASS_NAME, "jobs-search__job-details"
            )

            job_description = wait_till_get_element(
                detail_page, By.CLASS_NAME, "jobs-description__container"
            )

            # TODO: premium
            premium_applicant_insight = wait_till_get_element(
                detail_page, By.CLASS_NAME, "jobs-premium-applicant-insights"
            )
            premium_company_insight = wait_till_get_element(
                detail_page, By.CLASS_NAME, "jobs-premium-company-insights"
            )

            premium_company_link = premium_company_insight.find_element(
                By.CLASS_NAME, "jobs-details-premium-insight__company-link"
            ).get_attribute("href")
            # company section
            company_url = (
                wait_till_get_element(detail_page, By.CLASS_NAME, "jobs-company__box")
                .find_element(By.TAG_NAME, "a")
                .get_attribute("href")
            )

            title = job.find_element(By.CLASS_NAME, "job-card-list__title")
            company = wait_till_get_element(
                detail_page, By.CLASS_NAME, "jobs-unified-top-card__company-name"
            )
            posted_date = wait_till_get_element(
                detail_page, By.CLASS_NAME, "jobs-unified-top-card__posted-date"
            )

            applicant_count = wait_till_get_element(
                detail_page, By.CLASS_NAME, "jobs-unified-top-card__applicant-count"
            )

            # new hires for the last months
            # median tenure
            # headcounts
            # hires_from
            # num_employees
            # on_linked_in
            # followers
            # total_applicant
            # applicant_last_day

            yield {
                "job_id": job.get_attribute("data-occludable-job-id"),
                "description": job_description.text,
                "title": title.text,
                "company": company.text,
                "posted_date": posted_date.text,
                "applicant_count": int(applicant_count.text.split(" ")[0]),
                "icon_src": icon_src,
                "scrapped_at": datetime.datetime.now().timestamp(),
                "company_page": company_url,
                "insight_page": premium_company_link,
            }

        except Exception as e:
            time.sleep(3)
            loguru.logger.info(f"Sleeping to recover from {e}")


total_pages = find_total_job_pages(driver, start_url)
print("--------")
print(f"Total page = {total_pages}")

for i in tqdm.trange(total_pages):
    for job in scrape_job_page(driver, start_url + f"&start={i * 25}"):
        with open("job-board.txt", "a") as f:
            f.write(json.dumps(job))
            f.write("\n---SEP---\n")

time.sleep(100)
