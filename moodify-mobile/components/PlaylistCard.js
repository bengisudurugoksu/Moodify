import React, { useEffect } from 'react';
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  StyleSheet,
  Animated,
  Easing,
  Linking,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

const { width } = Dimensions.get('window');

const PlaylistCard = ({ playlist }) => {
  const scaleAnim = new Animated.Value(0.85);
  const opacityAnim = new Animated.Value(0);
  const slideAnim = new Animated.Value(20);

  useEffect(() => {
    Animated.parallel([
      Animated.timing(scaleAnim, {
        toValue: 1,
        duration: 400,
        delay: 200,
        easing: Easing.out(Easing.cubic),
        useNativeDriver: true,
      }),
      Animated.timing(opacityAnim, {
        toValue: 1,
        duration: 400,
        delay: 200,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 400,
        delay: 200,
        easing: Easing.out(Easing.cubic),
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  const handleOpenPlaylist = () => {
    if (playlist.url) {
      Linking.openURL(playlist.url);
    }
  };

  return (
    <Animated.View
      style={[
        styles.container,
        {
          opacity: opacityAnim,
          transform: [
            { scale: scaleAnim },
            { translateY: slideAnim },
          ],
        },
      ]}
    >
      <View style={styles.contentWrapper}>
        {/* Playlist Image */}
        {playlist.image && (
          <View style={styles.imageContainer}>
            <Image
              source={{ uri: playlist.image }}
              style={styles.playlistImage}
            />
            <View style={styles.imageOverlay} />
          </View>
        )}

        {/* Playlist Info */}
        <View style={styles.infoContainer}>
          <Text style={styles.playlistName} numberOfLines={2}>
            {playlist.name}
          </Text>
          <Text style={styles.playlistType}>Curated by Spotify</Text>

          {/* Action Button */}
          <TouchableOpacity
            onPress={handleOpenPlaylist}
            activeOpacity={0.8}
            style={styles.buttonWrapper}
          >
            <LinearGradient
              colors={['#9D4EDD', '#7B2CBF']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={styles.button}
            >
              <Text style={styles.buttonText}>Listen on Spotify</Text>
              <Text style={styles.buttonArrow}> →</Text>
            </LinearGradient>
          </TouchableOpacity>
        </View>
      </View>

      {/* Decorative accent */}
      <View style={styles.accentGradient} />
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: width - 96,
    alignSelf: 'flex-start',
    marginTop: 12,
    marginBottom: 8,
  },
  contentWrapper: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(157, 78, 221, 0.12)',
    shadowColor: '#9D4EDD',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.12,
    shadowRadius: 16,
    elevation: 6,
  },
  imageContainer: {
    width: '100%',
    aspectRatio: 1,
    backgroundColor: 'rgba(157, 78, 221, 0.1)',
    position: 'relative',
  },
  playlistImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  imageOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(157, 78, 221, 0.08)',
  },
  infoContainer: {
    padding: 16,
  },
  playlistName: {
    fontSize: 16,
    fontWeight: '700',
    color: '#4A0080',
    marginBottom: 4,
    lineHeight: 22,
  },
  playlistType: {
    fontSize: 12,
    color: '#8B5FC7',
    marginBottom: 14,
  },
  buttonWrapper: {
    overflow: 'hidden',
    borderRadius: 10,
  },
  button: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingVertical: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 13,
    fontWeight: '700',
  },
  buttonArrow: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '700',
  },
  accentGradient: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 3,
    backgroundColor: 'transparent',
  },
});

export default PlaylistCard;
