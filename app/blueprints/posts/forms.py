from wtforms import Form, StringField, TextAreaField, SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Tag


class PostForm(Form):
	title = StringField('Title')
	content = TextAreaField('Content')
	tags = QuerySelectField('Tags', query_factory=lambda: Tag.query.all(), get_label=lambda tag: tag.name, get_pk=lambda tag: tag.id)