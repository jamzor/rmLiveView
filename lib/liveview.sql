CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE Masters(
	m_id UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
	username TEXT UNIQUE NOT NULL,
	pw_salty TEXT NOT NULL,
	salt TEXT NOT NULL,
	email TEXT NOT NULL,
	enabled BOOL DEFAULT FALSE,
	created TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP
);

CREATE TABLE Companies(
	c_id UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
	company_name TEXT UNIQUE NOT NULL,
	clients INT DEFAULT 0,
	agents INT DEFAULT 0,
	devices INT DEFAULT 0,
	markers INT DEFAULT 0,
	enabled BOOL DEFAULT FALSE,
	created TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP
);

CREATE TABLE Clients(
	u_id UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
	username TEXT UNIQUE NOT NULL,
	pw_salty TEXT NOT NULL,
	salt TEXT NOT NULL,
	email TEXT NOT NULL,
	confirmed BOOL DEFAULT FALSE,
	company_id UUID REFERENCES Companies(c_id),
	company_name TEXT NOT NULL,
	enabled BOOL DEFAULT FALSE,
	created TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP
);

CREATE TABLE Agents(
	a_id UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
	agent_name TEXT UNIQUE NOT NULL,
	pw TEXT NOT NULL, /*Need to figure out a safe two-way encryption method*/
	company_id UUID REFERENCES Companies(c_id),
	company_name TEXT NOT NULL,
	created TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP,
    last_session TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP
);

CREATE TABLE Devices(
	d_id UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
	device_name TEXT NOT NULL,
	company_id UUID REFERENCES Companies(c_id),
	company_name TEXT NOT NULL,
	agent_id UUID REFERENCES Agents(a_id),
	agent_name TEXT NOT NULL,
	created TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP
);

CREATE TABLE Markers(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
    title TEXT UNIQUE NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
	company_id UUID REFERENCES Companies(c_id),
	company_name TEXT NOT NULL,
	device_id TEXT NOT NULL,
	device_name TEXT NOT NULL,
    device_address TEXT NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP,
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now()::TIMESTAMP
);