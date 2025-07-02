-- Table adminrooms
CREATE TABLE adminrooms (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL
);

-- Table bingos
CREATE TABLE bingos (
    id SERIAL PRIMARY KEY,
    case_text VARCHAR(50) NOT NULL
);

-- Table bingorooms
CREATE TABLE bingorooms (
    id SERIAL PRIMARY KEY,
    bingo_id INTEGER NOT NULL,
    case_text VARCHAR(50) NOT NULL,
    admin_id INTEGER NOT NULL,
    CONSTRAINT fk_bingos FOREIGN KEY (bingo_id) REFERENCES bingos(id),
    CONSTRAINT fk_adminrooms FOREIGN KEY (admin_id) REFERENCES adminrooms(id)
);

-- Table extendusers
CREATE TABLE extendusers (
    id SERIAL PRIMARY KEY,
    token VARCHAR(50) NOT NULL,
    img VARCHAR(50) NOT NULL,
    user_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    CONSTRAINT FK_1 FOREIGN KEY (user_id) REFERENCES auth_user (id)
);

-- Table predictions
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    question VARCHAR(50) NOT NULL,
    respons VARCHAR(50) NOT NULL,
    start_at TIME NOT NULL,
    end_at TIME NOT NULL,
    status VARCHAR(50) NOT NULL,
    timer TIME NOT NULL,
    is_validated VARCHAR(50) NOT NULL
);

-- Table rooms
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    prediction_id INTEGER NOT NULL,
    bingoroom_id INTEGER NOT NULL,
    admin_id INTEGER NOT NULL,
    created_at DATE NOT NULL,
    close_at DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    CONSTRAINT fk_extendusers FOREIGN KEY (user_id) REFERENCES extendusers(id),
    CONSTRAINT fk_adminrooms FOREIGN KEY (admin_id) REFERENCES adminrooms(id),
    CONSTRAINT fk_bingorooms FOREIGN KEY (bingoroom_id) REFERENCES bingorooms(id),
    CONSTRAINT fk_predictions FOREIGN KEY (prediction_id) REFERENCES predictions(id)
);

-- Table user_bingo_cases
CREATE TABLE user_bingo_cases (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    case_text VARCHAR(50) NOT NULL,
    is_checked BOOLEAN NOT NULL,
    position INTEGER NOT NULL,
    CONSTRAINT fk_extendusers FOREIGN KEY (user_id) REFERENCES extendusers(id),
    CONSTRAINT fk_rooms FOREIGN KEY (room_id) REFERENCES rooms(id)
);

-- Table user_scores
CREATE TABLE user_scores (
    id SERIAL PRIMARY KEY,
    score INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    update_at TIME NOT NULL,
    CONSTRAINT fk_rooms FOREIGN KEY (room_id) REFERENCES rooms(id),
    CONSTRAINT fk_extendusers FOREIGN KEY (user_id) REFERENCES extendusers(id)
);

-- Table validated_cases
CREATE TABLE validated_cases (
    id SERIAL PRIMARY KEY,
    bingoroom_id INTEGER NOT NULL,
    is_checked BOOLEAN NOT NULL,
    CONSTRAINT fk_bingorooms FOREIGN KEY (bingoroom_id) REFERENCES bingorooms(id)
);
