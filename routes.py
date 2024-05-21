from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app import db, bcrypt, jwt
from model import User, Train, Booking
from functools import wraps
import os

main_bp = Blueprint('main_bp', __name__)

# Define your API key
API_KEY = os.getenv('API_KEY')


def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('API-Key')
        if api_key and api_key == API_KEY:
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    return wrapper

# User Registration
@main_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password, role='user')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

# User Login
@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Get Seat Availability
@main_bp.route('/seat_availability', methods=['GET'])
def seat_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')
    trains = Train.query.filter_by(source=source, destination=destination).all()
    availability = [{'train_id': train.id, 'total_seats': train.total_seats - sum([booking.seats_booked for booking in train.bookings])} for train in trains]
    return jsonify(availability)

# Book a Seat
@main_bp.route('/book_seat', methods=['POST'])
@jwt_required()
def book_seat():
    data = request.get_json()
    train_id = data['train_id']
    seats_booked = data['seats_booked']
    train = Train.query.get(train_id)
    if not train:
        return jsonify({'message': 'Train not found'}), 404
    if train.total_seats < seats_booked:
        return jsonify({'message': 'Not enough seats available'}), 400
    current_user = get_jwt_identity()
    new_booking = Booking(user_id=current_user, train_id=train_id, seats_booked=seats_booked)
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Seat booked successfully'})

# Get Specific Booking Details
@main_bp.route('/booking_details', methods=['GET'])
@jwt_required()
def booking_details():
    current_user = get_jwt_identity()
    bookings = Booking.query.filter_by(user_id=current_user).all()
    booking_info = [{'train_id': booking.train_id, 'seats_booked': booking.seats_booked} for booking in bookings]
    return jsonify(booking_info)

@main_bp.route('/add_train', methods=['POST'])
@require_api_key
@jwt_required()
def add_train():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    new_train = Train(source=data['source'], destination=data['destination'], total_seats=data['total_seats'])
    db.session.add(new_train)
    db.session.commit()
    return jsonify({'message': 'Train added successfully'})
