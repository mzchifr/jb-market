CREATE TABLE raw_data (
	id INTEGER NOT NULL, 
	jd VARCHAR NOT NULL, 
	url VARCHAR NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE companies (
	id INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE roles (
	id INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE offer_monitoring (
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	count_applicant INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE skills (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	category VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE offers (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	role_id INTEGER NOT NULL, 
	city VARCHAR, 
	country VARCHAR, 
	remote_policy VARCHAR, 
	min_salary FLOAT, 
	max_salary FLOAT, 
	min_exp INTEGER, 
	url VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id), 
	FOREIGN KEY(role_id) REFERENCES roles (id)
);
