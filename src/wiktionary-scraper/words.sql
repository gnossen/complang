create database words;
use words;
create table words (
    id int not null primary key auto_increment,
    word varchar(128) not null,
    ipa varchar(128),
    language varchar(64) not null,
    url_retrieved varchar(256) not null,
    retrieved datetime not null
);
