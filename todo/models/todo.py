import datetime 
from . import db 
 
class Todo(db.Model): 
   __tablename__ = 'todos' 
 
   # This is how we define a column, this is also the primary key 
   id = db.Column(db.Integer, primary_key=True) 
   # This is a manadatory column of 80 characters 
   title = db.Column(db.String(80), nullable=False) 
   # This is an optional column of 120 characters 
   description = db.Column(db.String(120), nullable=True) 
   # This column has a default value of False 
   completed = db.Column(db.Boolean, nullable=False, default=False) 
   deadline_at = db.Column(db.DateTime, nullable=True) 
   # This column has a default value which is a function call 
   created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow) 
   # This column has a default value which is a function call and also updates on update 
   updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow) 
 
   # This is a helper method to convert the model to a dictionary 
   def to_dict(self): 
      return { 
         'id': self.id, 
         'title': self.title, 
         'description': self.description, 
         'completed': self.completed, 
         'deadline_at': self.deadline_at.isoformat() if self.deadline_at else None, 
         'created_at': self.created_at.isoformat() if self.created_at else None, 
         'updated_at': self.updated_at.isoformat() if self.updated_at else None, 
      } 
 
   def __repr__(self): 
      return f'<Todo {self.id} {self.title}>'
 
