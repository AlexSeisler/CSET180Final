from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    AdminID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Customer(db.Model):
    CustomerID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)

class Vendor(db.Model):
    VendorID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    storeName = db.Column(db.String(50))
    status = db.Column(db.Enum('A', 'R', 'P'), default='P')

class Product(db.Model):
    ProductID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Description = db.Column(db.Text)
    Price = db.Column(db.Numeric(10,2))
    StockQuantity = db.Column(db.Integer)
    Category = db.Column(db.String(100))
    DiscountID = db.Column(db.Integer, db.ForeignKey('discount.DiscountID'))
    VendorID = db.Column(db.Integer, db.ForeignKey('vendor.VendorID'))

class Discount(db.Model):
    DiscountID = db.Column(db.Integer, primary_key=True)
    Percentage = db.Column(db.Numeric(5,2))
    StartDate = db.Column(db.Date)
    EndDate = db.Column(db.Date)

class DiscountProduct(db.Model):
    DiscountID = db.Column(db.Integer, db.ForeignKey('discount.DiscountID'), primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('product.ProductID'), primary_key=True)

class Complaint(db.Model):
    ComplaintID = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.Text)
    Status = db.Column(db.Enum('R', 'P'), default='P')
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    VendorID = db.Column(db.Integer, db.ForeignKey('vendor.VendorID'))

class Message(db.Model):
    MessageID = db.Column(db.Integer, primary_key=True)
    SenderID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    ReceiverID = db.Column(db.Integer, db.ForeignKey('vendor.VendorID'))
    Timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    Content = db.Column(db.Text)

class Review(db.Model):
    ReviewID = db.Column(db.Integer, primary_key=True)
    Rating = db.Column(db.Integer)
    Comment = db.Column(db.Text)
    Date = db.Column(db.Date)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    ProductID = db.Column(db.Integer, db.ForeignKey('product.ProductID'))

class OrderTable(db.Model):
    OrderID = db.Column(db.Integer, primary_key=True)
    OrderDate = db.Column(db.DateTime, default=datetime.utcnow)
    TotalAmount = db.Column(db.Numeric(10,2))
    Status = db.Column(db.Enum('P', 'S', 'D'), default='P')
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    VendorID = db.Column(db.Integer, db.ForeignKey('vendor.VendorID'))

class OrderItem(db.Model):
    OrderID = db.Column(db.Integer, db.ForeignKey('order_table.OrderID'), primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('product.ProductID'), primary_key=True)
    Quantity = db.Column(db.Integer)
    PriceAtPurchase = db.Column(db.Numeric(10,2))

class Cart(db.Model):
    CartID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))

class CartItem(db.Model):
    CartID = db.Column(db.Integer, db.ForeignKey('cart.CartID'), primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('product.ProductID'), primary_key=True)
    Quantity = db.Column(db.Integer)