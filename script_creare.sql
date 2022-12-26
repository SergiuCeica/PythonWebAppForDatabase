CREATE TABLE IF NOT EXISTS pacient(
id decimal(3) NOT NULL,
nume varchar(30) NOT NULL,
prenume varchar(30),
varsta decimal(3),
telefon varchar(10),
localitate varchar(30),
email varchar(30),
CONSTRAINT pacient_id_pk PRIMARY KEY (id)
CONSTRAINT varsta_ck CHECK (varsta>0));

CREATE TABLE IF NOT EXISTS reteta(
id decimal(3) 
CONSTRAINT decimal_nn NOT NULL,
id_pacient decimal(3) NOT NULL,
diagnostic varchar(100),
medicamente varchar(200),
durata decimal(3),
data_intocmire date,
CONSTRAINT reteta_id_pk PRIMARY KEY (id),
CONSTRAINT FK_pacient FOREIGN KEY (id_pacient) REFERENCES pacient(id));

CREATE TABLE IF NOT EXISTS internare(
id decimal(3) NOT NULL,
id_pacient decimal(3) NOT NULL,
id_medic decimal(3) NOT NULL,
data_intrare date,
data_iesire date,
in_progres bit,
departament varchar(100),
CONSTRAINT internare_id_pk PRIMARY KEY(id),
CONSTRAINT FK_pacient FOREIGN KEY (id_pacient) REFERENCES pacient(id),
CONSTRAINT FK_medic FOREIGN KEY (id_medic) REFERENCES medic(id),
CONSTRAINT FK_departament FOREIGN KEY (departament) REFERENCES departament(nume_departament));

CREATE TABLE IF NOT EXISTS medic(
id decimal(3) NOT NULL,
nume varchar(30) NOT NULL,
prenume varchar(30),
varsta decimal(3),
telefon varchar(10),
email varchar(50),
CONSTRAINT medic_id_pk PRIMARY KEY(id));

CREATE TABLE IF NOT EXISTS departament(
id_medic varchar(30) NOT NULL,
nume_departament varchar(100) NOT NULL,
corp_cladire varchar(30),
numar_saloane decimal(2),
CONSTRAINT departament_id_medic_pk FOREIGN KEY(id_medic)
REFERENCES medi (id));