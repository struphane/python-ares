-- team table
CREATE TABLE team_def (
 team_id integer PRIMARY KEY AUTOINCREMENT,
 team_name text NOT NULL UNIQUE,
 role text DEFAULT 'Normal',
 crea_dt timestamp DEFAULT CURRENT_TIMESTAMP
);

-- file_map table
CREATE TABLE file_map (
 file_id integer PRIMARY KEY AUTOINCREMENT,
 alias text NOT NULL,
 file_type text NOT NULL,
 disk_name text NOT NULL UNIQUE,
 crea_dt text timestamp DEFAULT CURRENT_TIMESTAMP
);

--file_auth table
CREATE TABLE file_auth (
 file_id integer,
 team_id integer,
 stt_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 end_dt timestamp NOT NULL DEFAULT (datetime('now', '+30 days')),
 CONSTRAINT FK_FilemapFileauth FOREIGN KEY (file_id) REFERENCES file_map(file_id),
 CONSTRAINT FK_UseraccntFileauth FOREIGN KEY (team_id) REFERENCES team_def(team_id)
);

--env_def table
CREATE TABLE env_def (
 env_id integer PRIMARY KEY AUTOINCREMENT,
 env_name text NOT NULL UNIQUE,
 cmm text,
 crea_dt timestamp DEFAULT CURRENT_TIMESTAMP
);

--env_auth table
CREATE TABLE env_auth (
 env_id integer,
 team_id integer,
 stt_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 end_dt timestamp NOT NULL DEFAULT (datetime('now', '+30 days')),
 CONSTRAINT FK_EnvDefEnvAuth FOREIGN KEY (env_id) REFERENCES env_def(env_id),
 CONSTRAINT FK_UserAccntEnvAuth FOREIGN KEY (team_id) REFERENCES team_def(team_id)
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
 email text NOT NULL,
 team_name NOT NULL,
 env_id text NOT NULL,
 script text NOT NULL,
 lst_mod_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CONSTRAINT FK_EnvDefLogsCon FOREIGN KEY (env_id) REFERENCES env_def(env_id)
 );

--logs deployment
CREATE TABLE logs_deploy (
 email text NOT NULL,
 team_name NOT NULL,
 folder text NOT NULL,
 file text NOT NULL,
 type text NOT NULL,
 lst_mod_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
 );