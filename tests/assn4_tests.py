# # assn4_tests.py - Pytest tests for Pet Store application
# import pytest
# import requests

# # Base URLs for the services
# PET_STORE_1_URL = "http://localhost:5001"
# PET_STORE_2_URL = "http://localhost:5002"
# PET_ORDER_URL = "http://localhost:5003"

# # Pet Types payloads
# PET_TYPE1 = {"type": "Golden Retriever"}
# PET_TYPE2 = {"type": "Australian Shepherd"}
# PET_TYPE3 = {"type": "Abyssinian"}
# PET_TYPE4 = {"type": "bulldog"}

# # Expected values for pet types
# PET_TYPE1_VAL = {
#     "type": "Golden Retriever",
#     "family": "Canidae",
#     "genus": "Canis",
#     "attributes": [],
#     "lifespan": 12
# }

# PET_TYPE2_VAL = {
#     "type": "Australian Shepherd",
#     "family": "Canidae",
#     "genus": "Canis",
#     "attributes": ["Loyal", "outgoing", "and", "friendly"],
#     "lifespan": 15
# }

# PET_TYPE3_VAL = {
#     "type": "Abyssinian",
#     "family": "Felidae",
#     "genus": "Felis",
#     "attributes": ["Intelligent", "and", "curious"],
#     "lifespan": 13
# }

# PET_TYPE4_VAL = {
#     "type": "bulldog",
#     "family": "Canidae",
#     "genus": "Canis",
#     "attributes": ["Gentle", "calm", "and", "affectionate"],
#     "lifespan": None
# }

# # Pet payloads (EXACTLY as shown in official assignment slides)
# PET1_TYPE1 = {"name": "Lander", "birthdate": "14-05-2020"}
# PET2_TYPE1 = {"name": "Lanky"}  # No birthdate in slides
# PET3_TYPE1 = {"name": "Shelly", "birthdate": "07-07-2019"}
# PET4_TYPE2 = {"name": "Felicity", "birthdate": "27-11-2011"}
# PET5_TYPE3 = {"name": "Muscles"}  # No birthdate in slides
# PET6_TYPE3 = {"name": "Junior"}  # No birthdate in slides
# PET7_TYPE4 = {"name": "Lazy", "birthdate": "07-08-2018"}
# PET8_TYPE4 = {"name": "Lemon", "birthdate": "27-03-2020"}

# # Global variables to store IDs returned from POST requests
# store1_ids = {}  # {pet_type_name: id}
# store2_ids = {}  # {pet_type_name: id}


# class TestPetStoreApplication:
#     """Test class for Pet Store CI/CD assignment"""

#     # Tests 1 & 2: POST pet-types to store 1 and store 2
#     def test_01_post_pet_types_to_store1(self):
#         """
#         Test 1: Execute 3 POST /pet-types requests to pet store #1 
#         with payloads PET_TYPE1, PET_TYPE2, and PET_TYPE3.
#         """
#         global store1_ids
        
#         pet_types = [
#             (PET_TYPE1, PET_TYPE1_VAL, "type1"),
#             (PET_TYPE2, PET_TYPE2_VAL, "type2"),
#             (PET_TYPE3, PET_TYPE3_VAL, "type3")
#         ]
        
#         ids_collected = []
        
#         for payload, expected_val, key in pet_types:
#             response = requests.post(
#                 f"{PET_STORE_1_URL}/pet-types",
#                 json=payload,
#                 headers={"Content-Type": "application/json"}
#             )
            
#             # Check status code is 201
#             assert response.status_code == 201, f"Expected 201, got {response.status_code} for {payload['type']}"
            
#             data = response.json()
            
#             # Check ID exists and is unique
#             assert "id" in data, f"Response missing 'id' field for {payload['type']}"
#             assert data["id"] not in ids_collected, f"Duplicate ID returned for {payload['type']}"
#             ids_collected.append(data["id"])
            
#             # Check family and genus match expected values (case-insensitive)
#             assert data.get("family", "").lower() == expected_val["family"].lower(), \
#                 f"Family mismatch for {payload['type']}: expected {expected_val['family']}, got {data.get('family')}"
#             assert data.get("genus", "").lower() == expected_val["genus"].lower(), \
#                 f"Genus mismatch for {payload['type']}: expected {expected_val['genus']}, got {data.get('genus')}"
            
#             # Store the ID for later tests
#             store1_ids[key] = data["id"]
        
