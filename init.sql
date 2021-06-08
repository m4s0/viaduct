CREATE TABLE user
(
    id       INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(180) NOT NULL
);

CREATE TABLE api_key
(
    id      INT AUTO_INCREMENT PRIMARY KEY,
    value   VARCHAR(255) NOT NULL,
    user_id INT          NOT NULL,
    CONSTRAINT api_key_value_uindex UNIQUE (value),
    CONSTRAINT api_key_user_id_fk FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE api_key_usage
(
    used_at    datetime NULL,
    api_key_id INT NOT NULL,
    CONSTRAINT api_key_usage_api_key_id_fk FOREIGN KEY (api_key_id) REFERENCES api_key (id)
);

INSERT INTO user (username)
VALUES ('m4s0');

INSERT INTO api_key (value, user_id)
VALUES ('api-key', 1);