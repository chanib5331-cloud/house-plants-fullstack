import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import requests
from main import app


client = TestClient(app)

class TestPlantAPI:
    # Test cases for Plant API endpoints
    
    @patch('main.requests.get')
    def test_get_all_plants_success(self, mock_get):
        # Test successful retrieval of all plants
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": "1", "Latin name": "Test Plant", "Family": "Test Family", "Categories": "Test Category"}
        ]
        mock_get.return_value = mock_response
        
        response = client.get("/plants/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["Latin name"] == "Test Plant"
        assert data[0]["Family"] == "Test Family"
    
    @patch('main.requests.get')
    def test_get_all_plants_empty(self, mock_get):
        # Test when no plants are returned
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        response = client.get("/plants/")
        
        assert response.status_code == 204
        assert response.json() == {"message": "No plants found"}
    
   
    @patch('main.requests.get')
    def test_get_all_plants_connection_error(self, mock_get):
        # Test connection error handling
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        response = client.get("/plants/")
        
        assert response.status_code == 503
        assert "connect" in response.json()["detail"].lower()
    
    @patch('main.requests.get')
    def test_get_plant_detail_success(self, mock_get):
        # Test successful retrieval of plant details
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "123", 
            "Latin name": "Test Plant Detail", 
            "Family": "Test Family",
            "Description": "Test description"
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = client.get("/plants/123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["Latin name"] == "Test Plant Detail"
        assert data["id"] == "123"
    
    def test_get_plant_detail_empty_id(self):
        # Test plant detail with empty ID
        response = client.get("/plants/ ") 
        
        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]
    
    @patch('main.requests.get')
    def test_get_plant_detail_not_found(self, mock_get):
        # Test plant detail when plant not found
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        response = client.get("/plants/nonexistent")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
   

