from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    json,
    send_from_directory,
    session,
)
import os
from mySql.dbconn import get_db_conn


app = Flask(__name__)

app.secret_key = "amc_se"
app.config["UPLOAD_FOLDER"] = "uploads"


# cars = [
#     {
#         "name": "Ferrari Purosangue",
#         "image": "images/ferrari-purosangue.avif",
#         "description": "Ferrari racing cars have set benchmarks on tracks worldwide, combining speed, innovation and unmatched design. Below is a showcase of some ofour most iconic Ferrari racing cars",
#     },
#     {
#         "name": "Ferrari SF90 Stradale",
#         "image": "images/sf90-stradale.avif",
#         "description": "The Ferrari Stradale is a groundbreaking plug-in hybrid electric vehicle, combining a turbocharged V8 engine with three electric motors. What makes the SF90 Stradale fascinating is its ability to offer both extreme perfomance and a degree of environmental consciousness, positioning Ferrari within the hybrid landscape while staying true to its heritage",
#     },
#     {
#         "name": "Ferrari Monza SP1",
#         "image": "images/monza-sp1.avif",
#         "description": "The Ferrari Monza SP1 is a stunning, limited-production speedster designed to capture the essence of Ferrari's iconic racing heritage. Its engine is derived from the Ferrari 81 Superfast and the car is made up of carbon fiber, making the car lightweight and enhancing its perfomance",
#     },
#     {
#         "name": "Ferrari SF90 Spider",
#         "image": "images/sf90-spider.avif",
#         "description": "The Ferrari SF90 spider is an open top variant of the SF90 Stradale, combining the thrill of a convertible with the high-perfomance capabilities of a hybrid supercar. The overall look of this car is sleek and agggressive, with the state of the art aerodynamics",
#     },
#     {
#         "name": "Ferrari LaFerrari Aperta",
#         "image": "images/la-ferrari-aperta-land.avif",
#         "description": "The Ferrari LaFerrari Aperta is the convertible version of Ferrari's hybrid supercar, the LaFerrari. It is a limited edition model which is designed to celebrate Ferrari's 70th anniversary. The design also features a virtual windshield that detects airflow over the driver's head for added comfort",
#     },
#     {
#         "name": "Ferrari 812 Competizione",
#         "image": "images/812-competizione.avif",
#         "description": "The Ferrari 812 Competizione is a high perfomance, limited-edition variant of the 812 Superfast. It represents the pinnacle of Ferrari's front-engined v12 offerings. It also has lightweight materials such a carbon fiber and titanium which helps to reduce the overall weight of the car, enhancing its performance",
#     },
# ]


# @app.route("/")
# def about():
#     return render_template("racing.html", cars=cars)


# @app.route("/home")
# def home():
#     render_template("home.html")


# path to the listings file
listings_file = "listings/listings.json"

# ensuring that the upload file directory and listings directory exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(os.path.dirname(listings_file), exist_ok=True)


# Load existing listings from the listings.json file
def load_listings():
    if os.path.exists(listings_file):
        with open(listings_file, "r") as file:
            return json.load(file)
    return []


# Save updated listings to the listings.json file
def save_listings(listings):
    with open(listings_file, "w") as file:
        json.dump(listings, file, indent=4)


# Home route here displays upload_listing.html and retrieves the logged_in status and username from the session
@app.route("/", methods=["GET", "POST"])
def home():
    logged_in = session.get("logged_in", False)
    username = session.get("username", "Guest")

    listings = load_listings()

    return render_template(
        "upload_listing.html", username=username, logged_in=logged_in, listings=listings
    )


@app.route("/uploads", methods=["GET", "POST"])
def upload_listing():
    conn = get_db_conn()
    cursor = conn.cursor()
    listings = load_listings()

    if request.method == "POST":
        print("request method is post")
        title = request.form.get("title")
        description = request.form.get("description")
        image = request.files.get("cover_image")

        if not title or not description:
            return render_template(
                "upload_listing.html", error="Title and description are required"
            )

        print("Form Data:", title, description, image)

        image_filename = ""

        if image and image.filename:
            filename = image_filename
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            counter = 1
            base, ext = os.path.splitext(filename)
            while os.path.exists(filepath):
                filename = f"{base}_{counter}{ext}"
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                counter += 1
            image.save(filepath)
            image_filename = filename

            print("Image saved at", filename)
        else:
            print("No image uploaded")

        new_listing = {
            "title": title,
            "description": description,
            "cover_image": image_filename,
        }

        listings.append(new_listing)
        save_listings(listings)

        insert_query = (
            "INSERT INTO cars(Title, Description, Cover_image) VALUES(%s, %s, %s)"
        )
        values = (title, description, os.path.join("uploads", image_filename))

        cursor.execute(insert_query, values)
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for("home"))


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/login", methods=["GET", "POST"])
def login():
    logged_in = session.get("logged_in", False)
    username = session.get("username", "Guest")

    if request.method == "POST":
        username_input = request.form.get("username")
        password_input = request.form.get("password")

        print(f"Received Username: {username_input}, password: {password_input}")
        conn = get_db_conn()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username_input, password_input))

        user = cursor.fetchone()
        print(f"User found: {user}")

        cursor.close()
        # Here we check if the user's credentials exist in the database
        if user:
            session["username"] = username_input
            session["logged_in"] = True
            print(f"User{username_input} logged in successfully!")
            return redirect(url_for("home"))
        else:
            print("Invalid attempt to login")
            return render_template("upload_listing.html", error="Invalid Credentials")

    return render_template(
        "upload_listing.html", logged_in=logged_in, username=username
    )


@app.route("/logout", methods=["GET", "POST"])
def logout():
    print("Logging out user")
    session.clear()
    return redirect(url_for("home"))
