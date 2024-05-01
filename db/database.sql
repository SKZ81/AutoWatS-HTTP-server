PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

DROP TABLE Varieties;
DROP TABLE Plants;
DROP TABLE LastUpdatedTimestamps;

CREATE TABLE Varieties (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	short_descrp TEXT(240),
	photo_url TEXT
, blooming_time_days INTEGER);
INSERT INTO varieties VALUES(1,'Rose Bouquet','Visual, olfactive, sghort flowering ','rose_bouquet.png',50);
INSERT INTO varieties VALUES(2,'Lily Garden','Good yeild, long flowering','lily_garden.png',80);
INSERT INTO varieties VALUES(3,'Sunflower Fields','Productive, mid-term flowering','sunflower_fields.png',60);
INSERT INTO varieties VALUES(4,'Daisy Meadows','Edible, mid-term flowering','daisy_meadows.png',65);
INSERT INTO varieties VALUES(5,'Northern Widow','Short blooming, funny taste','northern_widow.png',55);
INSERT INTO varieties VALUES(6,'Orchid Paradize','Beautyfiul, many flowers','orchid_paradize.png',70);
CREATE TABLE Plants (
	UUID TEXT(36) NOT NULL,
	variety INTEGER,
	sex INTEGER DEFAULT (-1),
	germination_date TEXT(10),
	blooming_date TEXT(10),
	yielding_date TEXT(10),
	active INTEGER DEFAULT (TRUE),
	CONSTRAINT Plants_PK PRIMARY KEY (UUID)
);

INSERT INTO Plants VALUES('c586f3a2-3452-450e-a5b4-eb5b1d21e0ec',3,-1,'29/4/2024','','',TRUE);
INSERT INTO Plants VALUES('b8c9de57-669f-4dc4-bd9f-eb1e6e6e67d9',4,-1,'19/4/2024','29/4/2024','',TRUE);
INSERT INTO Plants VALUES('a9e2c8f1-8c98-4f35-ae22-84de0577e261',2,-1,'11/4/2024','29/4/2024','16/5/2024',TRUE);

DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('varieties',6);

COMMIT;
