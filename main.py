from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import RouteRequest
from app.agents.route_agent import RouteAgent

from app.database import get_connection
from app.models import UserRegister, UserLogin
import bcrypt

app = FastAPI(
    title="Agentic Maritime Brokerage Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

route_agent = RouteAgent()

@app.get("/")
def home():
    return {
        "message": "Agentic Maritime Brokerage API is running"
    }

@app.post("/api/routes/analyze")
def analyze_route(request: RouteRequest):

    return route_agent.analyze_route(
        request.origin,
        request.destination,
        request.cargo_type,
        request.containers
    )
@app.post("/register")
def register(user: UserRegister):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    )

    query = """
    INSERT INTO users (username, email, password)
    VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (
            user.username,
            user.email,
            hashed_password.decode('utf-8')
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "status": "success",
        "message": "User registered successfully"
    }
@app.post("/login")
def login(user: UserLogin):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (user.username,)
    )

    db_user = cursor.fetchone()

    # User does not exist → create account automatically
    if db_user is None:

        hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"),
            bcrypt.gensalt()
        )

        cursor.execute(
            """
            INSERT INTO users(username,email,password)
            VALUES(%s,%s,%s)
            """,
            (
                user.username,
                f"{user.username}@cargoai.local",
                hashed_password.decode("utf-8")
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "status": "success",
            "message": "New user created and logged in"
        }

    # Existing user → check password
    if bcrypt.checkpw(
        user.password.encode("utf-8"),
        db_user["password"].encode("utf-8")
    ):

        cursor.close()
        conn.close()

        return {
            "status": "success",
            "message": "Login successful"
        }

    cursor.close()
    conn.close()

    return {
        "status": "failed",
        "message": "Wrong password"
    }