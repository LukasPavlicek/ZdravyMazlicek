use vet_app;

CREATE TABLE Symptoms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symptoms_name VARCHAR(255) NOT NULL,
    symptoms_description TEXT
);

CREATE TABLE Diseases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    diseases_name VARCHAR(255) NOT NULL,
    diseases_description TEXT,
    severity ENUM('low', 'medium', 'high')
);

CREATE TABLE Disease_Symptoms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    disease_id INT NOT NULL,
    symptom_id INT NOT NULL,
    FOREIGN KEY (disease_id) REFERENCES Diseases(id),
    FOREIGN KEY (symptom_id) REFERENCES Symptoms(id)
);

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
	user_name VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pet_name VARCHAR(255) NOT NULL,
    species VARCHAR(50),
    age INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE diagnosis_history  (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pet_id INT NOT NULL,
    disease_id INT NOT NULL,
    symptoms TEXT,
    diagnosis TEXT,
    search_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (pet_id) REFERENCES Pets(id),
	FOREIGN KEY (disease_id) REFERENCES Diseases(id)
);

CREATE TABLE Articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(255),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);