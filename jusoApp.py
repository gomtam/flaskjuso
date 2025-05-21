from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///address_book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Contact {self.name}>'

@app.route('/')
def index():
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        
        if not name:
            flash('이름은 필수입니다!')
            return redirect(url_for('add'))
        
        new_contact = Contact(name=name, phone=phone, email=email, address=address)
        db.session.add(new_contact)
        db.session.commit()
        
        flash('연락처가 추가되었습니다!')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    contact = Contact.query.get_or_404(id)
    
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.phone = request.form['phone']
        contact.email = request.form['email']
        contact.address = request.form['address']
        
        if not contact.name:
            flash('이름은 필수입니다!')
            return redirect(url_for('edit', id=id))
        
        db.session.commit()
        flash('연락처가 수정되었습니다!')
        return redirect(url_for('index'))
    
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('연락처가 삭제되었습니다!')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('query', '')
    contacts = Contact.query.filter(
        (Contact.name.contains(query)) | 
        (Contact.email.contains(query)) | 
        (Contact.phone.contains(query)) |
        (Contact.address.contains(query))
    ).all()
    return render_template('index.html', contacts=contacts, search_query=query)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)