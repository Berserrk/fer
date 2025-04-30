/*
 
 1. **Trouver les 3 meilleurs clients en termes de montant total de paiements :** 
 Quels sont les trois clients qui ont dépensé le plus d'argent dans l'entreprise ?
 
 2. **Identifier les produits avec des quantités vendues supérieures à la moyenne des quantités commandées :** 
 Quels sont les produits qui ont été vendus en quantités significativement plus élevées que la moyenne ?
 
 3. **Lister les employés qui ont traité plus de commandes que la moyenne par employé :** 
 Quels sont les représentants commerciaux qui ont géré plus de commandes que la moyenne de l'équipe ?
 
 4. **Trouver les lignes de produits avec une valeur de ventes totale supérieure à la valeur médiane :** 
 Quelles sont les lignes de produits qui ont généré des revenus au-dessus de la moyenne globale ?
 
 5. **Trouver les clients qui ont effectué des paiements durant toutes les années présentes dans la base de données :** 
 Quels sont les clients fidèles qui ont fait des achats chaque année depuis que l'entreprise existe ?
 */
/*
 1. **Trouver les 3 meilleurs clients en termes de montant total de capacite de paiements :** 
 Quels sont les trois clients qui ont dépensé le plus d'argent dans l'entreprise ?
 */
SELECT customerName,
    sum(creditLimit) AS montant_total
FROM classicmodels.customers
group by customerName
order by montant_total DESC
limit 3;
/*
 UNION de tables, 2 conditions:
 - meme nombre de colonnes dans les 2 tables (condition strict)
 - meme ordre de colonnes (condition strict)
 - meme nom de colonnes (facultatif selon les languages SQL ou version SQL)
 - meme type de colonnes des deux cotes pour les colonnes qui match
 classicmodels.master1_2024:
 ID NOM PRENOM 
 1  n1  p1 
 
 classicmodels.new_joiners_master1_2024:
 ID NOM PRENOM 
 15 N15 P15
 */
/* Creer une table avec la liste de toutes les personnes presentes dans ma base de donnees/schema classicmodels*/
CREATE TABLE classicmodels.customers_name AS
SELECT contactLastName AS LastName,
    contactFirstName AS firstName
FROM classicmodels.customers;
CREATE TABLE classicmodels.employees_name AS
SELECT LastName,
    firstName
FROM classicmodels.employees;
CREATE TABLE classicmodels.all_persons AS
SELECT *
FROM classicmodels.customers_name
UNION
SELECT *
FROM classicmodels.employees_name;
/*145 lignes total*/
SELECT COUNT(*)
FROM classicmodels.all_persons
    /*122 lignes total*/
SELECT COUNT(*)
FROM classicmodels.customers_name
    /*23 lignes total*/
SELECT COUNT(*)
FROM classicmodels.employees_name;
CREATE TABLE master_paris13.m1bidabi_piano (
    nom VARCHAR(10),
    prenom VARCHAR(50),
    niveau VARCHAR(50),
    city VARCHAR(50)
);
INSERT INTO master_paris13.m1bidabi_piano (nom, prenom, niveau, city)
VALUES ("n1", "Phillipe", "1", "paris"),
    ("n2", "Ange", "1", "paris"),
    ("n3", "Rayan", "1", "paris"),
    ("n4", "Nacer", "1", "creteil"),
    ("n5", "Mevlut", "1", "creteil");
DROP TABLE master_paris13.m1bidabi_sport CREATE TABLE master_paris13.m1bidabi_sport (
    nom VARCHAR(10),
    prenom VARCHAR(50),
    niveau INT(50),
    city VARCHAR(50),
    country VARCHAR(50),
    phone VARCHAr(15)
);
INSERT INTO master_paris13.m1bidabi_sport (nom, prenom, niveau, city, country, phone)
VALUES ("n8", "Rina", "1", "paris", "France", "09123123"),
    (
        "n6",
        "Meriem",
        "1",
        "paris",
        "France",
        "09123123"
    ),
    (
        "n7",
        "Nouran",
        "1",
        "paris",
        "France",
        "09123123"
    ),
    (
        "n4",
        "Nacer",
        "1",
        "creteil",
        "France",
        "09123123"
    ),
    (
        "n5",
        "Mevlut",
        "1",
        "creteil",
        "France",
        "09123123"
    );
/*creer une table avec la liste des eleves qui vont aux 2 disciplines. On va faire appel au INNER JOIN */
CREATE TABLE master_paris13.m1bidabi_eleves_sport_piano AS
SELECT table1.*,
    table2.phone
