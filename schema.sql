create database gamedb;
use gamedb;
create table userdb(username varchar(20) primary key, password varchar(100) not null, money float not null, admin varchar(1) default 'F', banned date default NULL);
create table usermsgs(sender varchar(20) not null,recipient varchar(20) not null, message varchar(1024) not null, IsRead varchar(1) default 'F', MsgTimeStamp datetime default current_timestamp, foreign key (sender) references userdb (username),foreign key (recipient) references userdb (username));
insert into userdb values('admin','admin123',1.175494351E+38,'T',null);
