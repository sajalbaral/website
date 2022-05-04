CREATE DATABASE IF NOT EXISTS test;
USE test;

CREATE table account (
	id INT auto_increment,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    primary key (id));
    
CREATE TABLE post (
	post_id INT auto_increment,
    account_id INT NOT NULL,
    caption VARCHAR(255) NOT NULL,
    photo_link VARCHAR(255),
    date_posted VARCHAR(255) NOT NULL,
    primary key (post_id),
    FOREIGN KEY (account_id) REFERENCES account(id)
);