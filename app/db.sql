CREATE TABLE IF NOT EXISTS blacklist (
    tokens character varying(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    password character varying(500) NOT NULL,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
);

CREATE TABLE IF NOT EXISTS films (
    film_id serial PRIMARY KEY NOT NULL,
    title character varying(100) NOT NULL,
    description character varying(300)  NOT NULL,
    flag character varying(20)  NOT NULL,
    recommendation character varying(20)  NOT NULL,
    rating numeric (1) NULL,
    type character varying(10) NOT NULL,
    archive numeric (1) DEFAULT 0,
    created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
 );

 CREATE TABLE IF NOT EXISTS comentrate (
    comment_id serial PRIMARY KEY NOT NULL,
    movie_id numeric NOT NULL,
    created_by character varying(20) NOT NULL,
    comment character varying(1000) NOT NULL,
    rating numeric NOT NULL,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
);