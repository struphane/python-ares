-- usr_accnt table
CREATE TABLE user_accnt (
 uid integer PRIMARY KEY AUTOINCREMENT,
 email_addr text NOT NULL UNIQUE,
 hash_id text NOT NULL,
 role text DEFAULT 'Normal',
 crea_dt timestamp DEFAULT CURRENT_TIMESTAMP
);

-- file_map table
CREATE TABLE file_map (
 file_id integer PRIMARY KEY AUTOINCREMENT,
 alias text NOT NULL,
 disk_name text NOT NULL,
 crea_dt text timestamp DEFAULT CURRENT_TIMESTAMP
);

--file_auth table
CREATE TABLE file_auth (
 file_id integer,
 uid integer,
 stt_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 end_dt timestamp NOT NULL DEFAULT (datetime('now', '+30 days')),
 CONSTRAINT FK_FilemapFileauth FOREIGN KEY (file_id) REFERENCES file_map(file_id),
 CONSTRAINT FK_UseraccntFileauth FOREIGN KEY (uid) REFERENCES user_accnt(uid)
);

--env_def table
CREATE TABLE env_def (
 env_id integer PRIMARY KEY AUTOINCREMENT,
 env_name text NOT NULL UNIQUE,
 crea_dt timestamp DEFAULT CURRENT_TIMESTAMP
);

--env_auth table
CREATE TABLE env_auth (
 env_id integer,
 uid integer,
 stt_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 end_dt timestamp NOT NULL DEFAULT (datetime('now', '+30 days')),
 CONSTRAINT FK_EnvDefEnvAuth FOREIGN KEY (env_id) REFERENCES env_def(env_id),
 CONSTRAINT FK_UserAccntEnvAuth FOREIGN KEY (uid) REFERENCES user_accnt(uid)
);

--mrx_calls table
CREATE TABLE mrx_calls (
 hash_id text PRIMARY KEY,
 screen_id integer NOT NULL,
 param_string text NOT NULL,
 dynamic_params text,
 calling_mode text NOT NULL
);

--logs connection
CREATE TABLE logs_con (
 date text,
 folder text,
 report text,
 lst_mod_dt timestamp
 );

--logs deployment
CREATE TABLE logs_deploy (
 date text,
 folder text,
 script text,
 address text,
 lst_mod_dt timestamp
 );