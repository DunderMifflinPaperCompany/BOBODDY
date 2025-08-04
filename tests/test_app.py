import pytest
import json
import string
from app import app, generate_random_acronym, get_corporate_definition, get_creed_definition

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestAcronymGeneration:
    """Test the random acronym generation functionality"""
    
    def test_generate_random_acronym_default_length(self):
        """Test that random acronym generation produces reasonable lengths"""
        acronym = generate_random_acronym()
        assert len(acronym) >= 5
        assert len(acronym) <= 8
        assert acronym.isupper()
        assert all(c in string.ascii_uppercase for c in acronym)
    
    def test_generate_random_acronym_specific_length(self):
        """Test generating acronym with specific length"""
        for length in [3, 5, 7, 10]:
            acronym = generate_random_acronym(length)
            assert len(acronym) == length
            assert acronym.isupper()
            assert all(c in string.ascii_uppercase for c in acronym)
    
    def test_generate_random_acronym_uniqueness(self):
        """Test that multiple generations produce different results (usually)"""
        acronyms = set()
        for _ in range(10):
            acronyms.add(generate_random_acronym(5))
        # Should have some variety (allowing for small chance of duplicates)
        assert len(acronyms) >= 3

class TestDefinitionGeneration:
    """Test the definition generation for different modes"""
    
    def test_get_corporate_definition(self):
        """Test corporate jargon definition generation"""
        definition = get_corporate_definition('B')
        assert isinstance(definition, str)
        assert len(definition) > 0
        # Should be a meaningful word, not empty
        assert definition.strip() != ''
    
    def test_get_corporate_definition_various_letters(self):
        """Test corporate definitions for various letters"""
        for letter in ['A', 'B', 'O', 'D', 'Y', 'Z']:
            definition = get_corporate_definition(letter)
            assert isinstance(definition, str)
            assert len(definition) > 0
    
    def test_get_creed_definition(self):
        """Test Creed-style definition generation"""
        definition = get_creed_definition('B')
        assert isinstance(definition, str)
        assert len(definition) > 0
        # Should be one of the predefined Creed quotes
        from app import CREED_DEFINITIONS
        assert definition in CREED_DEFINITIONS
    
    def test_get_creed_definition_consistency(self):
        """Test that Creed definitions come from the predefined list"""
        from app import CREED_DEFINITIONS
        for _ in range(10):
            definition = get_creed_definition('X')
            assert definition in CREED_DEFINITIONS

class TestWebApp:
    """Test the Flask web application endpoints"""
    
    def test_index_page(self, client):
        """Test that the main page loads correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'BOBODDY Brainstorm Engine' in response.data
        assert b'acronym-letters' in response.data
    
    def test_health_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_generate_acronym_endpoint(self, client):
        """Test the acronym generation API endpoint"""
        response = client.get('/generate_acronym')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'acronym' in data
        acronym = data['acronym']
        assert isinstance(acronym, str)
        assert len(acronym) >= 5
        assert len(acronym) <= 8
        assert acronym.isupper()
    
    def test_get_definition_manual_mode(self, client):
        """Test definition endpoint in manual mode"""
        response = client.post('/get_definition',
                              json={'letter': 'B', 'mode': 'manual'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'definition' in data
        assert data['definition'] == ''  # Manual mode returns empty string
    
    def test_get_definition_corporate_mode(self, client):
        """Test definition endpoint in corporate mode"""
        response = client.post('/get_definition',
                              json={'letter': 'B', 'mode': 'corporate'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'definition' in data
        assert len(data['definition']) > 0
        assert isinstance(data['definition'], str)
    
    def test_get_definition_creed_mode(self, client):
        """Test definition endpoint in creed mode"""
        response = client.post('/get_definition',
                              json={'letter': 'C', 'mode': 'creed'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'definition' in data
        from app import CREED_DEFINITIONS
        assert data['definition'] in CREED_DEFINITIONS
    
    def test_get_definition_invalid_mode(self, client):
        """Test definition endpoint with invalid mode falls back to manual"""
        response = client.post('/get_definition',
                              json={'letter': 'B', 'mode': 'invalid_mode'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['definition'] == ''  # Should fall back to manual mode

class TestDataIntegrity:
    """Test the integrity of the data used in the app"""
    
    def test_corporate_jargon_data(self):
        """Test that corporate jargon data is properly structured"""
        from app import CORPORATE_JARGON
        
        assert isinstance(CORPORATE_JARGON, dict)
        assert 'business_words' in CORPORATE_JARGON
        assert 'optimization_words' in CORPORATE_JARGON
        assert 'general_words' in CORPORATE_JARGON
        
        for category, words in CORPORATE_JARGON.items():
            assert isinstance(words, list)
            assert len(words) > 0
            for word in words:
                assert isinstance(word, str)
                assert len(word) > 0
    
    def test_creed_definitions_data(self):
        """Test that Creed definitions data is properly structured"""
        from app import CREED_DEFINITIONS
        
        assert isinstance(CREED_DEFINITIONS, list)
        assert len(CREED_DEFINITIONS) > 0
        
        for definition in CREED_DEFINITIONS:
            assert isinstance(definition, str)
            assert len(definition) > 0
    
    def test_corporate_definition_letter_matching(self):
        """Test that corporate definitions can handle all letters"""
        # Test with letters that should have matches
        for letter in ['B', 'O', 'S']:
            definition = get_corporate_definition(letter)
            assert isinstance(definition, str)
            assert len(definition) > 0
        
        # Test with letters that might not have matches
        for letter in ['X', 'Z', 'Q']:
            definition = get_corporate_definition(letter)
            assert isinstance(definition, str)
            assert len(definition) > 0  # Should fall back to general words

if __name__ == '__main__':
    pytest.main([__file__])