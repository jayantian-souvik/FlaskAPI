from app import app

@app.route("/product/add")
def padd():
    return "This is Product add Operation"