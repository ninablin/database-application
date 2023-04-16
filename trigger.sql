
CREATE TRIGGER updateColor BEFORE INSERT ON Item_list 
FOR EACH ROW
BEGIN
    SET @review = (
                    SELECT review
                    FROM Game_info NATURAL JOIN Item_list
                    WHERE Game_info.gameId = NEW.gameId
                    );
                    
    IF @review >= 8 THEN
        SET NEW.color = "Red";
    ELSEIF @review >= 5 THEN
        SET NEW.color = "Orange";
    ELSE
        SET NEW.color ="Yellow";
    END IF;    
END;
