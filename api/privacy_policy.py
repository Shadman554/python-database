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
            background: linear-gradient(135deg, #1A3460, #2563eb);
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
        .highlight-box {
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 12px 16px;
            margin: 12px 0;
            border-radius: 6px;
        }
    </style>
</head>
<body>
<div class="container">

    <div class="header">
        <h1>Privacy Policy</h1>
        <div class="app-name">VET DICT+ &mdash; com.shaduman.vetdictplus</div>
        <div class="dates">
            <span class="date-chip">Effective: March 14, 2026</span>
            <span class="date-chip">Last Updated: March 14, 2026</span>
        </div>
    </div>

    <div class="section">
        <h2>1. Introduction</h2>
        <p>Welcome to VET DICT+ ("we", "us", or "our"). This Privacy Policy explains how we collect, use, store, and protect your information when you use the VET DICT+ mobile application ("App"). The App is an educational veterinary dictionary and reference tool designed for veterinary students and professionals.</p>
        <p>By using the App, you agree to the collection and use of information in accordance with this policy. If you do not agree with this policy, please do not use the App.</p>
    </div>

    <div class="section">
        <h2>2. Information We Collect</h2>

        <h3>2.1 Account Information (Optional)</h3>
        <p>When you create an account or sign in, we collect:</p>
        <ul>
            <li><strong>Name:</strong> Your display name</li>
            <li><strong>Username:</strong> A unique identifier for your account</li>
            <li><strong>Email address:</strong> For account recovery and communication</li>
            <li><strong>Password:</strong> Stored securely in hashed form (we never store plain-text passwords)</li>
            <li><strong>Profile photo URL:</strong> If you choose to add one or sign in with Google</li>
        </ul>
        
        <h3>2.2 Google Sign-In Data</h3>
        <p>If you sign in via Google Sign-In, we receive:</p>
        <ul>
            <li>Your name and email address from your Google account</li>
            <li>Your Google profile photo (if available)</li>
            <li>A unique Google ID for authentication</li>
            <li>Google authentication tokens (used only for verifying your identity)</li>
        </ul>
        <div class="highlight-box">
            <strong>Important:</strong> We do not receive or store your Google password. Google handles all password authentication.
        </div>

        <h3>2.3 Locally Stored Data (On Your Device)</h3>
        <p>The App stores the following data locally on your device using SharedPreferences and secure storage:</p>
        <ul>
            <li><strong>Favorites:</strong> Drugs, diseases, and terminology items you mark as favorites</li>
            <li><strong>Browsing History:</strong> Recently viewed items (drugs, diseases, terminology, notes, etc.)</li>
            <li><strong>Cached Content:</strong> Veterinary dictionary data, drugs, diseases, terminology, books, notes, instruments, normal ranges, and test information for offline access</li>
            <li><strong>App Preferences:</strong> Language selection (Kurdish/English), theme (light/dark mode), font size settings</li>
            <li><strong>Authentication Tokens:</strong> Access and refresh tokens stored in Flutter Secure Storage (Android Keystore/iOS Keychain)</li>
            <li><strong>User Profile Data:</strong> Non-sensitive user information cached for quick access</li>
            <li><strong>Introduction Status:</strong> Whether you've completed the app introduction</li>
            <li><strong>About Page Cache:</strong> Cached information about the app, team, and supporters</li>
        </ul>

        <h3>2.4 Push Notification Data</h3>
        <p>We use OneSignal (App ID: c680a189-e57c-48b4-9ce8-b28d91dc5c58) to deliver push notifications. OneSignal may collect:</p>
        <ul>
            <li>Device type, model, and operating system version</li>
            <li>A unique device identifier (OneSignal Player ID) for notification delivery</li>
            <li>Notification interaction data (opened, dismissed)</li>
            <li>User tags (e.g., "user_type: registered") for targeted notifications</li>
            <li>External user ID (your user ID or email) if you're signed in</li>
            <li>Timestamp of notification events</li>
        </ul>

        <h3>2.5 API Usage Data</h3>
        <p>When you use the App, we may collect:</p>
        <ul>
            <li>API request logs (for debugging and rate limiting)</li>
            <li>Search queries (to improve search functionality)</li>
            <li>Content synchronization data (when you sync local data to the server)</li>
            <li>App version and platform information</li>
        </ul>

        <h3>2.6 Information We Do NOT Collect</h3>
        <ul>
            <li>We do <strong>not</strong> collect precise location data or GPS coordinates</li>
            <li>We do <strong>not</strong> access your camera, microphone, contacts, or phone calls</li>
            <li>We do <strong>not</strong> collect financial or payment information (the App is free)</li>
            <li>We do <strong>not</strong> use advertising networks or ad tracking</li>
            <li>We do <strong>not</strong> sell your personal information to third parties</li>
            <li>We do <strong>not</strong> track your browsing activity outside the App</li>
        </ul>
    </div>

    <div class="section">
        <h2>3. How We Use Your Information</h2>
        <p>We use the collected information for the following purposes:</p>
        <ul>
            <li><strong>Account Management:</strong> Authenticate your identity, manage your account, and provide personalized features</li>
            <li><strong>Content Delivery:</strong> Provide access to veterinary drugs, diseases, terminology, books, notes, instruments, normal ranges, and test information</li>
            <li><strong>Offline Access:</strong> Cache content locally on your device for offline use</li>
            <li><strong>Personalization:</strong> Save your preferences (language, theme, font size), favorites, and browsing history</li>
            <li><strong>Push Notifications:</strong> Send you notifications about new content, updates, and important announcements</li>
            <li><strong>Search Functionality:</strong> Enable search across all content types (drugs, diseases, terminology, etc.)</li>
            <li><strong>Data Synchronization:</strong> Sync your locally created content (notes, dictionary terms) to the server if you choose</li>
            <li><strong>App Improvement:</strong> Analyze usage patterns to improve the App's performance and features</li>
            <li><strong>Security:</strong> Detect and prevent unauthorized access, fraud, and abuse</li>
            <li><strong>Communication:</strong> Send you important updates about the App or your account</li>
        </ul>
    </div>

    <div class="section">
        <h2>4. Third-Party Services</h2>
        <p>The App integrates with the following third-party services. Each service has its own privacy policy:</p>
        
        <h3>4.1 Google Services</h3>
        <ul>
            <li><strong>Google Sign-In:</strong> For optional user authentication (<a href="https://policies.google.com/privacy" target="_blank">Privacy Policy</a>)</li>
            <li><strong>Google Fonts:</strong> For app typography</li>
        </ul>

        <h3>4.2 OneSignal</h3>
        <ul>
            <li><strong>Purpose:</strong> Push notification delivery and management</li>
            <li><strong>Data Shared:</strong> Device identifiers, user ID (if signed in), notification preferences</li>
            <li><strong>Privacy Policy:</strong> <a href="https://onesignal.com/privacy_policy" target="_blank">OneSignal Privacy Policy</a></li>
        </ul>

        <h3>4.3 Railway</h3>
        <ul>
            <li><strong>Purpose:</strong> Backend API hosting (python-database.up.railway.app)</li>
            <li><strong>Data Shared:</strong> API requests, authentication tokens, user data</li>
            <li><strong>Privacy Policy:</strong> <a href="https://railway.app/legal/privacy" target="_blank">Railway Privacy Policy</a></li>
        </ul>

        <h3>4.4 Flutter/Dart Packages</h3>
        <p>The App uses various open-source Flutter packages for functionality:</p>
        <ul>
            <li><strong>flutter_secure_storage:</strong> Secure token storage (Android Keystore/iOS Keychain)</li>
            <li><strong>shared_preferences:</strong> Local data storage</li>
            <li><strong>cached_network_image:</strong> Image caching for offline access</li>
            <li><strong>http/dio:</strong> Network requests to our API</li>
            <li><strong>sqflite:</strong> Local database for offline content</li>
            <li><strong>url_launcher:</strong> Opening external links</li>
            <li><strong>share_plus:</strong> Sharing app content</li>
            <li><strong>webview_flutter:</strong> Displaying web content (privacy policy, about page)</li>
        </ul>
    </div>

    <div class="section">
        <h2>5. Data Storage &amp; Security</h2>
        
        <h3>5.1 Security Measures</h3>
        <ul>
            <li><strong>Encryption in Transit:</strong> All communications between the App and our servers use HTTPS/TLS encryption</li>
            <li><strong>Encryption at Rest:</strong> Authentication tokens are stored using Flutter Secure Storage with platform-specific encryption (Android Keystore, iOS Keychain)</li>
            <li><strong>Password Security:</strong> Passwords are hashed using industry-standard algorithms and never stored in plain text</li>
            <li><strong>Token-Based Authentication:</strong> We use JWT (JSON Web Tokens) with access and refresh tokens for secure authentication</li>
            <li><strong>Secure API:</strong> Our backend API requires authentication for sensitive operations</li>
            <li><strong>Rate Limiting:</strong> API rate limiting prevents abuse and unauthorized access</li>
        </ul>

        <h3>5.2 Data Storage Locations</h3>
        <ul>
            <li><strong>User Account Data:</strong> Stored on Railway servers (cloud-hosted database)</li>
            <li><strong>Cached Content:</strong> Stored locally on your device using SharedPreferences and SQLite</li>
            <li><strong>Authentication Tokens:</strong> Stored in device secure storage (Android Keystore/iOS Keychain)</li>
            <li><strong>Push Notification Data:</strong> Managed by OneSignal's infrastructure</li>
        </ul>

        <h3>5.3 Data Isolation</h3>
        <p>All locally stored data is sandboxed within the App and cannot be accessed by other apps on your device due to platform security restrictions.</p>
    </div>

    <div class="section">
        <h2>6. Data Retention</h2>
        <ul>
            <li><strong>Account Data:</strong> Retained as long as your account is active. You can delete your account at any time.</li>
            <li><strong>Locally Cached Content:</strong> Remains on your device until you clear the App's data, uninstall the App, or manually clear cache</li>
            <li><strong>Favorites &amp; History:</strong> Stored locally on your device and retained until you clear them or uninstall the App</li>
            <li><strong>Push Notification Tokens:</strong> Retained by OneSignal as long as the App is installed on your device</li>
            <li><strong>API Logs:</strong> Server logs are retained for debugging purposes and automatically deleted after 30 days</li>
            <li><strong>Deleted Accounts:</strong> When you delete your account, all associated server-side data is permanently removed within 30 days</li>
        </ul>
    </div>

    <div class="section">
        <h2>7. Your Rights &amp; Choices</h2>
        
        <h3>7.1 Account Management</h3>
        <ul>
            <li><strong>Access:</strong> View your account information in the Profile page</li>
            <li><strong>Update:</strong> Edit your name, email, and profile photo via the Profile page</li>
            <li><strong>Delete Account:</strong> Permanently delete your account and all associated data through the Profile page or by contacting us</li>
        </ul>

        <h3>7.2 Data Control</h3>
        <ul>
            <li><strong>Clear Favorites:</strong> Remove individual favorites or clear all favorites</li>
            <li><strong>Clear History:</strong> Delete your browsing history at any time</li>
            <li><strong>Clear Cache:</strong> Clear locally cached content via your device settings (Settings → Apps → VET DICT+ → Storage → Clear Cache)</li>
            <li><strong>Clear All Data:</strong> Remove all app data via device settings (Settings → Apps → VET DICT+ → Storage → Clear Data)</li>
        </ul>

        <h3>7.3 Notification Control</h3>
        <ul>
            <li><strong>Disable Push Notifications:</strong> Turn off notifications in your device settings (Settings → Apps → VET DICT+ → Notifications)</li>
            <li><strong>Notification Preferences:</strong> Manage notification types within the App (if available)</li>
        </ul>

        <h3>7.4 Privacy Rights (GDPR/CCPA)</h3>
        <p>If you are located in the European Union, California, or other regions with privacy laws, you have additional rights:</p>
        <ul>
            <li><strong>Right to Access:</strong> Request a copy of your personal data</li>
            <li><strong>Right to Rectification:</strong> Correct inaccurate personal data</li>
            <li><strong>Right to Erasure:</strong> Request deletion of your personal data</li>
            <li><strong>Right to Restrict Processing:</strong> Limit how we use your data</li>
            <li><strong>Right to Data Portability:</strong> Receive your data in a machine-readable format</li>
            <li><strong>Right to Object:</strong> Object to certain data processing activities</li>
            <li><strong>Right to Withdraw Consent:</strong> Withdraw consent for data processing at any time</li>
        </ul>
        <p>To exercise these rights, please contact us at shadmanothman59@gmail.com</p>
    </div>

    <div class="section">
        <h2>8. Children's Privacy</h2>
        <p>VET DICT+ is an educational tool designed for veterinary students and professionals. The App is not intended for children under 13 years of age.</p>
        <p>We do not knowingly collect personal information from children under 13. If you are a parent or guardian and believe your child has provided us with personal information, please contact us immediately at shadmanothman59@gmail.com so we can delete it.</p>
    </div>

    <div class="section">
        <h2>9. International Data Transfers</h2>
        <p>Your information may be transferred to and stored on servers located outside your country of residence. By using the App, you consent to the transfer of your information to countries that may have different data protection laws than your country.</p>
        <p>We take appropriate safeguards to ensure your data is protected in accordance with this Privacy Policy, regardless of where it is processed.</p>
    </div>

    <div class="section">
        <h2>10. Changes to This Privacy Policy</h2>
        <p>We may update this Privacy Policy from time to time to reflect changes in our practices, technology, legal requirements, or other factors.</p>
        <p>When we make changes:</p>
        <ul>
            <li>We will update the "Last Updated" date at the top of this policy</li>
            <li>For significant changes, we may notify you via push notification or email</li>
            <li>Your continued use of the App after changes constitutes acceptance of the updated policy</li>
        </ul>
        <p>We encourage you to review this Privacy Policy periodically to stay informed about how we protect your information.</p>
    </div>

    <div class="section">
        <h2>11. Contact Us</h2>
        <p>If you have any questions, concerns, or requests regarding this Privacy Policy or your personal data, please contact us:</p>
        <div class="contact-box">
            <p><strong>Developer:</strong> Shadman Othman</p>
            <p><strong>Email:</strong> <a href="mailto:shadmanothman59@gmail.com">shadmanothman59@gmail.com</a></p>
            <p><strong>App Package:</strong> com.shaduman.vetdictplus</p>
            <p><strong>Google Play:</strong> <a href="https://play.google.com/store/apps/details?id=com.shaduman.vetdictplus" target="_blank">VET DICT+ on Google Play</a></p>
            <p><strong>App Store:</strong> <a href="https://apps.apple.com/us/app/vet-dict/id6680200091" target="_blank">VET DICT+ on App Store</a></p>
            <p><strong>API Backend:</strong> python-database.up.railway.app</p>
        </div>
        <p style="margin-top: 16px;">We will respond to your inquiry within 30 days.</p>
    </div>

    <div class="footer">
        &copy; 2026 VET DICT+. All rights reserved.<br>
        Version 1.0.0+2 | Last Updated: March 14, 2026
    </div>

</div>
</body>
</html>"""

@router.get("/", response_class=HTMLResponse)
async def get_privacy_policy():
    """Serve the privacy policy as an HTML page"""
    return HTMLResponse(content=PRIVACY_POLICY_HTML)
