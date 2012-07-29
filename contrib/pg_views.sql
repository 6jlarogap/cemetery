CREATE OR REPLACE VIEW common_burial1 AS
select *, substring(account_book_n FROM '([^[:digit:]]*)[[:digit:]]*.*') AS s1,
to_number(CASE WHEN trim(both ' ' from substring(account_book_n FROM '[^[:digit:]]*([[:digit:]]*).*'))='' THEN '9999999999' ELSE substring(account_book_n FROM '[^[:digit:]]*([[:digit:]]*).*') END, '9999999999') AS s2,
substring(account_book_n FROM '[^[:digit:]]*[[:digit:]]*(.*)') AS s3
from common_burial;

CREATE OR REPLACE VIEW common_place1
AS select *, substring(area FROM '([^[:digit:]]*)[[:digit:]]*.*') AS s1,
to_number(CASE WHEN trim(both ' ' from substring(area FROM '[^[:digit:]]*([[:digit:]]*).*'))='' THEN '9999999999' ELSE substring(area FROM '[^[:digit:]]*([[:digit:]]*).*') END, '9999999999') AS s2,
substring(area FROM '[^[:digit:]]*[[:digit:]]*(.*)') AS s3,
substring(row FROM '([^[:digit:]]*)[[:digit:]]*.*') AS s4,
to_number(CASE WHEN trim(both ' ' from substring(row FROM '[^[:digit:]]*([[:digit:]]*).*'))='' THEN '9999999999' ELSE substring(row FROM '[^[:digit:]]*([[:digit:]]*).*') END, '9999999999') AS s5,
substring(row FROM '[^[:digit:]]*[[:digit:]]*(.*)') AS s6,
substring(seat FROM '([^[:digit:]]*)[[:digit:]]*.*') AS s7,
to_number(CASE WHEN trim(both ' ' from substring(seat FROM '[^[:digit:]]*([[:digit:]]*).*'))='' THEN '9999999999' ELSE substring(seat FROM '[^[:digit:]]*([[:digit:]]*).*') END, '9999999999') AS s8,
substring(seat FROM '[^[:digit:]]*[[:digit:]]*(.*)') AS s9
from common_place;
