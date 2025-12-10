import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  Easing,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

const MessageBubble = ({ type, text }) => {
  const scaleAnim = new Animated.Value(0.8);
  const opacityAnim = new Animated.Value(0);

  useEffect(() => {
    Animated.parallel([
      Animated.timing(scaleAnim, {
        toValue: 1,
        duration: 300,
        easing: Easing.out(Easing.cubic),
        useNativeDriver: true,
      }),
      Animated.timing(opacityAnim, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  const isUser = type === 'user';

  if (isUser) {
    return (
      <Animated.View
        style={[
          styles.userContainer,
          {
            opacity: opacityAnim,
            transform: [{ scale: scaleAnim }],
          },
        ]}
      >
        <LinearGradient
          colors={['#9D4EDD', '#7B2CBF']}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.userBubble}
        >
          <Text style={styles.userText}>{text}</Text>
        </LinearGradient>
      </Animated.View>
    );
  }

  return (
    <Animated.View
      style={[
        styles.botContainer,
        {
          opacity: opacityAnim,
          transform: [{ scale: scaleAnim }],
        },
      ]}
    >
      <View style={styles.botBubble}>
        <Text style={styles.botText}>{text}</Text>
      </View>
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  userContainer: {
    alignItems: 'flex-end',
  },
  userBubble: {
    maxWidth: '85%',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 20,
    borderBottomRightRadius: 4,
    shadowColor: '#9D4EDD',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 4,
  },
  userText: {
    color: '#FFFFFF',
    fontSize: 14,
    lineHeight: 20,
  },
  botContainer: {
    alignItems: 'flex-start',
  },
  botBubble: {
    maxWidth: '85%',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 20,
    borderBottomLeftRadius: 4,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: 'rgba(157, 78, 221, 0.15)',
    shadowColor: '#9D4EDD',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  botText: {
    color: '#4A0080',
    fontSize: 14,
    lineHeight: 20,
  },
});

export default MessageBubble;
