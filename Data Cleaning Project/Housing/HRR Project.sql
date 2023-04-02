﻿-- Issue with the data
-- some of the hire date do not coresponding to the salary start date. (fixed in section 6)
-- salary increase date might be different from the title change or department change date. (fixed by section 4)


-- 1.1 Inseert value - Departments

CREATE TABLE [departments] (
    [dept_no] nvarchar(4)  NOT NULL ,
    [dept_name] nvarchar(40)  NOT NULL ,
    CONSTRAINT [PK_departments] PRIMARY KEY CLUSTERED (
        [dept_no] ASC
    )
)

INSERT INTO departments (dept_no, dept_name) VALUES
('d009', '\"Customer Service\"'),
('d003', '\"Human Resources\"'),
('d006', '\"Quality Management\"'),
('d005', 'Development'),
('d002', 'Finance'),
('d001', 'Marketing'),
('d004', 'Production'),
('d008', 'Research'),
('d007', 'Sales')

-- 1.1.1 Clean Departments remove "\" from the department 

update departments 
set dept_name = replace(dept_name,'\"','')


-- 1.2 bulk dept_emp by insert csv
 CREATE TABLE [dept_emp] (
    [emp_no] int  NOT NULL ,
    [dept_no] nvarchar(4)  NOT NULL ,
    [from_date] date  NOT NULL ,
    [to_date] date  NOT NULL 
)


bulk insert dbo.dept_emp
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Employee\dept_emp.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
)

-- 1.3 bulk dept_manager by insert csv

CREATE TABLE [dept_manager] (
    [emp_no] int  NOT NULL ,
    [dept_no] nvarchar(4)  NOT NULL ,
    [from_date] date  NOT NULL ,
    [to_date] date  NOT NULL ,
    CONSTRAINT [PK_dept_manager] PRIMARY KEY CLUSTERED (
        [emp_no] ASC
    )
)

bulk insert dbo.dept_manager
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Employee\dept_manager.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=2
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
)

-- 1.4 bulk employees by insert csv
Drop table [employees]
CREATE TABLE [employees] (
    [emp_no] int  NOT NULL ,
    [birth_date] date  NOT NULL ,
    [first_name] nvarchar(14)  NOT NULL ,
    [last_name] nvarchar(16)  NOT NULL ,
    [gender] nvarchar(10)  NOT NULL ,
    [hire_date] date  NOT NULL 
)


bulk insert dbo.employees
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Employee\employees.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=3
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
)

-- 1.4.1 Change the M to Male, F to Female
update employees
set gender =  
	case when gender= 'M' then 'Male' 
		 when gender= 'F' then 'Female'
		 end


-- 1.5 bulk Salary by insert csv
Drop table [salaries]
CREATE TABLE [salaries] (
    [emp_no] int  NOT NULL ,
    [salary] int  NOT NULL ,
    [from_date] date  NOT NULL ,
    [to_date] date  NOT NULL 
    )


bulk insert dbo.salaries
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Employee\salaries.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=3
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
)


-- 1.6 bulk title by insert csv
drop table [title]
CREATE TABLE [title] (
    [emp_no] int  NOT NULL ,
    [title] nvarchar(50)  NOT NULL ,
    [from_date] date  NOT NULL ,
    [to_date] date  NOT NULL ,
)

bulk insert dbo.title
from 'C:\Users\admin\Desktop\Job\Data Analyst\Udemy Project\Employee\titles.csv'
with
(
  FORMAT = 'CSV'
, FIRSTROW=3
, FIELDQUOTE = '"'
, FIELDTERMINATOR = ','
, ROWTERMINATOR = '0x0a'
)

-- 1.6.1 Drop duplicate

with title_del_dup as(
select *
, ROW_NUMBER() over (partition by emp_no,title,from_date,to_date order by emp_no) as duplicate_rows
from title
)
delete 
from title_del_dup
where duplicate_rows >1

-- 2.1 Query: Salary for department manager

select dm.emp_no,dp.dept_name,em.first_name,em.last_name,em.gender,sa.salary
from dept_manager dm
join departments dp
	on dm.dept_no = dp.dept_no
join employees as em
	on dm.emp_no = em.emp_no
left join salaries as sa
	on dm.emp_no = sa.emp_no
