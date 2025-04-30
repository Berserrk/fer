/* Pour chaque productLine, compter le nombre de produits, nombre de productcode et le total de la quantite en stock*/
/*
 total rows: 110
 cd: 110
 
 */
CREATE TABLE classicmodels.todrop AS
SELECT count(distinct(productName)) as cd_product_name,
    productCode
FROM classicmodels.products
GROUP BY productCode
ORDER BY cd_product_name DESC;
SELECT *
FROM classicmodels.todrop
WHERE cd_product_name > 1;
/*
 =======================
 =======================
 =======================
 FILTER
 =======================
 =======================
 =======================*/
/*filtre standard*/
SELECT *
FROM classicmodels.products
WHERE productCode = "S10_1678";
/*multiple filtre standard*/
SELECT *
FROM classicmodels.products
WHERE productCode = "S10_1678"
    AND productName = '1969 Harley Davidson Ultimate Chopper';
/*filtrer avec or*/
SELECT *
FROM classicmodels.customers
WHERE country = "FRANCE"
    OR country = "USA"
    OR country = "SPAIN";
/* Meme requete mais filtre avec une liste*/
SELECT *
FROM classicmodels.customers
WHERE country in ("FRANCE", "USA", "SPAIN");
/*filter avec des quantities  
 -  ><
 -  between  
 */
SELECT *
FROM classicmodels.customers
WHERE creditLimit > 0;
SELECT *
FROM classicmodels.customers
WHERE creditLimit = 0;
SELECT *
FROM classicmodels.customers
WHERE creditLimit >= 10000
    AND creditLimit <= 15000
    /* pour les strictement sup/inf: WHERE creditLimit > 10000 AND creditLimit < 15000*/
;
SELECT *
FROM classicmodels.customers
WHERE creditLimit BETWEEN 10000 AND 15000;
/*requete avec de multiples et different filtres*/
SELECT *
FROM classicmodels.customers
WHERE creditLimit BETWEEN 10000 AND 15000
    AND country in ("FRANCE", "USA", "SPAIN");
/*
 Creer une nouvelle table tel que:
 - nom de table : value_stock_quantity
 - a partir de la table product 
 - cree une nouvelle colonne calculant la valeur par stock pour chaque productline et chaque productname
 - uniquement pour les "1995 Honda Civic" et "1962 LanciaA Delta 16V"
 - classez par ordre decroissant
 */
CREATE TABLE classicmodels.value_stock_quantity AS
SELECT productLine,
    productName,
    SUM(quantityInStock * buyPrice) AS quantitystock_x_buyprice
FROM classicmodels.products
GROUP BY productLine,
    productName;
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