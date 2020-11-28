from flask import Flask, url_for, abort
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import BaseView
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_mail import Mail
from .settings import DefaultConfig
from flask_bootstrap import Bootstrap

#____APP INIT SECTION____

app = Flask(__name__)

app.config.from_object(DefaultConfig)

#____DATABASE INIT SECTION____

db = SQLAlchemy(app)

#____MODELS IMPORT SECTION____

from .models import Post, Tag, User, Role

#____MAIL SECTION____

mail = Mail(app)

#____SECURITY SECTION____

app.user_datastore = SQLAlchemyUserDatastore(db, User, Role)

security = Security(app, app.user_datastore)

#____FLASK ADMIN SECTION____

class FlaskAdminDependenciesView(BaseView):
    def __init__(self, *args, **kwargs):
        self._default_view = True
        super(FlaskAdminDependenciesView, self).__init__(*args, **kwargs)
        self.admin = Admin()

class AdminPermissionMixin:
	def is_accessible(self):
		return current_user.has_role('admin')

	def inaccessible_callback(self, name, **kwargs):
		return abort(404)

class SecuredIndexView(AdminPermissionMixin, AdminIndexView):
	pass

class AdminModelView(AdminPermissionMixin, ModelView):
	pass

class AdminSlugModelView(AdminModelView):
	def on_model_change(self, form, model, is_created):
		model.generate_slug()
		return super(AdminSlugModelView, self).on_model_change(form, model, is_created)

admin = Admin(app, index_view=SecuredIndexView())

admin.add_view(AdminSlugModelView(Post, db.session))
admin.add_view(AdminSlugModelView(Tag, db.session))
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Role, db.session))

#____BLUEPRINTS SECTION____

from app.blueprints.posts.app import posts_blueprint

app.register_blueprint(posts_blueprint, url_prefix='/posts')

#____VIEWS SECTION____

from .views import *
