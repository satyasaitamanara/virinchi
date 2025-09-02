
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert dummy credentials for testing
INSERT INTO users (full_name, email, username, password, role) VALUES
('Admin User', 'admin@lmms.com', 'admin', '$2b$12$V4K1a5pWj/3wU5e3Xb8Jz.Da7q1J2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p', 'admin'),
('Test User', 'user@lmms.com', 'user', '$2b$12$V4K1a5pWj/3wU5e3Xb8Jz.Da7q1J2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p', 'user');

-- Add to existing schema.sql


CREATE TABLE IF NOT EXISTS content (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_link TEXT,
    video_link TEXT,
    program_category ENUM(
    'Skill Development & Vocational Training',
    'Inclusive Education & Early Intervention',
    'Entrepreneurship & Life Skills Development',
    'Soft Skills & IT Training',
    'Medical & Nursing Assistant Training',
    'Garment Making, Tailoring, Zardosi Work',
    'Job Placement & Industry Tie-ups',
    'Beautician Course',
    'Food and Beverages Associate',
    'Nursing Course',
    'Front Office Associate',
    'Multi Skill Technician (Electrical)',
    'Electrical Assembly Operator'
    ) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample content
INSERT INTO content (title, description, file_link, video_link, program_category) VALUES
('Introduction to Vocational Training', 'Basic concepts of vocational training and skill development', '/uploads/vocational-training.pdf', 'https://www.youtube.com/embed/otbe6M5mIEE', 'Skill Development & Vocational Training'),
('Early Intervention Strategies', 'Effective strategies for inclusive education and early intervention', '/uploads/early-intervention.pdf', 'https://www.youtube.com/embed/def456', 'Inclusive Education & Early Intervention'),
('job', '90 days to prepare for job', '', 'https://www.youtube.com/embed/Qn_TgNluu7w', 'Job Placement & Industry Tie-ups'),
('Skill development', 'Basic concept of Skill development', '', 'https://www.youtube.com/embed/JFehKCKaCD8?si=7jcXzKnLvSGAkX_j', 'Skill Development & Vocational Training'),
('Soft Skills', 'Soft skills and presentation skills', '', 'https://www.youtube.com/embed/ADJAcyTq1us', 'Soft Skills & IT Training'),
('beauty-therapist-english-class-11', 'The PDF provides basic English lessons and communication skills tailored for beauty therapy students to improve professional interaction', 'beauty-therapist-english-class-11.pdf', '', 'Beautician Course'),
('CONTENT-BT_PH_English.pdf', 'This PDF provides basic training material for the Beautician course in English.', 'COURSE_CONTENT-BT_PH_English.pdf', '', 'Beautician Course'),
('Fundamentals_for_Beauticians-level_1&2', 'A beginner-friendly guide covering essential skills and techniques for beauticians at Level 1 & 2.', 'Fundamentals_for_Beauticians-level_12.pdf', '', 'Beautician Course'),
('Beautician ', 'This video provide the basics of the Beautician', '', 'https://www.youtube.com/embed/0LwoPMMFenE', 'Beautician Course'),
('Food & Beverage Service - Associate_THC_Q0301_v2.0', 'The provides training guidelines and skills required for working as a food and beverage service associate in the hospitality industry', 'Food__Beverage_Service_-_Associate_THC_Q0301_v2.0.pdf', '', 'Food and Beverages Associate'),
('Hospitality_Assistant_English', 'The PDF provides basic training material to develop communication and service skills for hospitality assistants in English', '168911474-Hospitality_Assistant_English.pdf', '', 'Nursing Course'),
('Patient-Relations-Associate-final', 'The PDF provides training material on handling patient interactions, improving communication, and supporting patient care services', 'Patient-Relations-Associate-final.pdf', '', 'Nursing Course'),
('THC Q0102 _FRONT OFFICE ASSOCIATE', 'The PDF provides basic training and guidelines for working as a Front Office Associate in the hospitality industry', 'THC_Q0102__FRONT_OFFICE_ASSOCIATE.pdf', '', 'Front Office Associate'),
('Multi Skill Technician - Electrical - ELE_Q3115_v2.0', 'The PDF gives training details and guidelines for becoming a skilled electrical technician', 'Multi_Skill_Technician_-_Electrical_-_ELE_Q3115_v2.0.pdf', '', 'Multi Skill Technician (Electrical)'),
('Electrical Assembly Operator - Control Panel', 'The PDF provides basic training and guidelines for assembling, wiring, and maintaining electrical control panels', 'Electrical_Assembly_Operator_-_Control_Panel.pdf', '', 'Electrical Assembly Operator');
