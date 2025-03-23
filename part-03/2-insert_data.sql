INSERT INTO User (id, first_name, last_name, email, password, is_admin) VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$hashedpasswordhere', TRUE);

INSERT INTO Amenity (id, name) VALUES
(UUID(), 'WiFi'),
(UUID(), 'Swimming Pool'),
(UUID(), 'Air Conditioning');
