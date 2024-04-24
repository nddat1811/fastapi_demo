-- Procedure
CREATE OR REPLACE PROCEDURE WaterBillInMonth(
--     IN input_parameter input_parameter_type,
	   in p_Month INT,
       INOUT refcur refcursor DEFAULT 'rs_resultone'::refcursor)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    OPEN refcur for
    SELECT u.username, u2.username as creator, w.prev_volume, w.cur_volume, 
        w.total_volume, w.price, w.total_volume_price, w.due_date, w.payment_date, w.created_at
    FROM water_bills w JOIN users u ON w.user_id = u.id
    				   join users u2 on w.created_by = u2.id
    WHERE p_Month = EXTRACT (MONTH FROM w.created_at);
--     query command, for example:
--     SELECT * FROM "user";
END;
$BODY$;
-- call procedure
CALL WaterBillInMonth(4, 'rs_resultone');
FETCH ALL FROM rs_resultone;

-- Function
CREATE OR REPLACE FUNCTION queryVolumeLargeInMonth(
    IN p_month INT
)
RETURNS TABLE (
    username VARCHAR,
    prev_volume INT,
    cur_volume INT,
    total_volume INT,
    price INT,
    total_volume_price INT,
    due_date TIMESTAMP,
    payment_date TIMESTAMP,
    created_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT u.username, w.prev_volume, w.cur_volume, 
        w.total_volume, w.price, w.total_volume_price, w.due_date, w.payment_date, w.created_at
    FROM water_bills w JOIN users u ON w.user_id = u.id
    WHERE p_month = EXTRACT (MONTH FROM w.created_at) and w.total_volume >= 50
    order by w.total_volume desc;
END;
$$;

select  queryVolumeLargeInMonth(4)