# ✅ Moodify Mobile - Getting Started Checklist

Print this or check off items as you complete them!

---

## 📥 Installation (5 minutes)

- [ ] Node.js installed (check: `node --version`)
- [ ] npm installed (check: `npm --version`)
- [ ] Expo CLI installed (`npm install -g expo-cli`)
- [ ] Navigated to `moodify-mobile` folder
- [ ] Ran `npm install` (wait for completion)

---

## 🚀 First Run (5 minutes)

- [ ] Backend running on `http://localhost:3000`
  - Open new terminal
  - `cd backend && npm start`
  - See "Server running on" message

- [ ] Mobile app started (`npm start` in moodify-mobile)
- [ ] Chose platform:
  - [ ] Pressed `a` for Android emulator, OR
  - [ ] Pressed `i` for iOS simulator, OR
  - [ ] Scanned QR with Expo Go app on phone

- [ ] App loaded without errors
- [ ] Saw landing screen with "Start" button
- [ ] Tapped "Start" → went to chat screen
- [ ] Typed a message
- [ ] Got response from backend
- [ ] Saw playlist card with image
- [ ] Tapped "Listen on Spotify" → opened link
- [ ] Tapped back button → returned to landing

---

## 📖 Documentation Reading (30 minutes)

Read in this order:
- [ ] `INDEX.md` (navigation guide)
- [ ] `QUICK_REFERENCE.md` (quick lookups)
- [ ] `SETUP.md` (detailed setup)
- [ ] `README.md` (full overview)

Skim these for later reference:
- [ ] `ARCHITECTURE.md` (technical design)
- [ ] `DESIGN.md` (visual system)
- [ ] `DEPLOYMENT.md` (launch guide)

---

## 🎨 Customization (Optional - 15 minutes)

### Easy Changes (Try these!)

- [ ] Open `config.js`
- [ ] Change color `#9D4EDD` to your color
- [ ] See color change in app (press `r` to reload)

- [ ] Change title text in `LandingScreen.js`
- [ ] Reload app and see new text

- [ ] Change button text "Start" → something else
- [ ] See change in app

### Medium Changes

- [ ] Update `API.BASE_URL` in `config.js` for production
- [ ] Change welcome message in `ChatScreen.js`
- [ ] Modify colors in gradient button
- [ ] Adjust animation speeds (duration values)

---

## 🧪 Testing (10 minutes)

- [ ] Test on iOS simulator
- [ ] Test on Android emulator
- [ ] Test on physical phone via Expo Go
- [ ] Test with slow network (DevTools)
- [ ] Test error handling (disconnect internet, reconnect)
- [ ] Check console for errors (press `j` in Expo terminal)

---

## 📚 Code Exploration (20 minutes)

- [ ] Read `App.js` - understand navigation
- [ ] Read `screens/LandingScreen.js` - see first screen
- [ ] Read `screens/ChatScreen.js` - understand chat logic
- [ ] Read `components/MessageBubble.js` - see message styling
- [ ] Read `components/PlaylistCard.js` - see playlist UI
- [ ] Read `utils/api.js` - see API communication
- [ ] Read `config.js` - understand settings

---

## 🔧 Setup for Development

- [ ] Open project in VS Code or editor
- [ ] Install Expo DevTools extension (optional)
- [ ] Bookmark `QUICK_REFERENCE.md`
- [ ] Open `config.js` in editor (for easy tweaks)
- [ ] Understand project structure in `INDEX.md`

---

## 🌐 Production Preparation

Before deploying, complete these:

- [ ] Read `DEPLOYMENT.md`
- [ ] Update API URL for production
- [ ] Set `DEBUG: false` in `config.js`
- [ ] Create app icons (1024×1024 PNG)
- [ ] Create splash screen (512×512 PNG)
- [ ] Test on physical devices thoroughly
- [ ] Check console has no errors
- [ ] Verify Spotify links work
- [ ] Test error scenarios

---

## 📱 Platform Specific Setup

### iOS (Mac only)
- [ ] Xcode installed
- [ ] iOS simulator working
- [ ] Can run app in simulator
- [ ] Tested on physical iPhone (if available)

### Android
- [ ] Android Studio or emulator installed
- [ ] Android emulator running
- [ ] Can run app in emulator
- [ ] Tested on physical Android phone (if available)

