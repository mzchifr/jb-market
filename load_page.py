# import scrapy
import datetime
import json
import random
import re
import time

import loguru
import pandas as pd
import tqdm
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
start_url = "https://www.linkedin.com/jobs/search/?currentJobId=3616231565&geoId=105015875&keywords=data%20engineer&location=France&refresh=true"


def wait_till_get_element(driver, by, value, timeout: float = 2) -> WebElement:
    return WebDriverWait(driver, timeout).until(lambda x: x.find_element(by, value))


def find_total_job_pages(driver, url):
    driver.get(url)
    page_selectors = wait_till_get_element(
        driver, By.CLASS_NAME, "artdeco-pagination__pages--number"
    )

    last_page = int(page_selectors.find_elements(By.TAG_NAME, "li")[-1].text)
    return last_page


def scrape_job_page(driver, url):
    loguru.logger.info("Scrapping {}", url)
    driver.get(url)
    # this is for fixing the page half-loaded problem (resulting in a wrong job lists)
    time.sleep(2)
    jobs = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")

    for job in jobs:
        job.click()
        time.sleep(2)
        job.click()
        icon_src = None
        try:
            icon_src = job.find_element(By.TAG_NAME, "img").get_attribute("src")
        except NoSuchElementException as e:
            ...

        detail_page = wait_till_get_element(
            driver, By.CLASS_NAME, "jobs-search__job-details"
        )

        job_description = wait_till_get_element(
            detail_page, By.CLASS_NAME, "jobs-description__container"
        )

        # TODO: premium
        try:
            premium_applicant_insight = wait_till_get_element(
                detail_page, By.CLASS_NAME, "jobs-premium-applicant-insights"
            )
        except TimeoutException:
            # When there is not enough applicants
            ...
        # applicants_ul = wait_till_get_element(
        #     premium_applicant_insight,
        #     By.CSS_SELECTOR,
        #     ".jobs-details-premium-insight__list.jobs-premium-applicant-insights__list",
        # )

        # for l in applicants_ul.find_elements(By.TAG_NAME, "li"):
        #     print(
        #         l.find_element(
        #             By.CLASS_NAME, "jobs-premium-applicant-insights__list-num"
        #         ).text
        #     )

        # Find the median tenure
        median_tenure = None
        premium_company_link = None

        try:
            premium_company_insight = wait_till_get_element(
                detail_page, By.CLASS_NAME, "jobs-premium-company-insights"
            )

            _mt = re.search(
                # this allows finding float or int
                r".*(\d+\.*\d*).*",
                wait_till_get_element(
                    premium_company_insight,
                    By.CLASS_NAME,
                    "jobs-premium-company-growth",
                )
                .find_element(By.CLASS_NAME, "align-items-center")
                .text,
            ).group(  # type: ignore
                1
            )

            if _mt is not None:
                median_tenure = float(_mt)

            # for some companies, they don't have insight yet
            try:
                premium_company_link = premium_company_insight.find_element(
                    By.CLASS_NAME, "jobs-details-premium-insight__company-link"
                ).get_attribute("href")
            except NoSuchElementException as e:
                ...
        except TimeoutException as e:
            loguru.logger.warning("No company growth info {}", e)

        # company section
        try:
            company_url = (
                wait_till_get_element(detail_page, By.CLASS_NAME, "jobs-company__box")
                .find_element(By.TAG_NAME, "a")
                .get_attribute("href")
            )
        except TimeoutException:
            continue

        title = wait_till_get_element(job, By.CLASS_NAME, "job-card-list__title")
        company = wait_till_get_element(
            detail_page, By.CLASS_NAME, "jobs-unified-top-card__company-name"
        )
        posted_date = wait_till_get_element(
            detail_page, By.CLASS_NAME, "jobs-unified-top-card__posted-date"
        )

        applicant_count = "0 applicant"
        try:
            applicant_count = wait_till_get_element(
                detail_page, By.CLASS_NAME, "jobs-unified-top-card__applicant-count"
            ).text
        except TimeoutException:
            ...

        # new hires for the last months
        # headcounts
        # hires_from
        # num_employees
        # followers
        # applicant_last_day

        yield {
            "job_id": job.get_attribute("data-occludable-job-id"),
            "description": job_description.text,
            "title": title.text,
            "company": company.text,
            "posted_date": posted_date.text,
            # TODO: some problem with the texts
            "total_applicant": re.search(
                r".*(\d+)\s+applicant.*", applicant_count
            ).group(1),
            "icon_src": icon_src,
            "scrapped_at": datetime.datetime.now().timestamp(),
            "company_page": company_url,
            "insight_page": premium_company_link,
            "median_tenure": median_tenure,
        }


total_pages = find_total_job_pages(driver, start_url)
print("--------")
print(f"Total page = {total_pages}")

for i in tqdm.trange(total_pages):
    for job in scrape_job_page(driver, start_url + f"&start={i * 25}"):
        with open("job-board.txt", "a") as f:
            f.write(json.dumps(job))
            f.write("\n---SEP---\n")

time.sleep(100)
