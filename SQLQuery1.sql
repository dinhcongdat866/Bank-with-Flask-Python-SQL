use bank
go


create table AccountInfo(UserID INT IDENTITY(1,1) NOT NULL,AccountId nvarchar(16),Pass nvarchar(16),Amount int)

create table trans(transID INT IDENTITY(1,1) NOT NULL, act nvarchar(50),moment datetime, username_from nvarchar(16), username_to nvarchar(16),amount int)
insert into AccountInfo (AccountID,Pass,Amount) values('abcdef','abcdef','500000')

insert into Admin (AccountID,Pass) values('admin','admin')

drop table AccountInfo