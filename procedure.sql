DELIMITER //
CREATE PROCEDURE result()
BEGIN

DECLARE varGameId INT;
DECLARE varGameName VARCHAR(1000);
DECLARE varNewScore FLOAT;
DECLARE varReview FLOAT;
DECLARE varGlobalSales FLOAT;
DECLARE varNewTag VARCHAR(1000);
DECLARE varName2 VARCHAR(1000);
DECLARE varGlobalSale2 FLOAT;
DECLARE varTag2 VARCHAR(1000);
DECLARE exit_loop BOOLEAN DEFAULT FALSE;
-- DECLARE exit_loop_2 BOOLEAN DEFAULT FALSE;

DECLARE cusCur CURSOR FOR (
                        SELECT gameId, Game.name,review, Sales.Sale_Global
                        FROM Game_info left join (Sales) using(gameId) LEFT JOIN(Game) using(gameId)
                        );

DECLARE cusCur2 CURSOR FOR (
			SELECT Game.name, sum(Sale_Global) as totalSale
            FROM Game NATURAL JOIN Sales
			Group by Game.name);

-- DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;

DROP TABLE IF EXISTS FinalTable;
DROP TABLE IF EXISTS FinalTable2;

CREATE TABLE FinalTable(
    GameId INT Primary Key,
    GameName VARCHAR(1000),
    newScore FLOAT,
    newTag VARCHAR(1000)
);

CREATE TABLE FinalTable2(
Name2 VARCHAR(1000),
	newGlobalSale FLOAT,
	newTag2 VARCHAR(1000)
);

OPEN cusCur;
begin
    DECLARE exit_loop INT DEFAULT 0;
    declare continue handler for not FOUND set exit_loop = TRUE;
cloop: LOOP
    FETCH cusCur INTO varGameId, varGameName,varReview, varGlobalSales;
    IF(exit_loop) THEN
        LEAVE cloop;
    END IF;
    
    SET varNewScore = (varReview * 0.7) + (varGlobalSales * 0.07);
    IF (varNewScore >= 8) THEN
	    SET varNewTag = "Diamond";
    ELSEIF (varNewScore >= 7) THEN
	    SET varNewTag = "Gold";
    ELSEIF (varNewScore >= 6) THEN
        SET varNewTag = "Silver";
    ELSE
        SET varNewTag = "Bronze";
    END IF;
   
                        
   
    INSERT IGNORE INTO FinalTable VALUES (varGameId,varGameName, varNewScore, varNewTag);
   

END LOOP cloop;
END;
CLOSE cusCur;


OPEN cusCur2;
BEGIN
DECLARE exit_loop INT DEFAULT 0;
declare continue handler for not FOUND set exit_loop = TRUE;


cloop_2: LOOP
    FETCH cusCur2 INTO varName2, varGlobalSale2;
    IF(exit_loop) THEN
        LEAVE cloop_2;
    END IF;
    
    IF (    varGlobalSale2 >= 30  ) THEN
	SET varTag2 = "Diamond";
   ELSEIF (      varGlobalSale2 >= 10    ) THEN
	SET varTag2 = "Gold";
   ELSE
        SET varTag2 = "Silver";
   END IF;
                        
    INSERT IGNORE INTO FinalTable2 VALUES (varName2, varGlobalSale2, varTag2);
   

END LOOP cloop_2;
CLOSE cusCur2;
END;
END //
DELIMITER ;