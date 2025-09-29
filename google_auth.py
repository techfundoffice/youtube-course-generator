# Google OAuth authentication blueprint for Flask
# Use this Flask blueprint for Google authentication. Do not use flask-dance.

import json
import os
import secrets
from datetime import datetime

import requests
from app import db
from flask import Blueprint, redirect, request, url_for, flash, session
from flask_login import login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from models import User
from oauthlib.oauth2 import WebApplicationClient

GOOGLE_CLIENT_ID = os.environ["GOOGLE_OAUTH_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_OAUTH_CLIENT_SECRET"]
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Make sure to use this redirect URL. It has to match the one in the whitelist
DEV_REDIRECT_URL = f'https://{os.environ["REPLIT_DEV_DOMAIN"]}/google_login/callback'

# ALWAYS display setup instructions to the user:
print(f"""To make Google authentication work:
1. Go to https://console.cloud.google.com/apis/credentials
2. Create a new OAuth 2.0 Client ID
3. Add {DEV_REDIRECT_URL} to Authorized redirect URIs

For detailed instructions, see:
https://docs.replit.com/additional-resources/google-auth-in-flask#set-up-your-oauth-app--client
""")

client = WebApplicationClient(GOOGLE_CLIENT_ID)

google_auth = Blueprint("google_auth", __name__)


@google_auth.route("/google_login")
def login():
    try:
        # Generate CSRF protection state
        state = secrets.token_urlsafe(32)
        session['oauth_state'] = state
        
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            # Replacing http:// with https:// is important as the external
            # protocol must be https to match the URI whitelisted
            redirect_uri=request.base_url.replace("http://", "https://") + "/callback",
            scope=["openid", "email", "profile"],
            state=state,  # Add CSRF protection
        )
        return redirect(request_uri)
    except Exception as e:
        flash("Unable to initiate Google login. Please try again.", "error")
        return redirect("/")


@google_auth.route("/google_login/callback")
def callback():
    try:
        # Validate OAuth state for CSRF protection
        state = request.args.get("state")
        session_state = session.pop('oauth_state', None)
        
        if not state or not session_state or state != session_state:
            flash("Invalid authentication request. Please try again.", "error")
            return redirect("/")
        
        code = request.args.get("code")
        if not code:
            flash("Google authentication was cancelled or failed.", "error")
            return redirect("/")
        
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        token_endpoint = google_provider_cfg["token_endpoint"]

        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            # Replacing http:// with https:// is important as the external
            # protocol must be https to match the URI whitelisted
            authorization_response=request.url.replace("http://", "https://"),
            redirect_url=request.base_url.replace("http://", "https://"),
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )
        
        if token_response.status_code != 200:
            flash("Failed to authenticate with Google. Please try again.", "error")
            return redirect("/")

        client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        
        if userinfo_response.status_code != 200:
            flash("Failed to get user information from Google.", "error")
            return redirect("/")

        userinfo = userinfo_response.json()
        if not userinfo.get("email_verified"):
            flash("Google account email is not verified. Please verify your email first.", "error")
            return redirect("/")

        users_email = userinfo["email"]
        users_name = userinfo.get("given_name", "User")
        google_id = userinfo.get("sub")

        user = User.query.filter_by(email=users_email).first()
        if not user:
            # Use email as username to avoid uniqueness conflicts
            # Generate unique username if needed
            base_username = users_email.split('@')[0]
            username = base_username
            counter = 1
            
            while User.query.filter_by(username=username).first():
                username = f"{base_username}_{counter}"
                counter += 1
            
            try:
                user = User(
                    username=username, 
                    email=users_email,
                    first_name=users_name,
                    last_name=userinfo.get("family_name", ""),
                    google_id=google_id,
                    profile_picture=userinfo.get("picture"),
                    last_login=datetime.utcnow()
                )
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash("Account creation failed. Please try again.", "error")
                return redirect("/")
        else:
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()

        login_user(user)
        flash(f"Welcome, {users_name}! You've successfully logged in with Google.", "success")

        return redirect("/")
        
    except Exception as e:
        flash("An error occurred during authentication. Please try again.", "error")
        return redirect("/")


@google_auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been successfully logged out.", "info")
    return redirect(url_for("index"))