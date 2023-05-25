# extract data from Linkedin
# extract the job offers


from abc import abstractmethod
from datetime import datetime

# job offer skills extractor 
# make a database of skills 
# call the openapi to extract this for me

class BaseJobOfferLoader:
    
    @abstractmethod
    def search(self, keyword: str, region: str, published_after: datetime):
        ...
    
    @abstractmethod
    def process(self, doc):
        ...
    
    
class LinkedInJobOfferLoader(BaseJobOfferLoader):
    ...
    
class IndeedJobOfferLoader(BaseJobOfferLoader):
    ...
    
class MonsterJobOfferLoader(BaseJobOfferLoader):
    ...
    
# %%
import bs4
import httpx
