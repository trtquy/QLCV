-- Creating teams
INSERT INTO teams (name, description, is_active, created_at) VALUES ('Chính sách tín dụng', 'Banking team: Chính sách tín dụng', true, NOW()) ON CONFLICT (name) DO NOTHING;
INSERT INTO teams (name, description, is_active, created_at) VALUES ('Giám sát tín dụng', 'Banking team: Giám sát tín dụng', true, NOW()) ON CONFLICT (name) DO NOTHING;
INSERT INTO teams (name, description, is_active, created_at) VALUES ('Quản lý danh mục', 'Banking team: Quản lý danh mục', true, NOW()) ON CONFLICT (name) DO NOTHING;
INSERT INTO teams (name, description, is_active, created_at) VALUES ('Quản lý rủi ro tích hợp', 'Banking team: Quản lý rủi ro tích hợp', true, NOW()) ON CONFLICT (name) DO NOTHING;

-- Creating users
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('trangltt8', 'trangltt8@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('dinhnt4', 'dinhnt4@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('anhlv3', 'anhlv3@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('diepnn1', 'diepnn1@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('anhthh', 'anhthh@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('thanhlt10', 'thanhlt10@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('anh_nh', 'anh_nh@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('khoank', 'khoank@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('habh', 'habh@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('minhvc2', 'minhvc2@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('hainh7', 'hainh7@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('hoangnm11', 'hoangnm11@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('thangdv4', 'thangdv4@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('halth4', 'halth4@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('quytt2', 'quytt2@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('trangdt17', 'trangdt17@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('linhptm1', 'linhptm1@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('hangnt433', 'hangnt433@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('trung.dq', 'trung.dq@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('huyenltt16', 'huyenltt16@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('trangtt11', 'trangtt11@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('trungvq2', 'trungvq2@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('linhbtm1', 'linhbtm1@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('hoattn1', 'hoattn1@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('nganvt5', 'nganvt5@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('toannp', 'toannp@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('hieu.nt', 'hieu.nt@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('locdx', 'locdx@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('tuttn', 'tuttn@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('trangntm7', 'trangntm7@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('hanhtt6', 'hanhtt6@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('haonh', 'haonh@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('dungpt23', 'dungpt23@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('binhdm', 'binhdm@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('phongbth', 'phongbth@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('nganmk', 'nganmk@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('duclt6', 'duclt6@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('thuynp', 'thuynp@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('haptt', 'haptt@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('linhntt61', 'linhntt61@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('tanbtn', 'tanbtn@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('mynd1', 'mynd1@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('lyltk1', 'lyltk1@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('chiltm', 'chiltm@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('nhandh', 'nhandh@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('nhungnh15', 'nhungnh15@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('hieuns1', 'hieuns1@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('duyentt2', 'duyentt2@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('hang.vm', 'hang.vm@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('cont', 'cont@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('huongnb', 'huongnb@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('duylbk', 'duylbk@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('trangvth4', 'trangvth4@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('vukhang', 'vukhang@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('son_pv', 'son_pv@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('thulp', 'thulp@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;
INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('anhnh55', 'anhnh55@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;

-- Creating tasks
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'medium', 'medium', NOW(), NOW(), 5.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'trangltt8'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'todo', 'low', 'very_complex', NOW(), NOW(), 9.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dinhnt4'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'todo', 'low', 'complex', NOW(), NOW(), 11.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dinhnt4'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'completed', 'high', 'very_simple', NOW(), NOW(), 2.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'anhlv3'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Xây dựng chính sách tín dụng mới', 'Tham gia xây dựng, hoàn thiện các chính sách tín dụng áp dụng cho khách hàng cá nhân/doanh nghiệp.', 'completed', 'urgent', 'simple', NOW(), NOW(), 12.3, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'anhlv3'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'todo', 'low', 'very_complex', NOW(), NOW(), 7.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'diepnn1'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Xây dựng chính sách tín dụng mới', 'Tham gia xây dựng, hoàn thiện các chính sách tín dụng áp dụng cho khách hàng cá nhân/doanh nghiệp.', 'todo', 'low', 'very_simple', NOW(), NOW(), 15.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dinhnt4'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'todo', 'medium', 'medium', NOW(), NOW(), 17.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'anhthh'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'completed', 'high', 'simple', NOW(), NOW(), 11.2, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'thanhlt10'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'high', 'medium', NOW(), NOW(), 3.6, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'thanhlt10'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'urgent', 'simple', NOW(), NOW(), 11.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dinhnt4'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'todo', 'medium', 'complex', NOW(), NOW(), 6.2, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dinhnt4'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'todo', 'low', 'very_simple', NOW(), NOW(), 10.5, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dinhnt4'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'medium', 'medium', NOW(), NOW(), 11.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'anh_nh'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'urgent', 'very_complex', NOW(), NOW(), 12.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'anhlv3'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'urgent', 'very_simple', NOW(), NOW(), 17.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'diepnn1'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Xây dựng chính sách tín dụng mới', 'Tham gia xây dựng, hoàn thiện các chính sách tín dụng áp dụng cho khách hàng cá nhân/doanh nghiệp.', 'todo', 'medium', 'complex', NOW(), NOW(), 17.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dinhnt4'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'medium', 'complex', NOW(), NOW(), 17.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'anhthh'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'completed', 'medium', 'medium', NOW(), NOW(), 12.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'thanhlt10'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'todo', 'medium', 'simple', NOW(), NOW(), 18.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'thanhlt10'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'medium', 'very_simple', NOW(), NOW(), 11.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dinhnt4'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'completed', 'medium', 'very_complex', NOW(), NOW(), 12.2, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'trangltt8'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'todo', 'urgent', 'very_complex', NOW(), NOW(), 12.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dinhnt4'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'high', 'medium', NOW(), NOW(), 9.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dinhnt4'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'urgent', 'simple', NOW(), NOW(), 6.5, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'anhlv3'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'medium', 'very_simple', NOW(), NOW(), 14.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'anhlv3'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tổng hợp ý kiến về chính sách', 'Tổng hợp, phân tích các ý kiến góp ý cho các dự thảo chính sách tín dụng.', 'in_progress', 'low', 'very_simple', NOW(), NOW(), 6.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'trangltt8'), (SELECT id FROM teams WHERE name = 'Chính sách tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'in_progress', 'low', 'very_simple', NOW(), NOW(), 15.5, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'khoank'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Giám sát khoản vay lớn', 'Theo dõi, giám sát các khoản vay có giá trị lớn và rủi ro cao.', 'in_progress', 'low', 'simple', NOW(), NOW(), 20.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'habh'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Giám sát khoản vay lớn', 'Theo dõi, giám sát các khoản vay có giá trị lớn và rủi ro cao.', 'in_progress', 'medium', 'complex', NOW(), NOW(), 6.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'minhvc2'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'todo', 'medium', 'complex', NOW(), NOW(), 17.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hainh7'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Giám sát khoản vay lớn', 'Theo dõi, giám sát các khoản vay có giá trị lớn và rủi ro cao.', 'completed', 'high', 'very_simple', NOW(), NOW(), 4.5, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hoangnm11'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Giám sát khoản vay lớn', 'Theo dõi, giám sát các khoản vay có giá trị lớn và rủi ro cao.', 'todo', 'medium', 'very_simple', NOW(), NOW(), 6.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'thangdv4'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'todo', 'medium', 'simple', NOW(), NOW(), 11.3, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'halth4'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'todo', 'medium', 'medium', NOW(), NOW(), 11.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'quytt2'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'todo', 'low', 'very_complex', NOW(), NOW(), 17.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'khoank'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'completed', 'high', 'complex', NOW(), NOW(), 15.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'habh'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'in_progress', 'urgent', 'complex', NOW(), NOW(), 12.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'minhvc2'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'todo', 'medium', 'simple', NOW(), NOW(), 4.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hainh7'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'in_progress', 'high', 'medium', NOW(), NOW(), 19.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hoangnm11'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Giám sát khoản vay lớn', 'Theo dõi, giám sát các khoản vay có giá trị lớn và rủi ro cao.', 'todo', 'medium', 'complex', NOW(), NOW(), 13.6, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'thangdv4'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Giám sát khoản vay lớn', 'Theo dõi, giám sát các khoản vay có giá trị lớn và rủi ro cao.', 'in_progress', 'urgent', 'simple', NOW(), NOW(), 17.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'halth4'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Giám sát khoản vay lớn', 'Theo dõi, giám sát các khoản vay có giá trị lớn và rủi ro cao.', 'completed', 'urgent', 'simple', NOW(), NOW(), 10.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'quytt2'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'todo', 'low', 'simple', NOW(), NOW(), 2.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'khoank'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'todo', 'urgent', 'simple', NOW(), NOW(), 19.3, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'habh'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'completed', 'high', 'very_simple', NOW(), NOW(), 19.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'minhvc2'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Giám sát khoản vay lớn', 'Theo dõi, giám sát các khoản vay có giá trị lớn và rủi ro cao.', 'completed', 'urgent', 'simple', NOW(), NOW(), 13.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hainh7'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Giám sát khoản vay lớn', 'Theo dõi, giám sát các khoản vay có giá trị lớn và rủi ro cao.', 'todo', 'high', 'simple', NOW(), NOW(), 17.3, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hoangnm11'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'todo', 'high', 'very_complex', NOW(), NOW(), 19.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'thangdv4'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'todo', 'high', 'simple', NOW(), NOW(), 18.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'halth4'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Giám sát khoản vay lớn', 'Theo dõi, giám sát các khoản vay có giá trị lớn và rủi ro cao.', 'in_progress', 'medium', 'complex', NOW(), NOW(), 14.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'quytt2'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Kiểm tra hồ sơ vay vốn', 'Thực hiện kiểm tra, đánh giá các hồ sơ vay vốn của khách hàng.', 'todo', 'urgent', 'medium', NOW(), NOW(), 18.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'quytt2'), (SELECT id FROM teams WHERE name = 'Giám sát tín dụng'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'completed', 'high', 'simple', NOW(), NOW(), 19.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'trangdt17'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'completed', 'urgent', 'medium', NOW(), NOW(), 20.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'linhptm1'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'in_progress', 'urgent', 'very_simple', NOW(), NOW(), 14.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hangnt433'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'in_progress', 'high', 'medium', NOW(), NOW(), 17.2, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'trung.dq'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'completed', 'medium', 'complex', NOW(), NOW(), 10.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'huyenltt16'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'completed', 'urgent', 'very_simple', NOW(), NOW(), 11.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'trangtt11'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'in_progress', 'low', 'simple', NOW(), NOW(), 19.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'trungvq2'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'completed', 'high', 'simple', NOW(), NOW(), 14.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'linhbtm1'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'completed', 'low', 'very_complex', NOW(), NOW(), 6.5, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hoattn1'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'in_progress', 'high', 'complex', NOW(), NOW(), 17.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'nganvt5'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'in_progress', 'urgent', 'medium', NOW(), NOW(), 19.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'toannp'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'in_progress', 'low', 'very_complex', NOW(), NOW(), 3.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hieu.nt'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Rà soát danh mục sản phẩm', 'Kiểm tra, đánh giá và cập nhật danh mục sản phẩm hiện có.', 'todo', 'high', 'very_complex', NOW(), NOW(), 11.3, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'locdx'), (SELECT id FROM teams WHERE name = 'Quản lý danh mục'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'high', 'very_complex', NOW(), NOW(), 14.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'tuttn'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'high', 'very_complex', NOW(), NOW(), 3.3, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'trangntm7'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'completed', 'low', 'simple', NOW(), NOW(), 4.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hanhtt6'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'urgent', 'simple', NOW(), NOW(), 10.6, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'haonh'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'completed', 'high', 'simple', NOW(), NOW(), 13.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dungpt23'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'completed', 'urgent', 'very_complex', NOW(), NOW(), 17.0, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'binhdm'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'medium', 'very_simple', NOW(), NOW(), 11.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'phongbth'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'low', 'very_complex', NOW(), NOW(), 18.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'nganmk'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'in_progress', 'high', 'very_simple', NOW(), NOW(), 17.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'duclt6'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'high', 'very_simple', NOW(), NOW(), 11.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'thuynp'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'completed', 'low', 'very_simple', NOW(), NOW(), 14.2, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'haptt'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'high', 'medium', NOW(), NOW(), 2.5, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'linhntt61'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'high', 'complex', NOW(), NOW(), 5.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'tanbtn'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'completed', 'high', 'very_complex', NOW(), NOW(), 12.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'mynd1'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'todo', 'high', 'complex', NOW(), NOW(), 8.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'lyltk1'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'high', 'simple', NOW(), NOW(), 7.3, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'chiltm'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'medium', 'very_complex', NOW(), NOW(), 18.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'nhandh'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'medium', 'very_complex', NOW(), NOW(), 15.2, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'nhungnh15'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'completed', 'low', 'medium', NOW(), NOW(), 8.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hieuns1'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'in_progress', 'low', 'medium', NOW(), NOW(), 12.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'duyentt2'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'high', 'simple', NOW(), NOW(), 6.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hang.vm'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'completed', 'high', 'very_simple', NOW(), NOW(), 5.4, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'cont'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'completed', 'medium', 'complex', NOW(), NOW(), 2.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'huongnb'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'high', 'very_simple', NOW(), NOW(), 13.3, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'duylbk'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'todo', 'medium', 'simple', NOW(), NOW(), 3.2, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'trangvth4'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'in_progress', 'low', 'simple', NOW(), NOW(), 2.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'vukhang'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'completed', 'low', 'medium', NOW(), NOW(), 6.6, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'son_pv'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'medium', 'medium', NOW(), NOW(), 11.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'thulp'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'low', 'simple', NOW(), NOW(), 2.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'anhnh55'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'medium', 'medium', NOW(), NOW(), 13.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'hanhtt6'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'todo', 'urgent', 'complex', NOW(), NOW(), 4.7, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'haonh'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'completed', 'medium', 'simple', NOW(), NOW(), 12.2, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'dungpt23'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'completed', 'high', 'medium', NOW(), NOW(), 9.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'binhdm'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'low', 'medium', NOW(), NOW(), 10.2, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'phongbth'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'completed', 'high', 'medium', NOW(), NOW(), 9.5, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'nganmk'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'urgent', 'very_complex', NOW(), NOW(), 11.6, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'duclt6'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'urgent', 'simple', NOW(), NOW(), 15.3, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'thuynp'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'medium', 'medium', NOW(), NOW(), 5.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'haptt'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'urgent', 'simple', NOW(), NOW(), 16.8, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'linhntt61'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Tham gia đào tạo nội bộ', 'Tham gia các buổi đào tạo, chia sẻ kiến thức nội bộ.', 'in_progress', 'medium', 'very_complex', NOW(), NOW(), 3.9, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'tanbtn'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'urgent', 'complex', NOW(), NOW(), 15.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'mynd1'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'low', 'very_simple', NOW(), NOW(), 5.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'lyltk1'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'todo', 'low', 'very_simple', NOW(), NOW(), 5.6, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'lyltk1'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));
INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('Báo cáo tiến độ công việc', 'Cập nhật, báo cáo tiến độ công việc định kỳ.', 'in_progress', 'medium', 'simple', NOW(), NOW(), 3.1, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), (SELECT id FROM users WHERE username = 'lyltk1'), (SELECT id FROM teams WHERE name = 'Quản lý rủi ro tích hợp'));

-- Successfully generated SQL for 109 tasks
