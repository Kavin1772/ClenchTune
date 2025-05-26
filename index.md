<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ClenchTune – EMG Music Player</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f5f7fb;
      color: #333;
      padding: 40px;
      text-align: center;
    }
    h1 {
      color: #1d3f72;
      font-size: 2.8em;
    }
    h2 {
      margin-top: 40px;
      color: #2b2b2b;
    }
    p {
      font-size: 1.2em;
      max-width: 800px;
      margin: auto;
    }
    iframe, img {
      margin-top: 30px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      border-radius: 8px;
    }
    .footer {
      margin-top: 50px;
      font-size: 0.9em;
      color: #777;
    }
    a {
      color: #1a57c8;
      text-decoration: none;
    }
  </style>
</head>
<body>

  <h1>🎵 ClenchTune</h1>
  <p>A hands-free music player controlled by EMG muscle signals.<br>
  Developed by Kavin K, Rafi, and Ratchagan – ENGR 8445, San Francisco State University.</p>

  <h2>🎬 Demo Video</h2>
  <!-- ✅ Embed Google Drive video -->
  <iframe src="https://drive.google.com/file/d/1SGflaWPdg_cIZXje1ORA-oWwYBiqCF7I/view?usp=drive_link"></iframe>

  <h2>📸 Project Poster</h2>
  <!-- ✅ Embed Google Drive image -->
  <img src="https://drive.google.com/file/d/1HKbLJt1Xo5b-cgNu2HVXtj2JW6nvsx4r/view?usp=drive_link" width="720">

  <h2>🧠 How It Works</h2>
  <p>
    The system uses EMG sensors to detect muscle clenching in each palm.<br>
    A clench on the left hand pauses or resumes playback. A clench on the right hand skips the song.<br>
    The Arduino reads these values and sends them to a Python script that filters, detects patterns, and triggers media control.
  </p>

  <h2>🛠️ Tools & Tech</h2>
  <p>
    - Arduino Uno<br>
    - 2 Analog EMG Sensors (A0 = Pause, A1 = Skip)<br>
    - Python + Pygame<br>
    - Google Drive, GitHub Pages<br>
    - Signal Filtering & Moving Average
  </p>

  <h2>💻 View Source Code</h2>
  <p>
    <a href="https://github.com/Kavin1772/ClenchTune" target="_blank">GitHub Repository →</a>
  </p>

  <div class="footer">
    &copy; 2024 ClenchTune Project | Built with ❤️ for ENGR 8445
  </div>

</body>
</html>
