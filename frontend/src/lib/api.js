const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:5000';

export async function submitToMLBackend(payload) {
  try {
    const response = await fetch(`${BACKEND_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to connect to ML Backend:", error);
    throw error;
  }
}

export const API = {
  // Start the machine learning session by submitting initial symptoms
  initiateDiagnosis: (symptomsText) => {
    return submitToMLBackend({ symptoms: symptomsText });
  },

  // Submit answer for a specific structured question during the 'collecting' phase
  submitAnswer: (sessionId, answerValue) => {
    return submitToMLBackend({ session_id: sessionId, answer: answerValue });
  },

  // Ask a free-text follow-up question after the diagnosis hits 'final' phase
  askFollowUp: (sessionId, messageText) => {
    return submitToMLBackend({ session_id: sessionId, message: messageText });
  }
};
