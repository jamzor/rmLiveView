/*INSERT INTO Marker (name,latitude,longitude,link) VALUES ('Calgary', 51.0486, -114.0708, 'http://www.calgary.ca');
INSERT INTO Marker (name,latitude,longitude,link) VALUES ('Edmonton', 53.5557952, -113.6343729, 'http://www.edmonton.ca');
INSERT INTO Marker (name,latitude,longitude,link) VALUES ('Grande Prairie', 55.1597369, -118.8906059, 'http://www.cityofgp.ca');
INSERT INTO Marker (name,latitude,longitude,link) VALUES ('Fort McMurray', 56.704919, -111.3705794, 'http://www.fortmcmurraytourism.com');
INSERT INTO Marker (name,latitude,longitude,link) VALUES ('High Level', 58.5066893, -117.1660949, 'http://www.highlevel.ca');
INSERT INTO Marker (name,latitude,longitude,link) VALUES ('Red Deer', 52.2666952, -113.8743034, 'http://www.reddeer.ca');
INSERT INTO Marker (name,latitude,longitude,link) VALUES ('Lethbridge', 49.6880468, -112.9162765, 'http://www.lethbridge.ca');

INSERT INTO UserAgent(username,password,device) VALUES ('gamtech','gamtech','192.168.99.200');*/

/*Masters*/
INSERT INTO Masters (username,pw_salty,salt,email) VALUES ('james', 'pass hash', 'pass salt', 'james.macisaac@gamtech.ca');

/*Companies*/
INSERT INTO Companies(company_name,enabled) VALUES ('Somewhere Ltd.', TRUE);

/*Clients*/
INSERT INTO Clients (username,pw_salty,salt,email,confirmed,company,enabled) VALUES ('someone', 'pass hash', 'pass salt', 'somebody@somewhere.com',TRUE,(SELECT c_id FROM Companies WHERE company_name = 'Somewhere Ltd.' LIMIT 1),TRUE);

