INSERT INTO pacient VALUES (1,'Popescu','Ion',26,'0726783294','Iasi','popescuion@gmail.com');
INSERT INTO pacient VALUES (2,'Dumitru','Pavel',38,'0766497302','Botosani','dumitrupavel@gmail.com');
INSERT INTO pacient VALUES (3,'Dobrincu','Maria',18,'0748249276','Vaslui','dobrincumaria@gmail.com');
INSERT INTO pacient VALUES (4,'Stanciu','Dan',60,'0754208974','Galati','stanciudan@gmail.com');
INSERT INTO pacient VALUES (5,'Rusu','Cosmin',45,'0755558922','Roman','rusucosmin@gmail.com');
INSERT INTO pacient VALUES (6,'Radu','Alexandra',21,'0732302721','Piatra Neamt','radualexandra@gmail.com');

INSERT INTO reteta VALUES (1,3,'Hipermetropie',' ',' ','26-11-2022');
INSERT INTO reteta VALUES (2,5,'Tulburari ale sistemului circulator','Biomag Forte Circulatie','2 saptamani','20-11-2022');
INSERT INTO reteta VALUES (3,6,'Traumatism cranian','Gel pentru recuperare','1 saptamana','4-11-2022');
INSERT INTO reteta VALUES (4,1,'Meningita virala','Odihna/Medicamente pentru dureri de cap','1 saptamana','30-10-2022');
INSERT INTO reteta VALUES (5,4,'Hipertensiune arteriala','Tensiomar','10 zile','25-10-2022');
INSERT INTO reteta VALUES (6,2,'Durere toracica','Relaxare','5 zile','22-11-2022');
INSERT INTO reteta VALUES (7,3,'Extractii dentare si lucrari dentare',' ',' ','3-11-2022');

INSERT INTO internare VALUES (1,1,2,'25-11-2022',' ',1,'Boli infectioase');
INSERT INTO internare VALUES (2,4,3,' ',' ',0,'Medicina generala');
INSERT INTO internare VALUES (3,5,3,' ',' ',0,'Medicina generala');
INSERT INTO internare VALUES (4,6,3,' ',' ',0,'Medicina generala');

INSERT INTO medic VALUES (1,'Popa','Virgil',45,'0756876392','popavirgil@yahoo.com');
INSERT INTO medic VALUES (2,'Ionescu','Cristina',30,'0759873254','ionescucristina@yahoo.com');
INSERT INTO medic VALUES (3,'Ciobanu','Victor',52,'0733234592','ciobanuvictor@yahoo.com');
INSERT INTO medic VALUES (4,'Anghel','Mirabela',44,'0722843942','anghelmirabela@yahoo.com');
INSERT INTO medic VALUES (5,'Neagu','Andrei',28,'0768932401','neaguandrei@yahoo.com');

INSERT INTO departament VALUES (1,'Oftalmologie','B2',5);
INSERT INTO departament VALUES (2,'Boli infectioase','B2',5);
INSERT INTO departament VALUES (3,'Medicina generala','B2',5);
INSERT INTO departament VALUES (4,'Medicina dentara','B2',5);
INSERT INTO departament VALUES (5,'Pediatrie','B2',5);