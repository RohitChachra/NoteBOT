from flask import Blueprint, render_template_string, url_for

botUI = Blueprint("botUI", __name__)

# HTML Template for Notebot UI
template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>IT Notebot</title>
  <link rel="icon" href="{{ url_for('static', filename='NoteBot_favicon.png') }}" type="image/png">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

  <style>

    body { padding-top: 60px; }
    
    .bot-image { max-width: 180px; margin: 20px auto; display: block; }
    .flowchart-step { border: 2px solid #0d6efd; border-radius: 12px; padding: 15px; margin: 10px 0; background: #e9f2ff; width: 250px; }
    .arrow-down { font-size: 2rem; color: #0d6efd; margin: 10px 0; }
    .card { border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .card-header { font-weight: bold; font-size: 1.2rem; }
    footer { background: #212529; color: #f8f9fa; padding: 20px; text-align: center; margin-top: 40px; font-size: 1.1rem; }
    footer a { color: #ffc107; text-decoration: none; margin: 0 8px; font-weight: 500; }
    footer a:hover { text-decoration: underline; }
    
    .moving-text {
        width: 100%;
        background: yellow;
        color: red;
        font-weight: bold;
        white-space: nowrap;
        box-sizing: border-box;
        padding: 8px 0;
        text-align: center;
        border: 2px solid yellow;
        position: relative;
    }

    .moving-text span {
        animation: blink 3s step-start infinite;
    }

    @keyframes blink {
        60% {
            visibility: visible;
        }
        100% {
            visibility: hidden;
        }
    }

  </style>
</head>
<body>
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">📚 NoteBot</a>
      <div class="d-flex">
        <a class="btn btn-light active me-2" href="/">Notebot Mode</a>
        <a class="btn btn-outline-warning" href="/quiz">Quiz Mode</a>
      </div>
    </div>
  </nav>

  <!-- Moving Text Below Navbar -->
    <div class="moving-text">
        <span>IT NoteBot is running. Click "Use the Telegram Bot" button to access it on Telegram.</span>
    </div>


  <!-- Main Content -->
  <div class="container text-center">
    <img src="{{ url_for('static', filename='IT_NoteBot.png') }}" alt="Bot Image" class="bot-image">
    <h1 class="mt-3">Welcome to IT NoteBot 🤖</h1>
    <h2 class="text-muted">BE-IT Study Material 📘</h2>
    <p class="lead">Your one-stop solution for Notes, Assignments, Books, Lab Files, and PYQs.</p>

    <!-- Buttons -->
    <div class="d-grid gap-3 col-6 mx-auto mt-4">
      <a href="https://t.me/+J8zLk2dQb301OGE1" target="_blank" class="btn btn-primary btn-lg">📢 Join Study Material Channel</a>
      <a href="https://t.me/ITnotes_bot" target="_blank" class="btn btn-success btn-lg">🤖 Use the Telegram Bot</a>
    </div>

    <!-- Cards (Left) + Flowchart (Right) -->
    <div class="row mt-5">
      <!-- Left Column -->
      <div class="col-md-6 text-start">
        <!-- Commands Card -->
        <div class="card">
          <div class="card-header bg-secondary text-white">⚙️ Available NoteBoT Commands</div>
          <div class="card-body">
            <ul>
              <li><b>/start</b> – Start the bot and show the main menu</li>
              <li><b>/help</b> – View help instructions</li>
              <li><b>/web_dev</b> – Access Web Dev (MERN) Course</li>
            </ul>
          </div>
        </div>

        <!-- Web Dev Course Card -->
        <div class="card">
          <div class="card-header bg-warning">🚀 Web Dev (MERN) Course</div>
          <div class="card-body">
            <p>Complete Full Stack Web Development course from basics to advanced.</p>
             <ul>
                <li>🎥 Video Lectures</li>
                <li>📄 Cheat Sheets & PDFs</li>
                <li>📝 Notes</li>
                <li>💻 Code ZIP Files</li>
                <li>📂 Projects & Practice Files</li>
            </ul>
            <p><b>Topics Covered:</b></p>
            <ul>
                <li>🔗 Git & GitHub – Version control</li>
                <li>💻 VS Code – Setup, extensions, pro tips</li>
                <li>🌐 HTML5 – Structure & page building</li>
                <li>🎨 CSS – Styling, Flexbox, Grid, Animations</li>
                <li>⚡ JavaScript – From basics to ES6+</li>
                <li>⚛️ React – Components, hooks, state management</li>
                <li>🟪 Node.js & Express.js – Backend development</li>
                <li>🍃 MongoDB – NoSQL database management</li>
                <li>⏭️ Next.js – React framework with SSR</li>
                <li>🔐 Authentication & Authorization</li>
            </ul>
            <div class="text-center">
              <a href="https://t.me/+bdXSonKRluY5N2Nl" target="_blank" class="btn btn-warning">📢 Join Course Channel</a>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="col-md-6 text-center d-flex flex-column align-items-center justify-content-center">
        <h3 class="mb-4">📊 How NoteBot Works</h3>
        <div class="d-flex flex-column align-items-center">
          <div class="flowchart-step">1️⃣ Start with <b>/start</b></div>
          <div class="arrow-down">⬇️</div>
          <div class="flowchart-step">2️⃣ Select Semester</div>
          <div class="arrow-down">⬇️</div>
          <div class="flowchart-step">3️⃣ Choose Subject</div>
          <div class="arrow-down">⬇️</div>
          <div class="flowchart-step">4️⃣ Pick Resource (Books, Notes, PYQs)</div>
          <div class="arrow-down">⬇️</div>
          <div class="flowchart-step">5️⃣ Get Files Instantly 📂</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer>
    <p>
      <a href="https://t.me/+J8zLk2dQb301OGE1" target="_blank">UIET IT Study Material</a> | 
      <a href="https://t.me/ITnotes_bot" target="_blank">IT Notebot</a> | 
      <a href="https://t.me/+bdXSonKRluY5N2Nl" target="_blank">Web Dev (MERN) Course</a><br>
      © NoteBot 2025 | Created by ~RC~ (UIET CHD)
    </p>
  </footer>
</body>
</html>
"""

@botUI.route("/")
def home():
    return render_template_string(template)
