select * 
from Housing.dbo.NashHousing

-- standardize Date Format, use alter and update

select SaleDate, CONVERT(Date,SaleDate) as Sale_Date
from Housing.dbo.NashHousing

alter table Housing.dbo.NashHousing
add SaleDateConverted Date;

update Housing.dbo.NashHousing
set SaleDateConverted = CONVERT(Date,SaleDate)

-- Populate Property Address data
-- 1. visual the null

select *
from Housing.dbo.NashHousing
where PropertyAddress is null

-- 2. fill the Property Address refer to ParcellID use self join and use isnull to fill the address Null
select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, isnull(a.PropertyAddress,b.PropertyAddress)
from Housing.dbo.NashHousing a
join Housing.dbo.NashHousing b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null

-- 3.fill the na

update a 
set PropertyAddress = isnull(a.PropertyAddress,b.PropertyAddress)
from Housing.dbo.NashHousing a
join Housing.dbo.NashHousing b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null

-- Breaking out Address into Individual Columns (Address, City, State)

select PropertyAddress
from Housing.dbo.NashHousing

-- 1. split the address by ,

SELECT 
SUBSTRING(PropertyAddress, 1, CHARINDEX(',',PropertyAddress) -1 ) as Address 
, SUBSTRING(PropertyAddress, CHARINDEX(',',PropertyAddress) +1, len(PropertyAddress) ) as Address
from Housing.dbo.NashHousing

-- 2. update split

alter table Housing.dbo.NashHousing
add PropertySplitAddress Nvarchar(255);

update Housing.dbo.NashHousing
set PropertySplitAddress = SUBSTRING(PropertyAddress, 1, CHARINDEX(',',PropertyAddress) -1 );

alter table Housing.dbo.NashHousing
add PropertySplitCity Nvarchar(255);

update Housing.dbo.NashHousing
set PropertySplitCity = SUBSTRING(PropertyAddress, CHARINDEX(',',PropertyAddress) +1, len(PropertyAddress) );


select *
from Housing.dbo.NashHousing

-- 2.1 split owner's address,  alternative way parsename take . only, so need to replace the .
select 
PARSENAME(REPLACE(OwnerAddress,',','.'),3),
PARSENAME(REPLACE(OwnerAddress,',','.'),2),
PARSENAME(REPLACE(OwnerAddress,',','.'),1)
from Housing.dbo.NashHousing

-- 2.2 update owner address

alter table Housing.dbo.NashHousing
add OwnerSplitAddress Nvarchar(255);

update Housing.dbo.NashHousing
set OwnerSplitAddress = PARSENAME(REPLACE(OwnerAddress,',','.'),3);

alter table Housing.dbo.NashHousing
add OwnerSplitCity Nvarchar(255);

update Housing.dbo.NashHousing
set OwnerSplitCity = PARSENAME(REPLACE(OwnerAddress,',','.'),2);

alter table Housing.dbo.NashHousing
add OwnerSplitState Nvarchar(5);

update Housing.dbo.NashHousing
set OwnerSplitState = PARSENAME(REPLACE(OwnerAddress,',','.'),1);

select *
from Housing.dbo.NashHousing

-- Change Y and N to Yes and No in "Solid as Vacant" Field, use CWEE

select distinct(SoldAsVacant) , count(SoldAsVacant)
from Housing.dbo.NashHousing
group by SoldAsVacant
order by 2 desc

select SoldAsVacant
, CASE when SoldAsVacant = 'Y' then 'Yes'
	   when SoldAsVacant = 'N' then 'No'
	   else SoldAsVacant
	   End
from Housing.dbo.NashHousing

update Housing.dbo.NashHousing
set SoldAsVacant = 
	CASE when SoldAsVacant = 'Y' then 'Yes'
	   when SoldAsVacant = 'N' then 'No'
	   else SoldAsVacant
	   End

-- Remove Deuplicates

-- 1. use window function to find the duplicate row

select *,
	ROW_NUMBER() OVER ( 
	PARTITION BY ParcelID,
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 ORDER BY 
					UniqueID
					) row_num
from Housing.dbo.NashHousing

-- 2.use CTE and where to see the duplicate rows
with RowNumCTE as(
	select *,
		ROW_NUMBER() OVER ( 
		PARTITION BY ParcelID,
					 PropertyAddress,
					 SalePrice,
					 SaleDate,
					 LegalReference
					 ORDER BY 
						UniqueID
						) row_num
	from Housing.dbo.NashHousing
)
DELETE
from RowNumCTE
where row_num >1

-- remove unused column

select * 
from Housing.dbo.NashHousing 

alter table Housing.dbo.NashHousing 
drop column PropertyAddress, SaleDate, OwnerAddress, TaxDistrict
