from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for, session
import os
import socket   
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "shared_files"
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Required for session and flash messages

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"

hostname = socket.gethostname()
# ADMIN_IP = "192.168.22.173"
hostname = socket.gethostname()
ADMIN_IP = socket.gethostbyname(hostname)
 # Change this to your actual admin system's IP

@app.route("/", methods=["GET", "POST"])
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    client_ip = request.remote_addr
    print("ADMIN_IP="+ADMIN_IP+"\nIP="+request.remote_addr)
     
    print("Client ip="+client_ip)
    print("admin ip="+ADMIN_IP)
    is_admin = session.get("is_admin", False)
    show_admin_button = client_ip == ADMIN_IP  # Show login button only for admin IP
    return render_template("index.html", files=files, is_admin=is_admin, show_admin_button=show_admin_button)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.remote_addr != ADMIN_IP:
        flash("Access Denied! Only the Admin can log in.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["is_admin"] = True
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials, try again!", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("is_admin", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))

@app.route("/upload", methods=["POST"]) 
def upload_file():
    if not session.get("is_admin"):
        flash("Access Denied! Only Admin Can Upload.", "danger")
        return redirect(url_for("index"))
    
    if "file" not in request.files:
        flash("No file part", "danger")
        return redirect(url_for("index"))
    
    file = request.files["file"]
    if file.filename == "":
        flash("No selected file", "danger")
        return redirect(url_for("index"))

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    flash("File uploaded successfully!", "success")
    return redirect(url_for("index"))

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    if not session.get("is_admin"):
        flash("Access Denied! Only Admin Can Delete.", "danger")
        return redirect(url_for("index"))
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash("File deleted successfully!", "success")
    else:
        flash("File not found!", "danger")
    
    return redirect(url_for("index"))

if __name__ == "__main__":    
    app.run(host="0.0.0.0", port=8000, debug=True)
