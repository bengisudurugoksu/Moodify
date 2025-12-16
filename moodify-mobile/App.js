import React, { useState, useEffect } from 'react';
import { View, SafeAreaView } from 'react-native';
import * as SplashScreen from 'expo-splash-screen';
import LandingScreen from './screens/LandingScreen';
import ChatScreen from './screens/ChatScreen';

SplashScreen.preventAutoHideAsync();

export default function App() {
  const [appReady, setAppReady] = useState(false);
  const [currentScreen, setCurrentScreen] = useState('landing'); // 'landing' or 'chat'
  const [initialText, setInitialText] = useState('');

  useEffect(() => {
    async function prepare() {
      try {
        // Fonts are optional for this MVP - using system fonts as fallback
        // To add custom fonts, place .ttf files in assets/fonts/ and uncomment Font.loadAsync code
        await new Promise(resolve => setTimeout(resolve, 500));
        setAppReady(true);
      } catch (e) {
        console.warn('Setup error:', e);
        setAppReady(true);
      } finally {
        await SplashScreen.hideAsync();
      }
    }
    prepare();
  }, []);

  if (!appReady) {
    return null;
  }

  const handleStartChat = (text = '') => {
    setInitialText(text);
    setCurrentScreen('chat');
  };

  const handleBackToHome = () => {
    setInitialText('');
    setCurrentScreen('landing');
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#ffffff' }}>
      {currentScreen === 'landing' ? (
        <LandingScreen onStart={handleStartChat} />
      ) : (
        <ChatScreen onBack={handleBackToHome} initialText={initialText} />
      )}
    </SafeAreaView>
  );
}
