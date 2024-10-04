from flask import Flask,render_template,redirect,request
import random
import string
import json

app = Flask(__name__)

# storing urls in dictionary
shortened_urls={
}

def generate_short_url(length=6):
    #chars hold all possible letter and digits
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
        #checking if the short url exists already
        while short_url in shortened_urls:
            short_url = generate_short_url()

        shortened_urls[short_url]=long_url
        with open("urls.json","w") as f:
            json.dump(shortened_urls,f)
        return f"Shortened URL: {request.url_root}{short_url}"
    return render_template("index.html")

@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    return "URL NOT FOUND",404

if __name__ == "__main__":
    with open("urls.json",'r') as f:
        shortened_urls = json.load(f)
    app.run(debug=True)