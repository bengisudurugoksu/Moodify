# ⚡ Moodify Mobile - Quick Reference Card

## 🚀 Get Started in 30 Seconds

```bash
cd moodify-mobile
npm install
npm start
# Press 'a' for Android, 'i' for iOS, or scan QR code
```

---

## 📂 Key Files at a Glance

| File | Purpose |
|------|---------|
| `App.js` | Main app entry, screen navigation |
| `screens/LandingScreen.js` | Welcome screen |
| `screens/ChatScreen.js` | Chat interface |
| `components/MessageBubble.js` | Message display |
| `components/PlaylistCard.js` | Playlist UI |
| `utils/api.js` | Backend communication |
| `config.js` | Configuration (API URL, colors, etc.) |

---

## 🎨 Key Colors

```
Primary:    #9D4EDD (Buttons, user messages)
Dark:       #4A0080 (Headings)
Accent:     #6A2C91 (Secondary text)
Light:      #F0E6FF (Backgrounds)
Background: #FAF7FF (Screen fill)
White:      #FFFFFF (Cards, messages)
```

---

## 🔧 Configuration

**Change API URL:**
Edit `config.js`:
```javascript
API: {
  BASE_URL: 'http://localhost:3000',  // Change this
}
```

**For Android Emulator:**
```javascript
BASE_URL: 'http://10.0.2.2:3000',
```

---

## 📱 Component Props

### MessageBubble
```javascript
<MessageBubble 
  type="user" // or "bot"
  text="Message content"
/>
```

### PlaylistCard
```javascript
<PlaylistCard 
  playlist={{
    name: "Playlist Name",
    url: "spotify-url",
    image: "image-url"
  }}
/>
```

---

## 🎭 Key Features

| Feature | Location |
|---------|----------|
| Landing screen | `screens/LandingScreen.js` |
| Chat interface | `screens/ChatScreen.js` |
| Message bubbles | `components/MessageBubble.js` |
| Playlist cards | `components/PlaylistCard.js` |
| API calls | `utils/api.js` |
| Settings | `config.js` |

---

## 🔴 Troubleshooting

```
No API connection?
→ Check backend runs on http://localhost:3000
→ Verify API_BASE_URL in config.js
→ Android emulator? Use 10.0.2.2 not localhost

App won't start?
→ npm cache clean --force
→ rm -rf node_modules && npm install
→ npm start --clear

Messages not scrolling?
→ Check ScrollView in ChatScreen.js
→ Verify messagesContent styling

Animations jittery?
→ Ensure useNativeDriver: true
→ Test on physical device
→ Check for expensive operations
```

---

## 📝 Common Edits

### Change Button Text
File: `screens/LandingScreen.js` (line ~95)
```javascript
<Text style={styles.buttonText}>Start</Text>  // Change this
```

### Change Welcome Message
File: `screens/ChatScreen.js` (line ~17)
```javascript
text: "Hi there! I'm Moodify..."  // Change this
```

### Change Colors
File: `config.js` (line ~34)
```javascript
PRIMARY_PURPLE: '#9D4EDD',  // Change all colors here
```

### Change API Endpoint
File: `config.js` (line ~5)
```javascript
BASE_URL: 'https://api.example.com',  // Production
```

---

## ✅ Before Deploying

- [ ] API URL updated in `config.js`
- [ ] DEBUG set to `false` in `config.js`
- [ ] App icons added to `assets/`
- [ ] Tested on physical device
- [ ] No console errors
- [ ] Animations smooth (60fps)
- [ ] All strings updated (app name, messages)

---

## 📱 Screen Breakdown

### Landing Screen
- Location: `screens/LandingScreen.js`
- Components: Icon, title, description, button
- Animation: Fade-in on load
- Action: Navigate to chat

### Chat Screen
- Location: `screens/ChatScreen.js`
- Components: Header, messages, input, playlist
- Features: Auto-scroll, loading state, error handling
- Actions: Send message, open playlist, go back

---

## 🎬 Animation Speeds

```javascript
FAST:    300ms   // Button press
NORMAL:  400-500ms  // Message entrance
SLOW:    800ms   // Page transitions
```

---

## 🌐 API Integration

**Endpoint**: `POST /generate-response`

**Request:**
```json
{
  "emotion": "I'm feeling happy"
}
```

