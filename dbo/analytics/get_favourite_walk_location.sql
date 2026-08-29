SELECT walk_location AS walk_location
FROM vitalx_walk 
WHERE walk_location IS NOT NULL AND walk_location != ''
GROUP BY walk_location 
ORDER BY COUNT(*) DESC 
LIMIT 1;
