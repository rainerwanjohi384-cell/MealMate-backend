# Environment Setup Guide

This document describes all environment variables needed for the MealMate application.

## Backend (.env)

Create a `.env` file in the backend root directory:

```bash
# JWT Configuration
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sqlite:///./mealmate.db
# For production, use PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/mealmate

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://your-frontend-domain.github.io

# Firebase Admin SDK (Optional - for server-side Firebase token verification)
FIREBASE_SERVICE_ACCOUNT_KEY_PATH=path/to/serviceAccountKey.json
```

### How to Get Values:

1. **SECRET_KEY**: Generate a secure random string
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **DATABASE_URL**: 
   - Development: `sqlite:///./mealmate.db` (already set)
   - Production: Get from Render, Railway, or your hosting provider

3. **ALLOWED_ORIGINS**: 
   - Add your frontend URL once deployed
   - Example: `https://rainerwanjohi384-cell.github.io`

4. **Firebase Service Account** (Optional):
   - Go to Firebase Console > Project Settings > Service Accounts
   - Click "Generate New Private Key"
   - Download JSON file and save it securely

---

## Frontend (.env)

Create a `.env` file in the frontend root directory:

```bash
# Backend API URL
VITE_API_URL=http://localhost:8000
# For production:
# VITE_API_URL=https://your-backend-url.onrender.com

# Firebase Configuration
VITE_FIREBASE_API_KEY=your-firebase-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
VITE_FIREBASE_MEASUREMENT_ID=G-XXXXXXXXXX

# Cloudinary Configuration (for image uploads)
VITE_CLOUDINARY_NAME=your-cloudinary-cloud-name
```

### How to Get Values:

1. **Firebase Configuration**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Select your project (or create new one)
   - Go to Project Settings > General
   - Scroll to "Your apps" section
   - Click on web app icon (`</>`) or select existing web app
   - Copy the `firebaseConfig` values

2. **Cloudinary** (for recipe image uploads):
   - Go to [Cloudinary](https://cloudinary.com/)
   - Sign up for free account
   - Go to Dashboard
   - Copy your "Cloud Name"
   - Create upload preset:
     - Settings > Upload > Upload presets
     - Click "Add upload preset"
     - Set name to "dailydish"
     - Set signing mode to "Unsigned"
     - Save

---

## GitHub Secrets (for CI/CD)

### Frontend Repository Secrets

Go to your GitHub repository > Settings > Secrets and variables > Actions > New repository secret

Add the following secrets:

```
VITE_API_URL=https://your-backend-url.onrender.com
VITE_FIREBASE_API_KEY=your-firebase-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
VITE_FIREBASE_MEASUREMENT_ID=G-XXXXXXXXXX
VITE_CLOUDINARY_NAME=your-cloudinary-cloud-name
```

### Backend Repository Secrets (if using GitHub Actions for deployment)

```
SECRET_KEY=your-super-secret-jwt-key
DATABASE_URL=postgresql://user:password@host/database
```

---

## Quick Setup Commands

### Backend Setup
```bash
cd MealMate-backend
cp .env.example .env
# Edit .env with your values
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd MealMate-frontend
touch .env
# Add your environment variables to .env
npm install
npm run dev
```

---

## Firebase Setup Steps

1. **Create Firebase Project**:
   - Visit [Firebase Console](https://console.firebase.google.com/)
   - Click "Add project"
   - Enter project name: "MealMate"
   - Enable Google Analytics (optional)

2. **Enable Authentication**:
   - Go to Authentication > Sign-in method
   - Enable "Google" provider
   - Add authorized domains (your GitHub Pages URL)

3. **Create Web App**:
   - Project Settings > Your apps
   - Click web icon (`</>`)
   - Register app: "MealMate Web"
   - Copy config to frontend `.env`

4. **Update CORS for Firebase**:
   - Add your GitHub Pages URL to authorized domains
   - Authentication > Settings > Authorized domains

---

## Production Deployment Checklist

### Backend (Render/Railway)
- [ ] Set all environment variables in hosting platform
- [ ] Change `SECRET_KEY` to production value
- [ ] Update `DATABASE_URL` to PostgreSQL
- [ ] Add frontend URL to `ALLOWED_ORIGINS`
- [ ] Enable HTTPS

### Frontend (GitHub Pages)
- [ ] Add all secrets to GitHub repository
- [ ] Update `VITE_API_URL` to backend production URL
- [ ] Enable GitHub Pages in repository settings
- [ ] Add custom domain (optional)
- [ ] Add domain to Firebase authorized domains

---

## Security Notes

⚠️ **IMPORTANT**:
- Never commit `.env` files to Git
- Use different `SECRET_KEY` values for dev/prod
- Rotate secrets regularly
- Use HTTPS in production
- Keep Firebase service account keys secure
- Don't expose API keys in client-side code (except Firebase - it's designed for client use)

---

## Troubleshooting

### CORS Errors
- Check `ALLOWED_ORIGINS` includes your frontend URL
- Ensure no trailing slashes in URLs

### Firebase Authentication Fails
- Verify all Firebase env variables are correct
- Check authorized domains in Firebase Console
- Clear browser cache and cookies

### API Connection Issues
- Verify `VITE_API_URL` points to correct backend
- Check backend is running and accessible
- Inspect network tab in browser DevTools

---

## Example Values (Development)

`.env` files with example values for local development:

**Backend `.env`**:
```
SECRET_KEY=dev-secret-key-change-in-production-use-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./mealmate.db
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Frontend `.env`**:
```
VITE_API_URL=http://localhost:8000
VITE_FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
VITE_FIREBASE_AUTH_DOMAIN=mealmate-xxxxx.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=mealmate-xxxxx
VITE_FIREBASE_STORAGE_BUCKET=mealmate-xxxxx.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789012
VITE_FIREBASE_APP_ID=1:123456789012:web:abcdef123456
VITE_FIREBASE_MEASUREMENT_ID=G-XXXXXXXXXX
VITE_CLOUDINARY_NAME=your-cloud-name
```
