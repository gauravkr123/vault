from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from abc import ABC, abstractmethod
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mayank@localhost:5432/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Pet model using a dataclass
class Pet(db.Model):

    __tablename__ = 'pets'
    __table_args__ = {'schema': 'myschema'}

    # def __init__(self, id, name, category, status):
    #     self.id = id
    #     self.name = name
    #     self.category = category
    #     self.status = status
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "status": self.status
        }

# Repository Interface (ISP)
class PetRepository(ABC):
    @abstractmethod
    def add(self, pet: Pet):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def find_by_id(self, pet_id: str):
        pass

    @abstractmethod
    def delete(self, pet_id: str):
        pass

    @abstractmethod
    def update(self, pet_id: str, status: str):
        pass

# In-Memory Repository Implementation (DIP)
class PostGresPetRepository(PetRepository):
    def __init__(self):
        self.pets = []

    def add(self, pet: Pet):
        try:
            db.session.add(pet)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"An error e: {e} occured while adding pet: {pet.to_dict()}")
        finally:
            return pet

    def get_all(self):
        try:
            self.pets = db.session.query(Pet).all()
        except Exception as e:
            print(f"An error e: {e} occured while fetching all pets")
        finally:
            return self.pets

    def find_by_id(self, pet_id: str):
        pet = None
        try:
            pet = db.session.query(Pet).filter_by(id=pet_id).first()
        except Exception as e:
            print(f"An error e: {e} occured while fetching pet by id: {pet_id}")
        finally:
            return pet

    def delete(self, pet_id: str):
        try:
            pet = db.session.query(Pet).filter_by(id=pet_id).first()
            db.session.delete(pet)
            db.session.commit()
            return "Success"
        except Exception as e:
            db.session.rollback()
            print(f"An error e: {e} occured while deleting pet by id: {pet_id}")
            return "Failed"

    def update(self, pet_id: str, status: str):
        pet = self.find_by_id(pet_id)
        if pet:
            try:
                pet.status = status
                db.session.query(Pet).filter_by(id=pet_id).update({'status': status})
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"An error e: {e} occured while updating pet by id: {pet_id}")
            finally:
                return pet
        else:
            return "Pet with given ID does not exist"

# Service Layer (SRP)
class PetService:
    def __init__(self, repository: PetRepository):
        self.repository = repository

    def create_pet(self, id, name, category, status):
        pet = Pet(id=id, name=name, category=category, status=status)
        self.repository.add(pet)
        return pet

    def get_pets(self):
        return self.repository.get_all()

    def get_pet_by_id(self, pet_id):
        return self.repository.find_by_id(pet_id)

    def remove_pet(self, pet_id):
        self.repository.delete(pet_id)

    def change_pet_status(self, pet_id, status):
        return self.repository.update(pet_id, status)

# Controller Layer (SRP)
class PetController:
    def __init__(self, service: PetService):
        self.service = service

    def get_all_pets(self):
        pets = self.service.get_pets()
        return jsonify([pet.to_dict() for pet in pets]), 200

    def add_pet(self):
        data = request.json
        pet = self.service.create_pet(data['id'], data['name'], data['category'], data['status'])
        return jsonify(pet.to_dict()), 201

    def find_pet_by_id(self, pet_id):
        pet = self.service.get_pet_by_id(pet_id)
        if pet is None:
            return jsonify({"error": "Pet not found"}), 404
        return jsonify(pet.to_dict()), 200

    def delete_pet(self, pet_id):
        self.service.remove_pet(pet_id)
        return '', 204

    def update_pet(self, pet_id):
        data = request.json
        pet = self.service.change_pet_status(pet_id, data['status'])
        if pet is None:
            return jsonify({"error": "Pet not found"}), 404
        return jsonify(pet.to_dict()), 200

# Dependency Injection (DIP)
repository = PostGresPetRepository()
service = PetService(repository)
controller = PetController(service)

# Routes (OCP)
@app.route('/pets', methods=['GET'])
def get_pets():
    return controller.get_all_pets()

@app.route('/pets', methods=['POST'])
def add_pet():
    return controller.add_pet()

@app.route('/pets/<string:pet_id>', methods=['GET'])
def find_pet_by_id(pet_id):
    return controller.find_pet_by_id(pet_id)

@app.route('/pets/<string:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    return controller.delete_pet(pet_id)

@app.route('/pets/<string:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    return controller.update_pet(pet_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# CREATE TABLE pets ( id UUID DEFAULT uuid_generate_v4() PRIMARY KEY, name VARCHAR(255) NOT NULL, category VARCHAR(255) NOT NULL, status VARCHAR(50) NOT NULL );