where dm.to_date > '2023-03-28'
	and sa.to_date > '2023-03-28'

-- 2.2 Query all Staff Salary 

select em.emp_no,em.first_name,em.last_name,em.gender,dp.dept_name,sa.salary
from employees em
join dept_emp de
	on em.emp_no = de.emp_no
join departments as dp
	on de.dept_no = dp.dept_no
left join salaries as sa
	on em.emp_no = sa.emp_no
where de.to_date > '2023-03-28'
	and sa.to_date > '2023-03-28'

-- 2.3 Average Salary department (include manager)

select * --dp.dept_name, round(AVG(cast(sa.salary as float)),0)
from employees em
join dept_emp de
	on em.emp_no = de.emp_no
join departments as dp
	on de.dept_no = dp.dept_no
left join salaries as sa
	on em.emp_no = sa.emp_no
where de.to_date = '9999-01-01'
	and sa.to_date = '9999-01-01'
-- group by dp.dept_name
-- order by 2 desc

-- 2.4 Average Salary department (exclude manager)

select dp.dept_name, round(AVG(cast(sa.salary as float)),0)
from employees em
join dept_emp de
	on em.emp_no = de.emp_no
join departments as dp
	on de.dept_no = dp.dept_no
left join salaries as sa
	on em.emp_no = sa.emp_no
left join dept_manager as dm
	on em.emp_no = dm.emp_no
and de.to_date > '2023-03-28'
and sa.to_date > '2023-03-28'
and dm.to_date <> '9999-01-01'
group by dp.dept_name
order by 2 desc


-- 3.1 rolling percentage increase for certain employee, use CTE

with Salary_Trend as(
select year(from_date) as Year,max(salary) as Salary
from salaries
where emp_no = 110022
group by year(from_date)
)
select Year, Salary
, round((Salary - lag(Salary) over (order by Year) -1) 
		,2) as Per_Increase
, round((cast(Salary as float) / lag(cast(Salary as float)) over (order by Year) -1) * 100
		,2) as Per_Increase
from Salary_Trend

-- 3.2 rolling percentage increase for all, use lag and partition

select emp_no,year(from_date) as Year, salary
, round(salary - lag(salary) over (partition by emp_no order by year(from_date)) 
		,2) as Increase
, round((cast(salary as float) / lag(cast(salary as float)) over (partition by emp_no order by year(from_date)) -1) * 100
		,2) as Per_Increase
from salaries

-- 4.1 create view all_current_status, this approch has problem as it will eliminate 15 transacations as not all of them have all status to '9999-01-01'
create view cur_emp_problem as
	select  --*
		em.emp_no
		,em.birth_date
		,em.first_name
		,em.last_name
		,em.gender
		,em.hire_date
		,dp.dept_name
		,sa.salary
		,ti.title
	from employees em
	left join dept_emp de
		on em.emp_no = de.emp_no
	join departments as dp
		on de.dept_no = dp.dept_no
	left join dept_manager as dm
		on em.emp_no = dm.emp_no
	left join title as ti
		on em.emp_no = ti.emp_no
    join salaries as sa
		on em.emp_no = sa.emp_no
	where --de.to_date = '9999-01-01'
		 sa.to_date = '9999-01-01'
		and (dm.to_date = '9999-01-01' or dm.to_date  is null)
		and de.to_date  ='9999-01-01'
		and ti.to_date = '9999-01-01'
--		and em.emp_no = 32454
    

select emp_no, COUNT(emp_no) 
from cur_emp
group by emp_no
order by COUNT(emp_no) desc

-- get the most current department

select * 
from dept_emp as de
join departments dp
	on de.dept_no = dp.dept_no
where to_date = '9999-01-01'

-- get the most current salary 
select * 
from salaries as sa
where sa.to_date = '9999-01-01'

-- get the most current title
select * 
from title as ti
where ti.to_date = '9999-01-01'

-- get the most department manager
select * 
from dept_manager as dm
where dm.to_date = '9999-01-01'

-- join together
drop view cur_emp;
create view cur_emp as
select 
em.emp_no as emp_no
,em.birth_date
,em.first_name
,em.last_name
,em.gender
,em.hire_date
,dp.dept_name
,sa.salary
,ti.title
,case when dm.emp_no is null then 'No'
else 'Yes' 
end as Department_Manager
from employees em

