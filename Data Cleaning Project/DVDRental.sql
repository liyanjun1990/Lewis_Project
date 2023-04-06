-- 1.0 import table into database

-- 1.1.1 Inventory Table
 CREATE TABLE inventory (
    inventory_id int  NOT NULL ,
    film_id int NOT NULL ,
    store_id int  NOT NULL ,
    last_update date  NOT NULL 
)


bulk insert dbo.inventory
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\inventory.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
)

alter table inventory
drop column last_update;

-- 1.2.1 import rental 
drop table if exists rental
 CREATE TABLE rental (
    rental_id int   ,
    rental_date nvarchar(50)  ,
    inventory_id int   ,
    customer_id int  ,
	return_date nvarchar(50),
	staff_id int,
	last_update nvarchar(50)
)

bulk insert dbo.rental
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\rental.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
)

alter table rental
drop column last_update;

-- 1.2.2 use try_convert to detect if any row is uncovertable

select *, try_convert(datetime,rental_date,120) , try_convert(datetime,return_date,120) 
from rental
where try_convert(datetime,return_date,120) is null

-- 1.2.3 it seems like NULL is the issue, therefore set NULL to null and convert again
update rental
set return_date = null
where return_date = 'NULL'

-- 1.2.4 double check if error occured, and update table

select * 
,convert(datetime,rental_date,120)
,convert(datetime,return_date,120)
from rental

update rental
set rental_date = convert(datetime,rental_date,120),
    return_date = convert(datetime,return_date,120)

-- 1.2.5 split the date and time, as it is more friendly for power bi

alter table rental
add rental_time time
, return_time time

update rental
set rental_date = convert(date,rental_date)
	,rental_time = convert(time,rental_date)
    ,return_date = convert(date,return_date)
	,return_time = convert(time,return_date)

select * from rental

-- 1.3.1 import payment 
drop table if exists payment
 CREATE TABLE payment (
    payment_id int   ,
    customer_id int  ,
    staff_id int   ,
    rental_id int  ,
	amount float,
	payment_date nvarchar(50),
	last_update nvarchar(50)
)

bulk insert dbo.payment
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\payment.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
)

-- 1.3.2 fix the date issue if occured and drop last_update

alter table payment
drop column last_update;

alter table payment
add payment_time time;

select *, try_convert(datetime,payment_date,103) 
from payment
where try_convert(datetime,payment_date,103)  is null;

update payment
set payment_date = convert(date,convert(datetime,payment_date,103))
    ,payment_time = convert(time,convert(datetime,payment_date,103));

select * from payment

-- 1.4.1 import film
drop table if exists film
 CREATE TABLE film (
    film_id int   ,
    title nvarchar(50)  ,
    description nvarchar(255)   ,
    release_year int  ,
	language_id int,
	original_language_id nvarchar(10),
	rental_duration int,
	rental_rate float,
	length int,
	replacement_cost float,
	rating nvarchar(255),
	special_features nvarchar(255),
	last_update nvarchar(50)
)

bulk insert dbo.film
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\film.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
)

-- 1.4.2 drop last_update, fix original_language_id

alter table film
drop column last_update

update film
set original_language_id = null
where original_language_id = 'NULL'

-- 1.5.1 import store table

drop table if exists store
 CREATE TABLE store (
    store_id int   ,
    manager_staff_id int ,
    address_id int ,
	last_update nvarchar(50)
)

bulk insert dbo.store
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\store.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
)

alter table store
drop column last_update

-- 1.6.1 import address

drop table if exists address_table
 CREATE TABLE address_table (
    address_id int   ,
    address nvarchar(50) ,
    address2 nvarchar(50)  ,
	district nvarchar(50) ,
	city_id int ,
	postal_code nvarchar(10) ,
	phone nvarchar(20) ,
	last_update nvarchar(50)
)

bulk insert dbo.address_table
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\address.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
)

alter table address_table
drop column last_update

update address_table
set address2 = null
where address2 = 'NULL'

-- 1.7.1 import city and country table
drop table if exists city;
 CREATE TABLE city (
    city_id int   ,
    city nvarchar(50),
	country_id smallint,
	last_update nvarchar(50)
);

