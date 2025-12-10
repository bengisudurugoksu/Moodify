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
import { sendMessage } from '../utils/api';

const { width, height } = Dimensions.get('window');

const ChatScreen = ({ onBack }) => {
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
  const scrollViewRef = useRef(null);
  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 500,
      useNativeDriver: true,
    }).start();
  }, []);

  const scrollToBottom = () => {
    scrollViewRef.current?.scrollToEnd({ animated: true });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    Keyboard.dismiss();

    // Add user message to chat
    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      text: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setPlaylistData(null);

    try {
      // Call backend API
      const response = await sendMessage(inputValue);

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
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Moodify</Text>
          <View style={{ width: 44 }} />
        </View>

        {/* Messages Container */}
        <ScrollView
          ref={scrollViewRef}
          style={styles.messagesContainer}
          contentContainerStyle={styles.messagesContent}
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
              multiline
              maxLength={500}
              editable={!isLoading}
            />
            <TouchableOpacity
              onPress={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              activeOpacity={0.7}
              style={styles.sendButtonWrapper}
            >
              <LinearGradient
                colors={
                  inputValue.trim() && !isLoading
                    ? ['#9D4EDD', '#7B2CBF']
                    : ['#D4B5F0', '#C4A7E7']
                }
                style={styles.sendButton}
              >
                <Text style={styles.sendButtonText}>↑</Text>
              </LinearGradient>
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
    width: 44,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 22,
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
  inputArea: {
    paddingHorizontal: 16,
    paddingBottom: 16,
    paddingTop: 12,
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
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 6,
  },
  input: {
    flex: 1,
    fontSize: 14,
    color: '#4A0080',
    maxHeight: 100,
    paddingVertical: 0,
  },
  sendButtonWrapper: {
    marginBottom: 4,
  },
  sendButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonText: {
    fontSize: 18,
    color: '#FFFFFF',
    fontWeight: '700',
  },
});

export default ChatScreen;