### Web
- [ ] Can run `npm run web`
- [ ] App loads in browser
- [ ] Responsive on desktop

---

## 🎯 Customization Checklist

Choose items to customize:

**Easy (15 minutes)**
- [ ] Change primary color
- [ ] Change app title/welcome message
- [ ] Update API URL
- [ ] Change button text

**Medium (1 hour)**
- [ ] Adjust animation speeds
- [ ] Modify message styling
- [ ] Customize input field appearance
- [ ] Update error messages

**Hard (2+ hours)**
- [ ] Add voice input
- [ ] Create message persistence
- [ ] Add user authentication
- [ ] Build new features

---

## 🐛 Troubleshooting Checklist

If something goes wrong:

- [ ] Check `QUICK_REFERENCE.md` > Troubleshooting
- [ ] Check console for error messages (press `j`)
- [ ] Verify backend is running
- [ ] Check API URL in `config.js`
- [ ] Try reloading app (press `r`)
- [ ] Clear cache and reinstall:
  ```bash
  npm cache clean --force
  rm -rf node_modules
  npm install
  npm start --clear
  ```
- [ ] Check file paths (imports)
- [ ] Look at network tab in DevTools
- [ ] Test with fresh terminal session

---

## ✨ Feature Verification

Verify all features work:

- [ ] Landing screen displays correctly
- [ ] Start button navigates to chat
- [ ] Can type message in input
- [ ] Send button works (enabled/disabled correctly)
- [ ] Loading animation appears while waiting
- [ ] API response displays correctly
- [ ] Message bubbles animate smoothly
- [ ] Playlist card appears with image
- [ ] Playlist link opens Spotify
- [ ] Can continue chatting
- [ ] Back button returns to landing
- [ ] No console errors
- [ ] Animations are smooth (60fps)
- [ ] Responsive on different sizes

---

## 🚀 Deployment Checklist

When ready to launch:

- [ ] All features working perfectly
- [ ] No console errors or warnings
- [ ] Tested on multiple devices
- [ ] App icons created and placed
- [ ] Splash screen created
- [ ] Production API URL set
- [ ] DEBUG set to false
- [ ] App version updated
- [ ] Privacy policy ready (if needed)
- [ ] App description written
- [ ] Screenshots prepared
- [ ] Read `DEPLOYMENT.md` completely
- [ ] Follow iOS/Android specific steps
- [ ] Submit to stores
- [ ] Monitor for issues post-launch

---

## 📝 Final Notes

- Keep `QUICK_REFERENCE.md` bookmarked
- Save `config.js` as your customization hub
- Use `ARCHITECTURE.md` to understand code structure
- Refer to `DESIGN.md` for visual decisions
- Read `DEPLOYMENT.md` before going live

---

## 🎉 Celebration Milestones

- [ ] Got it running! 🎉
- [ ] Customized colors/text 🎨
- [ ] Tested all features ✅
- [ ] Explored the code 🔍
- [ ] Ready to deploy 🚀

---

## ❓ Questions to Ask Yourself

As you build and explore:

1. **Do I understand the structure?**
   - If no: Read `ARCHITECTURE.md`

2. **Can I customize the colors?**
   - If no: Check `config.js` and `DESIGN.md`

3. **How does API communication work?**
   - If unclear: Read `utils/api.js` and `ARCHITECTURE.md`

4. **What should I deploy?**
   - If unsure: Read `DEPLOYMENT.md`

5. **Where do I make changes?**
   - If lost: Check `PROJECT_SUMMARY.md` file structure

---

## 🏁 Success Criteria

You're ready to ship when:

✅ App runs without errors
✅ All features work correctly
✅ Customizations applied
✅ Tested on real device
✅ Documentation reviewed
✅ Ready for launch

---

## 📞 Quick Links

- Start here: `INDEX.md`
- Quick lookup: `QUICK_REFERENCE.md`
- Setup help: `SETUP.md`
- Full guide: `README.md`
- Code structure: `ARCHITECTURE.md`
- Visual design: `DESIGN.md`
- Go live: `DEPLOYMENT.md`

---

## 🎓 Learning Resources

**Within Project**
- Source code (well-commented)
- Component examples
- Styling patterns
- Configuration system

**External**
- React Native docs
- Expo docs
- Spotify API docs
- Material Design guidelines

---

**Print this, check items off, and enjoy building Moodify! 🚀💜**
