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

-- 4.1 create view all_current_status
drop view cur_emp;
create view cur_emp as
	select  
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
	left join salaries as sa
		on em.emp_no = sa.emp_no
	left join dept_manager as dm
		on em.emp_no = dm.emp_no
	left join title as ti
		on em.emp_no = ti.emp_no
	where de.to_date = '9999-01-01'
		and sa.to_date = '9999-01-01'
		and (dm.to_date = '9999-01-01' or dm.to_date  is null)
		and ti.to_date = '9999-01-01'
--    order by 1

-- 4.1.1 integrity check duplication
select distinct(emp_no),count(emp_no) 
from cur_emp
group by emp_no
order by 2 desc

-- 4.2.1 Create view Salary_Trend - use ROW_NUMBER() to investigate the duplicates

select *
, ROW_NUMBER() over (partition by em.emp_no,sa.salary,sa.from_date,ti.title order by em.emp_no)
	--em.emp_no
	--,em.birth_date
	--,em.first_name
	--,em.last_name
	--,em.gender
	--,em.hire_date
	--,dp.dept_name
	--,sa.salary
	--,ti.title
from employees em
left join dept_emp de
	on em.emp_no = de.emp_no
join departments as dp
	on de.dept_no = dp.dept_no
left join salaries as sa
	on em.emp_no = sa.emp_no
left join dept_manager as dm
	on em.emp_no = dm.emp_no
left join title as ti
	on em.emp_no = ti.emp_no
where (sa.from_date >= ti.from_date and sa.to_date <= ti.to_date) and
      (sa.from_date >= de.from_date and sa.to_date <= de.to_date)

order by ROW_NUMBER() over (partition by em.emp_no,sa.salary,ti.title order by em.emp_no) desc, em.emp_no 

-- 4.2.2 Create view Salary_Trend - use below to investigate individual employee, and see why the duplicate happened

select top(1000) *
from employees em
left join dept_emp de
	on em.emp_no = de.emp_no
join departments as dp
	on de.dept_no = dp.dept_no
left join salaries as sa
	on em.emp_no = sa.emp_no
left join dept_manager as dm
	on em.emp_no = dm.emp_no
left join title as ti
	on em.emp_no = ti.emp_no
where (sa.from_date >= ti.from_date and sa.to_date <= ti.to_date) and
      (sa.from_date >= de.from_date and sa.to_date <= de.to_date)
and em.emp_no = 17853
order by em.emp_no , sa.from_date

-- 4.2.3 Create view Salary_Trend
drop view salary_trend
create view salary_trend as
select 
	em.emp_no 
	,em.birth_date
	,em.first_name
	,em.last_name
	,em.gender
	,em.hire_date
	,de.from_date as dept_from_date
	,de.to_date as dept_to_date
	,dp.dept_name
	,sa.salary 
	,sa.from_date as salary_from_date
	,sa.to_date as salary_to_date
	,ti.title
	,ti.from_date as title_from_date
	,ti.to_date as title_to_date
	,max(sa.to_date) over (partition by em.emp_no) as termination_date
	,case when max(sa.to_date) over (partition by em.emp_no) = '9999-01-01' then 'Active'
		else 'Inactive'
		end as terminated 
from employees em
left join dept_emp de
	on em.emp_no = de.emp_no
join departments as dp
	on de.dept_no = dp.dept_no
left join salaries as sa
	on em.emp_no = sa.emp_no
left join dept_manager as dm
	on em.emp_no = dm.emp_no
left join title as ti
	on em.emp_no = ti.emp_no
where (sa.from_date >= ti.from_date and sa.to_date <= ti.to_date) and
      (sa.from_date >= de.from_date and sa.to_date <= de.to_date)


