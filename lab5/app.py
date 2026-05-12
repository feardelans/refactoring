"""Flask REST API for the Video Game Store application."""
import os

from flask import Flask, jsonify, request

from src.repositories.game_repository import GameRepository
from src.repositories.user_repository import UserRepository
from src.services.store_service import StoreService
from src.services.user_service import UserService

app = Flask(__name__)

user_repo = UserRepository()
game_repo = GameRepository()
user_service = UserService(user_repo)
store_service = StoreService(game_repo, user_repo)


@app.route("/health", methods=["GET"])
def health_check():
    """Returns service health status and database connectivity."""
    db_status = "not_configured"
    if os.getenv("DATABASE_URL"):
        try:
            import psycopg2  # pylint: disable=import-outside-toplevel
            conn = psycopg2.connect(os.getenv("DATABASE_URL"))
            conn.close()
            db_status = "connected"
        except Exception:  # pylint: disable=broad-except
            db_status = "unavailable"
    return jsonify({"status": "healthy", "database": db_status})


# ── User endpoints ──────────────────────────────────────────────


@app.route("/users", methods=["POST"])
def register_user():
    """Register a new user. Expects JSON with user_id, email, age."""
    data = request.get_json(force=True)
    try:
        user = user_service.register_user(
            data["user_id"], data["email"], data["age"]
        )
        return jsonify({
            "user_id": user.user_id,
            "email": user.email,
            "age": user.age,
            "library": user.library,
            "wishlist": user.wishlist,
        }), 201
    except (ValueError, KeyError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get user details by ID."""
    user = user_repo.find_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    return jsonify({
        "user_id": user.user_id,
        "email": user.email,
        "age": user.age,
        "library": user.library,
        "wishlist": user.wishlist,
    })


# ── Game / catalog endpoints ────────────────────────────────────


@app.route("/games", methods=["GET"])
def search_games():
    """Search games by title query parameter. Returns all games if empty."""
    query = request.args.get("q", "")
    games = store_service.search_games(query)
    return jsonify([{"game_id": g.game_id, "title": g.title} for g in games])


@app.route("/games/<int:game_id>", methods=["GET"])
def get_game(game_id):
    """Get a single game by ID."""
    game = game_repo.find_by_id(game_id)
    if not game:
        return jsonify({"error": "Game not found."}), 404
    return jsonify({"game_id": game.game_id, "title": game.title})


# ── Library endpoints ───────────────────────────────────────────


@app.route("/users/<int:user_id>/library", methods=["POST"])
def add_to_library(user_id):
    """Add a game to user's library. Expects JSON with game_id."""
    data = request.get_json(force=True)
    try:
        store_service.add_to_library(user_id, data["game_id"])
        return jsonify({"message": "Game added to library."}), 201
    except (ValueError, KeyError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/users/<int:user_id>/library/<int:game_id>", methods=["DELETE"])
def refund_game(user_id, game_id):
    """Refund (remove) a game from user's library."""
    try:
        store_service.refund_game(user_id, game_id)
        return jsonify({"message": "Game refunded successfully."})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


# ── Wishlist endpoints ──────────────────────────────────────────


@app.route("/users/<int:user_id>/wishlist", methods=["POST"])
def add_to_wishlist(user_id):
    """Add a game to user's wishlist. Expects JSON with game_id."""
    data = request.get_json(force=True)
    try:
        store_service.add_to_wishlist(user_id, data["game_id"])
        return jsonify({"message": "Game added to wishlist."}), 201
    except (ValueError, KeyError) as exc:
        return jsonify({"error": str(exc)}), 400


# ── Review endpoints ────────────────────────────────────────────


@app.route("/users/<int:user_id>/reviews", methods=["POST"])
def leave_review(user_id):
    """Leave a review for a game. Expects JSON with game_id, rating, text."""
    data = request.get_json(force=True)
    try:
        review = store_service.leave_review(
            user_id, data["game_id"], data["rating"], data["text"]
        )
        return jsonify({
            "user_id": review.user_id,
            "game_id": review.game_id,
            "rating": review.rating,
            "text": review.text,
        }), 201
    except (ValueError, KeyError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/reviews", methods=["GET"])
def get_reviews():
    """Get all reviews, optionally filtered by game_id query parameter."""
    game_id = request.args.get("game_id", type=int)
    reviews = store_service.reviews
    if game_id is not None:
        reviews = [r for r in reviews if r.game_id == game_id]
    return jsonify([{
        "user_id": r.user_id,
        "game_id": r.game_id,
        "rating": r.rating,
        "text": r.text,
    } for r in reviews])


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "0") == "1")
