--CREATE SCHEMA lyfter_car_rental


/*
CREATE TABLE lyfter_car_rental.users (
    id SERIAL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    email VARCHAR(35) UNIQUE NOT NULL,
    username VARCHAR(20) UNIQUE NOT NULL,
    "password" VARCHAR(15) NOT NULL,
    birth_date DATE NOT NULL,
    account_status VARCHAR(20) NOT NULL
);
*/
/*
INSERT INTO lyfter_car_rental.users (name, email, username, password, birth_date, account_status) 
VALUES 
    ('John Doe', 'johndoe1@example.com', 'johndoe1', 'password123', '1990-05-15', 'active'),
    ('Jane Smith', 'janesmith2@example.com', 'janesmith2', 'password123', '1988-03-22', 'active'),
    ('Alice Brown', 'alicebrown3@example.com', 'alicebrown3', 'password123', '1992-07-10', 'inactive'),
    ('Bob Johnson', 'bobjohnson4@example.com', 'bobjohnson4', 'password123', '1985-11-30', 'active'),
    ('Charlie Davis', 'charliedavis5@example.com', 'charliedavis5', 'password123', '1994-12-01', 'suspended'),
    ('David Wilson', 'davidwilson6@example.com', 'davidwilson6', 'password123', '1987-01-13', 'active'),
    ('Emily Clark', 'emilyclark7@example.com', 'emilyclark7', 'password123', '1995-09-05', 'inactive'),
    ('Frank Harris', 'frankharris8@example.com', 'frankharris8', 'password123', '1980-02-20', 'active'),
    ('Grace Walker', 'gracewalker9@example.com', 'gracewalker9', 'password123', '1991-10-25', 'suspended'),
    ('Helen Lewis', 'helenlewis10@example.com', 'helenlewis10', 'password123', '1993-04-17', 'active'),
    ('Ian Robinson', 'ianrobinson11@example.com', 'ianrobinson11', 'password123', '1990-06-09', 'inactive'),
    ('Jack Young', 'jackyoung12@example.com', 'jackyoung12', 'password123', '1986-05-14', 'active'),
    ('Kelly King', 'kellyking13@example.com', 'kellyking13', 'password123', '1996-08-30', 'active'),
    ('Liam Scott', 'liamscott14@example.com', 'liamscott14', 'password123', '1989-12-25', 'suspended'),
    ('Megan Adams', 'meganadams15@example.com', 'meganadams15', 'password123', '1992-02-28', 'active'),
    ('Nathaniel Turner', 'nathanielturner16@example.com', 'nathanielturner16', 'password123', '1988-01-18', 'inactive'),
    ('Olivia Moore', 'oliviamoore17@example.com', 'oliviamoore17', 'password123', '1995-07-12', 'active'),
    ('Paul Mitchell', 'paulmitchell18@example.com', 'paulmitchell18', 'password123', '1987-09-24', 'suspended'),
    ('Quincy Perez', 'quincyperez19@example.com', 'quincyperez19', 'password123', '1994-05-03', 'active'),
    ('Rachel Carter', 'rachelcarter20@example.com', 'rachelcarter20', 'password123', '1993-11-18', 'inactive'),
    ('Sam Reed', 'samreed21@example.com', 'samreed21', 'password123', '1991-01-14', 'active'),
    ('Tina Bell', 'tinabell22@example.com', 'tinabell22', 'password123', '1990-04-09', 'suspended'),
    ('Ursula Evans', 'ursulaevans23@example.com', 'ursulaevans23', 'password123', '1996-06-21', 'active'),
    ('Victor Murphy', 'victormurphy24@example.com', 'victormurphy24', 'password123', '1985-10-02', 'inactive'),
    ('Wendy Simmons', 'wendysimmons25@example.com', 'wendysimmons25', 'password123', '1992-08-17', 'active'),
    ('Xander Fisher', 'xanderfisher26@example.com', 'xanderfisher26', 'password123', '1989-12-05', 'active'),
    ('Yasmine Gray', 'yasminegray27@example.com', 'yasminegray27', 'password123', '1994-11-22', 'suspended'),
    ('Zachary Garcia', 'zacharygarcia28@example.com', 'zacharygarcia28', 'password123', '1986-02-15', 'active'),
    ('Aaron Walker', 'aaronwalker29@example.com', 'aaronwalker29', 'password123', '1983-06-30', 'inactive'),
    ('Betty Morris', 'bettymorris30@example.com', 'bettymorris30', 'password123', '1990-03-14', 'active'),
    ('Carlos Green', 'carlosgreen31@example.com', 'carlosgreen31', 'password123', '1992-12-12', 'active'),
    ('Diana Allen', 'dianaallen32@example.com', 'dianaallen32', 'password123', '1991-09-07', 'inactive'),
    ('Eric King', 'ericking33@example.com', 'ericking33', 'password123', '1988-10-14', 'active'),
    ('Fiona Carter', 'fionacarter34@example.com', 'fionacarter34', 'password123', '1993-04-02', 'active'),
    ('Gordon Scott', 'gordonscott35@example.com', 'gordonscott35', 'password123', '1987-03-23', 'suspended'),
    ('Holly Green', 'hollygreen36@example.com', 'hollygreen36', 'password123', '1995-08-17', 'active'),
    ('Isaac Martin', 'isaacmartin37@example.com', 'isaacmartin37', 'password123', '1984-07-10', 'inactive'),
    ('Julia Perez', 'juliaperez38@example.com', 'juliaperez38', 'password123', '1991-02-04', 'active'),
    ('Kyle Lopez', 'kylelopez39@example.com', 'kylelopez39', 'password123', '1990-11-12', 'suspended'),
    ('Laura Turner', 'lauraturner40@example.com', 'lauraturner40', 'password123', '1989-05-27', 'active'),
    ('Mike Collins', 'mikecollins41@example.com', 'mikecollins41', 'password123', '1992-09-19', 'inactive'),
    ('Nina Wright', 'ninawright42@example.com', 'ninawright42', 'password123', '1994-04-14', 'active'),
    ('Oscar Hill', 'oscarhill43@example.com', 'oscarhill43', 'password123', '1996-12-05', 'suspended'),
    ('Paula Bell', 'paulabell44@example.com', 'paulabell44', 'password123', '1990-07-22', 'active'),
    ('Quinn Young', 'quinnyoung45@example.com', 'quinnyoung45', 'password123', '1985-10-29', 'inactive'),
    ('Riley Clark', 'rileyclark46@example.com', 'rileyclark46', 'password123', '1993-08-05', 'active'),
    ('Sophie Green', 'sophiegreen47@example.com', 'sophiegreen47', 'password123', '1989-01-09', 'suspended'),
    ('Tom Hall', 'tomhall48@example.com', 'tomhall48', 'password123', '1994-07-15', 'active'),
    ('Una Lee', 'unalee49@example.com', 'unalee49', 'password123', '1992-11-23', 'inactive'),
    ('Vera Evans', 'veraevans50@example.com', 'veraevans50', 'password123', '1991-06-28', 'active');





CREATE TABLE lyfter_car_rental.vehicle_model(
	id SERIAL PRIMARY KEY,
	make VARCHAR(100) NOT NULL,
	model VARCHAR(70) NOT NULL,
	year INT NOT NULL
);


CREATE TABLE lyfter_car_rental.vehicles(
	id SERIAL PRIMARY KEY,
	vin VARCHAR(20) UNIQUE NOT NULL,
	model_id INT references lyfter_car_rental.vehicle_model(id) ON DELETE CASCADE ON UPDATE CASCADE,
	status VARCHAR(25)
);



INSERT INTO lyfter_car_rental.vehicle_model (make, model, year) VALUES
('Toyota', 'Corolla', 2020),
('Honda', 'Civic', 2019),
('Ford', 'Focus', 2021),
('Chevrolet', 'Malibu', 2022),
('Nissan', 'Altima', 2020);


INSERT INTO lyfter_car_rental.vehicle (vin, model_id, status) VALUES
('1HGCM82633A123456', 1, 'available'),
('1FAFP34N87W123456', 2, 'maintenance'),
('3N1AB7AP5KY123456', 3, 'available'),
('2G1WF55E369123456', 4, 'unavailable'),
('1N4AL3AP5HC123456', 5, 'available');



CREATE TABLE lyfter_car_rental.vehicle_user(
	id SERIAL PRIMARY KEY,
	rental_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	rental_status VARCHAR(25) NOT NULL,
	vehicle_id INT NOT NULL REFERENCES lyfter_car_rental.vehicles(id) ON DELETE CASCADE ON UPDATE CASCADE,
	user_id INT NOT NULL REFERENCES lyfter_car_rental.users(id) ON DELETE CASCADE ON UPDATE CASCADE,
	UNIQUE (vehicle_id, user_id)
);
*/