#         # Verify all IDs are unique
#         assert len(set(ids_collected)) == 3, "Not all IDs are unique in store 1"

#     def test_02_post_pet_types_to_store2(self):
#         """
#         Test 2: Execute 3 POST /pet-types requests to pet store #2 
#         with payloads PET_TYPE1, PET_TYPE2, and PET_TYPE4.
#         """
#         global store2_ids
        
#         pet_types = [
#             (PET_TYPE1, PET_TYPE1_VAL, "type1"),
#             (PET_TYPE2, PET_TYPE2_VAL, "type2"),
#             (PET_TYPE4, PET_TYPE4_VAL, "type4")
#         ]
        
#         ids_collected = []
        
#         for payload, expected_val, key in pet_types:
#             response = requests.post(
#                 f"{PET_STORE_2_URL}/pet-types",
#                 json=payload,
#                 headers={"Content-Type": "application/json"}
#             )
            
#             # Check status code is 201
#             assert response.status_code == 201, f"Expected 201, got {response.status_code} for {payload['type']}"
            
#             data = response.json()
            
#             # Check ID exists and is unique
#             assert "id" in data, f"Response missing 'id' field for {payload['type']}"
#             assert data["id"] not in ids_collected, f"Duplicate ID returned for {payload['type']}"
#             ids_collected.append(data["id"])
            
#             # Check family and genus match expected values (case-insensitive)
#             assert data.get("family", "").lower() == expected_val["family"].lower(), \
#                 f"Family mismatch for {payload['type']}: expected {expected_val['family']}, got {data.get('family')}"
#             assert data.get("genus", "").lower() == expected_val["genus"].lower(), \
#                 f"Genus mismatch for {payload['type']}: expected {expected_val['genus']}, got {data.get('genus')}"
            
#             # Store the ID for later tests
#             store2_ids[key] = data["id"]
        
#         # Verify all IDs are unique
#         assert len(set(ids_collected)) == 3, "Not all IDs are unique in store 2"

#     # Tests 3 & 4: POST pets to store 1
#     def test_03_post_pets_to_store1_type1(self):
#         """
#         Test 3: Execute POST /pet-types/{id_1}/pets to pet-store #1 
#         with payload PET1_TYPE1 and another with payload PET2_TYPE1.
#         """
#         id_1 = store1_ids.get("type1")
#         assert id_1 is not None, "ID for type1 in store 1 not found"
        
#         # POST PET1_TYPE1
#         response1 = requests.post(
#             f"{PET_STORE_1_URL}/pet-types/{id_1}/pets",
#             json=PET1_TYPE1,
#             headers={"Content-Type": "application/json"}
#         )
#         assert response1.status_code == 201, f"Expected 201, got {response1.status_code} for PET1_TYPE1"
        
#         # POST PET2_TYPE1
#         response2 = requests.post(
#             f"{PET_STORE_1_URL}/pet-types/{id_1}/pets",
#             json=PET2_TYPE1,
#             headers={"Content-Type": "application/json"}
#         )
#         assert response2.status_code == 201, f"Expected 201, got {response2.status_code} for PET2_TYPE1"

#     def test_04_post_pets_to_store1_type3(self):
#         """
#         Test 4: Execute POST /pet-types/{id_3}/pets to pet-store #1 
#         with payload PET5_TYPE3 and another with payload PET6_TYPE3.
#         """
#         id_3 = store1_ids.get("type3")
#         assert id_3 is not None, "ID for type3 in store 1 not found"
        
#         # POST PET5_TYPE3
#         response1 = requests.post(
#             f"{PET_STORE_1_URL}/pet-types/{id_3}/pets",
#             json=PET5_TYPE3,
#             headers={"Content-Type": "application/json"}
#         )
#         assert response1.status_code == 201, f"Expected 201, got {response1.status_code} for PET5_TYPE3"
        
#         # POST PET6_TYPE3
#         response2 = requests.post(
#             f"{PET_STORE_1_URL}/pet-types/{id_3}/pets",
#             json=PET6_TYPE3,
#             headers={"Content-Type": "application/json"}
#         )
#         assert response2.status_code == 201, f"Expected 201, got {response2.status_code} for PET6_TYPE3"

#     # Tests 5, 6, 7: POST pets to store 2
#     def test_05_post_pets_to_store2_type1(self):
#         """
#         Test 5: Execute POST /pet-types/{id_4}/pets to pet-store #2 
#         with payload PET3_TYPE1.
#         """
#         id_4 = store2_ids.get("type1")
#         assert id_4 is not None, "ID for type1 in store 2 not found"
        