**Response:**
```json
{
  "emotion": "I'm feeling happy",
  "message": "That's wonderful!...",
  "playlists": [{
    "name": "Happy Hits",
    "url": "spotify-url",
    "image": "image-url"
  }]
}
```

---

## 🛠️ Debug Shortcuts

| Action | Command |
|--------|---------|
| Clear app cache | Press `c` in Expo terminal |
| Reload app | Press `r` |
| Open DevTools | Press `j` |
| View QR code | Press `s` |
| Quit Expo | Press `q` |
| Reload native module | Press `shift + r` |

---

## 💻 Development Commands

```bash
# Start app
npm start

# For iOS
npm start -- --ios

# For Android
npm start -- --android

# For Web
npm run web

# Clear cache and start fresh
npm start -- --clear
```

---

## 📦 Dependencies

- `expo` - Framework
- `react-native` - Mobile framework
- `expo-linear-gradient` - Gradients
- `expo-splash-screen` - Splash screen

All already in `package.json` ✅

---

## 📖 Documentation Map

| Doc | Read Time | For |
|-----|-----------|-----|
| `PROJECT_SUMMARY.md` | 5 min | Overview |
| `SETUP.md` | 10 min | Getting started |
| `README.md` | 15 min | Features & setup |
| `ARCHITECTURE.md` | 15 min | Technical design |
| `DESIGN.md` | 15 min | Visual system |
| `DEPLOYMENT.md` | 20 min | Launch checklist |

---

## 🎯 What to Customize

### Easy (5 min)
- [ ] Button text
- [ ] Welcome messages
- [ ] Colors
- [ ] API URL

### Medium (30 min)
- [ ] App icons
- [ ] Greeting message
- [ ] Animation speeds
- [ ] Button styling

### Hard (hours)
- [ ] Add voice input
- [ ] Message persistence
- [ ] User authentication
- [ ] New screens

---

## 🚀 Deployment Checklist

```
Pre-Launch:
☐ npm install completes
☐ npm start works (no errors)
☐ Can send message and get response
☐ Playlist card displays and links work
☐ Animations are smooth
☐ No console errors

Config:
☐ API URL set correctly
☐ DEBUG = false in config.js
☐ App version updated
☐ App icons added

Testing:
☐ Works on iOS simulator
☐ Works on Android emulator
☐ Works on physical phone
☐ Works offline gracefully
☐ Tested with slow network

Final:
☐ Documentation updated
☐ Code commented where needed
☐ Git repository initialized
☐ README has setup instructions
```

---

## 🎨 Design System Quick Ref

**Button**: `height: 44px, borderRadius: 50px, gradient: #9D4EDD → #7B2CBF`

**Message Bubble**: `maxWidth: 85%, padding: 12-16px, borderRadius: 20px`

**Input**: `height: 48px, borderRadius: 50px, padding: 16px`

**Shadows**: `color: #9D4EDD, opacity: 0.1-0.3, radius: 8-16px`

---

## 💡 Pro Tips

1. **Always use `useNativeDriver: true`** on animations
2. **Test on real device** - simulator can hide issues
3. **Check network tab** in DevTools for API calls
4. **Compress images** for playlists
5. **Use console.log wisely** - turn off in production
6. **Comment complex logic** - help future you
7. **Commit often** - small, focused commits
8. **Use descriptive names** - for variables and functions

---

## 📞 Quick Help

**Can't connect to backend?**
1. Backend running? Check `http://localhost:3000`
2. API URL correct? Check `config.js`
3. Android emulator? Use `10.0.2.2` not `localhost`

**App won't start?**
1. `npm cache clean --force`
2. `npm install`
3. `npm start --clear`

**Animations not smooth?**
1. Check `useNativeDriver: true`
2. Test on physical device
3. Profile with DevTools

**Messages not appearing?**
1. Check backend response
2. Verify API call in DevTools network tab
3. Look at console for errors

---

## 🎓 Next Learning Steps

- [ ] Read ARCHITECTURE.md
- [ ] Explore component structure
- [ ] Try customizing colors
- [ ] Add console.logs to trace flow
- [ ] Try modifying animations
- [ ] Experiment with layout changes
- [ ] Add new messages
- [ ] Deploy to simulator

---

**⚡ Everything you need. Code well. Build fast. Launch soon.** 🚀💜
