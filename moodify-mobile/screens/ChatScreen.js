import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  ActivityIndicator,
  Dimensions,
  Animated,
  Keyboard,
  SafeAreaView,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import MessageBubble from '../components/MessageBubble';
import PlaylistCard from '../components/PlaylistCard';
import { sendMessage, sendAudio } from '../utils/api';
import MicrophoneIcon from '../public/microphone.svg';
import SendIcon from '../public/send.svg';
import BackIcon from '../public/back.svg';
import { Audio } from 'expo-av';


const { width, height } = Dimensions.get('window');

const ChatScreen = ({ onBack, initialText = '' }) => {
  const [messages, setMessages] = useState([
    {
      id: '0',
      type: 'bot',
      text: 'Hi there! I\'m Moodify, your music companion. Tell me how you\'re feeling right now, and I\'ll find the perfect soundtrack for your mood. 💭',
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [playlistData, setPlaylistData] = useState(null);
  const [recording, setRecording] = useState(null);
  const [isRecording, setIsRecording] = useState(false);

  const scrollViewRef = useRef(null);
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;

  const featureCards = [
    {
      id: 1,
      emoji: '🎵',
      title: 'Mood-Based Playlists',
      description: 'Tell us how you feel, get the perfect playlist',
    },
    {
      id: 2,
      emoji: '🎤',
      title: 'Voice & Text',
      description: 'Share your mood by typing or speaking',
    },
    {
      id: 3,
      emoji: '🎧',
      title: 'Personalized Music',
      description: 'AI-curated songs that match your vibe',
    },
  ];

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 500,
      useNativeDriver: true,
    }).start();
  }, []);

  // Pulse animation for recording
  useEffect(() => {
    if (isRecording) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.2,
            duration: 800,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 800,
            useNativeDriver: true,
          }),
        ])
      ).start();
    } else {
      pulseAnim.setValue(1);
    }
  }, [isRecording]);

  // Handle initial text from LandingScreen
  useEffect(() => {
    if (initialText && initialText.trim()) {
      setInputValue(initialText);
      // Auto-send the initial message
      setTimeout(() => {
        handleSendMessageWithText(initialText);
      }, 300);
    }
  }, [initialText]);

  const scrollToBottom = () => {
    scrollViewRef.current?.scrollToEnd({ animated: true });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessageWithText = async (text) => {
    if (!text.trim()) return;

    Keyboard.dismiss();

    // Add user message to chat
    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      text: text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setPlaylistData(null);

    try {
      // Call backend API
      const response = await sendMessage(text);

      if (response && response.message && response.playlists) {
        // Add bot response message
        const botMessage = {
          id: (Date.now() + 1).toString(),
          type: 'bot',
          text: response.message,
          timestamp: new Date(),
          playlist: response.playlists[0], // Use first playlist
        };

        setMessages((prev) => [...prev, botMessage]);
        setPlaylistData(response.playlists[0]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        text: 'Sorry, something went wrong. Could you try again?',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    await handleSendMessageWithText(inputValue);
  };

  const handleRecord = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (!permission.granted) return;

      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );

      setRecording(recording);
      setIsRecording(true);
    } catch (err) {
      console.error('🎤 Start recording error:', err);
    }
  };

  const stopRecording = async () => {
    if (!recording) return;

    try {
      setIsRecording(false);
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setRecording(null);

      if (uri) {
        const formData = new FormData();
        formData.append('audio', {
          uri: uri,
          type: 'audio/m4a',
          name: 'recording.m4a',
        });

        const data = await sendAudio(formData);
        
        // Set the transcribed text in the input field
        if (data.text) {
          setInputValue(data.text);
        }
      }
    } catch (err) {
      console.error('🎤 Stop recording error:', err);
      alert('Could not process audio. Please try again.');
    }
  };

  const handleFeatureCardPress = (card) => {
    // Pre-fill input with example text based on card
    const exampleTexts = {
      1: "I'm feeling happy and energetic!",
      2: "I need some calm music to relax",
      3: "Give me something upbeat!",
    };
    setInputValue(exampleTexts[card.id]);
  };

  return (
    <Animated.View style={[styles.container, { opacity: fadeAnim }]}>
      <LinearGradient
        colors={['#FAF7FF', '#F3EDFF']}
        start={{ x: 0, y: 0 }}
        end={{ x: 0, y: 1 }}
        style={styles.gradient}
      >
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity
            onPress={onBack}
            style={styles.backButton}
            activeOpacity={0.7}
          >
            <BackIcon width={20} height={20} fill="#9D4EDD" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Moodify</Text>
          <View style={{ width: 36 }} />
        </View>

        {/* Messages Container */}
        <ScrollView
          ref={scrollViewRef}
          style={styles.messagesContainer}
          contentContainerStyle={[
            styles.messagesContent,
            messages.length <= 1 && { justifyContent: 'center', flexGrow: 1 }
          ]}
          showsVerticalScrollIndicator={false}
          onContentSizeChange={scrollToBottom}
        >
          {messages.map((message) => (
            <View key={message.id} style={styles.messageWrapper}>
              <MessageBubble
                type={message.type}
                text={message.text}
              />
              {message.playlist && (
                <PlaylistCard playlist={message.playlist} />
              )}
            </View>
          ))}

          {isLoading && (
            <View style={styles.loadingContainer}>
              <View style={styles.loadingDots}>
                <View style={styles.dot} />
                <View style={styles.dot} />
                <View style={styles.dot} />
              </View>
              <Text style={styles.loadingText}>
                Finding the right sound for you…
              </Text>
            </View>
          )}

          {/* Feature Cards - Only show when chat is empty or just initial message */}
          {messages.length <= 1 && !isLoading && (
            <View style={styles.featureCardsContainer}>
              <Text style={styles.featureCardsTitle}>What Moodify Can Do</Text>
              <View style={styles.featureCardsGrid}>
                {featureCards.map((card) => (
                  <TouchableOpacity
                    key={card.id}
                    style={styles.featureCard}
                    activeOpacity={0.8}
                    onPress={() => handleFeatureCardPress(card)}
                  >
                    <Text style={styles.featureCardEmoji}>{card.emoji}</Text>
                    <Text style={styles.featureCardTitle}>{card.title}</Text>
                    <Text style={styles.featureCardDescription}>
                      {card.description}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          )}
        </ScrollView>

        {/* Input Area */}
        <View style={styles.inputArea}>
          <View style={styles.inputWrapper}>
            <TextInput
              style={styles.input}
              placeholder="Share your mood..."
              placeholderTextColor="#C4A7E7"
              value={inputValue}
              onChangeText={setInputValue}
              maxLength={500}
              editable={!isLoading}
              underlineColorAndroid="transparent"
            />

            <Animated.View style={{ transform: [{ scale: isRecording ? pulseAnim : 1 }] }}>
              <TouchableOpacity
                onPress={handleRecord}
                style={[styles.micButton, isRecording && styles.micButtonActive]}
                disabled={isLoading}
              >
                <MicrophoneIcon
                  width={20}
                  height={20}
                  fill="none"
                  stroke={isRecording ? '#FFFFFF' : '#8B5FC7'}
                  strokeWidth={2}
                />
              </TouchableOpacity>
            </Animated.View>
            <TouchableOpacity
              onPress={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              activeOpacity={0.7}
              style={[styles.sendButton, (isLoading || !inputValue.trim()) && styles.sendButtonDisabled]}
            >
              <SendIcon width={20} height={20} fill={(isLoading || !inputValue.trim()) ? '#C4A7E7' : '#9D4EDD'} />
            </TouchableOpacity>
          </View>
        </View>
      </LinearGradient>
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(157, 78, 221, 0.1)',
  },
  backButton: {
    width: 36,
    height: 36,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 18,
    backgroundColor: 'rgba(157, 78, 221, 0.1)',
  },
  backButtonText: {
    fontSize: 20,
    color: '#9D4EDD',
    fontWeight: '600',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#4A0080',
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    paddingHorizontal: 16,
    paddingVertical: 20,
  },
  messageWrapper: {
    marginBottom: 16,
  },
  loadingContainer: {
    alignItems: 'center',
    paddingVertical: 24,
  },
  loadingDots: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 6,
    marginBottom: 12,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#9D4EDD',
    opacity: 0.6,
  },
  loadingText: {
    fontSize: 13,
    color: '#8B5FC7',
    fontStyle: 'italic',
  },
  featureCardsContainer: {
    marginTop: 24,
    marginBottom: 16,
  },
  featureCardsTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#6A2C91',
    marginBottom: 16,
    textAlign: 'center',
  },
  featureCardsGrid: {
    gap: 12,
  },
  featureCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 20,
    borderWidth: 1.5,
    borderColor: 'rgba(157, 78, 221, 0.15)',
    shadowColor: '#9D4EDD',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 3,
  },
  featureCardEmoji: {
    fontSize: 32,
    marginBottom: 10,
  },
  featureCardTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#4A0080',
    marginBottom: 6,
  },
  featureCardDescription: {
    fontSize: 13,
    color: '#8B5FC7',
    lineHeight: 18,
  },
  inputArea: {
    paddingHorizontal: 16,
    paddingBottom: 16,
    paddingTop: 12,
    backgroundColor: 'transparent',
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: 10,
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: '#FFFFFF',
    borderRadius: 50,
    borderWidth: 1.5,
    borderColor: 'rgba(157, 78, 221, 0.2)',
    shadowColor: '#9D4EDD',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  input: {
    flex: 1,
    fontSize: 14,
    color: '#4A0080',
    height: 36,
    paddingVertical: 0,
  },
  micButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(157, 78, 221, 0.1)',
  },
  micButtonActive: {
    backgroundColor: '#9D4EDD',
    shadowColor: '#9D4EDD',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.6,
    shadowRadius: 10,
    elevation: 8,
  },
  sendButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(157, 78, 221, 0.1)',
  },
  sendButtonDisabled: {
    opacity: 0.4,
  },
});

export default ChatScreen;
