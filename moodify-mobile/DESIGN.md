# Moodify Mobile App - Visual Design Guide

## 🎨 Design Philosophy

**Emotion-First Design**: Every visual choice reflects warmth, safety, and emotional intelligence.

**Core Principles**:
1. **Calming**: Soft colors, smooth animations, no jarring elements
2. **Human**: Conversational UI, natural flow, relatable language
3. **Beautiful**: Modern aesthetics, thoughtful spacing, elegant details
4. **Accessible**: High contrast, readable fonts, touch-friendly sizes

---

## 🌈 Color System

### Primary Palette

```
┌─────────────────────────────────────────┐
│ PRIMARY PURPLE (#9D4EDD)                │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
│ Usage: User messages, buttons, accents │
│ Hex: #9D4EDD | RGB: 157, 78, 221      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ DARK PURPLE (#4A0080)                   │
│ ██████████████████████████████████████  │
│ Usage: Headlines, primary text          │
│ Hex: #4A0080 | RGB: 74, 0, 128         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ACCENT PURPLE (#6A2C91)                 │
│ ███████████████████████████████████     │
│ Usage: Subtitles, secondary text        │
│ Hex: #6A2C91 | RGB: 106, 44, 145       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ SOFT PURPLE (#C4A7E7)                   │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
│ Usage: Placeholders, borders, light UI  │
│ Hex: #C4A7E7 | RGB: 196, 167, 231      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ LIGHT PURPLE (#F0E6FF)                  │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ Usage: Backgrounds, subtle fills        │
│ Hex: #F0E6FF | RGB: 240, 230, 255      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ BACKGROUND (#FAF7FF)                    │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ Usage: Screen backgrounds, clean areas  │
│ Hex: #FAF7FF | RGB: 250, 247, 255      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ WHITE (#FFFFFF)                         │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ Usage: Message bubbles, cards, text     │
│ Hex: #FFFFFF | RGB: 255, 255, 255      │
└─────────────────────────────────────────┘
```

### Gradient Combinations

**Primary Gradient** (Buttons, User Messages):
```
From: #9D4EDD
To:   #7B2CBF
Angle: 45° (left-top to right-bottom)
```

**Background Gradient** (Screens):
```
From: #FAF7FF
To:   #F0E6FF
Angle: 135° (top-left to bottom-right)
```

### Color Usage Guidelines

| Component | Color | Why |
|-----------|-------|-----|
| Primary Button | #9D4EDD → #7B2CBF | Inviting, energetic |
| User Message | #9D4EDD → #7B2CBF | Distinguishes user input |
| Bot Message | #FFFFFF + border | Calm, approachable |
| Text Heading | #4A0080 | High contrast, readable |
| Text Body | #6A2C91 | Softer, secondary emphasis |
| Background | #FAF7FF | Very light, calming |
| Accent | #C4A7E7 | Subtle, non-intrusive |

---

## 🔤 Typography System

### Font Family
- **System Fonts**: San Francisco (iOS), Roboto (Android)
- **Custom Fonts** (Optional): Poppins family for premium feel
- **Fallback**: System defaults ensure compatibility

### Font Weights & Sizes

```
HEADINGS (Landing Screen)
├── Title: 48px Bold (#4A0080)
│   "Moodify"
├── Subtitle: 20px Semibold (#6A2C91)
│   "How are you feeling today?"
└── Description: 14px Regular (#8B5FC7)
    "Share your mood and discover..."

CHAT INTERFACE
├── Chat Header: 18px Bold (#4A0080)
│   "Moodify"
├── Message Text: 14px Regular (#4A0080 or #FFFFFF)
│   User & bot messages
├── Playlist Name: 16px Bold (#4A0080)
│   "Happy Hits"
├── Playlist Type: 12px Regular (#8B5FC7)
│   "Curated by Spotify"
└── Button Text: 13px Bold (#FFFFFF or #4A0080)
    "Listen on Spotify"

UTILITY TEXT
├── Loading: 13px Italic (#8B5FC7)
│   "Finding the right sound for you…"
├── Placeholder: 14px Regular (#C4A7E7)
│   "Share your mood..."
└── Error: 13px Regular (#D32F2F)
    "Connection error..."
```

### Line Heights
- **Headings**: 1.2× font size (tight)
- **Body**: 1.4-1.5× font size (readable)
- **Small Text**: 1.4× font size

---

## 📐 Layout & Spacing