--################### TAREA 2 ###############################################################################################

/*
INSERT INTO lyfter_car_rental.users(name, email, username, password, birth_date, account_status)
VALUES ('Nickole Morales', 'nickomorales@gmail.com', 'nickou', 'nicko123', '2002-09-26', 'active');

INSERT INTO lyfter_car_rental.vehicles(vin, model_id, status)
VALUES ('21SDDFD54EFW', 5, 'available');

UPDATE lyfter_car_rental.users
SET account_status = 'inactive'
WHERE id = 51
*/
/*
UPDATE lyfter_car_rental.vehicles
SET status = 'unavailable'
WHERE id = 1


INSERT INTO lyfter_car_rental.vehicle_user(rental_status, vehicle_id, user_id)
VALUES ('In use', 3, 3);
UPDATE lyfter_car_rental.vehicles  
SET status = 'In use'  
WHERE id = 3; 


UPDATE lyfter_car_rental.vehicle_user
SET rental_status = 'Completed', return_date = CURRENT_TIMESTAMP
WHERE id = 3;

UPDATE lyfter_car_rental.vehicles
SET status = 'Available'
WHERE id = 3;


UPDATE lyfter_car_rental.vehicles
SET status = 'unavailable'
WHERE id = 3


SELECT * FROM lyfter_car_rental.vehicles
WHERE status = 'In use'


SELECT * FROM lyfter_car_rental.vehicles
WHERE status = 'available'
*/