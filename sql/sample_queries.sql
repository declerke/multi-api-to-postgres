-- Sample Queries for ETL Pipeline Data
-- Use these queries to explore and analyze your collected data

-- ============================================
-- ADVICE QUOTES QUERIES
-- ============================================

-- Get 10 most recent advice quotes
SELECT 
    advice_id,
    advice_text,
    fetched_at
FROM advice_quotes
ORDER BY fetched_at DESC
LIMIT 10;

-- Search for advice containing specific keywords
SELECT 
    advice_text,
    fetched_at
FROM advice_quotes
WHERE advice_text ILIKE '%success%' OR advice_text ILIKE '%happy%'
ORDER BY fetched_at DESC;

-- Get the longest advice quotes
SELECT 
    advice_text,
    LENGTH(advice_text) as length,
    fetched_at
FROM advice_quotes
ORDER BY LENGTH(advice_text) DESC
LIMIT 10;

-- Count total advice collected
SELECT COUNT(*) as total_advice FROM advice_quotes;


-- ============================================
-- ACTIVITIES QUERIES
-- ============================================

-- Find free activities for 1 person
SELECT 
    activity,
    type,
    accessibility,
    fetched_at
FROM activities
WHERE price = 0.0 AND participants = 1
ORDER BY accessibility ASC;

-- Group activities by type
SELECT 
    type,
    COUNT(*) as count,
    AVG(price) as avg_price,
    AVG(accessibility) as avg_accessibility
FROM activities
GROUP BY type
ORDER BY count DESC;

-- Find activities by participant count
SELECT 
    participants,
    COUNT(*) as activity_count,
    AVG(price) as avg_price
FROM activities
GROUP BY participants
ORDER BY participants;

-- Find most accessible free activities
SELECT 
    activity,
    type,
    accessibility
FROM activities
WHERE price = 0.0
ORDER BY accessibility ASC
LIMIT 10;

-- Find expensive group activities
SELECT 
    activity,
    participants,
    price,
    type
FROM activities
WHERE price > 0.5 AND participants > 1
ORDER BY price DESC, participants DESC;

-- Activity statistics by type
SELECT 
    type,
    COUNT(*) as total_activities,
    MIN(price) as min_price,
    MAX(price) as max_price,
    AVG(accessibility) as avg_accessibility
FROM activities
GROUP BY type
ORDER BY total_activities DESC;


-- ============================================
-- DOG IMAGES QUERIES
-- ============================================

-- Count images by breed
SELECT 
    breed,
    COUNT(*) as image_count
FROM dog_images
GROUP BY breed
ORDER BY image_count DESC;

-- Get most recent dog images
SELECT 
    breed,
    image_url,
    fetched_at
FROM dog_images
ORDER BY fetched_at DESC
LIMIT 10;

-- Find all images of a specific breed
SELECT 
    image_url,
    fetched_at
FROM dog_images
WHERE breed ILIKE '%husky%'
ORDER BY fetched_at DESC;

-- Get random dog image
SELECT 
    breed,
    image_url
FROM dog_images
ORDER BY RANDOM()
LIMIT 1;


-- ============================================
-- CROSS-TABLE ANALYTICS
-- ============================================

-- Data collection summary
SELECT 
    'Advice Quotes' as data_type,
    COUNT(*) as total_records,
    MIN(fetched_at) as first_record,
    MAX(fetched_at) as last_record
FROM advice_quotes
UNION ALL
SELECT 
    'Activities',
    COUNT(*),
    MIN(fetched_at),
    MAX(fetched_at)
FROM activities
UNION ALL
SELECT 
    'Dog Images',
    COUNT(*),
    MIN(fetched_at),
    MAX(fetched_at)
FROM dog_images
ORDER BY data_type;

-- Records collected per day
SELECT 
    DATE(fetched_at) as collection_date,
    'advice' as type,
    COUNT(*) as records
FROM advice_quotes
GROUP BY DATE(fetched_at)
UNION ALL
SELECT 
    DATE(fetched_at),
    'activities',
    COUNT(*)
FROM activities
GROUP BY DATE(fetched_at)
UNION ALL
SELECT 
    DATE(fetched_at),
    'dog_images',
    COUNT(*)
FROM dog_images
GROUP BY DATE(fetched_at)
ORDER BY collection_date DESC, type;

-- Records collected per hour (for today)
SELECT 
    EXTRACT(HOUR FROM fetched_at) as hour,
    COUNT(*) as total_records
FROM (
    SELECT fetched_at FROM advice_quotes WHERE DATE(fetched_at) = CURRENT_DATE
    UNION ALL
    SELECT fetched_at FROM activities WHERE DATE(fetched_at) = CURRENT_DATE
    UNION ALL
    SELECT fetched_at FROM dog_images WHERE DATE(fetched_at) = CURRENT_DATE
) as all_records
GROUP BY EXTRACT(HOUR FROM fetched_at)
ORDER BY hour;


-- ============================================
-- DATA QUALITY CHECKS
-- ============================================

-- Check for any NULL values in advice
SELECT 
    'advice_quotes' as table_name,
    COUNT(*) as null_count
FROM advice_quotes
WHERE advice_text IS NULL OR advice_id IS NULL;

-- Check for any invalid activity data
SELECT 
    'activities' as table_name,
    COUNT(*) as invalid_count
FROM activities
WHERE 
    activity IS NULL OR
    price < 0 OR price > 1 OR
    accessibility < 0 OR accessibility > 1 OR
    participants < 1;

-- Check for duplicate image URLs
SELECT 
    image_url,
    COUNT(*) as duplicate_count
FROM dog_images
GROUP BY image_url
HAVING COUNT(*) > 1;

-- Find recently added records (last hour)
SELECT 
    'advice' as type,
    COUNT(*) as recent_records
FROM advice_quotes
WHERE fetched_at > NOW() - INTERVAL '1 hour'
UNION ALL
SELECT 
    'activities',
    COUNT(*)
FROM activities
WHERE fetched_at > NOW() - INTERVAL '1 hour'
UNION ALL
SELECT 
    'dog_images',
    COUNT(*)
FROM dog_images
WHERE fetched_at > NOW() - INTERVAL '1 hour';


-- ============================================
-- CLEANUP QUERIES (USE WITH CAUTION)
-- ============================================

-- Delete old records (older than 30 days)
-- UNCOMMENT ONLY IF YOU WANT TO RUN THESE

-- DELETE FROM advice_quotes WHERE fetched_at < NOW() - INTERVAL '30 days';
-- DELETE FROM activities WHERE fetched_at < NOW() - INTERVAL '30 days';
-- DELETE FROM dog_images WHERE fetched_at < NOW() - INTERVAL '30 days';

-- Truncate all tables (removes all data but keeps structure)
-- UNCOMMENT ONLY IF YOU WANT TO RUN THESE

-- TRUNCATE TABLE advice_quotes RESTART IDENTITY;
-- TRUNCATE TABLE activities RESTART IDENTITY;
-- TRUNCATE TABLE dog_images RESTART IDENTITY;