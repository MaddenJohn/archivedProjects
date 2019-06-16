--@(#) script.ddl
 
CREATE TABLE l5.Employee
(
	lastName varchar2 (255),
	jobTitle varchar2 (255),
	department varchar2 (255),
	id_Employee integer,
	fk_Employeeid_Employee integer,
	PRIMARY KEY(id_Employee),
	CONSTRAINT is supervised by FOREIGN KEY(fk_Employeeid_Employee) REFERENCES l5.Employee (id_Employee)
);  
  
CREATE SEQUENCE l5.Employee_SEQ;
   ---SKIPPED: Class REMOVED_BY_CUSTOM_TRANSFORMATION
    