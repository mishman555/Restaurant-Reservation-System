import os
from flask import request, jsonify,Flask,render_template,session,redirect,url_for
import random
from views.customer import customerView
from views.reservation import reservationView
from views.admin import adminView
from flask import flash
from datetime import datetime, time

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Define the working hours
working_hours_start = time(10, 0)  # 10 am
working_hours_end = time(23, 0)   # 11 pm

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/new_customer', methods=['GET'])
def new_customer_form():
    """Render the new customer form page."""
    return render_template('new_customer.html')

@app.route('/existing_user')
def existing_user():
    """Render the existing user page."""
    return render_template('existing_user.html')

@app.route('/make_reservation', methods=['GET'])
def make_reservation():
    """Render the reservation page."""
    user_data = session.get('user_data')
    if user_data:
        return render_template('reservation.html', user_data=user_data)
    else:
        return redirect(url_for('login')) 

@app.route('/api/new_customer', methods=['POST'])
def add_customer():
    """Add a new customer."""
    username=request.form.get('username'),
    # Check if the username already exists
    if customerView(username=username).find():
        return jsonify({"success": False, "message": "Username already exists"})
    
    customerId=random.randint(1000,9999),
    name=request.form.get('name'),
    address=request.form.get('address'),
    phoneNumber=request.form.get('phone_number'),
    email=request.form.get('email')
    print(f"customerID is {customerId}")
    customer = customerView(
    customerId[0],
    username[0],
    name[0],
    address[0],
    phoneNumber[0],
    email
    )
    session['user_data'] = {
            "username": username[0],
            "name": name[0],
            "email": email,
            "phone_number": phoneNumber[0]
        }
    result_msg=customer.insert()
    return redirect(url_for('make_reservation'))

@app.route('/login', methods=['POST'])
def login():
    """Handle user login."""
    customer = customerView(username=request.form.get('username'))
    user=customer.find()

    if user:
        session['user_data'] = {
            "username": user["username"],
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "phone_number": user.get("phone_number", "")
        }
        return redirect(url_for('make_reservation'))
    else:
        # User does not exist, return an error message
        return render_template('error_user_not_found.html', error_message="User not found")
#        return jsonify({"error": "User not found"})

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Handle admin login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Add your simple authentication logic here
        if username == 'admin' and password == 'qwerTy100$':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid admin credentials", "error")

    return render_template('admin_login.html')

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    """Handle admin logout."""
    # Clear admin session
    session.pop('admin', None)
    return redirect(url_for('index'))
    
@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    """Submit a reservation."""
    # Get the reservation date and time from the form
    reservation_date_str = request.form['reservation_date']
    reservation_date = datetime.strptime(reservation_date_str, '%Y-%m-%dT%H:%M').time()

    # Check if the reservation time is within working hours
    if not working_hours_start <= reservation_date <= working_hours_end:
        # Render a template with a message about reservations only during working hours
        return render_template('outside_working_hours.html')

    username=request.form['username'],
    reservationId=random.randint(10000,99999),
    number_of_seats=request.form['number_of_seats'],
    reservation = reservationView(
        username[0],
        reservationId[0],
        number_of_seats[0],
        reservation_date_str
    )
    result_msg=reservation.insert()
    if result_msg['success']:
        return render_template('reservation_success.html', reservationId=reservationId[0])
    else:
        return jsonify(result_msg)
    
@app.route('/admin/dashboard')
def admin_dashboard():
    """Render the admin dashboard."""
    # Check if the admin is logged in
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    admin=adminView()
    return render_template('admin_dashboard.html', customer_reservations=admin.adminData())

@app.route('/remove_all_customers', methods=['POST'])
def remove_all_customers():
    """Remove all customers."""
    admin_view = adminView()
    result = admin_view.remove_all_customers()
    if result['success']:
        return render_template('remove_customers_success.html')
    else:
        return render_template('error.html', error_message=result['message'])


@app.route('/update_customer_status/<string:customer_username>/<int:reservation_id>', methods=['POST'])
def update_customer_status(customer_username, reservation_id):
    """Update customer status."""
    admin_view = adminView()
    admin_view.update_customer_status(customer_username, reservation_id)
    return redirect('/admin/dashboard')

@app.route('/cancel_reservation/<string:customer_username>/<int:reservation_id>', methods=['POST'])
def cancel_reservation(customer_username, reservation_id):
    """Cancel a reservation."""
    admin_view = adminView()

    # Update reservation status to canceled
    result_reservation = admin_view.cancel_reservation(customer_username, reservation_id)

    if result_reservation['success']:
        return render_template('cancel_reservation_success.html')
    else:
        return render_template('error.html', error_message=result_reservation['message'])

if __name__ == '__main__':
    app.run(debug=True)
