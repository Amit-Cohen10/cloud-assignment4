# assn4_tests.py - Pytest tests for Pet Store application
import pytest
import requests

# Base URLs for the services
PET_STORE_1_URL = "http://localhost:5001"
PET_STORE_2_URL = "http://localhost:5002"
PET_ORDER_URL = "http://localhost:5003"

# Pet Types payloads
PET_TYPE1 = {"type": "Golden Retriever"}
PET_TYPE2 = {"type": "Australian Shepherd"}
PET_TYPE3 = {"type": "Abyssinian"}
PET_TYPE4 = {"type": "bulldog"}

# Expected values for pet types
PET_TYPE1_VAL = {
    "type": "Golden Retriever",
    "family": "Canidae",
    "genus": "Canis",
    "attributes": [],
    "lifespan": 12
}

PET_TYPE2_VAL = {
    "type": "Australian Shepherd",
    "family": "Canidae",
    "genus": "Canis",
    "attributes": ["Loyal", "outgoing", "and", "friendly"],
    "lifespan": 15
}

PET_TYPE3_VAL = {
    "type": "Abyssinian",
    "family": "Felidae",
    "genus": "Felis",
    "attributes": ["Intelligent", "and", "curious"],
    "lifespan": 13
}

PET_TYPE4_VAL = {
    "type": "bulldog",
    "family": "Canidae",
    "genus": "Canis",
    "attributes": ["Gentle", "calm", "and", "affectionate"],
    "lifespan": None
}

# Pet payloads
PET1_TYPE1 = {"name": "Lander", "birthdate": "14-05-2020"}
PET2_TYPE1 = {"name": "Lanky", "birthdate": "07-07-2019"}
PET3_TYPE1 = {"name": "Shelly", "birthdate": "27-11-2011"}
PET4_TYPE2 = {"name": "Felicity", "birthdate": "27-11-2011"}
PET5_TYPE3 = {"name": "Muscles", "birthdate": "07-08-2018"}
PET6_TYPE3 = {"name": "Lazy", "birthdate": "07-08-2018"}
PET7_TYPE4 = {"name": "Junior", "birthdate": "27-03-2020"}
PET8_TYPE4 = {"name": "Lemon", "birthdate": "27-03-2020"}

# Global variables to store IDs returned from POST requests
store1_ids = {}  # {pet_type_name: id}
store2_ids = {}  # {pet_type_name: id}


