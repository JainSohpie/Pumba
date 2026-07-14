"""품바 — 품의서 Agent (사내망 배포용)
API 키는 서버 환경변수 ANTHROPIC_API_KEY에만 존재하며 브라우저에 노출되지 않습니다.
"""
import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ALLOWED_MODEL = "claude-sonnet-4-6"   # 필요시 claude-haiku-4-5-20251001 로 교체하면 비용 1/3
MAX_TOKENS_CAP = 2000


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/health")
def health():
    return jsonify({"ok": True, "key_configured": bool(ANTHROPIC_API_KEY)})


@app.route("/api/messages", methods=["POST"])
def proxy_messages():
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": {"message": "서버에 ANTHROPIC_API_KEY가 설정되지 않았습니다."}}), 500

    body = request.get_json(force=True, silent=True) or {}
    # 서버에서 모델/토큰 상한 강제 (오남용 방지)
    body["model"] = ALLOWED_MODEL
    body["max_tokens"] = min(int(body.get("max_tokens", 1000)), MAX_TOKENS_CAP)

    try:
        r = requests.post(
            ANTHROPIC_URL,
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=body,
            timeout=120,
        )
        return (r.text, r.status_code, {"Content-Type": "application/json"})
    except requests.RequestException as e:
        return jsonify({"error": {"message": f"Anthropic API 연결 실패: {e}"}}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
