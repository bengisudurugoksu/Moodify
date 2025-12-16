import CONFIG from '../config.js';

// API communication with backend

export async function sendMessage(emotion) {
  try {
    const endpoint = `${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.GENERATE_RESPONSE}`;
    
    if (CONFIG.APP.DEBUG) {
      console.log('📤 Sending request to:', endpoint);
      console.log('📝 Emotion:', emotion);
    }

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: emotion,
      }),
      timeout: CONFIG.API.TIMEOUT,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API Error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    
    if (CONFIG.APP.DEBUG) {
      console.log('📥 Response received:', data);
    }
    
    return data;
  } catch (error) {
    console.error('❌ API Error:', error.message);
    throw error;
  }
}

export async function sendAudio(formData) {
  try {
    const endpoint = `${CONFIG.API.BASE_URL}/api/speech-to-text`;
    
    if (CONFIG.APP.DEBUG) {
      console.log('🎤 Sending audio to:', endpoint);
    }

    const response = await fetch(endpoint, {
      method: 'POST',
      body: formData,
      timeout: CONFIG.API.TIMEOUT,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Speech API Error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    
    if (CONFIG.APP.DEBUG) {
      console.log('📥 Transcription received:', data);
    }
    
    return data;
  } catch (error) {
    console.error('❌ Speech API Error:', error.message);
    throw error;
  }
}