bulk insert dbo.city
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\city.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
);

-- 

drop table if exists country;
 CREATE TABLE country (
	country_id smallint,
	country nvarchar(50),
	last_update nvarchar(50)
);

bulk insert dbo.country
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\country.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
);

alter table country
drop column last_update;

-- 1.8.1 import film category and category

drop table if exists film_category;
 CREATE TABLE film_category (
    film_id smallint   ,
    category_id smallint,
	last_update nvarchar(50)
);

bulk insert dbo.film_category
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\film_category.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
);

alter table film_category
drop column last_update;

-- 

drop table if exists category;
 CREATE TABLE category (
	category_id smallint,
	name nvarchar(50),
	last_update nvarchar(50)
);

bulk insert dbo.category
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\category.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
);

alter table category
drop column last_update;

-- 1.9.1 import film_actor and actor

drop table if exists film_actor;
 CREATE TABLE film_actor (
    actor_id smallint   ,
    film_id smallint,
	last_update nvarchar(50)
);

bulk insert dbo.film_actor
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\film_actor.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
);

alter table film_actor
drop column last_update;

-- 

drop table if exists actor;
 CREATE TABLE actor (
	actor_id smallint,
	first_name nvarchar(50),
	last_name nvarchar(50),
	last_update nvarchar(50)
);

bulk insert dbo.actor
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\actor.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
);

alter table actor
drop column last_update;

-- 1.10.1 import customer table

drop table if exists customer;
 CREATE TABLE customer (
	customer_id smallint,
	store_id smallint,
	first_name nvarchar(50),
	last_name nvarchar(50),
	email nvarchar(100),
	address_id smallint,
	active bit ,
	created_date nvarchar(50),
	last_update nvarchar(50)
);

bulk insert dbo.customer
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Rental\customer.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
);

alter table customer
drop column last_update;

alter table customer
add created_time time;

select *, try_convert(datetime,created_date,103) 
from customer
where try_convert(datetime,created_date,103)  is null;

update customer
set created_date = convert(date,convert(datetime,created_date,103))
    ,created_time = convert(time,convert(datetime,created_date,103));


select * from customer

-- 2.0.1 investigate the revenue problem 

select * 
from rental re
join payment pa
	on re.rental_id = pa.rental_id
join inventory inv
	on re.inventory_id = inv.inventory_id
join film fi
	on fi.film_id = inv.film_id

-- 2.0.2 from the result we can conclude the revenue do not charged by the duration of the DVD

select 
re.rental_date
,re.return_date
,DATEDIFF(day,re.rental_date,re.return_date) as diff
,DATEDIFF(day,re.rental_date,re.return_date) * rental_rate as check_rev
,amount
,amount - DATEDIFF(day,re.rental_date,re.return_date) * rental_rate

from rental re
join payment pa
	on re.rental_id = pa.rental_id
join inventory inv
	on re.inventory_id = inv.inventory_id
join film fi
	on fi.film_id = inv.film_id
where DATEDIFF(day,re.rental_date,re.return_date) <> 1 and (abs(amount - DATEDIFF(day,re.rental_date,re.return_date) * rental_rate) <1 )

-- 2.0.3 investigate the durtion of DVD and duration of the rental, the result showed that for every addtional day, it will be $1 actual.

select 
re.rental_date
,re.return_date
,fi.rental_duration
,DATEDIFF(day,re.rental_date,re.return_date) as diff
,fi.rental_duration - DATEDIFF(day,re.rental_date,re.return_date)
,amount
,fi.rental_rate
,(amount - fi.rental_rate)/(fi.rental_duration - DATEDIFF(day,re.rental_date,re.return_date))
from rental re
join payment pa
	on re.rental_id = pa.rental_id
join inventory inv
	on re.inventory_id = inv.inventory_id
join film fi
	on fi.film_id = inv.film_id
where (fi.rental_duration - DATEDIFF(day,re.rental_date,re.return_date)) = 0
order by (amount - fi.rental_rate)/(fi.rental_duration - DATEDIFF(day,re.rental_date,re.return_date))


