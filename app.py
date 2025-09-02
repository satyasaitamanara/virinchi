# from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# from flask_bcrypt import Bcrypt
# import pymysql
# import re
# from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_bcrypt import Bcrypt
import pymysql
import re
import os
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production
bcrypt = Bcrypt(app)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lmms_auth',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# File upload configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # project root
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_db_connection():
    return pymysql.connect(**db_config)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Login required decorator
def login_required(role='user'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('user_login'))
            if role == 'admin' and session.get('role') != 'admin':
                flash('Admin access required', 'danger')
                return redirect(url_for('user_login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        
        # Basic validation
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return render_template('signup.html')
        
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Save to database
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (full_name, email, username, password, role) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (full_name, email, username, hashed_password, role))
                connection.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('user_login'))
        except pymysql.err.IntegrityError:
            flash('Username or email already exists', 'danger')
        except Exception as e:
            flash('An error occurred. Please try again.', 'danger')
        finally:
            connection.close()
    
    return render_template('signup.html')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s OR email = %s"
                cursor.execute(sql, (username, username))
                user = cursor.fetchone()
                
                if user and bcrypt.check_password_hash(user['password'], password):
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    
                    if user['role'] == 'admin':
                        return redirect(url_for('admin_panel'))
                    else:
                        return redirect(url_for('user_dashboard'))
                else:
                    flash('Invalid credentials', 'danger')
        except Exception as e:
            flash('An error occurred. Please try again.', 'danger')
        finally:
            connection.close()
    
    return render_template('user_login.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

# User Dashboard Routes
@app.route('/user_dashboard')
@login_required()
def user_dashboard():
    return render_template('user_dashboard.html', username=session.get('username'))

@app.route('/program_detail/<program_category>')
@login_required()
def program_detail(program_category):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM content WHERE program_category = %s ORDER BY created_at DESC"
            cursor.execute(sql, (program_category,))
            content = cursor.fetchall()
    except Exception as e:
        flash('Error loading program content: ' + str(e), 'danger')
        content = []
    finally:
        connection.close()
    
    return render_template('program_detail.html', 
                         username=session.get('username'),
                         program_category=program_category,
                         content=content)

# Helper function to convert YouTube URLs to embed format
def convert_to_embed_url(url):
    """
    Convert various YouTube URL formats to embed format
    Supports:
    - youtu.be/VIDEO_ID
    - youtube.com/watch?v=VIDEO_ID
    - youtube.com/embed/VIDEO_ID (already correct)
    """
    if not url:
        return ""
    
    # If already in embed format, return as-is
    if 'youtube.com/embed/' in url:
        return url
    
    # Handle youtu.be short URLs
    if 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[-1].split('?')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    
    # Handle watch URLs
    if 'youtube.com/watch' in url:
        video_id = url.split('v=')[-1].split('&')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    
    # Return original if format not recognized
    return url

# Admin Panel Routes
@app.route('/admin_panel')
@login_required(role='admin')
def admin_panel():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Get all content
            sql = "SELECT * FROM content ORDER BY created_at DESC"
            cursor.execute(sql)
            content = cursor.fetchall()
            
            # Get content count by category
            sql_count = "SELECT program_category, COUNT(*) as count FROM content GROUP BY program_category"
            cursor.execute(sql_count)
            content_counts = cursor.fetchall()
            
    except Exception as e:
        flash('Error loading content: ' + str(e), 'danger')
        content = []
        content_counts = []
    finally:
        connection.close()
    
    return render_template('admin_panel.html', 
                         username=session.get('username'),
                         content=content,
                         content_counts=content_counts)

@app.route('/add_content', methods=['POST'])
@login_required(role='admin')
def add_content():
    title = request.form['title']
    description = request.form['description']
    program_category = request.form['program_category']
    video_link = request.form['video_link']
    
    # Convert YouTube URL to embed format if provided
    if video_link:
        video_link = convert_to_embed_url(video_link)
    
    # Handle file upload
    file_link = ''
    if 'file_upload' in request.files:
        file = request.files['file_upload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Store only the filename, not the full path
            file_link = filename
    
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO content (title, description, file_link, video_link, program_category) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (title, description, file_link, video_link, program_category))
            connection.commit()
            flash('Content added successfully!', 'success')
    except Exception as e:
        flash('Error adding content: ' + str(e), 'danger')
    finally:
        connection.close()
    
    return redirect(url_for('admin_panel'))

# Update the download_file function to use the correct path
@app.route('/download_file/<filename>')
@login_required()
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        flash('File not found. It may have been deleted or moved.', 'danger')
        return redirect(request.referrer or url_for('user_dashboard'))

# Add this new route to your app.py
@app.route('/view_pdf/<filename>')
@login_required()
def view_pdf(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        # Send file without forcing download (inline display)
        return send_file(file_path, as_attachment=False)
    except FileNotFoundError:
        flash('File not found. It may have been deleted or moved.', 'danger')
        return redirect(request.referrer or url_for('user_dashboard'))


@app.route('/delete_content/<int:content_id>')
@login_required(role='admin')
def delete_content(content_id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "DELETE FROM content WHERE id = %s"
            cursor.execute(sql, (content_id,))
            connection.commit()
            flash('Content deleted successfully!', 'success')
    except Exception as e:
        flash('Error deleting content: ' + str(e), 'danger')
    finally:
        connection.close()
    
    return redirect(url_for('admin_panel'))


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)