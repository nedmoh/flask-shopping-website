from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sample user data (in production, use a database)
users = {
    'admin': {
        'username': 'admin',
        'password': generate_password_hash('admin123'),
        'email': 'admin@example.com'
    },
    'customer': {
        'username': 'customer',
        'password': generate_password_hash('customer123'),
        'email': 'customer@example.com'
    }
}

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['username']
        self.username = user_data['username']
        self.email = user_data['email']

@login_manager.user_loader
def load_user(user_id):
    user_data = users.get(user_id)
    if user_data:
        return User(user_data)
    return None

# Sample product data
products = [
    {
        'id': 1,
        'name': 'Wireless Headphones',
        'description': 'Noise-cancelling wireless headphones with 30-hour battery life',
        'price': 129.99,
        'category': 'Electronics',
        'image': 'headphones.jpg',
        'rating': 4.5,
        'stock': 25
    },
    {
        'id': 2,
        'name': 'Smart Watch',
        'description': 'Fitness tracker with heart rate monitor and GPS',
        'price': 199.99,
        'category': 'Electronics',
        'image': 'smartwatch.jpg',
        'rating': 4.3,
        'stock': 15
    },
    {
        'id': 3,
        'name': 'Running Shoes',
        'description': 'Lightweight running shoes with cushion technology',
        'price': 89.99,
        'category': 'Sports',
        'image': 'shoes.jpg',
        'rating': 4.7,
        'stock': 30
    },
    {
        'id': 4,
        'name': 'Coffee Maker',
        'description': 'Programmable coffee maker with thermal carafe',
        'price': 79.99,
        'category': 'Home',
        'image': 'coffeemaker.jpg',
        'rating': 4.2,
        'stock': 20
    },
    {
        'id': 5,
        'name': 'Backpack',
        'description': 'Water-resistant backpack with laptop compartment',
        'price': 49.99,
        'category': 'Fashion',
        'image': 'backpack.jpg',
        'rating': 4.4,
        'stock': 40
    },
    {
        'id': 6,
        'name': 'Bluetooth Speaker',
        'description': 'Portable Bluetooth speaker with 360° sound',
        'price': 59.99,
        'category': 'Electronics',
        'image': 'speaker.jpg',
        'rating': 4.6,
        'stock': 35
    }
]

@app.route('/')
def index():
    """Home page showing all products"""
    return render_template('index.html', products=products, user=current_user)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('index'))
    
    # Get related products (same category)
    related_products = [p for p in products if p['category'] == product['category'] and p['id'] != product_id][:3]
    
    return render_template('product.html', product=product, related_products=related_products, user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_data = users.get(username)
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('index.html', products=products, user=current_user)

@app.route('/search')
def search():
    """Search products"""
    query = request.args.get('q', '').lower()
    if query:
        filtered_products = [
            p for p in products 
            if query in p['name'].lower() or query in p['description'].lower() or query in p['category'].lower()
        ]
    else:
        filtered_products = products
    
    return render_template('index.html', products=filtered_products, user=current_user, search_query=query)

@app.route('/category/<category_name>')
def category(category_name):
    """Show products by category"""
    category_products = [p for p in products if p['category'].lower() == category_name.lower()]
    return render_template('index.html', products=category_products, user=current_user, category=category_name)

if __name__ == '__main__':
    app.run(debug=True)