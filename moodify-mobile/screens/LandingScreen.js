import React, { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Animated,
  Easing,
  Dimensions,
  TextInput,
  ScrollView,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import MicrophoneIcon from '../public/microphone.svg';
import SendIcon from '../public/send.svg';
import MusicArtistIcon from '../public/music-artist.svg';
import { Audio } from 'expo-av';


const { width } = Dimensions.get('window');

const LandingScreen = ({ onStart }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.9)).current;
  const translateYAnim = useRef(new Animated.Value(30)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;


  const [recording, setRecording] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [text, setText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 700,
        easing: Easing.out(Easing.cubic),
        useNativeDriver: true,
      }),
      Animated.timing(scaleAnim, {
        toValue: 1,
        duration: 700,
        easing: Easing.out(Easing.cubic),
        useNativeDriver: true,
      }),
      Animated.timing(translateYAnim, {
        toValue: 0,
        duration: 700,
        easing: Easing.out(Easing.cubic),
        useNativeDriver: true,
      }),
    ]).start();
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

  /* ---------------- Audio Logic ---------------- */

  const startRecording = async () => {
    try {
      const { granted } = await Audio.requestPermissionsAsync();
      if (!granted) {
        alert('Permission to access microphone is required!');
        return;
      }

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
      console.error('Failed to start recording', err);
      alert('Could not start recording');
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
        await sendAudioToBackend(uri);
      }
    } catch (err) {
      console.error('Failed to stop recording', err);
      alert('Could not stop recording');
    }
  };

  const sendAudioToBackend = async (audioUri) => {
    try {
      setIsProcessing(true);
      const formData = new FormData();
      formData.append('audio', {
        uri: audioUri,
        type: 'audio/m4a',
        name: 'recording.m4a',
      });

      // Import sendAudio from api.js
      const { sendAudio } = await import('../utils/api.js');
      const data = await sendAudio(formData);

      // Set the transcribed text in the input field
      if (data.text) {
        setText(data.text);
      }
    } catch (err) {
      console.error('Failed to send audio', err);
      alert('Could not process audio. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRecord = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };


  const features = [
    {
      id: 1,
      icon: '🎭',
      title: 'Mood Analysis',
      description: 'Share your feelings and let AI understand your emotional state',
      color: '#9D4EDD',
    },
    {
      id: 2,
      icon: '🎵',
      title: 'Smart Playlists',
      description: 'Get personalized Spotify playlists that match your vibe',
      color: '#BD86FA',
    },
    {
      id: 3,
      icon: '💬',
      title: 'Natural Chat',
      description: 'Express yourself freely - Moodify speaks your language',
      color: '#C77DFF',
    },
  ];

  return (
    <LinearGradient
      colors={['#FAF7FF', '#F0E6FF']}
      style={styles.container}
    >
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.content}>
          <Animated.View
            style={[
              styles.logoContainer,
              {
                opacity: fadeAnim,
                transform: [{ scale: scaleAnim }, { translateY: translateYAnim }],
              },
            ]}
          >
            <View style={styles.musicNoteIcon}>
              <MusicArtistIcon width={50} height={50} fill="none" stroke="#9D4EDD" strokeWidth={2} />
            </View>
          </Animated.View>

          <Animated.View
            style={[
              styles.textContainer,
              { opacity: fadeAnim, transform: [{ translateY: translateYAnim }] },
            ]}
          >
            <Text style={styles.title}>Moodify</Text>
            <Text style={styles.subtitle}>How are you feeling today?</Text>
          </Animated.View>

          <Animated.View
            style={[
              styles.inputArea,
              { opacity: fadeAnim, transform: [{ translateY: translateYAnim }] },
            ]}
          >
            <View style={styles.inputWrapper}>
              <TextInput
                value={text}
                onChangeText={setText}
                placeholder="Share your mood..."
                placeholderTextColor="#C4A7E7"
                style={styles.input}
                editable={!isProcessing}
                underlineColorAndroid="transparent"
              />

              <Animated.View style={{ transform: [{ scale: isRecording ? pulseAnim : 1 }] }}>
                <TouchableOpacity 
                  onPress={handleRecord} 
                  disabled={isProcessing}
                  style={[
                    styles.micButton,
                    isRecording && styles.micButtonActive
                  ]}>
                  <MicrophoneIcon width={20} height={20} fill="none" stroke={isRecording ? '#FFFFFF' : '#8B5FC7'} strokeWidth={2} />
                </TouchableOpacity>
              </Animated.View>
              <TouchableOpacity 
                onPress={() => {
                  if (text.trim()) {
                    onStart(text);
                  }
                }} 
                disabled={!text.trim() || isProcessing}
                style={[styles.sendButton, (!text.trim() || isProcessing) && styles.sendButtonDisabled]}>
                <SendIcon width={20} height={20} fill={(!text.trim() || isProcessing) ? '#C4A7E7' : '#9D4EDD'} />
              </TouchableOpacity>
            </View>

            <Text style={styles.description}>
              Moodify turns your emotions into the perfect soundtrack.
            </Text>
          </Animated.View>

          {/* Feature Cards */}
          <Animated.View
            style={[
              styles.featuresContainer,
              { opacity: fadeAnim, transform: [{ translateY: translateYAnim }] },
            ]}
          >
            {features.map((feature, index) => (
              <Animated.View
                key={feature.id}
                style={[
                  styles.featureCard,
                  {
                    opacity: fadeAnim,
                    transform: [
                      {
                        translateY: translateYAnim.interpolate({
                          inputRange: [0, 30],
                          outputRange: [0, 30 + index * 10],
                        }),
                      },
                    ],
                  },
                ]}
              >
                <View style={[styles.iconCircle, { backgroundColor: `${feature.color}15` }]}>
                  <Text style={styles.featureIcon}>{feature.icon}</Text>
                </View>
                <View style={styles.featureContent}>
                  <Text style={styles.featureTitle}>{feature.title}</Text>
                  <Text style={styles.featureDescription}>{feature.description}</Text>
                </View>
              </Animated.View>
            ))}
          </Animated.View>

          <View style={styles.decorBlob1} />
          <View style={styles.decorBlob2} />
        </View>
      </ScrollView>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 20,
  },
  content: {
    width: '100%',
    alignItems: 'center',
  },
  logoContainer: {
    marginTop: 0,
    marginBottom: 18,
  },
  musicNoteIcon: {
    width: 90,
    height: 90,
    borderRadius: 45,
    backgroundColor: 'rgba(157,78,221,0.15)',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'rgba(157,78,221,0.3)',
  },
  textContainer: {
    alignItems: 'center',
    marginBottom: 18,
  },
  title: {
    fontSize: 44,
    fontWeight: '700',
    color: '#4A0080',
  },
  subtitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#6A2C91',
    marginTop: 6,
  },
  inputArea: {
    width: '100%',
    alignItems: 'center',
    marginTop: 24,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 18,
    paddingVertical: 8,
    backgroundColor: '#FFFFFF',
    borderRadius: 26,
    borderWidth: 1.2,
    borderColor: 'rgba(157,78,221,0.22)',
    width: '92%',
    maxWidth: 380,
    shadowColor: '#9D4EDD',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.12,
    shadowRadius: 8,
    elevation: 6,
    gap: 10,
  },
input: {
  flex: 1,
  fontSize: 14,
  color: '#4A0080',
  height: 36,            // 🔥 BU ORTALIYOR
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
    shadowOpacity: 0.5,
    shadowRadius: 8,
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
  description: {
    fontSize: 12,
    color: '#8B5FC7',
    marginTop: 10,
    textAlign: 'center',
  },
  featuresContainer: {
    width: '92%',
    maxWidth: 380,
    marginTop: 32,
    gap: 16,
  },
  featureCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(157,78,221,0.15)',
    shadowColor: '#9D4EDD',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 6,
    elevation: 3,
  },
  iconCircle: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 14,
  },
  featureIcon: {
    fontSize: 24,
  },
  featureContent: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#4A0080',
    marginBottom: 4,
  },
  featureDescription: {
    fontSize: 13,
    color: '#8B5FC7',
    lineHeight: 18,
  },
  decorBlob1: {
    position: 'absolute',
    width: 140,
    height: 140,
    borderRadius: 70,
    backgroundColor: 'rgba(189,134,250,0.1)',
    top: 90,
    left: -50,
  },
  decorBlob2: {
    position: 'absolute',
    width: 110,
    height: 110,
    borderRadius: 55,
    backgroundColor: 'rgba(157,78,221,0.08)',
    bottom: 120,
    right: -40,
  },
});

export default LandingScreen;