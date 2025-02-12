from flask import Flask, render_template, request, json
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"


cars = [
    {
        "name": "Ferrari Purosangue",
        "image": "images/ferrari-purosangue.avif",
        "description": "Ferrari racing cars have set benchmarks on tracks worldwide, combining speed, innovation and unmatched design. Below is a showcase of some ofour most iconic Ferrari racing cars",
    },
    {
        "name": "Ferrari SF90 Stradale",
        "image": "images/sf90-stradale.avif",
        "description": "The Ferrari Stradale is a groundbreaking plug-in hybrid electric vehicle, combining a turbocharged V8 engine with three electric motors. What makes the SF90 Stradale fascinating is its ability to offer both extreme perfomance and a degree of environmental consciousness, positioning Ferrari within the hybrid landscape while staying true to its heritage",
    },
    {
        "name": "Ferrari Monza SP1",
        "image": "images/monza-sp1.avif",
        "description": "The Ferrari Monza SP1 is a stunning, limited-production speedster designed to capture the essence of Ferrari's iconic racing heritage. Its engine is derived from the Ferrari 81 Superfast and the car is made up of carbon fiber, making the car lightweight and enhancing its perfomance",
    },
    {
        "name": "Ferrari SF90 Spider",
        "image": "images/sf90-spider.avif",
        "description": "The Ferrari SF90 spider is an open top variant of the SF90 Stradale, combining the thrill of a convertible with the high-perfomance capabilities of a hybrid supercar. The overall look of this car is sleek and agggressive, with the state of the art aerodynamics",
    },
    {
        "name": "Ferrari LaFerrari Aperta",
        "image": "images/la-ferrari-aperta-land.avif",
        "description": "The Ferrari LaFerrari Aperta is the convertible version of Ferrari's hybrid supercar, the LaFerrari. It is a limited edition model which is designed to celebrate Ferrari's 70th anniversary. The design also features a virtual windshield that detects airflow over the driver's head for added comfort",
    },
    {
        "name": "Ferrari 812 Competizione",
        "image": "images/812-competizione.avif",
        "description": "The Ferrari 812 Competizione is a high perfomance, limited-edition variant of the 812 Superfast. It represents the pinnacle of Ferrari's front-engined v12 offerings. It also has lightweight materials such a carbon fiber and titanium which helps to reduce the overall weight of the car, enhancing its performance",
    },
]


@app.route("/")
def about():
    return render_template("racing.html", cars=cars)


@app.route("/home")
def home():
    render_template("home.html")


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


@app.route("/uploads", methods=["GET", "POST"])
def upload_listing():
    listings = load_listings()
    if os.path.exists(listings_file):
        with open(listings_file, "r") as file:
            listings = json.load(file)

    else:
        listings = []

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        image = request.files.get("cover_image")

        image_path = ""

        if image:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(filepath)
            image_path = filepath

        new_listing = {
            "title": title,
            "description": description,
            "cover_image": image_path,
        }

        listings.append(new_listing)

    with open(listings_file, "w") as file:
        json.dump(listings, file, indent=4)

    return render_template("upload_listing.html", listings=listings)
