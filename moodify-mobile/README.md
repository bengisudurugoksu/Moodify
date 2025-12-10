# Moodify Mobile App

A beautiful, modern React Native mobile app that provides emotional support through music recommendations. The app uses AI to understand your mood and suggests personalized playlists.

## Features

- 🎵 **Mood-Based Music Recommendations**: Share how you're feeling, and get AI-powered playlist suggestions
- 💬 **ChatGPT-Style Interface**: Intuitive chat-based interaction with empathetic responses
- 🎨 **Beautiful Design**: Modern, soft purple theme with smooth animations
- 🎯 **Simple & Intuitive**: No login required, just start chatting
- 🎧 **Spotify Integration**: Direct links to recommended playlists

## Tech Stack

- **Framework**: React Native with Expo
- **UI**: React Native Components, Linear Gradient, Animated API
- **Styling**: StyleSheet with modern design patterns
- **Backend**: Node.js/Express API (included in this workspace)

## Project Structure

```
moodify-mobile/
├── App.js                    # Main app entry point
├── app.json                  # Expo configuration
├── package.json              # Dependencies
├── .babelrc                  # Babel configuration
├── .env.example              # Environment variables template
├── screens/
│   ├── LandingScreen.js      # Welcome/intro screen
│   └── ChatScreen.js         # Main chat interface
├── components/
│   ├── MessageBubble.js      # Chat message bubbles
│   └── PlaylistCard.js       # Playlist display card
├── utils/
│   └── api.js                # Backend API communication
└── assets/
    └── fonts/                # Custom fonts directory
```

## Installation

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Expo CLI (install globally: `npm install -g expo-cli`)

### Setup Steps

1. **Navigate to the mobile app directory**:
   ```bash
   cd moodify-mobile
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure API URL** (optional):
   - Copy `.env.example` to `.env`
   - Update the API base URL if your backend is running on a different host/port

4. **Start the app**:
   ```bash
   npm start
   ```

   Then choose your platform:
   - Press `i` for iOS simulator
   - Press `a` for Android emulator
   - Scan QR code with Expo Go app on your phone

## How to Use

### Landing Screen
1. Open the app to see a welcoming intro screen
2. Tap the "Start" button to enter the chat

### Chat Screen
1. Type how you're feeling in the input field
2. Send your message
3. Moodify will respond with:
   - An empathetic, personalized message
   - A Spotify playlist recommendation with cover image
4. Continue the conversation or tap the back button to return home

## Configuration

### API Base URL

Update the API URL in `utils/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:3000'; // Change this to your backend URL
```

For production, use your actual server URL (e.g., `https://api.example.com`).

### Custom Styling

All styling is defined in each component's `StyleSheet`. Key colors:
- **Primary Purple**: `#9D4EDD`
- **Dark Purple**: `#4A0080`
- **Light Purple**: `#F0E6FF`

## Backend Integration

The app communicates with a Node.js/Express backend at the `/generate-response` endpoint.

**Request Format**:
```json
{
  "emotion": "I'm feeling happy and energized"
}
```

**Expected Response**:
```json
{
  "emotion": "I'm feeling happy and energized",
  "message": "That's wonderful! Here's a playlist...",
  "playlists": [
    {
      "name": "Happy Hits",
      "url": "https://open.spotify.com/playlist/...",
      "image": "https://mosaic.scdn.co/..."
    }
  ]
}
```

## Development Notes

- **Animations**: Uses React Native's `Animated` API for smooth transitions
- **Styling**: Consistent use of purple gradient colors across UI
- **Message Bubbles**: User messages appear on the right (purple), bot on left (white)
- **Loading State**: Shows animated dots with "Finding the right sound for you…" message

## Future Enhancements

- Voice input support (already structured for it)
- Message history/persistence
- User preferences and mood tracking
- Multiple playlist recommendations
- Share feature for discovered playlists
- Dark mode toggle

## Troubleshooting

### API Connection Error
- Ensure backend server is running (`npm start` in `/backend`)
- Verify API URL in `utils/api.js` matches your backend
- Check network connectivity

### Font Loading Issues
- Fonts are optional; app will work with system fonts if custom fonts fail
- Check font files exist in `assets/fonts/`

### Expo CLI Issues
```bash
# Clear cache and reinstall
npm cache clean --force
npm install
npx expo start --clear
```

## Notes

- The app is designed mobile-first with a portrait orientation
- No user authentication required for MVP
- Responsive design works on various screen sizes
- Smooth animations enhance user experience without being distracting

---

**Built with ❤️ for emotional wellness through music**
