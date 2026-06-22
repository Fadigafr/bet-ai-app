from fastapi import FastAPI, Request
import sqlite3
from fastapi import FastAPI, Request, HTTPException
import sqlite3
import hmac
import hashlib

app = FastAPI()

conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

PAYSTACK_SECRET = "TON_SECRET_PAYSTACK"

# ==========================================
# VERIFY SIGNATURE
# ==========================================
def verify_signature(request_body, signature):
    expected = hmac.new(
        PAYSTACK_SECRET.encode(),
        request_body,
        hashlib.sha512
    ).hexdigest()

    return hmac.compare_digest(expected, signature)

# ==========================================
# WEBHOOK PAYSTACK
# ==========================================
@app.post("/paystack/webhook")
async def webhook(request: Request):

    body = await request.body()
    signature = request.headers.get("x-paystack-signature")

    if not verify_signature(body, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    data = await request.json()

    if data["event"] == "charge.success":

        email = data["data"]["customer"]["email"]

        cursor.execute("""
        UPDATE users SET vip=1 WHERE username=?
        """, (email,))

        conn.commit()

        return {"status": "VIP ACTIVATED"}

    return {"status": "ignored"}
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
