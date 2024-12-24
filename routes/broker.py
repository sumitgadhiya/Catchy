from flask import Flask, request, jsonify
from models import db, Broker
from config import Config
from flask import current_app


def broker():
    data = request.get_json()
    broker_name = data.get('broker_name')
    broker_user_id = data.get('broker_user_id')
    broker_pin = data.get('broker_pin')
    broker_qr_key = data.get('broker_qr_key')
    broker_api = data.get('broker_api')
    broker_api_secret = data.get('broker_api_secret')
    broker_password = data.get('broker_password')
    redirect_url = data.get('redirect_url')
    is_active = data.get('is_active')




    # if not broker_name or not broker_user_id:
    #     return jsonify({'error': 'broker_name and broker_user_id are required'}), 400

    # Check for existing user with the same email
    if Broker.query.filter_by(broker_user_id=broker_user_id).first():
        return jsonify({'error': 'Broker already exists'}), 409

    # Create a new Broker instance
    new_broker = Broker(broker_name=broker_name, broker_user_id=broker_user_id, broker_pin=broker_pin, broker_qr_key=broker_qr_key, broker_api=broker_api, broker_api_secret=broker_api_secret, broker_password=broker_password)

    # Add to the database and commit
    db.session.add(new_broker)
    db.session.commit()

    return jsonify({'message': 'Broker created successfully', 'broker': {'id': new_broker.id, 'broker_user_id': new_broker.broker_user_id, 'broker_pin': new_broker.broker_pin}}), 201











def get_broker():
    # Fetch all brokers from the database
    data = Broker.query.all()
    
    # Serialize the broker data
    brokers_list = []
    for broker in data:
        brokers_list.append({
            'id': broker.id,
            'broker_name': broker.broker_name,
            'broker_user_id': broker.broker_user_id,
            'broker_pin': broker.broker_pin,
            'broker_qr_key': broker.broker_qr_key,
            'broker_api': broker.broker_api,
            'broker_api_secret': broker.broker_api_secret,
            'broker_password': broker.broker_password,
            'redirect_url' : broker.redirect_url,
            'is_active': broker.is_active
        })
    
    return jsonify({'data': brokers_list}), 200