#         response = requests.post(
#             f"{PET_STORE_2_URL}/pet-types/{id_4}/pets",
#             json=PET3_TYPE1,
#             headers={"Content-Type": "application/json"}
#         )
#         assert response.status_code == 201, f"Expected 201, got {response.status_code} for PET3_TYPE1"

#     def test_06_post_pets_to_store2_type2(self):
#         """
#         Test 6: Execute POST /pet-types/{id_5}/pets to pet-store #2 
#         with payload PET4_TYPE2.
#         """
#         id_5 = store2_ids.get("type2")
#         assert id_5 is not None, "ID for type2 in store 2 not found"
        
#         response = requests.post(
#             f"{PET_STORE_2_URL}/pet-types/{id_5}/pets",
#             json=PET4_TYPE2,
#             headers={"Content-Type": "application/json"}
#         )
#         assert response.status_code == 201, f"Expected 201, got {response.status_code} for PET4_TYPE2"

#     def test_07_post_pets_to_store2_type4(self):
#         """
#         Test 7: Execute POST /pet-types/{id_6}/pets to pet-store #2 
#         with payload PET7_TYPE4 and another with payload PET8_TYPE4.
#         """
#         id_6 = store2_ids.get("type4")
#         assert id_6 is not None, "ID for type4 in store 2 not found"
        
#         # POST PET7_TYPE4
#         response1 = requests.post(
#             f"{PET_STORE_2_URL}/pet-types/{id_6}/pets",
#             json=PET7_TYPE4,
#             headers={"Content-Type": "application/json"}
#         )
#         assert response1.status_code == 201, f"Expected 201, got {response1.status_code} for PET7_TYPE4"
        
#         # POST PET8_TYPE4
#         response2 = requests.post(
#             f"{PET_STORE_2_URL}/pet-types/{id_6}/pets",
#             json=PET8_TYPE4,
#             headers={"Content-Type": "application/json"}
#         )
#         assert response2.status_code == 201, f"Expected 201, got {response2.status_code} for PET8_TYPE4"

#     # Test 8: GET pet-type from store 1
#     def test_08_get_pet_type_from_store1(self):
#         """
#         Test 8: Execute GET /pet-types/{id2} to pet-store #1.
#         The test is successful if the JSON returned matches all the fields 
#         given in PET_TYPE2_VAL and the return status code is 200.
#         """
#         id_2 = store1_ids.get("type2")
#         assert id_2 is not None, "ID for type2 in store 1 not found"
        
#         response = requests.get(f"{PET_STORE_1_URL}/pet-types/{id_2}")
        
#         assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
#         data = response.json()
        
#         # Verify all fields match PET_TYPE2_VAL (case-insensitive for strings)
#         assert data.get("type", "").lower() == PET_TYPE2_VAL["type"].lower(), \
#             f"Type mismatch: expected {PET_TYPE2_VAL['type']}, got {data.get('type')}"
#         assert data.get("family", "").lower() == PET_TYPE2_VAL["family"].lower(), \
#             f"Family mismatch: expected {PET_TYPE2_VAL['family']}, got {data.get('family')}"
#         assert data.get("genus", "").lower() == PET_TYPE2_VAL["genus"].lower(), \
#             f"Genus mismatch: expected {PET_TYPE2_VAL['genus']}, got {data.get('genus')}"
#         assert data.get("lifespan") == PET_TYPE2_VAL["lifespan"], \
#             f"Lifespan mismatch: expected {PET_TYPE2_VAL['lifespan']}, got {data.get('lifespan')}"
        
#         # Check attributes (may be in different order, case-insensitive)
#         expected_attrs = {attr.lower() for attr in PET_TYPE2_VAL["attributes"]}
#         actual_attrs = {attr.lower() for attr in data.get("attributes", [])}
#         assert expected_attrs == actual_attrs, \
#             f"Attributes mismatch: expected {expected_attrs}, got {actual_attrs}"

#     # Test 9: GET pets from store 2
#     def test_09_get_pets_from_store2(self):
#         """
#         Test 9: Execute a GET /pet-types/{id6}/pets to pet-store #2.
#         The test is successful if the returned value is a JSON array containing 
#         JSON pet objects with the fields given in PET7_TYPE4 and PET8_TYPE4,
#         and the return status code is 200.
#         """
#         id_6 = store2_ids.get("type4")
#         assert id_6 is not None, "ID for type4 in store 2 not found"
        
