from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from hashlib import sha256
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = os.path.join(basedir, "images")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

ma = Marshmallow(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  foodTitle = db.Column(db.String(70))
  foodFlavor = db.Column(db.String(70))
  foodDescription = db.Column(db.String(8000))
  imageData = db.Column(db.String(8000)) 
  foodPrice = db.Column(db.Float)
  isDrink = db.Column(db.Boolean)

  def __init__(self, foodTitle, foodFlavor, foodDescription, imageData, foodPrice, isDrink):
    self.foodTitle = foodTitle
    self.foodFlavor = foodFlavor
    self.foodDescription = foodDescription
    self.imageData = imageData
    self.foodPrice = foodPrice
    self.isDrink = isDrink

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'foodTitle', 'foodFlavor', 'foodDescription', 'imageData', 'foodPrice','isDrink' )

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route('/product', methods = ['POST'])
def add_product():
    foodTitle = request.json['foodTitle']
    foodFlavor = request.json['foodFlavor']
    foodDescription = request.json['foodDescription']
    imageData = ""
    foodPrice = request.json['foodPrice']
    isDrink = request.json['isDrink']
    #criando produto
    new_product = Product(foodTitle, foodFlavor, foodDescription, imageData, foodPrice, isDrink)
    print(new_product)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

@app.route('/product/<id>', methods=["PUT"])
def update_product_image(id):
    product = Product.query.get(id)
  
    print(request.files['image'])
    print('\n\n\n')

    file = request.files['image']
    if file and allowed_file(file.filename):
        filetype= file.filename.rsplit('.', 1)[1].lower()
        print('\n\n\n')
        print(filetype)
        print('\n\n\n')
        filename = sha256(file.filename.encode()).hexdigest()+'.'+filetype
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imageData = url_for('uploaded_file', filename=filename)
    else:
        imageData=""
    product.imageData=imageData
    db.session.commit()
    return product_schema.jsonify(product)


@app.route('/products', methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    result.reverse()
    response = { 'message':"sucesso", 'products':result}
    return jsonify(response)


@app.route('/product/<id>', methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run(debug=True)