FROM master_paris13.m1bidabi_piano as table1
    INNER JOIN master_paris13.m1bidabi_sport as table2 ON table1.nom = table2.nom
    AND table1.prenom = table2.prenom;
/*on garde la table piano, je veux garder les donnees de cette table mais
 je veux ajouter le numero de telephone a cette table comme donnee additionel: 
 on va faire appel au LEFT JOIN*/
CREATE TABLE master_paris13.m1bidabi_piano_avec_ntelephone
SELECT table1.*,
    table2.phone
FROM master_paris13.m1bidabi_piano as table1
    LEFT JOIN master_paris13.m1bidabi_sport as table2 on table1.nom = table2.nom
    AND table1.prenom = table2.prenom;
/*
 creer une table avec uniquement les eleves qui ont un cours de piano (non present dans le cours de sport).
 On va faire appel au LEFT ANTI JOIN (selon les version de SQL ou selon l'interface peut aussi etre appele LEFT OUTER)
 2 moyens de le faire selon la plateforme: 
 */
/* methode 1 marche pas ici sur mysql: LEFT ANTI JOIN utilise dans HIVE, spark sql, presto, bigquery*/
SELECT table1.*
FROM master_paris13.m1bidabi_piano as table1 LEFT ANTI
    JOIN master_paris13.m1bidabi_sport as table2 on table1.nom = table2.nom
    AND table1.prenom = table2.prenom
    /*methode 2: LEFT JOIN + WHERE col is null utilise dans MYSQL, POSTGRESQL*/
SELECT table1.*
FROM master_paris13.m1bidabi_piano as table1
    LEFT JOIN master_paris13.m1bidabi_sport as table2 on table1.nom = table2.nom
    AND table1.prenom = table2.prenom
WHERE table2.nom IS NULL
    AND table2.prenom is NULL
    /* Creer une table avec la liste totale des eleves participant aux cours: on va faire appel au FULL JOIN
     2 methodes pouvant etre utilise selon le systeme de base de donnes 
     - Full join : PostgreSQL, SQL Server, Oracle (12c and later), SQLite (3.39.0 and later), Google BigQuery, Snowflake, Amazon Redshift
     */
SELECT table1.*
FROM master_paris13.m1bidabi_piano as table1
    FULL JOIN master_paris13.m1bidabi_sport as table2 ON table1.nom = table2.nom
    AND table1.prenom = table2.prenom
    /*methode 2 a ne pas apprendre*/
SELECT *
FROM master_paris13.m1bidabi_piano
    LEFT JOIN master_paris13.m1bidabi_sport ON master_paris13.m1bidabi_piano.nom = master_paris13.m1bidabi_sport.nom
UNION
SELECT *
FROM master_paris13.m1bidabi_piano
    RIGHT JOIN master_paris13.m1bidabi_sport on master_paris13.m1bidabi_piano.prenom = master_paris13.m1bidabi_sport.prenom
    /*
     Table voulu : les eleves qui ont soit uniquement un cours de piano soit uniquement un cours de sport.
     On va utiliser un full outer join 
     */
    /*methode 1 valable sur  PostgreSQL, SQL Server, Oracle (12c and later), SQLite (3.39.0 and later), Google BigQuery, Snowflake, Amazon Redshift*/
SELECT table1.*
FROM master_paris13.m1bidabi_piano as table1
    FULL OUTER JOIN master_paris13.m1bidabi_sport as table2 ON table1.nom = table2.nom
    AND table1.prenom = table2.prenom
    /*methode 2 a ne pas apprendre*/
SELECT master_paris13.m1bidabi_piano.*
FROM master_paris13.m1bidabi_piano
    LEFT JOIN master_paris13.m1bidabi_sport ON master_paris13.m1bidabi_piano.nom = master_paris13.m1bidabi_sport.nom
    AND master_paris13.m1bidabi_piano.prenom = master_paris13.m1bidabi_sport.prenom
WHERE master_paris13.m1bidabi_sport.nom is NULL
    AND master_paris13.m1bidabi_sport.prenom is NULL
UNION
SELECT master_paris13.m1bidabi_sport.nom,
    master_paris13.m1bidabi_sport.prenom,
    master_paris13.m1bidabi_sport.niveau,
    master_paris13.m1bidabi_sport.city
FROM master_paris13.m1bidabi_sport
    LEFT JOIN master_paris13.m1bidabi_piano on master_paris13.m1bidabi_piano.prenom = master_paris13.m1bidabi_sport.prenom
    AND master_paris13.m1bidabi_piano.nom = master_paris13.m1bidabi_sport.nom
WHERE master_paris13.m1bidabi_piano.nom is NULL
    AND master_paris13.m1bidabi_piano.prenom is NULL