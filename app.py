import os
import uuid
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, jsonify, session
)
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from config import Config
from models import User, Post, get_db

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def save_image(file):
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filename
    return None


def login_required_ajax(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route('/')
def index():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        feed_type = request.args.get('feed', 'all')

        if feed_type == 'following':
            posts = Post.get_following_posts(current_user.id, page=page)
        else:
            posts = Post.get_all(page=page)

        enriched_posts = []
        for post in posts:
            likes_count = post.get_likes_count()
            is_liked = post.is_liked_by(current_user.id)
            comments = post.get_comments()
            enriched_posts.append({
                'post': post,
                'likes_count': likes_count,
                'is_liked': is_liked,
                'comments': comments,
            })
        return render_template('index.html', posts=enriched_posts, feed_type=feed_type)
    return render_template('index.html', posts=[])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        errors = []
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        if not email or '@' not in email:
            errors.append('Please enter a valid email.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm_password:
            errors.append('Passwords do not match.')

        if User.get_by_username(username):
            errors.append('Username already taken.')
        if User.get_by_email(email):
            errors.append('Email already registered.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html', username=username, email=email)

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = User.create(username, email, hashed_pw)
        user = User.get_by_id(user_id)
        login_user(user)
        flash('Account created successfully! Welcome to SocialSphere.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.get_by_email(email)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            User.set_online(user.id, True)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    User.set_online(current_user.id, False)
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/profile/<username>')
def profile(username):
    user = User.get_by_username(username)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    posts_data = Post.get_by_user(user.id, page=page)
    post_count = user.get_post_count()
    followers_count = user.get_followers_count()
    following_count = user.get_following_count()

    is_following = False
    if current_user.is_authenticated and current_user.id != user.id:
        is_following = current_user.is_following(user.id)

    enriched_posts = []
    for post in posts_data:
        likes_count = post.get_likes_count()
        is_liked = post.is_liked_by(current_user.id) if current_user.is_authenticated else False
        comments = post.get_comments()
        enriched_posts.append({
            'post': post,
            'likes_count': likes_count,
            'is_liked': is_liked,
            'comments': comments,
        })

    return render_template('profile.html',
                           profile_user=user,
                           posts=enriched_posts,
                           post_count=post_count,
                           followers_count=followers_count,
                           following_count=following_count,
                           is_following=is_following)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        bio = request.form.get('bio', '').strip()
        profile_image = None

        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename:
                profile_image = save_image(file)
                if not profile_image:
                    flash('Invalid image file. Allowed: png, jpg, jpeg, gif, webp', 'danger')
                    return redirect(url_for('edit_profile'))

        User.update_profile(current_user.id, bio=bio, profile_image=profile_image)
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile', username=current_user.username))

    return render_template('edit_profile.html')


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        image = None

        if not content and 'image' not in request.files:
            flash('Post must have text or an image.', 'danger')
            return redirect(url_for('create_post'))

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image = save_image(file)
                if not image:
                    flash('Invalid image file. Allowed: png, jpg, jpeg, gif, webp', 'danger')
                    return redirect(url_for('create_post'))

        Post.create(current_user.id, content, image)
        flash('Post created!', 'success')
        return redirect(url_for('index'))

    return render_template('create_post.html')


@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.get_by_id(post_id)
    if not post:
        flash('Post not found.', 'danger')
        return redirect(url_for('index'))
    if post.user_id != current_user.id:
        flash('You can only delete your own posts.', 'danger')
        return redirect(url_for('index'))
    Post.delete(post_id)
    flash('Post deleted.', 'info')
    return redirect(request.referrer or url_for('index'))


@app.route('/like/<int:post_id>', methods=['POST'])
@login_required_ajax
def like_post(post_id):
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    db = get_db()
    conn = db.get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM likes WHERE user_id = %s AND post_id = %s",
            (current_user.id, post_id)
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                "DELETE FROM likes WHERE user_id = %s AND post_id = %s",
                (current_user.id, post_id)
            )
            liked = False
        else:
            cursor.execute(
                "INSERT INTO likes (user_id, post_id) VALUES (%s, %s)",
                (current_user.id, post_id)
            )
            liked = True
        conn.commit()

        cursor.execute("SELECT COUNT(*) as count FROM likes WHERE post_id = %s", (post_id,))
        count = cursor.fetchone()['count']

        return jsonify({'liked': liked, 'count': count})
    finally:
        conn.close()


@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.get_by_id(post_id)
    if not post:
        flash('Post not found.', 'danger')
        return redirect(request.referrer or url_for('index'))

    comment_text = request.form.get('comment', '').strip()
    if not comment_text:
        flash('Comment cannot be empty.', 'danger')
        return redirect(request.referrer or url_for('index'))

    db = get_db()
    conn = db.get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO comments (post_id, user_id, comment) VALUES (%s, %s, %s)",
            (post_id, current_user.id, comment_text)
        )
        conn.commit()
    finally:
        conn.close()

    flash('Comment added!', 'success')
    return redirect(request.referrer or url_for('index'))


@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    db = get_db()
    conn = db.get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM comments WHERE id = %s", (comment_id,))
        comment = cursor.fetchone()
        if not comment:
            flash('Comment not found.', 'danger')
            return redirect(request.referrer or url_for('index'))
        if comment['user_id'] != current_user.id:
            flash('You can only delete your own comments.', 'danger')
            return redirect(request.referrer or url_for('index'))
        cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
        conn.commit()
    finally:
        conn.close()

    flash('Comment deleted.', 'info')
    return redirect(request.referrer or url_for('index'))


@app.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
    if current_user.id == user_id:
        flash('You cannot follow yourself.', 'danger')
        return redirect(url_for('profile', username=request.form.get('username', '')))

    target = User.get_by_id(user_id)
    if not target:
        flash('User not found.', 'danger')
        return redirect(url_for('index'))

    db = get_db()
    conn = db.get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM followers WHERE follower_id = %s AND following_id = %s",
            (current_user.id, user_id)
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                "DELETE FROM followers WHERE follower_id = %s AND following_id = %s",
                (current_user.id, user_id)
            )
            flash(f'Unfollowed {target.username}.', 'info')
        else:
            cursor.execute(
                "INSERT INTO followers (follower_id, following_id) VALUES (%s, %s)",
                (current_user.id, user_id)
            )
            flash(f'Now following {target.username}!', 'success')
        conn.commit()
    finally:
        conn.close()

    return redirect(request.referrer or url_for('index'))


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = []
    if query:
        results = User.search(query)
    return render_template('search.html', query=query, results=results)


@app.route('/toggle_dark_mode', methods=['POST'])
def toggle_dark_mode():
    current = session.get('dark_mode', False)
    session['dark_mode'] = not current
    return jsonify({'dark_mode': session['dark_mode']})


@app.route('/online_status/<int:user_id>')
def online_status(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'is_online': user.is_online,
        'last_seen': user.get_time_ago()
    })


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
