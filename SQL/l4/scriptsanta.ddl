--@(#) script.ddl
 
CREATE TABLE l4.Child
(
	name varchar2 (255),
	address varchar2 (255),
	whereBorn varchar2 (255),
	id_Child integer,
	PRIMARY KEY(id_Child)
);  
  
CREATE SEQUENCE l4.Child_SEQ;

CREATE SEQUENCE l4.santaList_SEQ;

CREATE SEQUENCE l4.Toys_SEQ;

CREATE SEQUENCE l4.childList_SEQ;
   ---SKIPPED: Class REMOVED_BY_CUSTOM_TRANSFORMATION
  
CREATE TABLE l4.Toys
(
	name varchar2 (255),
	weight int,
	id_Toys integer,
	PRIMARY KEY(id_Toys)
);  
    
CREATE TABLE l4.childList
(
	listDesired varchar2 (255),
	id_childList integer,
	fk_Toysid_Toys integer NOT NULL,
	fk_Childid_Child integer NOT NULL,
	PRIMARY KEY(id_childList),
	FOREIGN KEY(fk_Toysid_Toys) REFERENCES l4.Toys (id_Toys),
	FOREIGN KEY(fk_Childid_Child) REFERENCES l4.Child (id_Child)
);  
  
CREATE TABLE l4.santaList
(
	naughtyList varchar2 (255),
	previousToys varchar2 (255),
	id_santaList integer,
	fk_Childid_Child integer NOT NULL,
	fk_Toysid_Toys integer NOT NULL,
	PRIMARY KEY(id_santaList),
	FOREIGN KEY(fk_Childid_Child) REFERENCES l4.Child (id_Child),
	FOREIGN KEY(fk_Toysid_Toys) REFERENCES l4.Toys (id_Toys)
);  
  