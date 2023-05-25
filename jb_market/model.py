# raw data storage

# processed job offers
# 1. job name
# 2. company name
# 3. deduplication
# 4. reference id
# 5. skills 
# 6. responsability


# job offer skills extractor 
# make a database of skills 
# call the openapi to extract this for me
import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    ...
    
    
class RawData(Base):
    __tablename__ = "raw_data"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    jd: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)


class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    offers: Mapped[List["Offer"]] = relationship()
    
class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    offers: Mapped[List["Offer"]] = relationship()

class Offer(Base):
    __tablename__ = "offers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    company: Mapped["Company"] = relationship(back_populates="offers")
    role: Mapped["Role"] = relationship(back_populates="offers")
    city: Mapped[Optional[str]]
    country: Mapped[Optional[str]]
    remote_policy: Mapped[Optional[str]]
    min_salary: Mapped[Optional[float]]
    max_salary: Mapped[Optional[float]]
    min_exp: Mapped[Optional[int]]
    url: Mapped[str]

class OfferMonitoring(Base):
    __tablename__ = "offer_monitoring"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    count_applicant: Mapped[int] = mapped_column(default=0)

class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    category: Mapped[str]
    

engine = create_engine("sqlite:///a.db")

Base.metadata.create_all(engine)


# analysis that I want to carry out
# job market, which is more tensed
# show it on a map: which is the city that offers the most of data engineer jobs
# what's the salary that could we expect for different regions
# what's the most valuable certificate to have? 