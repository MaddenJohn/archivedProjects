--@(#) script.ddl
 
CREATE SEQUENCE l5.2.TripleTable_SEQ;
   ---SKIPPED: Class REMOVED_BY_CUSTOM_TRANSFORMATION
  
CREATE TABLE l5.2.TripleTable
(
	vertexI,
	vertexJ,
	edgeLabel varchar2 (255),
	id_TripleTable integer,
	PRIMARY KEY(id_TripleTable)
);  
    
CREATE TABLE l5.2.TripleTable_TripleTable
(
	fk_TripleTableid_TripleTable integer,
	fk_TripleTableid_TripleTable1 integer,
	PRIMARY KEY(fk_TripleTableid_TripleTable, fk_TripleTableid_TripleTable1),
	FOREIGN KEY(fk_TripleTableid_TripleTable) REFERENCES l5.2.TripleTable (id_TripleTable),
	FOREIGN KEY(fk_TripleTableid_TripleTable1) REFERENCES l5.2.TripleTable (id_TripleTable)
);  
  