--@(#) script.ddl
 
CREATE TABLE aggr.Customer
(
	name varchar2 (255),
	id_Customer integer,
	PRIMARY KEY(id_Customer)
);  
  
CREATE SEQUENCE aggr.Prescription_SEQ;

CREATE SEQUENCE aggr.Order_SEQ;

CREATE SEQUENCE aggr.Customer_SEQ;
   ---SKIPPED: Class REMOVED_BY_CUSTOM_TRANSFORMATION
    
CREATE TABLE aggr.Order
(
	orderName varchar2 (255),
	id_Order integer,
	fk_Customerid_Customer integer NOT NULL,
	PRIMARY KEY(id_Order),
	FOREIGN KEY(fk_Customerid_Customer) REFERENCES aggr.Customer (id_Customer)
);  
  
CREATE TABLE aggr.Prescription
(
	prescName varchar2 (255),
	id_Prescription integer,
	fk_Orderid_Order integer NOT NULL,
	PRIMARY KEY(id_Prescription),
	FOREIGN KEY(fk_Orderid_Order) REFERENCES aggr.Order (id_Order)
);  
  