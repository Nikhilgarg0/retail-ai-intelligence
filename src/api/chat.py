# src/api/chat.py
# Chat endpoints for the Report Chatbot tab
# Plug into app.py with:
#   from src.api.chat import chat_bp
#   app.register_blueprint(chat_bp)

import json
import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from bson import ObjectId
from google import genai
from src.database.mongo_manager import db_manager
from config.settings import settings

logger = logging.getLogger(__name__)

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")

# ── Gemini client ─────────────────────────────────────────────────────────────
_gemini_client = None

def get_gemini():
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = genai.Client(api_key=settings.gemini_api_key)
    return _gemini_client


# ── Helper: serialize ObjectId / datetime ─────────────────────────────────────
def _clean(doc: dict) -> dict:
    out = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            out[k] = str(v)
        elif isinstance(v, datetime):
            out[k] = v.isoformat()
        elif isinstance(v, dict):
            out[k] = _clean(v)
        elif isinstance(v, list):
            out[k] = [
                _clean(i) if isinstance(i, dict)
                else (str(i) if isinstance(i, ObjectId) else i)
                for i in v
            ]
        else:
            out[k] = v
    return out


# ── Helper: build a readable text summary of a report ────────────────────────
def _report_to_text(report: dict) -> str:
    """
    Converts a MongoDB report document into a plain-text block
    that Gemini can reason about.
    """
    analysis = report.get("analysis", {})
    lines = []

    lines.append(f"Report ID     : {report.get('_id', 'N/A')}")
    lines.append(f"Report Type   : {report.get('report_type', 'N/A')}")
    lines.append(f"Platform      : {report.get('platform', 'N/A')}")
    lines.append(f"Category      : {report.get('category', 'N/A')}")
    lines.append(f"Generated At  : {report.get('generated_at', 'N/A')}")
    lines.append(f"Products Analysed: {report.get('products_analyzed', 'N/A')}")
    lines.append("")

    # ── Quick analysis fields ──────────────────────────────────────────────
    pr = analysis.get("price_range", {})
    if pr:
        lines.append("── Price Range ──")
        lines.append(f"  Min     : ₹{pr.get('min', 'N/A')}")
        lines.append(f"  Max     : ₹{pr.get('max', 'N/A')}")
        lines.append(f"  Average : ₹{pr.get('average', 'N/A')}")
        lines.append("")

    top = analysis.get("top_rated_product", {})
    if top:
        lines.append("── Top Rated Product ──")
        lines.append(f"  Title  : {top.get('title', 'N/A')}")
        lines.append(f"  Rating : {top.get('rating', 'N/A')}")
        lines.append(f"  Price  : ₹{top.get('price', 'N/A')}")
        lines.append("")

    best = analysis.get("best_value_product", {})
    if best:
        lines.append("── Best Value Product ──")
        lines.append(f"  Title  : {best.get('title', 'N/A')}")
        lines.append(f"  Reason : {best.get('reason', 'N/A')}")
        lines.append("")

    insights = analysis.get("price_insights", [])
    if insights:
        lines.append("── Price Insights ──")
        for ins in insights:
            lines.append(f"  • {ins}")
        lines.append("")

    recs = analysis.get("recommendations", [])
    if recs:
        lines.append("── Recommendations ──")
        for i, rec in enumerate(recs, 1):
            lines.append(f"  {i}. {rec}")
        lines.append("")

    # ── Deep analysis (CrewAI) fields ─────────────────────────────────────
    agent_outputs = analysis.get("agent_outputs", [])
    if agent_outputs:
        lines.append("── Agent Analysis ──")
        for ao in agent_outputs:
            lines.append(f"\n[ {ao.get('agent', 'Agent')} ]")
            lines.append(ao.get("output", ""))
        lines.append("")

    final = analysis.get("final_report", "")
    if final:
        lines.append("── Final Report ──")
        lines.append(final)

    return "\n".join(lines)


