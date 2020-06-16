create database retailbanking;
use retailbanking;
create table customerstatus( ssnid int, customerid int, status varchar(20), message varchar(20));
ALTER TABLE customerstatus ADD lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
create table accountstatus(customerid int, accountid int, accounttype varchar(30),status varchar(20), message varchar(20));
ALTER TABLE accountstatus ADD lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE customerstatus ADD PRIMARY KEY (customerid);
ALTER TABLE accountstatus ADD PRIMARY KEY (customerid);


create table customerdetails(ssnid int,customername varchar(30),age int, address varchar(100),state char(20), city char(20));

alter table accounts add lastupdated varchar(30);


create table createaccount( customerid int, accounttype varchar(20),depositamount int);

create table accountstatement(trasid int,des varchar(10),date DATE, amount int);

create table balanceamount( accountid int,finalamount int);

alter table customerdetails add customerid int;

insert into customerdetails values(113458969,'rajesh',21,'nce','tm','kodak',147852371);

ALTER TABLE accountstatus DROP PRIMARY KEY;
ALTER TABLE accountstatus ADD PRIMARY KEY (accountid);
ALTER TABLE accountstatus ADD CONSTRAINT fk_id FOREIGN KEY (customerid) REFERENCES customerstatus(customerid);
create table accounts(customerid int, accountid int, accounttype varchar(20), amt int);
ALTER TABLE accounts ADD CONSTRAINT fk_id FOREIGN KEY (customerid) REFERENCES customerstatus(customerid);


insert into accounts values(113458969,131245875,'savings',1500,'2018-02-15');


alter table accounts drop lastupdated;
ALTER TABLE accounts ADD lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP;


alter table balanceamount add customerid int;



ALTER TABLE accountstatement CHANGE trasid transid INT(10 )AUTO_INCREMENT PRIMARY KEY;


insert into accountstatement values(258967,'CREDIT','2018-02-09',1500,131245877);


drop table balanceamount;


alter table accountstatement drop date;
ALTER TABLE accountstatement ADD date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;