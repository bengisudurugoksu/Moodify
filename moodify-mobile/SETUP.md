# Moodify Mobile App - Setup & Quick Start Guide

## 🚀 Quick Start (5 minutes)

### Prerequisites
- **Node.js** v14 or higher
- **npm** or **yarn**
- **Expo CLI**: Install globally with `npm install -g expo-cli`

### Installation Steps

1. **Navigate to the mobile app directory**:
   ```bash
   cd /path/to/moodify-mobile
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Choose your platform**:
   - Press `i` for iOS Simulator (macOS only)
   - Press `a` for Android Emulator
   - Press `w` for Web Browser
   - Scan QR code with **Expo Go** app on your phone (available on App Store & Google Play)

## 📱 App Overview

### Screen 1: Landing Screen
A welcoming intro screen with:
- Soft purple gradient background
- Music note icon
- "How are you feeling today?" message
- "Start" button that navigates to chat

**Design highlights**:
- Smooth fade-in animations
- Calming color scheme (#FAF7FF to #F0E6FF)
- Responsive button with gradient

### Screen 2: Chat Screen
A ChatGPT-style chat interface with:
- Message bubbles (user: purple on right, bot: white on left)
- Real-time message input
- Playlist recommendations displayed as beautiful cards
- Smooth scroll-to-bottom animation
- Loading state with animated dots

**Features**:
- Back button to return to landing
- Disabled input while loading
- Auto-scroll to latest message
- Responsive design for all screen sizes

## 🎨 Design System

### Colors (Purple Theme)
```
Primary Purple:      #9D4EDD
Dark Purple:         #4A0080 & #6A2C91
Light Purple:        #F0E6FF & #C4A7E7
Background:          #FAF7FF
White:               #FFFFFF
```

### Typography
- **Bold**: Font weight 700
- **Semibold**: Font weight 600
- **Regular**: Font weight 400 (default)

### Spacing & Components
- Rounded corners: 16px to 50px
- Shadows: Soft shadows with purple tint
- Message bubbles: 20px border radius, 4px bottom corner
- Buttons: 50px border radius (pill-shaped)

## 🔌 API Integration

The app connects to your backend at: `http://localhost:3000`

### Endpoint: POST `/generate-response`

**Request:**
```json
{
  "emotion": "I'm feeling happy and energized"
}
```

**Expected Response:**
```json
{
  "emotion": "I'm feeling happy and energized",
  "message": "That's wonderful! Here's a playlist that captures that energy...",
  "playlists": [
    {
      "name": "Happy Hits",
      "url": "https://open.spotify.com/playlist/...",
      "image": "https://mosaic.scdn.co/..."
    }
  ]
}
```

### Configuring API URL

Edit `/utils/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:3000'; // Change this
```

For production:
```javascript
const API_BASE_URL = 'https://your-api.com';
```

## 📁 Project Structure

```
moodify-mobile/
├── App.js                           # Main app entry & navigation logic
├── app.json                         # Expo configuration
├── package.json                     # Dependencies & scripts
├── .babelrc                         # Babel configuration
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
│
├── screens/
│   ├── LandingScreen.js            # Welcome/intro screen
│   └── ChatScreen.js               # Main chat interface
│
├── components/
│   ├── MessageBubble.js            # Chat message bubbles (user & bot)
│   └── PlaylistCard.js             # Spotify playlist display card
│
├── utils/
│   └── api.js                      # Backend API communication
│
├── assets/                          # App assets
│   └── fonts/                       # Custom fonts (optional)
│
├── README.md                        # Detailed documentation
└── SETUP.md                         # This file
```

## 🎯 Component Details

### MessageBubble Component
- Animates in with scale + fade effect
- User messages: Purple gradient, right-aligned
- Bot messages: White with border, left-aligned
- Custom border radius for natural look

### PlaylistCard Component
- Displays playlist image, name, and link
- Opens Spotify link when tapped
- Animated entrance with slide effect
- "Listen on Spotify" button with gradient

### ChatScreen Features
- Auto-scrolls to latest message
- Loading state with animated dots
- Handles API errors gracefully
- Input field disables during loading
- Clears input after sending

## 🛠️ Development Tips

### Testing Locally

1. **Start the backend first**:
   ```bash
   cd backend
   npm start
   ```
   Ensure it's running on `http://localhost:3000`

2. **In another terminal, start the mobile app**:
   ```bash
   cd moodify-mobile
   npm start
   ```

3. **Test API connection** - Try sending a message and check:
   - Network tab in Expo DevTools (press `j` in terminal)
   - Console logs for errors
   - Backend logs for requests

### Debugging

Press `j` in the Expo terminal to open React Native Debugger:
- View console logs
- Inspect network requests
- Check component state

### Hot Reloading
Changes to files automatically reload:
- Press `r` to reload
- Press `s` to sign/build QR code
- Press `q` to quit

## 📦 Dependencies

Essential packages:
- **expo**: Framework & tools
- **react-native**: Mobile framework
- **expo-linear-gradient**: Purple gradient backgrounds
- **expo-splash-screen**: Splash screen management

These are already in `package.json`.

## ⚠️ Troubleshooting

### "Cannot connect to backend"
```
✗ Problem: API error when sending message
✓ Solution: 
  1. Ensure backend is running: cd backend && npm start
  2. Check API_BASE_URL in utils/api.js
  3. On Android emulator, use 10.0.2.2 instead of localhost
```

### "Expo start fails"
```bash
npm cache clean --force
rm -rf node_modules
npm install
npm start
```

### "Module not found error"
```bash
# Clear Expo cache
npx expo start --clear

# Or reinstall
npm install
```

### Font loading issues
The app uses system fonts by default. Custom fonts are optional and go in `assets/fonts/`.

## 🚀 Deployment

### iOS (requires Apple Developer account)
```bash
npm run ios  # Builds and runs on simulator
eas build --platform ios  # Production build
```

### Android (requires Android Studio)
```bash
npm run android  # Builds and runs on emulator
eas build --platform android  # Production build
```

### Web
```bash
npm run web  # Runs in browser
```

## 📝 Notes

- App is **portrait-only** by design
- No user authentication required for MVP
- Backend must be running for full functionality
- Smooth animations enhance UX without being distracting
- All colors are carefully chosen for emotional warmth

## 🎨 Customization

### Change Primary Color
Update all occurrences of `#9D4EDD` to your color in:
- `screens/LandingScreen.js`
- `screens/ChatScreen.js`
- `components/MessageBubble.js`
- `components/PlaylistCard.js`

### Adjust Animation Speed
All animations use duration values (ms) like:
```javascript
duration: 800  // Change this number
```

### Add Voice Input
Uncomment and implement voice recording using `expo-av` and `expo-speech` (already structured for this).

---

**Happy coding! 🎵 Build amazing emotional experiences with Moodify.**
