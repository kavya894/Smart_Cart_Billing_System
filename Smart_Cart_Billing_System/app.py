
import firebase_admin
from firebase_admin import credentials, firestore, auth
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import stripe
from flask import Flask, render_template, request, jsonify

# Firebase Setup
cred = credentials.Certificate("path_to_your_firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Flask Setup
app = Flask(__name__)

# YOLO Setup
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Payment System Setup (Stripe)
stripe.api_key = "your_stripe_api_key"

# Routes and Methods
@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    items = request.json['items']
    total = sum(item['price'] for item in items)
    return jsonify({"total": total})

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    