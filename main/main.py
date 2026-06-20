from fastapi import FastAPI, Request
import sqlite3

app = FastAPI()

conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

# ==========================================
# GET USER
# ==========================================
@app.get("/user/{username}")
def get_user(username: str):
    user = cursor.execute(
        "SELECT vip FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if user:
        return {"vip": user[0]}

    return {"vip": 0}

# ==========================================
# PAYSTACK WEBHOOK
# ==========================================
@app.post("/paystack/webhook")
async def paystack_webhook(request: Request):

    data = await request.json()

    event = data.get("event")

    if event == "charge.success":

        email = data["data"]["customer"]["fadigafr2000@yahoo.fr"]

        # convert email → username (à adapter)
        username = email.split("@")[0]

        cursor.execute("""
        UPDATE users SET vip=1 WHERE username=?
        """,(username,))
        conn.commit()

        return {"status":"VIP ACTIVATED"}

    return {"status":"ignored"}
