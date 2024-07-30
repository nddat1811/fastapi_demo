-- Creating table SYS_USER
DROP TABLE IF EXISTS SYS_USER;
CREATE TABLE SYS_USER (
    id INT PRIMARY KEY ,
    username VARCHAR(255) UNIQUE NOT NULL,
    hash_password VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    full_name VARCHAR(255),
    status NUMERIC,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT, -- id user who created new user
    updated_by INT  -- id user who updated user
)  ;

-- Creating table SYS_ROLE
DROP TABLE IF EXISTS SYS_ROLE;
CREATE TABLE SYS_ROLE (
    id INT PRIMARY KEY ,
    name VARCHAR(255),
    description VARCHAR(255),
    status NUMERIC,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT, -- id user who created new role
    updated_by INT  -- id user who updated role
)  ;

-- Creating table SYS_USER_ROLE
DROP TABLE IF EXISTS SYS_USER_ROLE;
CREATE TABLE SYS_USER_ROLE (
    id INT PRIMARY KEY ,
    user_id INT,
    role_id INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT, -- id user who created new user role
    FOREIGN KEY (user_id) REFERENCES SYS_USER(id),
    FOREIGN KEY (role_id) REFERENCES SYS_ROLE(id)
)  ;

-- Creating table SYS_FUNCTION
DROP TABLE IF EXISTS SYS_FUNCTION;
CREATE TABLE SYS_FUNCTION (
    id INT PRIMARY KEY ,
    name VARCHAR(255),
    path VARCHAR(255),
    description VARCHAR(255),
    parent_id INT,
    type VARCHAR(50),
    status NUMERIC, -- 0 - ok, 1 - stop
    icon_url VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT, -- id user who created new function
    updated_by INT, -- id user who updated function
    FOREIGN KEY (parent_id) REFERENCES SYS_FUNCTION(id)
)  ;

-- Creating table SYS_ROLE_FUNCTION
DROP TABLE IF EXISTS SYS_ROLE_FUNCTION;
CREATE TABLE SYS_ROLE_FUNCTION (
    id INT PRIMARY KEY ,
    role_id INT,
    function_id INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT, -- id user who created new role function
    FOREIGN KEY (role_id) REFERENCES SYS_ROLE(id),
    FOREIGN KEY (function_id) REFERENCES SYS_FUNCTION(id)
)  ;

-- Creating table SYS_LOG
DROP TABLE IF EXISTS SYS_LOG;
CREATE TABLE SYS_LOG (
    id INT PRIMARY KEY,
    action_datetime TIMESTAMP,
    path_name VARCHAR(255),
    method VARCHAR(50),
    ip VARCHAR(50),
    status_response VARCHAR(50), -- http status response
    response VARCHAR(255),  -- msg response
    description VARCHAR(255),
    request VARCHAR(255),   -- body query
    duration FLOAT -- time from request to response
)  ;

-- Creating table DATA_DICTIONARY
DROP TABLE IF EXISTS DATA_DICTIONARY;
CREATE TABLE DATA_DICTIONARY (
    id INT PRIMARY KEY,
    table_name VARCHAR(255),
    column_name VARCHAR(255),
    description VARCHAR(255),
    value INT  -- enum for each column name
)  ;