#         response = requests.get(f"{PET_STORE_2_URL}/pet-types/{id_6}/pets")
        
#         assert response.status_code == 200, f"Expected 200, got {response.status_code}"
#         # assert response.status_code == 404, f"Expected 200, got {response.status_code}"
        
#         data = response.json()
        
#         # Should be a list
#         assert isinstance(data, list), f"Expected list, got {type(data)}"
        
#         # Should contain 2 pets
#         assert len(data) == 2, f"Expected 2 pets, got {len(data)}"
        
#         # Extract pet names from response (case-insensitive)
#         pet_names = {pet.get("name", "").lower() for pet in data}
#         expected_names = {PET7_TYPE4["name"].lower(), PET8_TYPE4["name"].lower()}
        
#         assert expected_names == pet_names, \
#             f"Pet names mismatch: expected {expected_names}, got {pet_names}"
        
#         # Verify each pet has the correct fields (case-insensitive name matching)
#         for pet in data:
#             if pet.get("name", "").lower() == PET7_TYPE4["name"].lower():
#                 assert pet.get("birthdate") == PET7_TYPE4["birthdate"], \
#                     f"Birthdate mismatch for {PET7_TYPE4['name']}"
#             elif pet.get("name", "").lower() == PET8_TYPE4["name"].lower():
#                 assert pet.get("birthdate") == PET8_TYPE4["birthdate"], \
#                     f"Birthdate mismatch for {PET8_TYPE4['name']}"


# - tester file -

import pytest
import requests
import json

# Test data from Assignment #4 specification
PET_TYPE1 = {"type": "Golden Retriever"}
PET_TYPE1_VAL = {
    "type": "Golden Retriever",
    "family": "Canidae",
    "genus": "Canis",
    "attributes": [],
    "lifespan": 12
}

PET_TYPE2 = {"type": "Australian Shepherd"}
PET_TYPE2_VAL = {
    "type": "Australian Shepherd",
    "family": "Canidae",
    "genus": "Canis",
    "attributes": ["Loyal", "outgoing", "and", "friendly"],
    "lifespan": 15
}

PET_TYPE3 = {"type": "Abyssinian"}
PET_TYPE3_VAL = {
    "type": "Abyssinian",
    "family": "Felidae",
    "genus": "Felis",
    "attributes": ["Intelligent", "and", "curious"],
    "lifespan": 13
}

PET_TYPE4 = {"type": "bulldog"}
PET_TYPE4_VAL = {
    "type": "bulldog",
    "family": "Canidae",
    "genus": "Canis",
    "attributes": ["Gentle", "calm", "and", "affectionate"],
    "lifespan": None
}

PET1_TYPE1 = {"name": "Lander", "birthdate": "14-05-2020"}
PET2_TYPE1 = {"name": "Lanky"}
PET3_TYPE1 = {"name": "Shelly", "birthdate": "07-07-2019"}
PET4_TYPE2 = {"name": "Felicity", "birthdate": "27-11-2011"}
PET5_TYPE3 = {"name": "Muscles"}
PET6_TYPE3 = {"name": "Junior"}
PET7_TYPE4 = {"name": "Lazy", "birthdate": "07-08-2018"}
PET8_TYPE4 = {"name": "Lemon", "birthdate": "27-03-2020"}

# Base URLs for the services
STORE1_URL = "http://localhost:5001"
STORE2_URL = "http://localhost:5002"

# Global variables to store IDs
pet_type_ids = []


