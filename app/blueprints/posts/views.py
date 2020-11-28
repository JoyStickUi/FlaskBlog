from flask import render_template, request, flash, redirect, url_for, abort
from flask_security import login_required, current_user
from app.app import db, FlaskAdminDependenciesView
from app.models import Post, Tag, slugify
from .app import posts_blueprint
from .forms import PostForm

@posts_blueprint.route('/')
def posts():
	search_request = request.args.get('search')

	posts = []

	page = request.args.get('page')

	if page and page.isdigit():
		page = int(page)
	else:
		page = 1

	if search_request:
		posts = Post.query.filter(Post.title.contains(search_request) | Post.content.contains(search_request))
	else:
		posts = Post.query.order_by(Post.created_date.desc())

	pages = posts.paginate(page=page, per_page=5)

	return render_template('posts/posts.html', pages=pages)

@posts_blueprint.route('/post/<path:post_slug>/')
def get_post(post_slug = None):
	post = Post.query.filter(Post.slug==post_slug).first_or_404()
	return render_template('posts/post.html', post=post)

@posts_blueprint.route('/tag/<path:tag_slug>/')
def get_posts_by_tag(tag_slug):
	posts = None
	tag = Tag.query.filter(Tag.slug==tag_slug).first_or_404()
	if tag:
		posts = tag.posts

	pages = []

	page = request.args.get('page')

	if page and page.isdigit():
		page = int(page)
	else:
		page = 1

	if posts:
		pages = posts.paginate(page=page, per_page=5)

	return render_template('posts/posts.html', pages=pages)

@posts_blueprint.route('/post/create/', methods=['GET', 'POST'])
@login_required
def create_post():

	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		tags = request.form.getlist('tags')

		# try:
		post = Post(title=title, content=content)
		for tag in tags:
			post.tags.append(Tag.query.filter(Tag.id==tag).first_or_404())
		db.session.add(post)
		db.session.commit()
		flash('New post was added', 'success')

		return redirect(url_for('posts.get_post', post_slug=post.slug)) 
		# except Exception:
		flash('Oops, something went wrong', 'danger')



	form = PostForm()
	return FlaskAdminDependenciesView().render('posts/create_post.html', form=form)

@posts_blueprint.route('/post/<post_slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit_post(post_slug):
	post = Post.query.filter(Post.slug==post_slug).first_or_404()
	if (current_user.is_authenticated and current_user == post.owner) or (current_user.has_role('admin')):

		if request.method == 'POST':
			try:
				post.title = request.form['title']
				post.content = request.form['content']
				post.slug = slugify(request.form['title'])
				post.tags.clear()
				for tag in request.form.getlist('tags'):
					post.tags.append(Tag.query.filter(Tag.id==tag).first_or_404())

				db.session.add(post)
				db.session.commit()

				flash('Post was successfuly updated', 'success')
				return redirect(url_for('posts.get_post', post_slug=post.slug))
			except Exception:
				flash('Oops, something went wrong', 'danger')

		form = PostForm(obj=post)
		return FlaskAdminDependenciesView().render('posts/edit_post.html', form=form, post_slug=post.slug)
	abort(404)