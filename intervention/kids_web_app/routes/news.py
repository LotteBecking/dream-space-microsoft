"""Internal /api/news endpoint — served to the carousel JS."""

from flask import Blueprint, jsonify
from services.news_service import get_news

news_bp = Blueprint("news", __name__)


@news_bp.route("/api/news")
def news():
    return jsonify(get_news())
