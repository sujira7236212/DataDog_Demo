from flask import Flask, jsonify, render_template_string
import time

app = Flask(__name__)

# --- ส่วนของหน้าตาเว็บ (UI) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Datadog AI Demo - Control Panel</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        async function hitApi(endpoint, btnElement) {
            const logBox = document.getElementById('log-box');
            const originalText = btnElement.innerText;
            btnElement.innerText = "Processing...";
            btnElement.disabled = true;

            const startTime = Date.now();
            
            try {
                const response = await fetch(endpoint);
                const timeTaken = Date.now() - startTime;
                
                let logMsg = `[${new Date().toLocaleTimeString()}] GET ${endpoint} - Status: ${response.status} (${timeTaken}ms)\\n`;
                
                if (!response.ok) {
                    logMsg = `<span class="text-red-500">${logMsg} ❌ ERROR Triggered!</span>\\n`;
                } else {
                    if (timeTaken > 2000) {
                        logMsg = `<span class="text-yellow-400">${logMsg} ⚠️ High Latency Detected!</span>\\n`;
                    } else {
                        logMsg = `<span class="text-green-400">${logMsg} ✅ Success</span>\\n`;
                    }
                }
                
                logBox.innerHTML = logMsg + logBox.innerHTML;
            } catch (error) {
                const timeTaken = Date.now() - startTime;
                logBox.innerHTML = `<span class="text-red-500">[${new Date().toLocaleTimeString()}] GET ${endpoint} - ❌ Connection Failed! (${timeTaken}ms)</span>\\n` + logBox.innerHTML;
            } finally {
                btnElement.innerText = originalText;
                btnElement.disabled = false;
            }
        }
    </script>
</head>
<body class="bg-gray-900 text-white font-sans p-10">
    <div class="max-w-3xl mx-auto">
        <h1 class="text-4xl font-bold text-blue-400 mb-2">Datadog AI Demo</h1>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <button onclick="hitApi('/api/normal', this)" class="bg-green-600 hover:bg-green-500 text-white font-bold py-4 px-4 rounded shadow-lg transition duration-200">
                1. Normal
            </button>
            
            <button onclick="hitApi('/api/slow', this)" class="bg-yellow-600 hover:bg-yellow-500 text-white font-bold py-4 px-4 rounded shadow-lg transition duration-200">
                2. Trigger Latency (5s)
            </button>

            <button onclick="hitApi('/api/crash', this)" class="bg-red-600 hover:bg-red-500 text-white font-bold py-4 px-4 rounded shadow-lg transition duration-200">
                3. Trigger Error 500
            </button>
        </div>

        <div class="bg-black p-4 rounded-lg shadow-inner border border-gray-700">
            <h2 class="text-lg font-semibold text-gray-300 border-b border-gray-700 pb-2 mb-2">Live Activity Log</h2>
            <pre id="log-box" class="h-64 overflow-y-auto text-sm text-gray-300 whitespace-pre-wrap font-mono"></pre>
        </div>
    </div>
</body>
</html>
"""

# --- ส่วนของ API Backend ---

# หน้าแรกสำหรับแสดง UI
@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

# 1. เส้นทางปกติ (ไม่มีปัญหา)
@app.route('/api/normal')
def normal():
    return jsonify({"message": "Everything is OK!", "status": "success"})

# 2. จำลองปัญหาแอปพัง (Error 500 Spike)
@app.route('/api/crash')
def crash():
    # แกล้งหารด้วยศูนย์ เพื่อบังคับให้แอปสาด Error ทันที
    return 1 / 0 

# 3. จำลองปัญหาเว็บอืด (High Latency) 
@app.route('/api/slow')
def slow():
    # สั่งให้ระบบหยุดรอ (Sleep) 5 วินาที ก่อนจะตอบกลับ
    time.sleep(5)
    return jsonify({"message": "Sorry for the delay...", "status": "warning"})

if __name__ == '__main__':
    # รันบนพอร์ต 8080
    app.run(host='0.0.0.0', port=8080)