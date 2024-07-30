-- Creating table SYS_USER
DROP TABLE IF EXISTS "SYS_USER";
CREATE TABLE "SYS_USER" (
    id SERIAL PRIMARY KEY ,
    username VARCHAR(255) UNIQUE NOT NULL,
    hash_password VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    full_name VARCHAR(255),
    status INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT, -- id user who created new user
    updated_by INT  -- id user who updated user
)  ;

-- Creating table SYS_ROLE
DROP TABLE IF EXISTS "SYS_ROLE";
CREATE TABLE "SYS_ROLE" (
    id SERIAL PRIMARY KEY ,
    name VARCHAR(255),
    description VARCHAR(255),
    status INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT, -- id user who created new role
    updated_by INT  -- id user who updated role
)  ;

-- Creating table SYS_USER_ROLE
DROP TABLE IF EXISTS "SYS_USER_ROLE";
CREATE TABLE "SYS_USER_ROLE" (
    id SERIAL PRIMARY KEY ,
    user_id INT,
    role_id INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT, -- id user who created new user role
    FOREIGN KEY (user_id) REFERENCES "SYS_USER"(id),
    FOREIGN KEY (role_id) REFERENCES "SYS_ROLE"(id)
)  ;

-- Creating table SYS_FUNCTION
DROP TABLE IF EXISTS "SYS_FUNCTION";
CREATE TABLE "SYS_FUNCTION" (
    id SERIAL PRIMARY KEY ,
    name VARCHAR(255),
    path VARCHAR(255),
    description VARCHAR(255),
    parent_id INT,
    type VARCHAR(50),
    status INT,
    icon_url VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT, -- id user who created new function
    updated_by INT, -- id user who updated function
    FOREIGN KEY (parent_id) REFERENCES "SYS_FUNCTION"(id)
)  ;

-- Creating table SYS_ROLE_FUNCTION
DROP TABLE IF EXISTS "SYS_ROLE_FUNCTION";
CREATE TABLE "SYS_ROLE_FUNCTION" (
    id SERIAL PRIMARY KEY ,
    role_id INT,
    function_id INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT, -- id user who created new role function
    FOREIGN KEY (role_id) REFERENCES "SYS_ROLE"(id),
    FOREIGN KEY (function_id) REFERENCES "SYS_FUNCTION"(id)
)  ;

-- Creating table SYS_LOG
DROP TABLE IF EXISTS "SYS_LOG";
CREATE TABLE "SYS_LOG" (
    id SERIAL PRIMARY KEY,
    action_datetime TIMESTAMP,
    path_name VARCHAR(255),
    method VARCHAR(50),
    ip VARCHAR(50),
    status_response INT, -- http status response
    response TEXT,  -- msg response
    description VARCHAR(255),
    request_body TEXT,   -- body
    request_query TEXT,   -- query
    duration FLOAT -- time from request to response
)  ;

-- Creating table DATA_DICTIONARY
DROP TABLE IF EXISTS "DATA_DICTIONARY";
CREATE TABLE "DATA_DICTIONARY" (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(255),
    column_name VARCHAR(255),
    description VARCHAR(255),
    value INT  -- enum for each column name
);
