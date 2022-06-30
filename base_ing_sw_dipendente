--tabella per i dipendenti
CREATE TABLE dipendenti (
	id_dipendente SERIAL --non presente nelle indicazioni
	nome VARCHAR(30) NOT NULL
	cognome VARCHAR(30) NOT NULL
	luogo_di_nascita VARCHAR(30) NOT NULL
	data_di_nascita DATE NOT NULL
	nazionalità VARCHAR(30) NOT NULL
	email VARCHAR(30) UNIQUE NOT NULL
	telefono VARCHAR(12) CHECK (telefono SIMILAR TO '\+?[0-9]+') 
	PRIMARY KEY (id_dipendente)
);

--potrei anche inserirlo in dipendente
CREATE TABLE credenziali_accesso(
	login VARCHAR(30) UNIQUE NOT NULL 
	pw VARCHAR(30) NOT NULL
	dipendente SERIAL REFERENCES dipendenti(id_dipendente)
);

--serial è equivalente a id integer NOT NULL DEFAULT nextval('table_name_id_seq')