class TestPetStoreAssignment4:
    """Test suite for Assignment #4 - Pet Store Application"""

    def test_01_post_pet_types_to_store1(self):
        """Test 1-2: POST 3 pet-types to pet-store #1"""
        global pet_type_ids
        
        # POST PET_TYPE1 to store #1
        response1 = requests.post(f"{STORE1_URL}/pet-types", json=PET_TYPE1)
        assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
        data1 = response1.json()
        
        # Validate returned data
        assert "id" in data1, "Response should contain 'id' field"
        assert data1["type"] == PET_TYPE1_VAL["type"], f"Type mismatch"
        assert data1["family"] == PET_TYPE1_VAL["family"], f"Family mismatch"
        assert data1["genus"] == PET_TYPE1_VAL["genus"], f"Genus mismatch"
        
        id_1 = data1["id"]
        pet_type_ids.append(id_1)
        
        # POST PET_TYPE2 to store #1
        response2 = requests.post(f"{STORE1_URL}/pet-types", json=PET_TYPE2)
        assert response2.status_code == 201, f"Expected 201, got {response2.status_code}"
        data2 = response2.json()
        
        assert "id" in data2, "Response should contain 'id' field"
        assert data2["type"] == PET_TYPE2_VAL["type"], f"Type mismatch"
        assert data2["family"] == PET_TYPE2_VAL["family"], f"Family mismatch"
        assert data2["genus"] == PET_TYPE2_VAL["genus"], f"Genus mismatch"
        
        id_2 = data2["id"]
        pet_type_ids.append(id_2)
        
        # POST PET_TYPE3 to store #1
        response3 = requests.post(f"{STORE1_URL}/pet-types", json=PET_TYPE3)
        assert response3.status_code == 201, f"Expected 201, got {response3.status_code}"
        data3 = response3.json()
        
        assert "id" in data3, "Response should contain 'id' field"
        assert data3["type"] == PET_TYPE3_VAL["type"], f"Type mismatch"
        assert data3["family"] == PET_TYPE3_VAL["family"], f"Family mismatch"
        assert data3["genus"] == PET_TYPE3_VAL["genus"], f"Genus mismatch"
        
        id_3 = data3["id"]
        pet_type_ids.append(id_3)
        
        # Verify all IDs are unique
        assert len(set([id_1, id_2, id_3])) == 3, "All IDs should be unique"

    def test_02_post_pet_types_to_store2(self):
        """Test 1-2: POST 3 pet-types to pet-store #2"""
        global pet_type_ids
        
        # POST PET_TYPE1 to store #2
        response4 = requests.post(f"{STORE2_URL}/pet-types", json=PET_TYPE1)
        assert response4.status_code == 201, f"Expected 201, got {response4.status_code}"
        data4 = response4.json()
        
        assert "id" in data4, "Response should contain 'id' field"
        assert data4["type"] == PET_TYPE1_VAL["type"], f"Type mismatch"
        assert data4["family"] == PET_TYPE1_VAL["family"], f"Family mismatch"
        assert data4["genus"] == PET_TYPE1_VAL["genus"], f"Genus mismatch"
        
        id_4 = data4["id"]
        pet_type_ids.append(id_4)
        
        # POST PET_TYPE2 to store #2
        response5 = requests.post(f"{STORE2_URL}/pet-types", json=PET_TYPE2)
        assert response5.status_code == 201, f"Expected 201, got {response5.status_code}"
        data5 = response5.json()
        
        assert "id" in data5, "Response should contain 'id' field"
        assert data5["type"] == PET_TYPE2_VAL["type"], f"Type mismatch"
        assert data5["family"] == PET_TYPE2_VAL["family"], f"Family mismatch"
        assert data5["genus"] == PET_TYPE2_VAL["genus"], f"Genus mismatch"
        
        id_5 = data5["id"]
        pet_type_ids.append(id_5)
        
        # POST PET_TYPE4 to store #2
        response6 = requests.post(f"{STORE2_URL}/pet-types", json=PET_TYPE4)
        assert response6.status_code == 201, f"Expected 201, got {response6.status_code}"
        data6 = response6.json()
        
        assert "id" in data6, "Response should contain 'id' field"
        assert data6["type"] == PET_TYPE4_VAL["type"], f"Type mismatch"
        assert data6["family"] == PET_TYPE4_VAL["family"], f"Family mismatch"
        assert data6["genus"] == PET_TYPE4_VAL["genus"], f"Genus mismatch"
        
        id_6 = data6["id"]
        pet_type_ids.append(id_6)
        
        # Verify all IDs are unique (within store #2)
        assert len(set([id_4, id_5, id_6])) == 3, "All IDs should be unique"

    def test_03_post_pets_to_store1_type1(self):
        """Test 3: POST 2 pets of type 1 to pet-store #1"""
        global pet_type_ids
        id_1 = pet_type_ids[0]
        
        # POST PET1_TYPE1
        response1 = requests.post(
            f"{STORE1_URL}/pet-types/{id_1}/pets",
            json=PET1_TYPE1
        )
        assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
        
        # POST PET2_TYPE1
        response2 = requests.post(
            f"{STORE1_URL}/pet-types/{id_1}/pets",
            json=PET2_TYPE1
        )
        assert response2.status_code == 201, f"Expected 201, got {response2.status_code}"

    def test_04_post_pets_to_store1_type3(self):
        """Test 4: POST 2 pets of type 3 to pet-store #1"""
        global pet_type_ids
        id_3 = pet_type_ids[2]
        
        # POST PET5_TYPE3
        response1 = requests.post(
            f"{STORE1_URL}/pet-types/{id_3}/pets",
            json=PET5_TYPE3
        )
        assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
        
        # POST PET6_TYPE3
        response2 = requests.post(
            f"{STORE1_URL}/pet-types/{id_3}/pets",
            json=PET6_TYPE3
        )
        assert response2.status_code == 201, f"Expected 201, got {response2.status_code}"

    def test_05_post_pet_to_store2_type1(self):
        """Test 5: POST 1 pet of type 1 to pet-store #2"""
        global pet_type_ids
        id_4 = pet_type_ids[3]
        
        # POST PET3_TYPE1
        response = requests.post(
            f"{STORE2_URL}/pet-types/{id_4}/pets",
            json=PET3_TYPE1
        )
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    def test_06_post_pet_to_store2_type2(self):
        """Test 6: POST 1 pet of type 2 to pet-store #2"""
        global pet_type_ids
        id_5 = pet_type_ids[4]
        
        # POST PET4_TYPE2
        response = requests.post(
            f"{STORE2_URL}/pet-types/{id_5}/pets",
            json=PET4_TYPE2
        )
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    def test_07_post_pets_to_store2_type4(self):
        """Test 7: POST 2 pets of type 4 to pet-store #2"""
        global pet_type_ids
        id_6 = pet_type_ids[5]
        
        # POST PET7_TYPE4
        response1 = requests.post(
            f"{STORE2_URL}/pet-types/{id_6}/pets",
            json=PET7_TYPE4
        )
        assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
        
        # POST PET8_TYPE4
        response2 = requests.post(
            f"{STORE2_URL}/pet-types/{id_6}/pets",
            json=PET8_TYPE4
        )
        assert response2.status_code == 201, f"Expected 201, got {response2.status_code}"

    def test_08_get_pet_type2_from_store1(self):
        """Test 8: GET /pet-types/{id2} from pet-store #1"""
        global pet_type_ids
        id_2 = pet_type_ids[1]
        
        response = requests.get(f"{STORE1_URL}/pet-types/{id_2}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Validate all fields match PET_TYPE2_VAL
        assert data["type"] == PET_TYPE2_VAL["type"], f"Type mismatch"
        assert data["family"] == PET_TYPE2_VAL["family"], f"Family mismatch"
        assert data["genus"] == PET_TYPE2_VAL["genus"], f"Genus mismatch"
        assert data["lifespan"] == PET_TYPE2_VAL["lifespan"], f"Lifespan mismatch"
        
        # Check attributes (order may vary)
        assert set(data["attributes"]) == set(PET_TYPE2_VAL["attributes"]), f"Attributes mismatch"

    def test_09_get_pets_of_type6_from_store2(self):
        """Test 9: GET /pet-types/{id6}/pets from pet-store #2"""
        global pet_type_ids
        id_6 = pet_type_ids[5]
        
        response = requests.get(f"{STORE2_URL}/pet-types/{id_6}/pets")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Should be an array
        assert isinstance(data, list), "Response should be a JSON array"
        
        # Should contain 2 pets
        assert len(data) == 2, f"Expected 2 pets, got {len(data)}"
        
        # Extract pet names
        pet_names = [pet["name"] for pet in data]
        
        # Should contain both PET7_TYPE4 and PET8_TYPE4
        assert PET7_TYPE4["name"] in pet_names, f"{PET7_TYPE4['name']} not found in response"
        assert PET8_TYPE4["name"] in pet_names, f"{PET8_TYPE4['name']} not found in response"
        
        # Validate each pet has expected fields
        for pet in data:
            assert "name" in pet, "Pet should have 'name' field"
            assert "birthdate" in pet, "Pet should have 'birthdate' field"
            
            # Validate specific pet data
            if pet["name"] == PET7_TYPE4["name"]:
                assert pet["birthdate"] == PET7_TYPE4["birthdate"], "Birthdate mismatch for Lazy"
            elif pet["name"] == PET8_TYPE4["name"]:
                assert pet["birthdate"] == PET8_TYPE4["birthdate"], "Birthdate mismatch for Lemon"
