from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Models
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    room = db.relationship('Room', backref=db.backref('reservations', lazy=True))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rooms', methods=['GET', 'POST'])
def manage_rooms():
    if request.method == 'POST':
        room_number = request.form['room_number']
        room_type = request.form['room_type']
        price_per_night = float(request.form['price_per_night'])
        new_room = Room(room_number=room_number, room_type=room_type, price_per_night=price_per_night)
        try:
            db.session.add(new_room)
            db.session.commit()
            flash('Room added successfully!', 'success')
        except:
            flash('Room number already exists.', 'danger')
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)

@app.route('/reservations', methods=['GET', 'POST'])
def manage_reservations():
    rooms = Room.query.all()
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        room_id = int(request.form['room_id'])
        check_in = datetime.strptime(request.form['check_in'], '%Y-%m-%d').date()
        check_out = datetime.strptime(request.form['check_out'], '%Y-%m-%d').date()

        if check_out > check_in:
            new_reservation = Reservation(customer_name=customer_name, room_id=room_id, check_in=check_in, check_out=check_out)
            db.session.add(new_reservation)
            db.session.commit()
            flash('Reservation created successfully!', 'success')
        else:
            flash('Check-out date must be after check-in date.', 'danger')
    reservations = Reservation.query.all()
    return render_template('reservations.html', reservations=reservations, rooms=rooms)

@app.route('/cancel_reservation/<int:reservation_id>')
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation canceled successfully!', 'success')
    return redirect(url_for('manage_reservations'))

@app.route('/calculate/<int:reservation_id>')
def calculate_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    nights = (reservation.check_out - reservation.check_in).days
    total_price = nights * reservation.room.price_per_night
    flash(f'Total price for {reservation.customer_name}: ${total_price:.2f}', 'info')
    return redirect(url_for('manage_reservations'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
