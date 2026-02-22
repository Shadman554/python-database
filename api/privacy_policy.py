from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

PRIVACY_POLICY_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - VET DICT+</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.7;
            color: #1e293b;
            background: #f8fafc;
            padding: 20px;
        }
        .container { max-width: 800px; margin: 0 auto; }
        .header {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            padding: 32px 24px;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 24px;
        }
        .header h1 { font-size: 24px; margin-bottom: 4px; }
        .header .app-name { font-size: 14px; opacity: 0.85; margin-bottom: 12px; }
        .header .dates {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }
        .header .date-chip {
            background: rgba(255,255,255,0.2);
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 12px;
        }
        .section {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        .section h2 {
            font-size: 18px;
            color: #1e293b;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }
        .section p, .section ul { margin-bottom: 12px; color: #475569; font-size: 15px; }
        .section ul { padding-left: 24px; }
        .section li { margin-bottom: 6px; }
        .section h3 { font-size: 16px; color: #334155; margin: 16px 0 8px; }
        .contact-box {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 10px;
            padding: 16px;
            margin-top: 8px;
        }
        .contact-box a { color: #2563eb; text-decoration: none; }
        .contact-box a:hover { text-decoration: underline; }
        .footer {
            text-align: center;
            padding: 24px;
            color: #94a3b8;
            font-size: 13px;
        }
    </style>
</head>
<body>
<div class="container">

    <div class="header">
        <h1>Privacy Policy</h1>
        <div class="app-name">VET DICT+ &mdash; com.shada.vetdictplus</div>
        <div class="dates">
            <span class="date-chip">Effective: February 22, 2025</span>
            <span class="date-chip">Last Updated: February 22, 2025</span>
        </div>
    </div>

    <div class="section">
        <h2>1. Introduction</h2>
        <p>Welcome to VET DICT+ ("we", "us", or "our"). This Privacy Policy explains how we collect, use, and protect your information when you use the VET DICT+ mobile application ("App"). The App is an educational veterinary dictionary designed for veterinary students and professionals.</p>
        <p>By using the App, you agree to the collection and use of information in accordance with this policy.</p>
    </div>

    <div class="section">
        <h2>2. Information We Collect</h2>

        <h3>2.1 Account Information</h3>
        <p>When you create an account or sign in, we collect:</p>
        <ul>
            <li>Name</li>
            <li>Email address</li>
            <li>Password (stored securely in hashed form)</li>
        </ul>
        <p>If you sign in via Google Sign-In, we receive your name, email, and profile information from Google. We do not receive or store your Google password.</p>

        <h3>2.2 Locally Stored Data</h3>
        <p>The App stores the following data on your device:</p>
        <ul>
            <li>Favorites and browsing history</li>
            <li>Cached content for offline use</li>
            <li>App preferences (language, theme, font size)</li>
            <li>Authentication tokens (encrypted via platform secure storage)</li>
        </ul>

        <h3>2.3 Push Notification Data</h3>
        <p>We use OneSignal to deliver push notifications. OneSignal may collect:</p>
        <ul>
            <li>Device type and operating system</li>
            <li>A unique device identifier for notification delivery</li>
            <li>Notification interaction data</li>
        </ul>

        <h3>2.4 Information We Do NOT Collect</h3>
        <ul>
            <li>We do not collect location data</li>
            <li>We do not access your camera, contacts, or phone calls</li>
            <li>We do not collect financial or payment information</li>
            <li>We do not use advertising or ad tracking</li>
        </ul>
    </div>

    <div class="section">
        <h2>3. How We Use Your Information</h2>
        <p>We use the collected information to:</p>
        <ul>
            <li>Provide and maintain the App's features and functionality</li>
            <li>Authenticate your identity and manage your account</li>
            <li>Send push notifications about new content</li>
            <li>Cache content for offline access and improve performance</li>
            <li>Save your preferences (language, theme, font size, favorites, history)</li>
            <li>Improve the App</li>
        </ul>
    </div>

    <div class="section">
        <h2>4. Third-Party Services</h2>
        <p>The App uses the following third-party services:</p>
        <ul>
            <li><strong>Google Sign-In</strong> &mdash; for user authentication</li>
            <li><strong>Firebase (Google)</strong> &mdash; for backend infrastructure</li>
            <li><strong>OneSignal</strong> &mdash; for push notifications</li>
            <li><strong>Railway</strong> &mdash; for API hosting</li>
        </ul>
        <p>Each of these services has its own privacy policy. We encourage you to review them.</p>
    </div>

    <div class="section">
        <h2>5. Data Storage &amp; Security</h2>
        <ul>
            <li>Authentication tokens are stored using Flutter Secure Storage, which uses Android Keystore and iOS Keychain for encryption</li>
            <li>Locally cached data is encrypted by the platform's built-in encryption and is not accessible by other apps</li>
            <li>All server communications are encrypted via HTTPS</li>
            <li>Passwords are hashed and never stored in plain text</li>
        </ul>
    </div>

    <div class="section">
        <h2>6. Data Retention</h2>
        <ul>
            <li>Account data is retained as long as your account is active</li>
            <li>Locally cached data remains on your device until you clear the App's data or uninstall the App</li>
            <li>Push notification tokens are retained by OneSignal as long as the App is installed</li>
        </ul>
    </div>

    <div class="section">
        <h2>7. Your Rights</h2>
        <p>You have the right to:</p>
        <ul>
            <li>Access the personal information stored in your account</li>
            <li>Update your account information via the Profile page</li>
            <li>Delete your account and associated data by contacting us</li>
            <li>Opt out of push notifications via your device settings</li>
            <li>Delete locally stored data by clearing the App's storage in your device settings</li>
        </ul>
    </div>

    <div class="section">
        <h2>8. Children's Privacy</h2>
        <p>The App is an educational tool for veterinary students and professionals. We do not knowingly collect personal information from children under 13. If you believe a child under 13 has provided us with personal information, please contact us so we can delete it.</p>
    </div>

    <div class="section">
        <h2>9. Changes to This Policy</h2>
        <p>We may update this Privacy Policy from time to time. We will notify you of any changes by updating the "Last Updated" date at the top of this policy. We recommend reviewing this policy periodically.</p>
    </div>

    <div class="section">
        <h2>10. Contact Us</h2>
        <p>If you have any questions or concerns about this Privacy Policy, please contact us:</p>
        <div class="contact-box">
            <p><strong>Email:</strong> <a href="mailto:shadmanothman59@gmail.com">shadmanothman59@gmail.com</a></p>
            <p><strong>Google Play:</strong> <a href="https://play.google.com/store/apps/details?id=com.shada.vetdictplus" target="_blank">VET DICT+ on Google Play</a></p>
            <p><strong>App Store:</strong> <a href="https://apps.apple.com/us/app/vet-dict/id6680200091" target="_blank">VET DICT+ on App Store</a></p>
        </div>
    </div>

    <div class="footer">
        &copy; 2025 VET DICT+. All rights reserved.
    </div>

</div>
</body>
</html>"""

@router.get("/", response_class=HTMLResponse)
async def get_privacy_policy():
    """Serve the privacy policy as an HTML page"""
    return HTMLResponse(content=PRIVACY_POLICY_HTML)
