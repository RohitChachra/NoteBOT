import os
import json
import requests
import re
from flask import Blueprint, render_template, request, jsonify

# Blueprint for quiz UI + APIs
quiz = Blueprint("quiz", __name__, template_folder="templates")

# ==========================
#  CONFIG
# ==========================

# From your .env
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
# Good default: cheap + good enough; you can set PERPLEXITY_MODEL=sonar-pro in .env later if you want
PERPLEXITY_MODEL = os.getenv("PERPLEXITY_MODEL", "sonar")

# Simple soft usage protection (approx)
MAX_QUESTIONS_BUDGET = 300   # total questions that can be generated in this process
usage_counter = {"questions_generated": 0}

def extract_json_block(text: str) -> str:
    """
    Try to pull out a JSON object from a model response that may contain
    extra text or ```json code fences``` around it.
    """
    if not text:
        return text

    # 1) If there's a ```json ... ``` fenced block, grab inside it
    fenced = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        return fenced.group(1).strip()

    # 2) Fallback: take substring from first '{' to last '}'
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1].strip()

    # 3) If nothing sensible found, just return original
    return text.strip()

# ==========================
#  QUIZ HOME ROUTE
# ==========================

@quiz.route("/quiz")
def quiz_home():
    """
    Renders the main QuizBot UI.
    This will use templates/quiz_home.html and that template will include CSS/JS partials.
    """
    return render_template("quiz_home.html")


# ==========================
#  GENERATE QUIZ API
# ==========================

@quiz.route("/quiz/api/generate", methods=["POST"])
def generate_quiz():
    """
    POST /quiz/api/generate
    Expects JSON body:
    {
      "topic": "...",
      "num_questions": 10,
      "difficulty": "easy|medium|hard|extremely hard|exam prep",
      "navigation_mode": "sequential"|"free",
      "timer_mode": "per_question"|"total_time",
      "per_question_seconds": 30,
      "total_timer_minutes": 5
    }
    Returns:
    {
      "questions": [...],
      "navigation_mode": "...",
      "timer_mode": "...",
      "per_question_seconds": ...,
      "total_timer_minutes": ...,
      "total_time_seconds": ...
    }
    """
    if not PERPLEXITY_API_KEY:
        return jsonify({"error": "PERPLEXITY_API_KEY is not set"}), 500

    data = request.get_json() or {}

    topic = (data.get("topic") or "").strip()
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    # Number of questions (1–20)
    try:
        num_questions = int(data.get("num_questions", 5))
    except (TypeError, ValueError):
        num_questions = 5
    num_questions = max(1, min(20, num_questions))

    difficulty = (data.get("difficulty") or "medium").lower()
    allowed_difficulties = {"easy", "medium", "hard", "extremely hard", "exam prep"}
    if difficulty not in allowed_difficulties:
        difficulty = "medium"

    navigation_mode = data.get("navigation_mode", "sequential")
    if navigation_mode not in {"sequential", "free"}:
        navigation_mode = "sequential"

    timer_mode = data.get("timer_mode", "per_question")
    if timer_mode not in {"per_question", "total_time"}:
        timer_mode = "per_question"

    # Per-question timer (seconds) for per_question mode
    try:
        per_question_seconds = int(data.get("per_question_seconds", 30))
    except (TypeError, ValueError):
        per_question_seconds = 30
    # clamp between 5 and 180 seconds just in case
    per_question_seconds = max(5, min(180, per_question_seconds))

    # Total quiz timer (minutes) for total_time mode
    try:
        total_timer_minutes = int(data.get("total_timer_minutes", 5))
    except (TypeError, ValueError):
        total_timer_minutes = 5
    total_timer_minutes = max(1, min(60, total_timer_minutes))

    # ========== Usage limit (very approximate) ==========
    global usage_counter
    if usage_counter["questions_generated"] + num_questions > MAX_QUESTIONS_BUDGET:
        return jsonify({
            "error": "Monthly quiz generation limit (for this server) reached. Please try again later."
        }), 429

    # ==========================
    #  Build prompts for Perplexity
    # ==========================

    system_prompt = (
        "You are an expert MCQ generator AI for college-level students. "
        "You MUST respond with strictly valid JSON only. "
        "No markdown, no explanations, no extra text."
    )

    user_prompt = f"""
Generate {num_questions} multiple-choice questions on the topic "{topic}" 
with difficulty level "{difficulty}".

Difficulty meaning:
- easy: basic recall questions
- medium: conceptual understanding
- hard: application-level questions
- extremely hard: very challenging, deep analytical questions
- exam prep: exam-style mix of medium and hard

Return ONLY valid JSON in this exact structure:

{{
  "questions": [
    {{
      "question": "Question text...",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer_index": 0
    }}
  ]
}}

Rules:
- Always 4 options per question.
- answer_index is the 0-based index of the correct option.
- No explanations, no comments, no markdown, only the JSON object above.
"""

    # ==========================
    #  CALL PERPLEXITY CHAT COMPLETIONS API
    # ==========================

    try:
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": PERPLEXITY_MODEL,  # e.g. "sonar" or "sonar-pro"
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 2000,
                "temperature": 0.3,
                # we don't want web search here, just pure generation
                "disable_search": True,
            },
            timeout=40,
        )
    except Exception as e:
        return jsonify({"error": f"Error contacting Perplexity API: {e}"}), 502

    if resp.status_code != 200:
        return jsonify({
            "error": "Perplexity API returned an error",
            "details": resp.text,
        }), 502

    api_data = resp.json()
    content = (
        api_data.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )

    # ==========================
    #  PARSE JSON CONTENT
    # ==========================
    clean_text = extract_json_block(content)

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return jsonify({"error": "AI returned invalid JSON, please try again."}), 500

    questions_raw = parsed.get("questions", [])
    clean_questions = []

    for q in questions_raw:
        if not isinstance(q, dict):
            continue
        text = q.get("question")
        options = q.get("options")
        answer_index = q.get("answer_index", 0)

        if not text or not isinstance(options, list) or len(options) < 2:
            continue

        # ensure 0 <= answer_index < len(options)
        if not isinstance(answer_index, int) or not (0 <= answer_index < len(options)):
            answer_index = 0

        clean_questions.append({
            "question": text,
            "options": options,
            "answer_index": answer_index
        })

        if len(clean_questions) >= num_questions:
            break

    if not clean_questions:
        return jsonify({"error": "No valid questions generated. Please try again."}), 500

    # Update usage estimate
    usage_counter["questions_generated"] += len(clean_questions)

    # ==========================
    #  TIMER CALCULATION
    # ==========================

    if timer_mode == "per_question":
        total_time_seconds = len(clean_questions) * per_question_seconds
    else:  # "total_time"
        total_time_seconds = total_timer_minutes * 60

    # ==========================
    #  RESPONSE TO FRONTEND
    # ==========================

    return jsonify({
        "questions": clean_questions,
        "navigation_mode": navigation_mode,
        "timer_mode": timer_mode,
        "per_question_seconds": per_question_seconds,
        "total_timer_minutes": total_timer_minutes,
        "total_time_seconds": total_time_seconds,
    })