### Spacing Scale
```
4px  - Minimal spacing
8px  - Small gaps
12px - Standard padding
16px - Medium padding
20px - Large padding
24px - Extra large padding
32px - Section spacing
```

### Safe Area & Padding
```
Screen Edge
├─ 16px Horizontal Padding (standard)
├─ 12px Vertical Padding (header/footer)
└─ 20px Vertical Padding (content area)
```

### Component Sizing
```
BUTTONS
├── Large: 44px height, 50px border radius
├── Medium: 36px height, 18px border radius
└── Small: 28px height, 14px border radius

ICONS
├── Large: 100px (logo)
├── Medium: 40-48px (UI icons)
└── Small: 24px (auxiliary icons)

INPUT FIELDS
├── Height: 44px minimum (touch target)
├── Border Radius: 50px (pill-shaped)
└── Padding: 16px horizontal, 12px vertical
```

### Touch Targets
- **Minimum**: 44×44 points (Apple HIG)
- **Comfortable**: 48×48 points recommended
- **Gap**: 8+ points between targets

---

## 🎭 Component Designs

### Message Bubble (User)

```
┌─────────────────────────────┐
│ I'm feeling happy today!    │ (User message)
└────────────────┘
  └─ Rounded corner (20px)
     Max width: 85% of screen
     Background: Gradient #9D4EDD → #7B2CBF
     Text color: White
     Padding: 12-16px
     Alignment: Right side
     Border radius: 20px with 4px flat corner
```

### Message Bubble (Bot)

```
┌─────────────────────────────┐
│ That sounds wonderful! I've │ (Bot message)
│ found a playlist...         │
└─────────────────────────────┘
  └─ Rounded corner (20px)
     Max width: 85% of screen
     Background: White
     Text color: #4A0080
     Border: 1px #E0D4FF
     Padding: 12-16px
     Alignment: Left side
     Border radius: 20px with 4px flat corner
     Shadow: Subtle, soft
```

### Playlist Card

```
┌─────────────────────────────────┐
│  ┌─────────────────────────┐    │
│  │                         │    │ Height: 180px
│  │  [Playlist Image]       │    │ Overlay: Soft purple
│  │  with slight overlay    │    │
│  └─────────────────────────┘    │
│                                 │
│  Happy Hits                     │ 16px bold, #4A0080
│  Curated by Spotify             │ 12px regular, #8B5FC7
│                                 │
│  ┌─────────────────────────┐    │
│  │ Listen on Spotify →     │    │ Gradient button
│  └─────────────────────────┘    │
└─────────────────────────────────┘
  └─ Border radius: 16px
     Border: 1px #E0D4FF
     Padding: 16px
     Width: Full - 32px margins
     Shadow: Soft purple tint
```

### Input Area

```
┌──────────────────────────────────────┐
│ Share your mood...           [↑]    │
└──────────────────────────────────────┘
  └─ Height: 48-64px (expands with text)
     Border radius: 50px
     Border: 1.5px #E0D4FF
     Padding: 16px horizontal, 12px vertical
     Input text: 14px #4A0080
     Placeholder: 14px #C4A7E7
     Send button: 36px circle with gradient
     Shadow: Soft elevation effect
```

### Landing Screen

```
     ┌─────────────────────────┐
     │      ♪ Music Icon       │
     │     (animated pulse)    │
     ├─────────────────────────┤
     │                         │
     │        Moodify          │ 48px bold
     │                         │
     │  How are you feeling    │ 20px semibold
     │      today?             │
     │                         │
     │  Share your mood and    │ 14px regular
     │  discover the perfect   │ (max 2 lines)
     │  soundtrack for your    │
     │  moment.                │
     │                         │
     │    ┌─────────────┐      │
     │    │   Start  →  │      │
     │    └─────────────┘      │
     │  (pill-shaped button)   │
     │                         │
     └─────────────────────────┘
```

---

## ✨ Animation Specifications

### Timing Functions
```
Fast: 300ms - Quick feedback (button press)
Standard: 400-500ms - Message appearance
Slow: 800ms - Page transitions, entrance

Easing: 
├── In: Easing.in(Easing.cubic)
├── Out: Easing.out(Easing.cubic)
└── InOut: Easing.inOut(Easing.cubic)
```

### Key Animations

