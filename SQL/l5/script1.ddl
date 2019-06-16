--@(#) script.ddl
 
CREATE TABLE l5.Employee
(
	firstName varchar2 (255),
	lastName varchar2 (255),
	phone varchar2 (255),
	jobTitle varchar2 (255),
	payGrade int,
	id_Employee integer,
	fk_Employeeid_Employee integer NOT NULL,
	fk_Employeeid_Employee1 integer,
	PRIMARY KEY(id_Employee),
	UNIQUE(fk_Employeeid_Employee),
	FOREIGN KEY(fk_Employeeid_Employee) REFERENCES l5.Employee (id_Employee),
	CONSTRAINT is supervised by FOREIGN KEY(fk_Employeeid_Employee1) REFERENCES l5.Employee (id_Employee)
);  
  
CREATE SEQUENCE l5.Employee_SEQ;
   ---SKIPPED: Class REMOVED_BY_CUSTOM_TRANSFORMATION
    