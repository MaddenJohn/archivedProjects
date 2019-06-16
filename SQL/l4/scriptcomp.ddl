--@(#) script.ddl
 
CREATE TABLE comp.Customer
(
	name varchar2 (255),
	id_Customer integer,
	PRIMARY KEY(id_Customer)
);  
  
CREATE SEQUENCE comp.Order_SEQ;

CREATE SEQUENCE comp.Customer_SEQ;

CREATE SEQUENCE comp.Prescription_SEQ;
   ---SKIPPED: Class REMOVED_BY_CUSTOM_TRANSFORMATION
    
CREATE TABLE comp.Order
(
	orderName varchar2 (255),
	id_Order integer,
	fk_Customerid_Customer integer NOT NULL,
	PRIMARY KEY(id_Order),
	FOREIGN KEY(fk_Customerid_Customer) REFERENCES comp.Customer (id_Customer)
);  
  
CREATE TABLE comp.Prescription
(
	prescName varchar2 (255),
	id_Prescription integer,
	fk_Orderid_Order integer NOT NULL,
	PRIMARY KEY(id_Prescription, fk_Orderid_Order),
	FOREIGN KEY(fk_Orderid_Order) REFERENCES comp.Order (id_Order)
);  
  