# pet_order.py - Pet Order Service with MongoDB Persistence
import os
import requests
import random
import uuid
from flask import Flask, request, jsonify
from pymongo import MongoClient
import logging

app = Flask(__name__)

# Configuration from environment variables
PORT = int(os.getenv("PORT", 8080))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
DB_NAME = os.getenv("DB_NAME", "petstore")
TRANSACTIONS_COLLECTION = "transactions"

# Pet store service URLs (internal Docker network)
PET_STORE_1_URL = os.getenv("PET_STORE_1_URL", "http://pet-store1:8000")
PET_STORE_2_URL = os.getenv("PET_STORE_2_URL", "http://pet-store2:8000")

# Owner authentication
OWNER_PC_KEY = "OwnerPC"
OWNER_PC_VALUE = "LovesPetsL2M3n4"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- MongoDB Connection ---
def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def get_transactions_collection():
    db = get_db()
    return db[TRANSACTIONS_COLLECTION]

def get_next_purchase_id():
    return str(uuid.uuid4())[:8]


# --- Helper Functions ---
def get_pet_store_url(store_num):
    if store_num == 1:
        return PET_STORE_1_URL
    elif store_num == 2:
        return PET_STORE_2_URL
    return None

def get_all_pet_types_from_store(store_num):
    url = get_pet_store_url(store_num)
    if not url:
        return []
    try:
        response = requests.get(f"{url}/pet-types", timeout=10)
        if response.ok:
            return response.json()
    except Exception as e:
        logger.error(f"Error getting pet types from store {store_num}: {e}")
    return []

def find_pet_type_by_name_in_store(store_num, pet_type_name):
    pet_types = get_all_pet_types_from_store(store_num)
    for pt in pet_types:
        if pt.get('type', '').lower() == pet_type_name.lower():
            return pt
    return None

def get_pets_of_type_from_store(store_num, pet_type_id):
    url = get_pet_store_url(store_num)
    if not url:
        return []
    try:
        response = requests.get(f"{url}/pet-types/{pet_type_id}/pets", timeout=10)
        if response.ok:
            return response.json()
    except Exception as e:
        logger.error(f"Error getting pets from store {store_num}: {e}")
    return []

def get_specific_pet_from_store(store_num, pet_type_id, pet_name):
    url = get_pet_store_url(store_num)
    if not url:
        return None
    try:
        response = requests.get(f"{url}/pet-types/{pet_type_id}/pets/{pet_name}", timeout=10)
        if response.ok:
            return response.json()
    except Exception as e:
        logger.error(f"Error getting pet {pet_name} from store {store_num}: {e}")
    return None

def delete_pet_from_store(store_num, pet_type_id, pet_name):
    url = get_pet_store_url(store_num)
    if not url:
        return False
    try:
        response = requests.delete(f"{url}/pet-types/{pet_type_id}/pets/{pet_name}", timeout=10)
        return response.status_code == 204
    except Exception as e:
        logger.error(f"Error deleting pet {pet_name} from store {store_num}: {e}")
    return False

def find_available_pet(pet_type_name, store=None, pet_name=None):
    """
    Find an available pet based on the request criteria.
    Returns: (store_num, pet_type_id, pet_name, pet_type_name) or None
    """
    stores_to_check = [store] if store else [1, 2]
    available_pets = []
    
    for store_num in stores_to_check:
        pet_type = find_pet_type_by_name_in_store(store_num, pet_type_name)
        if not pet_type:
            continue
        
        pet_type_id = pet_type['id']
        actual_pet_type_name = pet_type['type']
        
        if pet_name:
            # Specific pet requested
            pet = get_specific_pet_from_store(store_num, pet_type_id, pet_name)
            if pet:
                return (store_num, pet_type_id, pet['name'], actual_pet_type_name)
        else:
            # Any pet of this type
            pets = get_pets_of_type_from_store(store_num, pet_type_id)
            for pet in pets:
                available_pets.append((store_num, pet_type_id, pet['name'], actual_pet_type_name))
    
    if pet_name:
        return None
    
    if available_pets:
        return random.choice(available_pets)
    
    return None

