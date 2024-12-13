from flask import Flask, render_template, request, redirect, url_for, session
import pyotp

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a strong secret key for session management

# Predefined password to access the tool
TOOL_PASSWORD = "Welcome@123"  # Replace with your chosen password

# Sample TOTP keys with names
TOTP_KEYS = {
    "VI048": {"name": "Nitin.Parikh.shareindia", "key": "EFGQDGX2PU54OTUNPWFF3IXWZYRPQXUN"},
    "VI034": {"name": "Ashit Vora", "key": "6XUTRP3YCZMW2BJDCLF2Y4JSWSRO3KHP"},
    "VI046": {"name": "anjana.parikh.shareindia", "key": "KXPBI4FFFFTIIVCI4DCVEOQXR374NO2A"},
    "VI051": {"name": "atul.parikh.huf.shareindia", "key": "JK7SB2ZCEDMFSV34JNGYFJNN5SQNQM5Z"},
    "VI049": {"name": "abdhi.shah.shareindia", "key": "RXZNDQJB6X6EELOE5NLFA26KB4BMZAIW"},
    "VI062": {"name": "Prasoon Patel", "key": "UOFBAQPK2IAOGFVIRMKDHRG33RTBXRHR"},
    "VI042": {"name": "ABHAY ANILKUMAR JAIN", "key": "7AOCF632GSVLAOQTS6FSYQTOUCFJXA52"},
}


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if the entered password matches
        entered_password = request.form.get("password")
        if entered_password == TOOL_PASSWORD:
            # Save a session to confirm the user is logged in
            session["logged_in"] = True
            return redirect(url_for("totp_tool"))
        else:
            return '''
                <div style="text-align: center; margin-top: 20%;">
                    <p style="color: red;">Invalid Password. Please try again.</p>
                    <a href="/">Go back</a>
                </div>
            '''

    return '''
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column;">
            <h2>Login to TOTP Tool</h2>
            <form method="POST">
                <input type="password" name="password" placeholder="Enter password" required>
                <button type="submit">Login</button>
            </form>
        </div>
    '''


@app.route("/tool", methods=["GET", "POST"])
def totp_tool():
    # Check if the user is logged in
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    generated_totps = {}  # Store the generated TOTPs

    for client_id, client_info in TOTP_KEYS.items():
        totp = pyotp.TOTP(client_info["key"])
        generated_totps[client_id] = {
            "name": client_info["name"],
            "totp": totp.now(),
        }

    return '''
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column;">
            <h2>TOTP Generator</h2>
            <table border="1" style="border-collapse: collapse; margin-bottom: 20px;">
                <tr>
                    <th style="padding: 10px;">Client ID</th>
                    <th style="padding: 10px;">Name</th>
                    <th style="padding: 10px;">TOTP</th>
                </tr>
                {}
            </table>
            <form method="GET">
                <button type="submit" style="margin-right: 10px;">Refresh</button>
            </form>
            <a href="/" style="text-decoration: none; color: blue;">Logout</a>
        </div>
    '''.format(
        "".join(
            f"<tr><td style='padding: 10px;'>{client_id}</td><td style='padding: 10px;'>{info['name']}</td><td style='padding: 10px;'>{info['totp']}</td></tr>"
            for client_id, info in generated_totps.items()
        )
    )


if __name__ == "__main__":
    app.run(port=5004)