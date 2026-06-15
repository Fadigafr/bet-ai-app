from flask import Flask, request
import json

app = Flask(__name__)

def load réussidef load_users():
    if data["event"] == "charge.success":

        email = data["data"]["customer"]["email"]

        users = load_users()

        if email in users:
            users[email]["vip"] = True
            save_users(users)
            print(f"{email} VIP activé ")

    return "OK"

if __name__ == "__main__":
    app.run()

    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

