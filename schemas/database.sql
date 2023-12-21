CREATE TABLE IF NOT EXISTS vouches(
    user_id BIGINT,
    vouch_id TEXT PRIMARY KEY,
    time TEXT,
    vouchby BIGINT,
    reason TEXT,
    accepted BOOLEAN DEFAULT 'False',
    denied BOOLEAN DEFAULT 'False',
    manual_verify BOOLEAN DEFAULT 'False',
    denyreason TEXT
);

CREATE TABLE IF NOT EXISTS usercheck(
    user_id BIGINT PRIMARY KEY,
    vouches INT DEFAULT 0,
    imported INT DEFAULT 0,
    scammer BOOLEAN DEFAULT 'False',
    dwc BOOLEAN DEFAULT 'False',
    blacklisted BOOLEAN DEFAULT 'False',
    scammer_reason TEXT
);

CREATE TABLE IF NOT EXISTS shop(
    user_id BIGINT PRIMARY KEY,
    shop TEXT,
    img TEXT,
    forum TEXT,
    product TEXT,
    color VARCHAR DEFAULT 'FDED00'
);

CREATE TABLE IF NOT EXISTS staffs(
    user_id BIGINT PRIMARY KEY,
    noprefix BOOLEAN DEFAULT 'False',
    vouchadmin BOOLEAN DEFAULT 'False',
    vouchstaff BOOLEAN DEFAULT 'False'
);

CREATE TABLE IF NOT EXISTS token(
    user_id BIGINT PRIMARY KEY,
    token TEXT,
    used BOOLEAN
);

CREATE TABLE IF NOT EXISTS serverdata(
    guild_id BIGINT PRIMARY KEY,
    scammerrole BIGINT,
    dwcrole BIGINT,
    logch BIGINT,
    autoban BOOLEAN
);

