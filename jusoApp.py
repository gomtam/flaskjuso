from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CONTACTS_FILE = 'contacts.txt'

class Contact:
    def __init__(self, id=None, name='', phone='', email='', address='', created_at=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.created_at = created_at or datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            address=data.get('address', ''),
            created_at=data.get('created_at')
        )

def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            contacts_data = json.load(f)
            return [Contact.from_dict(data) for data in contacts_data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_contacts(contacts):
    contacts_data = [contact.to_dict() for contact in contacts]
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(contacts_data, f, ensure_ascii=False, indent=2)

def get_next_id():
    contacts = load_contacts()
    if not contacts:
        return 1
    return max(contact.id for contact in contacts) + 1

@app.route('/')
def index():
    contacts = load_contacts()
    # 이름 순으로 정렬
    contacts.sort(key=lambda x: x.name)
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
        
        contacts = load_contacts()
        new_contact = Contact(
            id=get_next_id(),
            name=name,
            phone=phone,
            email=email,
            address=address
        )
        contacts.append(new_contact)
        save_contacts(contacts)
        
        flash('연락처가 추가되었습니다!')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    contacts = load_contacts()
    contact = next((c for c in contacts if c.id == id), None)
    
    if contact is None:
        flash('연락처를 찾을 수 없습니다!')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.phone = request.form['phone']
        contact.email = request.form['email']
        contact.address = request.form['address']
        
        if not contact.name:
            flash('이름은 필수입니다!')
            return redirect(url_for('edit', id=id))
        
        save_contacts(contacts)
        flash('연락처가 수정되었습니다!')
        return redirect(url_for('index'))
    
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete(id):
    contacts = load_contacts()
    contacts = [c for c in contacts if c.id != id]
    save_contacts(contacts)
    flash('연락처가 삭제되었습니다!')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    contacts = load_contacts()
    
    if query:
        contacts = [
            c for c in contacts if 
            query in c.name.lower() or 
            query in (c.email.lower() if c.email else '') or 
            query in (c.phone.lower() if c.phone else '') or 
            query in (c.address.lower() if c.address else '')
        ]
    
    return render_template('index.html', contacts=contacts, search_query=query)

if __name__ == '__main__':
    app.run(debug=True)