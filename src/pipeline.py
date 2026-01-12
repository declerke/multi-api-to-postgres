import logging
from src.extractors import AdviceExtractor, QuoteExtractor, DogExtractor
from src.transformers import transform_advice, transform_quote_to_activity, transform_dog_image
from src.database import DatabaseConnection

logger = logging.getLogger(__name__)

def run_pipeline(batch_size=1):
    db = DatabaseConnection()
    advice_ext = AdviceExtractor()
    quote_ext = QuoteExtractor()
    dog_ext = DogExtractor()
    
    success = True
    
    try:
        for _ in range(batch_size):
            advice_raw = advice_ext.fetch_advice()
            advice_clean = transform_advice(advice_raw)
            if advice_clean:
                db.execute_query(
                    "INSERT INTO advice_quotes (advice_id, advice_text, fetched_at) VALUES (%s, %s, %s) ON CONFLICT (advice_id) DO NOTHING",
                    (advice_clean["advice_id"], advice_clean["advice_text"], advice_clean["fetched_at"])
                )

            quote_raw = quote_ext.fetch_quote()
            quote_clean = transform_quote_to_activity(quote_raw)
            if quote_clean:
                db.execute_query(
                    "INSERT INTO activities (activity_key, activity, type, participants, price, accessibility, fetched_at) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (activity_key) DO NOTHING",
                    (quote_clean["activity_key"], quote_clean["activity"], quote_clean["type"], quote_clean["participants"], quote_clean["price"], quote_clean["accessibility"], quote_clean["fetched_at"])
                )

            dog_raw = dog_ext.fetch_dog_image()
            dog_clean = transform_dog_image(dog_raw)
            if dog_clean:
                db.execute_query(
                    "INSERT INTO dog_images (breed, image_url, fetched_at) VALUES (%s, %s, %s) ON CONFLICT (image_url) DO NOTHING",
                    (dog_clean["breed"], dog_clean["image_url"], dog_clean["fetched_at"])
                )
                
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        success = False
        
    return success