class TestPetStoreApplication:
    """Test class for Pet Store CI/CD assignment"""

    # Tests 1 & 2: POST pet-types to store 1 and store 2
    def test_01_post_pet_types_to_store1(self):
        """
        Test 1: Execute 3 POST /pet-types requests to pet store #1 
        with payloads PET_TYPE1, PET_TYPE2, and PET_TYPE3.
        """
        global store1_ids
        
        pet_types = [
            (PET_TYPE1, PET_TYPE1_VAL, "type1"),
            (PET_TYPE2, PET_TYPE2_VAL, "type2"),
            (PET_TYPE3, PET_TYPE3_VAL, "type3")
        ]
        
        ids_collected = []
        
        for payload, expected_val, key in pet_types:
            response = requests.post(
                f"{PET_STORE_1_URL}/pet-types",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            # Check status code is 201
            assert response.status_code == 201, f"Expected 201, got {response.status_code} for {payload['type']}"
            
            data = response.json()
            
            # Check ID exists and is unique
            assert "id" in data, f"Response missing 'id' field for {payload['type']}"
            assert data["id"] not in ids_collected, f"Duplicate ID returned for {payload['type']}"
            ids_collected.append(data["id"])
            
            # Check family and genus match expected values
            assert data.get("family") == expected_val["family"], \
                f"Family mismatch for {payload['type']}: expected {expected_val['family']}, got {data.get('family')}"
            assert data.get("genus") == expected_val["genus"], \
                f"Genus mismatch for {payload['type']}: expected {expected_val['genus']}, got {data.get('genus')}"
            
            # Store the ID for later tests
            store1_ids[key] = data["id"]
        
        # Verify all IDs are unique
        assert len(set(ids_collected)) == 3, "Not all IDs are unique in store 1"

    def test_02_post_pet_types_to_store2(self):
        """
        Test 2: Execute 3 POST /pet-types requests to pet store #2 
        with payloads PET_TYPE1, PET_TYPE2, and PET_TYPE4.
        """
        global store2_ids
        
        pet_types = [
            (PET_TYPE1, PET_TYPE1_VAL, "type1"),
            (PET_TYPE2, PET_TYPE2_VAL, "type2"),
            (PET_TYPE4, PET_TYPE4_VAL, "type4")
        ]
        
        ids_collected = []
        
        for payload, expected_val, key in pet_types:
            response = requests.post(
                f"{PET_STORE_2_URL}/pet-types",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            # Check status code is 201
            assert response.status_code == 201, f"Expected 201, got {response.status_code} for {payload['type']}"
            
            data = response.json()
            
            # Check ID exists and is unique
            assert "id" in data, f"Response missing 'id' field for {payload['type']}"
            assert data["id"] not in ids_collected, f"Duplicate ID returned for {payload['type']}"
            ids_collected.append(data["id"])
            
            # Check family and genus match expected values
            assert data.get("family") == expected_val["family"], \
                f"Family mismatch for {payload['type']}: expected {expected_val['family']}, got {data.get('family')}"
            assert data.get("genus") == expected_val["genus"], \
                f"Genus mismatch for {payload['type']}: expected {expected_val['genus']}, got {data.get('genus')}"
            
            # Store the ID for later tests
            store2_ids[key] = data["id"]
        
        # Verify all IDs are unique
        assert len(set(ids_collected)) == 3, "Not all IDs are unique in store 2"

    # Tests 3 & 4: POST pets to store 1
    def test_03_post_pets_to_store1_type1(self):
        """
        Test 3: Execute POST /pet-types/{id_1}/pets to pet-store #1 
        with payload PET1_TYPE1 and another with payload PET2_TYPE1.
        """
        id_1 = store1_ids.get("type1")
        assert id_1 is not None, "ID for type1 in store 1 not found"
        
        # POST PET1_TYPE1
        response1 = requests.post(
            f"{PET_STORE_1_URL}/pet-types/{id_1}/pets",
            json=PET1_TYPE1,
            headers={"Content-Type": "application/json"}
        )
        assert response1.status_code == 201, f"Expected 201, got {response1.status_code} for PET1_TYPE1"
        
        # POST PET2_TYPE1
        response2 = requests.post(
            f"{PET_STORE_1_URL}/pet-types/{id_1}/pets",
            json=PET2_TYPE1,
            headers={"Content-Type": "application/json"}
        )
        assert response2.status_code == 201, f"Expected 201, got {response2.status_code} for PET2_TYPE1"

    def test_04_post_pets_to_store1_type3(self):
        """
        Test 4: Execute POST /pet-types/{id_3}/pets to pet-store #1 
        with payload PET5_TYPE3 and another with payload PET6_TYPE3.
        """
        id_3 = store1_ids.get("type3")
        assert id_3 is not None, "ID for type3 in store 1 not found"
        
        # POST PET5_TYPE3
        response1 = requests.post(
            f"{PET_STORE_1_URL}/pet-types/{id_3}/pets",
            json=PET5_TYPE3,
            headers={"Content-Type": "application/json"}
        )
        assert response1.status_code == 201, f"Expected 201, got {response1.status_code} for PET5_TYPE3"
        
        # POST PET6_TYPE3
        response2 = requests.post(
            f"{PET_STORE_1_URL}/pet-types/{id_3}/pets",
            json=PET6_TYPE3,
            headers={"Content-Type": "application/json"}
        )
        assert response2.status_code == 201, f"Expected 201, got {response2.status_code} for PET6_TYPE3"

    # Tests 5, 6, 7: POST pets to store 2
    def test_05_post_pets_to_store2_type1(self):
        """
        Test 5: Execute POST /pet-types/{id_4}/pets to pet-store #2 
        with payload PET3_TYPE1.
        """
        id_4 = store2_ids.get("type1")
        assert id_4 is not None, "ID for type1 in store 2 not found"
        
        response = requests.post(
            f"{PET_STORE_2_URL}/pet-types/{id_4}/pets",
            json=PET3_TYPE1,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 201, f"Expected 201, got {response.status_code} for PET3_TYPE1"

    def test_06_post_pets_to_store2_type2(self):
        """
        Test 6: Execute POST /pet-types/{id_5}/pets to pet-store #2 
        with payload PET4_TYPE2.
        """
        id_5 = store2_ids.get("type2")
        assert id_5 is not None, "ID for type2 in store 2 not found"
        
        response = requests.post(
            f"{PET_STORE_2_URL}/pet-types/{id_5}/pets",
            json=PET4_TYPE2,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 201, f"Expected 201, got {response.status_code} for PET4_TYPE2"

    def test_07_post_pets_to_store2_type4(self):
        """
        Test 7: Execute POST /pet-types/{id_6}/pets to pet-store #2 
        with payload PET7_TYPE4 and another with payload PET8_TYPE4.
        """
        id_6 = store2_ids.get("type4")
        assert id_6 is not None, "ID for type4 in store 2 not found"
        
        # POST PET7_TYPE4
        response1 = requests.post(
            f"{PET_STORE_2_URL}/pet-types/{id_6}/pets",
            json=PET7_TYPE4,
            headers={"Content-Type": "application/json"}
        )
        assert response1.status_code == 201, f"Expected 201, got {response1.status_code} for PET7_TYPE4"
        
        # POST PET8_TYPE4
        response2 = requests.post(
            f"{PET_STORE_2_URL}/pet-types/{id_6}/pets",
            json=PET8_TYPE4,
            headers={"Content-Type": "application/json"}
        )
        assert response2.status_code == 201, f"Expected 201, got {response2.status_code} for PET8_TYPE4"

    # Test 8: GET pet-type from store 1
    def test_08_get_pet_type_from_store1(self):
        """
        Test 8: Execute GET /pet-types/{id2} to pet-store #1.
        The test is successful if the JSON returned matches all the fields 
        given in PET_TYPE2_VAL and the return status code is 200.
        """
        id_2 = store1_ids.get("type2")
        assert id_2 is not None, "ID for type2 in store 1 not found"
        
        response = requests.get(f"{PET_STORE_1_URL}/pet-types/{id_2}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Verify all fields match PET_TYPE2_VAL
        assert data.get("type") == PET_TYPE2_VAL["type"], \
            f"Type mismatch: expected {PET_TYPE2_VAL['type']}, got {data.get('type')}"
        assert data.get("family") == PET_TYPE2_VAL["family"], \
            f"Family mismatch: expected {PET_TYPE2_VAL['family']}, got {data.get('family')}"
        assert data.get("genus") == PET_TYPE2_VAL["genus"], \
            f"Genus mismatch: expected {PET_TYPE2_VAL['genus']}, got {data.get('genus')}"
        assert data.get("lifespan") == PET_TYPE2_VAL["lifespan"], \
            f"Lifespan mismatch: expected {PET_TYPE2_VAL['lifespan']}, got {data.get('lifespan')}"
        
        # Check attributes (may be in different order)
        expected_attrs = set(PET_TYPE2_VAL["attributes"])
        actual_attrs = set(data.get("attributes", []))
        assert expected_attrs == actual_attrs, \
            f"Attributes mismatch: expected {expected_attrs}, got {actual_attrs}"

    # Test 9: GET pets from store 2
    def test_09_get_pets_from_store2(self):
        """
        Test 9: Execute a GET /pet-types/{id6}/pets to pet-store #2.
        The test is successful if the returned value is a JSON array containing 
        JSON pet objects with the fields given in PET7_TYPE4 and PET8_TYPE4,
        and the return status code is 200.
        """
        id_6 = store2_ids.get("type4")
        assert id_6 is not None, "ID for type4 in store 2 not found"
        
        response = requests.get(f"{PET_STORE_2_URL}/pet-types/{id_6}/pets")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Should be a list
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        
        # Should contain 2 pets
        assert len(data) == 2, f"Expected 2 pets, got {len(data)}"
        
        # Extract pet names from response
        pet_names = {pet.get("name") for pet in data}
        expected_names = {PET7_TYPE4["name"], PET8_TYPE4["name"]}
        
        assert expected_names == pet_names, \
            f"Pet names mismatch: expected {expected_names}, got {pet_names}"
        
        # Verify each pet has the correct fields
        for pet in data:
            if pet.get("name") == PET7_TYPE4["name"]:
                assert pet.get("birthdate") == PET7_TYPE4["birthdate"], \
                    f"Birthdate mismatch for {PET7_TYPE4['name']}"
            elif pet.get("name") == PET8_TYPE4["name"]:
                assert pet.get("birthdate") == PET8_TYPE4["birthdate"], \
                    f"Birthdate mismatch for {PET8_TYPE4['name']}"