# ── Helper: build Gemini messages from history ────────────────────────────────
def _build_prompt(report_text: str, history: list, user_message: str) -> str:
    """
    Builds the full prompt string sent to Gemini.
    history = [{ "role": "user"|"assistant", "content": "..." }, ...]
    """
    system = f"""You are a smart retail business analyst assistant.
The user is chatting about a specific retail intelligence report. 
Your job is to answer questions, summarise sections, compare metrics, 
and give actionable advice — all strictly based on the report data below.

You also understand Hinglish (mixed Hindi-English). Reply in the same 
language style the user uses (if they write in Hinglish, reply in Hinglish; 
if English, reply in English).

Rules:
- Only use information from the report. Do not make up data.
- Be concise but complete.
- If the user asks something not covered in the report, say so clearly.
- Format numbers with ₹ symbol and commas where relevant.

━━━━━━━━━━━━━━ REPORT DATA ━━━━━━━━━━━━━━
{report_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    conversation = []
    for msg in history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            conversation.append(f"User: {content}")
        else:
            conversation.append(f"Assistant: {content}")

    conversation.append(f"User: {user_message}")
    conversation.append("Assistant:")

    return system + "\n\n" + "\n\n".join(conversation)


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 1 — GET /api/chat/reports
# Returns list of all saved reports (id, type, platform, category, date)
# Used by the frontend to populate the report selector
# ══════════════════════════════════════════════════════════════════════════════
@chat_bp.route("/reports", methods=["GET"])
def list_reports():
    try:
        raw = list(
            db_manager.reports.find(
                {"report_type": {"$in": ["quick_analysis", "deep_analysis"]}},
                # Only fetch metadata, NOT the full analysis blob (keeps response small)
                {"_id": 1, "report_type": 1, "platform": 1,
                 "category": 1, "generated_at": 1, "products_analyzed": 1}
            ).sort([("_id", -1)]).limit(50)   # _id is always present & monotonically increasing
        )

        reports = []
        for i, r in enumerate(raw, 1):
            reports.append({
                "id"               : str(r["_id"]),
                "report_number"    : i,                           # "Report 1", "Report 2" ...
                "report_type"      : r.get("report_type", "N/A"),
                "platform"         : r.get("platform", "all"),
                "category"         : r.get("category", "all"),
                "products_analyzed": r.get("products_analyzed", 0),
                "generated_at"     : r["generated_at"].isoformat()
                                     if isinstance(r.get("generated_at"), datetime)
                                     else str(r.get("generated_at", "")),
                # Human-readable label shown in the UI dropdown / sidebar
                "label"            : (
                    f"Report {i} — "
                    f"{r.get('report_type','').replace('_',' ').title()} | "
                    f"{r.get('platform','all').upper()} | "
                    f"{r.get('category','all').capitalize()}"
                )
            })

        return jsonify({"reports": reports, "total": len(reports)})

    except Exception as e:
        logger.error(f"list_reports error: {e}")
        return jsonify({"error": str(e)}), 500


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 2 — POST /api/chat
# Body: { "message": str, "report_id": str, "history": [...] }
# Returns: { "reply": str, "report_id": str }
# ══════════════════════════════════════════════════════════════════════════════
@chat_bp.route("", methods=["POST"])
def chat():
    body = request.get_json() or {}

    user_message = body.get("message", "").strip()
    report_id    = body.get("report_id", "").strip()
    history      = body.get("history", [])   # list of {role, content}

    # ── Validate ──────────────────────────────────────────────────────────
    if not user_message:
        return jsonify({"error": "message is required"}), 400

    if not report_id:
        return jsonify({"error": "report_id is required. Ask the user to select a report first."}), 400

    # ── Fetch report from MongoDB ─────────────────────────────────────────
    try:
        report = db_manager.reports.find_one({"_id": ObjectId(report_id)})
    except Exception:
        return jsonify({"error": "Invalid report_id format"}), 400

    if not report:
        return jsonify({"error": f"No report found with id: {report_id}"}), 404

    report = _clean(report)

    # ── Convert report to readable text ───────────────────────────────────
    report_text = _report_to_text(report)

    # ── Build prompt with full conversation history ────────────────────────
    prompt = _build_prompt(report_text, history, user_message)

    # ── Call Gemini ───────────────────────────────────────────────────────
    try:
        client   = get_gemini()
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )
        reply = response.text.strip()
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return jsonify({"error": f"AI error: {str(e)}"}), 500

    return jsonify({
        "reply"    : reply,
        "report_id": report_id,
    })