join (
select emp_no,dept_no
from dept_emp
where to_date = '9999-01-01') de
on em.emp_no = de.emp_no

join departments dp
on dp.dept_no = de.dept_no

join (
select emp_no,salary
from salaries
where to_date = '9999-01-01') sa
on em.emp_no = sa.emp_no

join (
select emp_no,title
from title
where to_date = '9999-01-01') ti
on em.emp_no = ti.emp_no

left join (
select *
from dept_manager
where to_date = '9999-01-01') dm
on em.emp_no = dm.emp_no

-- 4.1.1 integrity check duplication
select emp_no from cur_emp
except
select emp_no from cur_emp_problem

select * from cur_emp
where Id = 111877

-- 4.2 Create view Salary_Trend - use ROW_NUMBER() to investigate the duplicates

-- 4.2.1 talbe 1 as merge salary with title at the exact day

select top(1000) --*
	sa.emp_no
	,sa.salary
	,sa.from_date
	,sa.to_date
	,ti.title
from salaries sa
left outer join title ti
	on sa.emp_no = ti.emp_no and sa.from_date = ti.from_date
order by sa.emp_no, sa.salary

--4.2.1 table 2 as title with not match 
select top(1000) * 
from salaries sa
right join title ti
	on sa.emp_no = ti.emp_no and sa.from_date = ti.from_date
where sa.emp_no is null
order by ti.emp_no, ti.from_date

--4.2.2 create a table and use two  CTE to merge the table
drop table if exists Salary_Title
create table Salary_Title
(
emp_no int,
salary int,
from_date date,
to_date date,
title nvarchar(40)
);

with SA_table as
	(
	select --top(1000) 
		sa.emp_no
		,sa.salary
		,sa.from_date
		,sa.to_date
		,ti.title
	from salaries sa
	left outer join title ti
		on sa.emp_no = ti.emp_no and sa.from_date = ti.from_date
--	order by sa.emp_no, sa.salary
	) 
,TI_table as
	(
	select --top(1000) --*
		ti.emp_no as emp_no
		,ti.title as title
		,ti.from_date as from_date
	from salaries sa
	right join title ti
		on sa.emp_no = ti.emp_no and sa.from_date = ti.from_date
	where sa.emp_no is null
--	order by ti.emp_no, ti.from_date
	)

insert into Salary_Title(emp_no,salary,from_date,to_date,title)

select emp_no,salary,from_date,to_date,title
from SA_table

UNION ALL

select emp_no, null as salary, from_date, null as to_date,title 
from TI_table
order by emp_no, from_date

-- 4.2.3 investigate in individual
select * 
from Salary_Title
--where emp_no = 499996

--4.2.4 create table for salary_trend denormalized table, and drop 

drop table if exists Salary_Titles
create table Salary_Titles
(
emp_no int,
salary int,
from_date date,
to_date date,
title nvarchar(40)
);

with cte as (
	select *
	,case when lead(salary) over (order by emp_no, from_date) is null and lead(from_date) over (order by emp_no, from_date) is not null then lead(from_date) over (order by emp_no, from_date)
		  when to_date is null then lag(to_date) over (partition by emp_no order by from_date)
		  else to_date
		  end as fix_to_date
	,COUNT(title) OVER (PARTITION BY emp_no ORDER BY from_date) as grouper
	,case when salary is null then lag(salary) over(partition by emp_no order by from_date) 
	else salary
	end as fsalary 
	from Salary_Title
--	where emp_no = 110344
--	order by emp_no, from_date
	)

insert into Salary_Titles(emp_no,salary,from_date,to_date,title)

select emp_no
, fsalary as salary
,from_date
,fix_to_date as to_date
, FIRST_VALUE(title) over (partition by emp_no,grouper order by from_date) as title
from cte

drop table Salary_Title

--order by emp_no, from_date;

-- 4.3 Put department into Salary_Titles (save way as above)
-- 4.3.1 

drop table if exists Salary_Title_Department
create table Salary_Title_Department
(
emp_no int,
salary int,
from_date date,
to_date date,
title nvarchar(40),
department nvarchar(40)
);