def save_transaction(transaction):
    collection = get_transactions_collection()
    collection.insert_one(transaction)

def get_all_transactions(filters=None):
    collection = get_transactions_collection()
    query = {}
    
    if filters:
        for key, value in filters.items():
            if key == 'store':
                try:
                    query['store'] = int(value)
                except ValueError:
                    query['store'] = value
            elif key == 'purchaser':
                query['purchaser'] = value
            elif key == 'pet-type':
                query['pet-type'] = {'$regex': f'^{value}$', '$options': 'i'}
            elif key == 'purchase-id':
                query['purchase-id'] = value
    
    transactions = list(collection.find(query, {'_id': 0}))
    return transactions


# --- Error Handlers ---
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Malformed data"}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "unauthorized"}), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({"error": "Expected application/json media type"}), 415


# --- Kill Endpoint for Testing Restart ---
@app.route('/kill', methods=['GET'])
def kill_container():
    os._exit(1)


# --- Endpoints ---
@app.route('/purchases', methods=['POST'])
def create_purchase():
    if not request.is_json:
        return unsupported_media_type(None)
    
    data = request.get_json()
    
    # Validate allowed fields only (reject extra fields as per Q&A)
    allowed_fields = {'purchaser', 'pet-type', 'store', 'pet-name'}
    provided_fields = set(data.keys())
    
    # Reject if purchase-id is included (server must generate it)
    if 'purchase-id' in provided_fields:
        return bad_request(None)
    
    # Reject if any unexpected fields are present
    if not provided_fields.issubset(allowed_fields):
        return bad_request(None)
    
    # Validate required fields
    if 'purchaser' not in data or 'pet-type' not in data:
        return bad_request(None)
    
    purchaser = data['purchaser']
    pet_type_name = data['pet-type']
    store = data.get('store')
    pet_name = data.get('pet-name')
    
    # Validate store value if provided
    if store is not None:
        if store not in [1, 2]:
            return bad_request(None)
    
    # pet-name can only be supplied if store is supplied
    if pet_name and store is None:
        return bad_request(None)
    
    # Find an available pet
    result = find_available_pet(pet_type_name, store, pet_name)
    
    if not result:
        return jsonify({"error": "No pet of this type is available"}), 400
    
    chosen_store, pet_type_id, chosen_pet_name, actual_pet_type_name = result
    
    # Delete the pet from the store
    if not delete_pet_from_store(chosen_store, pet_type_id, chosen_pet_name):
        return jsonify({"error": "Failed to complete purchase"}), 500
    
    # Generate purchase ID
    purchase_id = get_next_purchase_id()
    
    # Create the transaction record (without pet-name as per spec)
    transaction = {
        "purchaser": purchaser,
        "pet-type": actual_pet_type_name,
        "store": chosen_store,
        "purchase-id": purchase_id
    }
    
    # Save transaction to MongoDB
    save_transaction(transaction.copy())
    
    # Create the purchase response (includes pet-name)
    purchase_response = {
        "purchaser": purchaser,
        "pet-type": actual_pet_type_name,
        "store": chosen_store,
        "pet-name": chosen_pet_name,
        "purchase-id": purchase_id
    }
    
    return jsonify(purchase_response), 201


@app.route('/transactions', methods=['GET'])
def get_transactions():
    # Check authorization
    owner_pc = request.headers.get(OWNER_PC_KEY)
    if owner_pc != OWNER_PC_VALUE:
        return unauthorized(None)
    
    # Get query parameters for filtering
    filters = {}
    allowed_filters = ['purchaser', 'pet-type', 'store', 'purchase-id']
    
    for param in allowed_filters:
        if param in request.args:
            filters[param] = request.args[param]
    
    transactions = get_all_transactions(filters)
    return jsonify(transactions), 200


if __name__ == '__main__':
    logger.info(f"Starting Pet Order Service on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