**Landing Screen Entrance**
```
Duration: 800ms
Timing: Easing.out(Easing.cubic)
Elements:
├── Logo: scale 0.9 → 1, opacity 0 → 1
├── Text: translateY 30 → 0, opacity 0 → 1
└── Button: scale 0.8 → 1, opacity 0 → 1
Delay: Staggered (0, 100, 200ms)
```

**Message Bubble Entrance**
```
Duration: 300ms
Timing: Easing.out(Easing.cubic)
Animation:
├── Scale: 0.8 → 1
├── Opacity: 0 → 1
└── Transform: Smooth interpolation
```

**Playlist Card Entrance**
```
Duration: 400ms
Delay: 200ms after message
Timing: Easing.out(Easing.cubic)
Animation:
├── Scale: 0.85 → 1
├── Opacity: 0 → 1
├── TranslateY: 20 → 0
└── Smooth upward slide
```

**Loading Animation**
```
Duration: 1200ms (repeating)
Elements: Three dots
Animation:
├── Dot 1: Opacity pulse 0.3 → 1 → 0.3
├── Dot 2: Delayed 100ms
└── Dot 3: Delayed 200ms
Effect: Wave-like loading indicator
```

**Button Press Feedback**
```
Duration: 150ms
Animation: Slight scale down 1 → 0.95
Native feedback + animation
```

### Animation Principles
- Always use `useNativeDriver: true`
- Avoid janky animations - test on real devices
- Use easing for natural motion
- Keep animations under 500ms for responsiveness
- Provide visual feedback on every interaction

---

## 🌙 Dark Mode (Future)

For future implementation:

```
Dark Mode Colors:
├── Background: #1A1A1A
├── Secondary: #2D2D2D
├── Text: #F5F5F5
├── Accent: #B88FE7
└── Purple: #A671DB

Inverted Logic:
├── User messages: Same gradient (works both modes)
├── Bot messages: Dark background with light text
├── All borders: Lighter purple tint
└── Shadows: More prominent
```

---

## ♿ Accessibility

### Color Contrast
- Text on background: Minimum 4.5:1 ratio
- Purple on white: ✅ 4.6:1 (WCAG AA+)
- White on purple: ✅ 4.6:1 (WCAG AA+)

### Touch Targets
- Minimum 44×44 points
- Buttons: 44-48 points
- Spacing: 8+ points minimum

### Text Readability
- Minimum font size: 14px body text
- Line height: 1.4-1.5 for readable text
- High contrast dark on light

### Screen Reader Support
- Semantic labels for buttons
- Descriptive alt text for images
- Proper heading hierarchy
- No purely visual information

---

## 🎬 Before & After

### Visual Hierarchy
```
❌ BAD: All text same size and color
✅ GOOD:
   ┌─ Large bold headlines (#4A0080)
   ├─ Medium regular body (#6A2C91)
   ├─ Small soft secondary (#C4A7E7)
   └─ Whitespace for breathing room
```

### Button Design
```
❌ BAD: Flat color, no feedback
✅ GOOD:
   ├─ Gradient background (visual interest)
   ├─ Shadow elevation (depth)
   ├─ Border radius (modern feel)
   └─ Active state feedback
```

### Message Bubbles
```
❌ BAD: Both sides same style
✅ GOOD:
   ├─ User: Colored gradient, right-aligned
   ├─ Bot: White with border, left-aligned
   ├─ Distinct visual hierarchy
   └─ Easy to scan conversation
```

---

## 📸 Design Assets Needed

### Essential Files
```
assets/
├── icon.png (1024×1024 - app icon)
├── splash.png (512×512 - splash screen)
├── adaptive-icon.png (1080×1080 - Android)
└── favicon.png (192×192 - web)

fonts/ (optional)
├── Poppins-Regular.ttf
├── Poppins-Medium.ttf
├── Poppins-SemiBold.ttf
└── Poppins-Bold.ttf
```

### Design Tool Resources
- **Figma**: Create mockups, export assets
- **Sketch**: macOS design tool
- **Adobe XD**: Cloud-based design
- **Penpot**: Open-source alternative

---

## 🎓 Design References

**Inspiration**:
- Spotify app (music context)
- ChatGPT interface (conversation UX)
- Headspace app (calming aesthetics)
- Notion (modern, clean design)

**Color Psychology**:
- Purple: Creativity, calm, trust
- Soft tones: Approachable, safe
- Gradients: Modern, sophisticated
- White space: Clarity, breathing room

---

**Design is about making users feel understood and cared for. Every color, every animation, every pixel matters.** 💜