with ST_table as
	(
	select --top(1000) 
		st.emp_no
		,st.salary
		,st.from_date
		,st.to_date
		,st.title
		,de.dept_no
	from Salary_Titles st
	left outer join dept_emp de
		on st.emp_no = de.emp_no and st.from_date = de.from_date
--	order by st.emp_no, st.salary
	) 
,DE_table as
	(
	select --top(1000) --*
		de.emp_no as emp_no
		,de.dept_no 
		,de.from_date as from_date
	from Salary_Titles st
	right join dept_emp de
		on st.emp_no = de.emp_no and st.from_date = de.from_date
	where st.emp_no is null
--	order by de.emp_no, de.from_date
	)

insert into Salary_Title_Department(emp_no,salary,from_date,to_date,title,department)

select emp_no,salary,from_date,to_date,title,dept_no as department
from ST_table

UNION ALL

select emp_no, null as salary, from_date, null as to_date,null as title , dept_no as department
from DE_table
order by emp_no, from_date


--4.3.2 create table for salary_trend denormalized table, and drop 
--drop table Salary_Titles

drop table if exists Salary_Titles_Dep
create table Salary_Titles_Dep
(
emp_no int,
salary int,
from_date date,
to_date date,
title nvarchar(40),
department nvarchar(40)
);

with cte as (
	select *
	,case when lead(salary) over (order by emp_no, from_date) is null and lead(from_date) over (order by emp_no, from_date) is not null then lead(from_date) over (order by emp_no, from_date)
		  when to_date is null then lag(to_date) over (partition by emp_no order by from_date)
		  else to_date
		  end as fix_to_date
	,COUNT(department) OVER (PARTITION BY emp_no ORDER BY from_date) as grouper
	,case when salary is null then lag(salary) over(partition by emp_no order by from_date) 
	else salary
	end as fsalary 
	,case when title is null then lag(title) over(partition by emp_no order by from_date) 
	else title
	end as ftitle 
	from Salary_Title_Department

--	where emp_no = 110344
--	order by emp_no, from_date
	)

insert into Salary_Titles_Dep(emp_no,salary,from_date,to_date,title,department)

select emp_no
, fsalary as salary
,from_date
,fix_to_date as to_date
,ftitle as title
, FIRST_VALUE(department) over (partition by emp_no,grouper order by from_date) as department

from cte

-- drop temp table

drop table Salary_Title_Department
drop table Salary_Titles

-- 4.3.3 Integrity Check with cur_employee view

select emp_no
from cur_salary_trend
where to_date = '9999-01-01'
except 
select emp_no
from cur_emp

select count(distinct(emp_no))
from Salary_Titles_Dep
where to_date = '9999-01-01'

select count(distinct(emp_no))
from cur_emp

-- 5.0 add column terminated and termination_date into table

-- 5.1 copy the table over as Temp
create table Salary_Titles_Dep_Temp
(
emp_no int,
salary int,
from_date date,
to_date date,
title nvarchar(40),
department nvarchar(40)
);

insert into Salary_Titles_Dep_Temp 
select * from Salary_Titles_Dep

ALTER TABLE Salary_Titles_Dep_Temp
ADD terminated nvarchar(4)

ALTER TABLE Salary_Titles_Dep_Temp
ADD termination_date date

-- 5.2 update the table 

-- clear content
update Salary_Titles_Dep
set terminated = null,termination_date = null;

with table2 as
(
select 
emp_no
,from_date
,case when to_date <> '9999-01-01' and max(to_date) over (partition by emp_no) > to_date then 'No'
      when to_date = '9999-01-01' then 'No'
	  else 'Yes'
	  end as terminated
,case when max(to_date) over (partition by emp_no) = '9999-01-01' then null
      when to_date = max(to_date) over (partition by emp_no) then to_date
	  else null
	  end as termination_date
from Salary_Titles_Dep
)
update Salary_Titles_Dep_Temp 
set Salary_Titles_Dep_Temp.terminated = table2.terminated
	,Salary_Titles_Dep_Temp.termination_date = table2.termination_date
from Salary_Titles_Dep_Temp
join table2 on Salary_Titles_Dep_Temp.emp_no = table2.emp_no and Salary_Titles_Dep_Temp.from_date = table2.from_date

