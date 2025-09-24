from flask import Blueprint, render_template_string

quiz = Blueprint("quiz", __name__)

# HTML Template for Quiz Mode
template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>QuizBot</title>
  <link rel="icon" href="{{ url_for('static', filename='QuizBot_favicon.png') }}" type="image/png">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { padding-top: 60px; }
    footer { background: #f8f9fa; padding: 15px; text-align: center; margin-top: 20px; }
  </style>
</head>
<body>
  <!-- Navbar with toggle -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand" href="/quiz">📝 QuizBot</a>
      <div class="d-flex">
        <a class="btn btn-outline-light me-2" href="/">Notebot Mode</a>
        <a class="btn btn-warning active">Quiz Mode</a>
      </div>
    </div>
  </nav>

  <!-- Main Content -->
  <div class="container text-center">
    <h1 class="mt-4">📝 Quiz Mode</h1>
    <p class="lead">Test your knowledge with interactive quizzes!</p>

    <div class="card mt-4 shadow">
      <div class="card-body">
        <h5 class="card-title">Coming Soon 🚧</h5>
        <p class="card-text">Here you will be able to attempt subject-wise quizzes.</p>
        <button class="btn btn-primary" disabled>Start Quiz</button>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer>
    <p>© QuizBot 2025 | Created by ~RC~ (UIET CHD)
  </footer>
</body>
</html>
"""

@quiz.route("/quiz")
def quiz_home():
    return render_template_string(template)
