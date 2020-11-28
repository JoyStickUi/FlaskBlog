from flask_security import UserMixin, RoleMixin, current_user
from datetime import datetime
import re
from app.app import db

def slugify(string):
	pattern = r'[^\w+]'
	return re.sub(pattern, '-', string)

post_tags = db.Table(
	'post_tags',
	db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	slug = db.Column(db.String(140), unique=True)
	content = db.Column(db.Text)
	created_date = db.Column(db.DateTime, default=datetime.now())
	tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))

	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, *args, **kwargs):
		super(Post, self).__init__(*args, **kwargs)
		self.generate_slug()
		self.owner = current_user

	def generate_slug(self):
		if self.title:
			self.slug = slugify(self.title)

	def __repr__(self):
		return f'<Post {self.slug}, id: {self.id}>'


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	slug = db.Column(db.String(100))

	def __init__(self, *args, **kwargs):
		super(Tag, self).__init__(*args, **kwargs)
		self.slug = slugify(self.name)

	def generate_slug(self):
		if self.name:
			self.slug = slugify(self.name)

	def __repr__(self):
		return f'<Tag {self.name}, id {self.id}>'


roles_users = db.Table(
	'roles_users',
	db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
	db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)

	def __repr__(self):
		return f'<Role {self.name}>'

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(255))
	active = db.Column(db.Boolean())
	roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

	posts = db.relationship('Post', backref='owner', lazy=True)

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		self.roles.append(Role.query.filter(Role.name=='user').first())

	def __repr__(self):
		return f'<User {self.email}>'