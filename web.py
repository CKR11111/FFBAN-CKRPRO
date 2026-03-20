from flask import Flask, request, jsonify, render_template_string
import subprocess, threading, os, sys

app = Flask(__name__)
LOG_FILE = "run.log"

def run_ckr_script(token):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("Ready for input ...\n")
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        process = subprocess.Popen(
            [sys.executable, "ckr.py"],
            stdin=subprocess.PIPE,
            stdout=f,
            stderr=f,
            text=True,
            bufsize=1
        )
        process.stdin.write(f"{token}\n")
        process.stdin.flush()
        process.wait()
        with open(LOG_FILE, "a") as f_end:
            f_end.write("\n[!] Process Finished.")

UI_DESIGN = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FF Info Tool</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, sans-serif; }
        
        body { 
            background: linear-gradient(180deg, #F9D0D9 0%, #E6A8B8 100%); 
            height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
        }

        /* Main Glass Card */
        .card { 
            background: rgba(255, 255, 255, 0.4); 
            backdrop-filter: blur(10px); 
            -webkit-backdrop-filter: blur(10px);
            border-radius: 40px; 
            width: 90%; 
            max-width: 400px; 
            padding: 35px 25px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Input Field Style */
        .input-field {
            width: 100%;
            padding: 18px;
            background: rgba(255, 255, 255, 0.6);
            border: none;
            border-radius: 18px;
            font-size: 16px;
            color: #555;
            outline: none;
            margin-bottom: 15px;
        }
        .input-field::placeholder { color: #999; }

        /* Blue Button Style */
        .btn {
            width: 100%;
            padding: 18px;
            background: #007AFF;
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 16px;
            font-weight: 600;
            text-transform: uppercase;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
            margin-bottom: 20px;
        }

        /* Terminal Box Style */
        .terminal {
            background: #2C2424;
            border-radius: 20px;
            padding: 15px;
            height: 200px;
            overflow-y: auto;
            text-align: left;
        }

        .dots {
            display: flex;
            gap: 6px;
            margin-bottom: 10px;
        }
        .dot { width: 10px; height: 10px; border-radius: 50%; }
        .red { background: #FF5F56; }
        .yellow { background: #FFBD2E; }
        .green { background: #27C93F; }

        #log-output {
            color: #B2FF59;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.5;
            white-space: pre-wrap;
        }

        .footer {
            margin-top: 20px;
            text-align: center;
            font-size: 12px;
            color: rgba(0,0,0,0.3);
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div class="card">
        <input type="text" id="token" class="input-field" placeholder="Enter access token">
        
        <button class="btn" id="startBtn" onclick="execute()">BAN PLAYER</button>

        <div class="terminal">
            <div class="dots">
                <div class="dot red"></div>
                <div class="dot yellow"></div>
                <div class="dot green"></div>
            </div>
            <pre id="log-output">Ready for input ...</pre>
        </div>
        
        <div class="footer">CKRPRO DEVELOPER</div>
    </div>

    <script>
        function execute() {
            const tk = $('#token').val();
            if(!tk) return;

            $('#startBtn').prop('disabled', true).text('LOADING...');
            
            $.post('/start', {token: tk}, function() {
                setInterval(fetchLogs, 1000);
            });
        }

        function fetchLogs() {
            $.get('/get_logs', function(data) {
                $('#log-output').text(data);
                const term = document.querySelector(".terminal");
                term.scrollTop = term.scrollHeight;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(UI_DESIGN)

@app.route('/start', methods=['POST'])
def start():
    token = request.form.get('token')
    threading.Thread(target=run_ckr_script, args=(token,)).start()
    return jsonify({"status": "started"})

@app.route('/get_logs')
def get_logs():
    if not os.path.exists(LOG_FILE): return "Ready for input ..."
    with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
