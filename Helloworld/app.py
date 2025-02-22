from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    session_id = db.Column(db.String(100), nullable=False)
    product = db.relationship('Product', backref='cart_items')

# Create database tables
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

# About Route
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Route with Form Submission
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

# API Route for JSON Data
@app.route('/api/data')
def api_data():
    tasks = Product.query.all()
    data = [{"id": t.id, "title": t.name, "completed": t.stock} for t in tasks]
    return jsonify({"status": "success", "data": data})

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/admin/products')
def admin_products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            stock=int(request.form['stock']),
            image_url=request.form['image_url']
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('admin_products'))
    return render_template('admin/add_product.html')

@app.route('/cart')
def view_cart():
    if 'cart_id' not in session:
        session['cart_id'] = str(datetime.utcnow().timestamp())
    cart_items = CartItem.query.filter_by(session_id=session['cart_id']).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart_id' not in session:
        session['cart_id'] = str(datetime.utcnow().timestamp())
    
    quantity = int(request.form.get('quantity', 1))
    product = Product.query.get_or_404(product_id)
    
    if product.stock < quantity:
        flash('Not enough stock available!')
        return redirect(url_for('product_detail', product_id=product_id))
    
    cart_item = CartItem.query.filter_by(
        product_id=product_id,
        session_id=session['cart_id']
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            product_id=product_id,
            quantity=quantity,
            session_id=session['cart_id']
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Product added to cart!')
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True)