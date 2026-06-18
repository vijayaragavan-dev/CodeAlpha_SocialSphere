from flask import current_app
from flask_login import UserMixin
from datetime import datetime
import mysql.connector


class MySQLConnection:
    def __init__(self):
        self.config = {
            'host': current_app.config['MYSQL_HOST'],
            'user': current_app.config['MYSQL_USER'],
            'password': current_app.config['MYSQL_PASSWORD'],
            'database': current_app.config['MYSQL_DB'],
            'port': current_app.config['MYSQL_PORT'],
            'charset': 'utf8mb4',
        }

    def get_connection(self):
        return mysql.connector.connect(**self.config)


def get_db():
    return MySQLConnection()


class User(UserMixin):
    def __init__(self, id, username, email, password, bio='', profile_image='default.jpg', is_online=False, last_seen=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        self.profile_image = profile_image
        self.is_online = is_online
        self.last_seen = last_seen or datetime.utcnow()
        self.created_at = created_at or datetime.utcnow()

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(**row)
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_email(email):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cursor.fetchone()
            if row:
                return User(**row)
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_username(username):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
            if row:
                return User(**row)
            return None
        finally:
            conn.close()

    @staticmethod
    def create(username, email, password):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def update_profile(user_id, bio=None, profile_image=None):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            if bio and profile_image:
                cursor.execute(
                    "UPDATE users SET bio = %s, profile_image = %s WHERE id = %s",
                    (bio, profile_image, user_id)
                )
            elif bio:
                cursor.execute(
                    "UPDATE users SET bio = %s WHERE id = %s",
                    (bio, user_id)
                )
            elif profile_image:
                cursor.execute(
                    "UPDATE users SET profile_image = %s WHERE id = %s",
                    (profile_image, user_id)
                )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def search(query):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE username LIKE %s OR email LIKE %s LIMIT 20",
                (f'%{query}%', f'%{query}%')
            )
            rows = cursor.fetchall()
            return [User(**row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def set_online(user_id, status):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "UPDATE users SET is_online = %s, last_seen = %s WHERE id = %s",
                (status, now, user_id)
            )
            conn.commit()
        finally:
            conn.close()

    def get_post_count(self):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as count FROM posts WHERE user_id = %s", (self.id,))
            row = cursor.fetchone()
            return row['count']
        finally:
            conn.close()

    def get_followers_count(self):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as count FROM followers WHERE following_id = %s", (self.id,))
            row = cursor.fetchone()
            return row['count']
        finally:
            conn.close()

    def get_following_count(self):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as count FROM followers WHERE follower_id = %s", (self.id,))
            row = cursor.fetchone()
            return row['count']
        finally:
            conn.close()

    def is_following(self, other_user_id):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM followers WHERE follower_id = %s AND following_id = %s",
                (self.id, other_user_id)
            )
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def get_time_ago(self):
        diff = datetime.utcnow() - self.last_seen
        seconds = diff.total_seconds()
        if seconds < 60:
            return 'just now'
        minutes = int(seconds // 60)
        if minutes < 60:
            return f'{minutes}m ago'
        hours = int(minutes // 60)
        if hours < 24:
            return f'{hours}h ago'
        days = int(hours // 24)
        if days < 30:
            return f'{days}d ago'
        return self.last_seen.strftime('%b %d, %Y')


class Post:
    def __init__(self, id, user_id, content, image=None, created_at=None, author_username=None, author_profile_image=None):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.image = image
        self.created_at = created_at or datetime.utcnow()
        self.author_username = author_username
        self.author_profile_image = author_profile_image

    @staticmethod
    def get_by_id(post_id):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.*, u.username as author_username, u.profile_image as author_profile_image
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = %s
            """, (post_id,))
            row = cursor.fetchone()
            if row:
                return Post(**row)
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all(page=1, per_page=10):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            offset = (page - 1) * per_page
            cursor.execute("""
                SELECT p.*, u.username as author_username, u.profile_image as author_profile_image
                FROM posts p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.created_at DESC
                LIMIT %s OFFSET %s
            """, (per_page, offset))
            rows = cursor.fetchall()
            return [Post(**row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_following_posts(user_id, page=1, per_page=10):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            offset = (page - 1) * per_page
            cursor.execute("""
                SELECT p.*, u.username as author_username, u.profile_image as author_profile_image
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.user_id IN (
                    SELECT following_id FROM followers WHERE follower_id = %s
                ) OR p.user_id = %s
                ORDER BY p.created_at DESC
                LIMIT %s OFFSET %s
            """, (user_id, user_id, per_page, offset))
            rows = cursor.fetchall()
            return [Post(**row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_by_user(user_id, page=1, per_page=10):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            offset = (page - 1) * per_page
            cursor.execute("""
                SELECT p.*, u.username as author_username, u.profile_image as author_profile_image
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.user_id = %s
                ORDER BY p.created_at DESC
                LIMIT %s OFFSET %s
            """, (user_id, per_page, offset))
            rows = cursor.fetchall()
            return [Post(**row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def create(user_id, content, image=None):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO posts (user_id, content, image) VALUES (%s, %s, %s)",
                (user_id, content, image)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def delete(post_id):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def get_likes_count(self):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as count FROM likes WHERE post_id = %s", (self.id,))
            row = cursor.fetchone()
            return row['count']
        finally:
            conn.close()

    def is_liked_by(self, user_id):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM likes WHERE user_id = %s AND post_id = %s",
                (user_id, self.id)
            )
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def get_comments(self):
        db = get_db()
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.*, u.username, u.profile_image
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.post_id = %s
                ORDER BY c.created_at ASC
            """, (self.id,))
            return cursor.fetchall()
        finally:
            conn.close()

    def get_time_ago(self):
        diff = datetime.utcnow() - self.created_at
        seconds = diff.total_seconds()
        if seconds < 60:
            return 'just now'
        minutes = int(seconds // 60)
        if minutes < 60:
            return f'{minutes}m ago'
        hours = int(minutes // 60)
        if hours < 24:
            return f'{hours}h ago'
        days = int(hours // 24)
        if days < 30:
            return f'{days}d ago'
        return self.created_at.strftime('%b %d, %Y')
