import pytest
from unittest.mock import Mock, patch, MagicMock
from src.extractors import AdviceExtractor, QuoteExtractor, DogExtractor
from src.transformers import (
    transform_advice, 
    transform_quote_to_activity, 
    transform_dog_image,
    extract_breed_from_url
)
from src.database import DatabaseConnection

class TestExtractors:
    
    @patch('src.extractors.requests.get')
    def test_advice_extractor_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'slip': {'id': 123, 'advice': 'Test advice'}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        extractor = AdviceExtractor()
        result = extractor.fetch_advice()
        
        assert result is not None
        assert result['id'] == 123
        assert result['advice'] == 'Test advice'
    
    @patch('src.extractors.requests.get')
    def test_quote_extractor_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [{
            'q': 'Test quote content',
            'a': 'Test Author'
        }]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        extractor = QuoteExtractor()
        result = extractor.fetch_quote()
        
        assert result is not None
        assert result[0]['q'] == 'Test quote content'
    
    @patch('src.extractors.requests.get')
    def test_dog_extractor_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'success',
            'message': 'https://images.dog.ceo/breeds/husky/image.jpg'
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        extractor = DogExtractor()
        result = extractor.fetch_dog_image()
        
        assert result is not None
        assert 'image_url' in result

class TestTransformers:
    
    def test_transform_advice_success(self):
        raw_data = {'id': 123, 'advice': '  Test advice  '}
        result = transform_advice(raw_data)
        
        assert result is not None
        assert result['advice_id'] == 123
        assert result['advice_text'] == 'Test advice'
    
    def test_transform_advice_invalid(self):
        result = transform_advice({'invalid': 'data'})
        assert result is None
    
    def test_transform_quote_to_activity_success(self):
        raw_data = [{
            'q': 'Test quote content',
            'a': 'Test Author'
        }]
        result = transform_quote_to_activity(raw_data)
        
        assert result is not None
        assert 'Quote by Test Author' in result['type']
        assert result['activity'] == 'Test quote content'
    
    def test_extract_breed_from_url(self):
        url = 'https://images.dog.ceo/breeds/husky-siberian/image.jpg'
        breed = extract_breed_from_url(url)
        assert breed == 'Husky Siberian'
        
        url2 = 'https://images.dog.ceo/breeds/beagle/image.jpg'
        breed2 = extract_breed_from_url(url2)
        assert breed2 == 'Beagle'
    
    def test_transform_dog_image_success(self):
        raw_data = {
            'image_url': 'https://images.dog.ceo/breeds/husky/image.jpg'
        }
        result = transform_dog_image(raw_data)
        
        assert result is not None
        assert 'image_url' in result
        assert 'breed' in result

class TestDatabase:
    
    def test_connection_string_generation(self):
        from src.config import Config
        conn_string = Config.get_db_connection_string()
        assert 'host=' in conn_string
        assert 'dbname=' in conn_string
    
    @patch('src.database.psycopg2.connect')
    def test_database_connection(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        db = DatabaseConnection()
        with db.get_connection() as conn:
            assert conn is not None

@pytest.mark.integration
class TestIntegration:
    
    def test_full_pipeline(self):
        pytest.skip("Requires live database connection")

if __name__ == '__main__':
    pytest.main([__file__, '-v'])