-- delete and create database
DROP DATABASE IF EXISTS task_scheme;

CREATE DATABASE task_scheme;

USE task_scheme;

-- create table for users
CREATE TABLE users (
    id int NOT NULL AUTO_INCREMENT UNIQUE,
    name varchar(64),
    surname varchar(64),
    login varchar(64) NOT NULL UNIQUE,
    password varchar(64) NOT NULL,
    PRIMARY KEY (id)
);

-- table for tasks
CREATE TABLE tasks (
    id int NOT NULL AUTO_INCREMENT UNIQUE,
    title varchar(128),
    start datetime DEFAULT CURRENT_TIMESTAMP,
    stop datetime,
    description varchar(1024),
    PRIMARY KEY (id)
);

-- table for relation user > tast
CREATE TABLE user_task_relation (
    id int NOT NULL AUTO_INCREMENT UNIQUE,
    user_id int,
    task_id int,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

-- table for active sessions
CREATE TABLE user_sessions (
    id int NOT NULL AUTO_INCREMENT UNIQUE,
    user_id int,
    token varchar(64),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);