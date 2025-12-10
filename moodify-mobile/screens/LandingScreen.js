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
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import MicrophoneIcon from '../public/microphone.svg';
import SendIcon from '../public/send.svg';
import MusicArtistIcon from '../public/music-artist.svg';

const { width } = Dimensions.get('window');

const LandingScreen = ({ onStart }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.9)).current;
  const translateYAnim = useRef(new Animated.Value(30)).current;
  const [recording, setRecording] = useState(false);

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

  const handleRecord = () => {
    setRecording((prev) => !prev);
  };

  return (
    <LinearGradient
      colors={['#FAF7FF', '#F0E6FF']}
      style={styles.container}
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
              placeholder="Share your mood..."
              placeholderTextColor="#C4A7E7"
              style={styles.input}
              multiline
              underlineColorAndroid="transparent"
              textAlignVertical="center"
            />
            <TouchableOpacity onPress={handleRecord} style={styles.micButton}>
              <MicrophoneIcon width={20} height={20} fill="none" stroke={recording ? '#9D4EDD' : '#8B5FC7'} strokeWidth={2} />
            </TouchableOpacity>
            <TouchableOpacity onPress={onStart} style={styles.sendButton}>
              <SendIcon width={20} height={20} fill="#9D4EDD" />
            </TouchableOpacity>
          </View>

          <Text style={styles.description}>
            Moodify turns your emotions into the perfect soundtrack.
          </Text>
        </Animated.View>

        <View style={styles.decorBlob1} />
        <View style={styles.decorBlob2} />
      </View>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  content: {
    width: '100%',
    alignItems: 'center',
  },
  logoContainer: {
    marginTop: -70,
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
    marginTop: 10,
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

    paddingVertical: 0,
    paddingTop: 0,
    paddingBottom: 0,

    lineHeight: 18,          // ✅ prevents “ruled lines” look
    textAlignVertical: 'center',
  },
  micButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(157, 78, 221, 0.1)',
  },
  sendButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(157, 78, 221, 0.1)',
  },
  description: {
    fontSize: 12,
    color: '#8B5FC7',
    marginTop: 10,
    textAlign: 'center',
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

