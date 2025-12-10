// Configuration file for Moodify Mobile App
// Update these values based on your environment

export const CONFIG = {
  // API Configuration
  API: {
    // Backend server URL - change this based on your environment
    BASE_URL: 'http://localhost:3000',
    
    // For Android emulator on local machine, use:
    // BASE_URL: 'http://10.0.2.2:3000',
    
    // For iOS simulator on local machine, use:
    // BASE_URL: 'http://localhost:3000',
    
    // For production, use your deployed backend URL:
    // BASE_URL: 'https://api.moodify.com',
    
    ENDPOINTS: {
      GENERATE_RESPONSE: '/generate-response',
    },
    
    // Request timeout in milliseconds
    TIMEOUT: 15000,
  },

  // App Configuration
  APP: {
    NAME: 'Moodify',
    VERSION: '1.0.0',
    DEBUG: true, // Set to false in production
  },

  // Color Theme
  COLORS: {
    PRIMARY_PURPLE: '#9D4EDD',
    DARK_PURPLE: '#4A0080',
    LIGHT_PURPLE: '#F0E6FF',
    ACCENT_PURPLE: '#6A2C91',
    SOFT_PURPLE: '#C4A7E7',
    BACKGROUND: '#FAF7FF',
    WHITE: '#FFFFFF',
  },

  // Animation Durations (in milliseconds)
  ANIMATIONS: {
    FADE_IN: 800,
    SLIDE_IN: 400,
    BOUNCE: 300,
  },
};

export default CONFIG;