-- integrity check 
select count(distinct(emp_no)) - (select count(distinct(emp_no)) from Salary_Titles_Dep_temp where termination_date is not null)
from Salary_Titles_Dep_temp
--order by emp_no,from_date

-- 5.3 update real table 
ALTER TABLE Salary_Titles_Dep
ADD terminated nvarchar(4)

ALTER TABLE Salary_Titles_Dep
ADD termination_date date

-- 5.4 update the table 

-- clear content
update Salary_Titles_Dep
set terminated = null,termination_date = null;

with table2 as
(
select 
emp_no
,from_date
,case when to_date <> '9999-01-01' and max(to_date) over (partition by emp_no) > to_date then 'No'
      when to_date = '9999-01-01' then 'No'
	  else 'Yes'
	  end as terminated
,case when max(to_date) over (partition by emp_no) = '9999-01-01' then null
      when to_date = max(to_date) over (partition by emp_no) then to_date
	  else null
	  end as termination_date
from Salary_Titles_Dep
)
update Salary_Titles_Dep 
set Salary_Titles_Dep.terminated = table2.terminated
	,Salary_Titles_Dep.termination_date = table2.termination_date
from Salary_Titles_Dep
join table2 on Salary_Titles_Dep.emp_no = table2.emp_no and Salary_Titles_Dep.from_date = table2.from_date

--integrity Check
create table Salary_Titles_Dep_Temp
(
emp_no int,
salary int,
from_date date,
to_date date,
title nvarchar(40),
department nvarchar(40)
);

select count(distinct(emp_no)) - (select count(distinct(emp_no)) from Salary_Titles_Dep where termination_date is not null)
from Salary_Titles_Dep

-- 6.0 fix hire date do not have salary problem
-- 6.1 create a new table 

drop table if exists Salary_Titles_Dep_Hire
create table Salary_Titles_Dep_Hire
(
emp_no int,
salary int,
from_date date,
to_date date,
title nvarchar(40),
department nvarchar(40),
terminated nvarchar(3),
termination_date date
);

-- use the same method to append hire date as a new row
with Hire_Table as
(select em.emp_no, em.hire_date
	--de.emp_no as emp_no
	--,de.dept_no 
	--,de.from_date as from_date
from Salary_Titles_Dep stp
right join employees em
	on stp.emp_no = em.emp_no and stp.from_date = em.hire_date
where stp.emp_no is null
--order by em.emp_no
)

insert into Salary_Titles_Dep_Hire

select emp_no,null as salary, hire_date as from_date, null as to_date,null as title,null as department,null as terminated,null as termination_date
from Hire_Table

union all

select * from Salary_Titles_Dep
order by emp_no,from_date

with cte as
(
select *
,case --when lag(salary) over (order by emp_no, from_date) is null and lag(from_date) over (order by emp_no, from_date) is not null then lag(from_date) over (order by emp_no, from_date)
		  when to_date is null then lead(from_date) over (partition by emp_no order by from_date)
		  else to_date
		  end as fix_to_date
,case when salary is null then lead(salary) over (partition by emp_no order by from_date)
else salary
end as bf_salary
,
case when title is null then lead(title) over (partition by emp_no order by from_date)
else title
end as bf_title
,
case when department is null then lead(department) over (partition by emp_no order by from_date)
else department
end as bf_department
,
case when terminated is null then 'No'
else terminated
end as bf_terminated
from Salary_Titles_Dep_Hire
)

update Salary_Titles_Dep_Hire 
set Salary_Titles_Dep_Hire.salary = cte.bf_salary,
    Salary_Titles_Dep_Hire.to_date = cte.fix_to_date,
	Salary_Titles_Dep_Hire.title = cte.bf_title,
	Salary_Titles_Dep_Hire.department = cte.bf_department,
	Salary_Titles_Dep_Hire.terminated = cte.bf_terminated
from Salary_Titles_Dep_Hire
join cte 
	on Salary_Titles_Dep_Hire.emp_no = cte.emp_no 
	and Salary_Titles_Dep_Hire.from_date = cte.from_date
where Salary_Titles_Dep_Hire.salary is null

-- create view with partition by
drop view if exists STPDwithpartition
create view STPDwithpartition as
(
select *
,row_number() over (partition by emp_no order by from_date) as partitionbyemp_no
from Salary_Titles_Dep_Hire
)