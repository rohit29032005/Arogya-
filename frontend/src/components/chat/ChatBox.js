import React, { useState, useEffect, useRef } from 'react';
import { Send } from 'lucide-react';
import MessageBubble from './MessageBubble';
import { useChats } from '../../hooks/useChats';
import { doc, onSnapshot } from 'firebase/firestore';
import { db } from '../../lib/firebase';
import { useAuth } from '../../contexts/AuthContext';
import { API } from '../../lib/api';

export default function ChatBox({ activeChatId }) {
  const { currentUser } = useAuth();
  const { addMessage, updateChatMeta, resetChat } = useChats();
  const [messages, setMessages] = useState([]);
  const [mlSessionId, setMlSessionId] = useState(null);
  const [chatStatus, setChatStatus] = useState('collecting');
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  // Sync messages and metadata in real-time
  useEffect(() => {
    if (!activeChatId || !currentUser) {
      setMessages([]);
      setMlSessionId(null);
      return;
    }

    const chatRef = doc(db, 'users', currentUser.uid, 'chats', activeChatId);
    const unsubscribe = onSnapshot(chatRef, (snapshot) => {
      if (snapshot.exists()) {
        const chatData = snapshot.data();
        setMessages(chatData.messages || []);
        setMlSessionId(chatData.ml_session_id || null);
        setChatStatus(chatData.status || 'collecting');
      } else {
        setMessages([]);
      }
    });

    return () => unsubscribe();
  }, [activeChatId, currentUser]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Basic Heuristic Intent Engine
  const detectNewDiagnosisIntent = (text) => {
    const SYMPTOM_KEYWORDS = [
      "fever", "pain", "nausea", "headache", "cough", "vomit", "stomach", "ache", 
      "rash", "dizzy", "fatigue", "tired", "chill", "diarrhea", "constipation",
      "burning", "itching", "swelling", "bleeding", "weakness"
    ];
    const normalized = text.toLowerCase();
    
    // If it's a direct question about reasoning or treatment, it's follow-up
    if (normalized.includes("why") || normalized.includes("how") || normalized.includes("what")) {
      return false;
    }
    return SYMPTOM_KEYWORDS.some(kw => normalized.includes(kw));
  };

  const handleStartNewDiagnosis = async (initialSymptom = null) => {
    setIsTyping(true);
    try {
      await resetChat(activeChatId);
      if (initialSymptom) {
        await addMessage(activeChatId, initialSymptom, 'user');
        const response = await API.initiateDiagnosis(initialSymptom);
        
        let newMeta = {};
        if (response && response.session_id) {
           newMeta.ml_session_id = response.session_id;
        }
        newMeta.status = response.status || 'collecting';
        
        await addMessage(activeChatId, response.question, 'ai', {
          type: response.type,
          options: response.options || []
        }, newMeta);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsTyping(false);
    }
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleOptionClick = (option) => {
    // Treat button click as submitting text
    setInput(option);
    // Use timeout to allow state to settle, or directly call submit (since state is async)
    handleApiSubmission(option);
  };

  const handleApiSubmission = async (overrideText = null) => {
    const textToSubmit = overrideText || input.trim();
    if (!textToSubmit || !activeChatId) return;

    setInput('');
    setIsTyping(true);

    try {
      // Intent Detection
      if (chatStatus === 'chat_after_result' || chatStatus === 'final') {
        if (detectNewDiagnosisIntent(textToSubmit)) {
          setIsTyping(false); // handleStartNewDiagnosis controls its own loading
          await handleStartNewDiagnosis(textToSubmit);
          return;
        }
      }

      await addMessage(activeChatId, textToSubmit, 'user');

      let response;
      let newMeta = {};

      if (!mlSessionId) {
        response = await API.initiateDiagnosis(textToSubmit);
        
        if (response && response.session_id) {
           newMeta.ml_session_id = response.session_id;
           newMeta.status = response.status || 'collecting';
        }
      } else if (chatStatus === 'chat_after_result' || chatStatus === 'final') {
        response = await API.askFollowUp(mlSessionId, textToSubmit);
      } else {
        response = await API.submitAnswer(mlSessionId, textToSubmit);
      }

      if (response.reply) {
        await addMessage(activeChatId, response.reply, 'ai', null, newMeta);
      } else if (response.status === 'collecting' || response.status === 'need_clarification') {
        newMeta.status = response.status;
        await addMessage(activeChatId, response.question, 'ai', {
          type: response.type,
          options: response.options || []
        }, newMeta);
      } else if (response.status === 'final' || response.status === 'alternative_suggested') {
        newMeta.status = 'chat_after_result';
        let introMsg = response.message || response.llm_explanation || "Here is the diagnosis.";
        
        await addMessage(activeChatId, introMsg, 'ai', {
          isFinal: true,
          status: response.status,
          predicted_disease: response.predicted_disease || response.alternative_disease,
          confidence: response.confidence,
          confidence_explanation: response.confidence_explanation || null,
          alternatives: response.top3 || [],
          ayurveda: response.ayurveda || null
        }, newMeta);
      } else {
         await addMessage(activeChatId, "Unexpected response from server: " + JSON.stringify(response), 'ai', null, newMeta);
      }

    } catch (error) {
      console.error(error);
      try {
        await addMessage(activeChatId, "System error: " + error.message, 'ai');
      } catch(e) { /* ignore secondary throw */ }
    } finally {
      setIsTyping(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleApiSubmission();
  };

  // Determine if the LAST AI message asked a multiple choice question
  const lastMsg = messages[messages.length - 1];
  const lastAiMsg = [...messages].reverse().find(m => m.sender === 'ai');
  const showOptions = lastMsg && lastMsg.sender === 'ai' && lastMsg.payload?.type === 'choice' && lastMsg.payload?.options;

  if (!activeChatId) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center bg-gray-950/50">
        <div className="w-16 h-16 bg-gray-900 rounded-2xl flex items-center justify-center border border-gray-800 mb-6 shadow-xl">
          <svg className="w-8 h-8 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <h2 className="text-xl font-bold text-gray-200">Welcome to Arogya AI</h2>
        <p className="text-gray-500 mt-2 max-w-sm text-center">Select an existing chat from the sidebar or start a new conversation to get begun.</p>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-gray-950">
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 relative">
        {messages.map((ms, idx) => (
          <MessageBubble key={idx} message={ms} />
        ))}
        
        {isTyping && (
          <div className="flex w-full mt-4 space-x-3 justify-start max-w-4xl mx-auto">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center mt-1 text-white">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
            <div className="px-4 py-4 rounded-2xl bg-gray-800 border border-gray-700 rounded-tl-sm flex items-center space-x-2">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 sm:p-6 bg-gray-900 border-t border-gray-800">
        
        {/* Dynamic Buttons for Multiple Choice */}
        {showOptions && !isTyping && (
           <div className="max-w-4xl mx-auto flex flex-wrap gap-2 mb-4 px-2">
             {lastMsg.payload.options.map((opt, i) => (
               <button
                 key={i}
                 onClick={() => handleOptionClick(opt)}
                 className="px-4 py-2 bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 rounded-full text-sm hover:bg-indigo-600/40 transition-colors"
               >
                 {opt}
               </button>
             ))}
           </div>
        )}

        {/* Dynamic Follow-Up Suggestions for Post-Result */}
        {(chatStatus === 'chat_after_result' || chatStatus === 'final') && !isTyping && lastMsg && lastMsg.sender === 'ai' && (
           <div className="max-w-4xl mx-auto flex flex-wrap gap-2 mb-6 px-2 mt-2 border-t border-gray-800/50 pt-4">
             <p className="w-full text-xs text-gray-500 mb-1 font-medium ml-1">Suggested Follow-ups:</p>
             {[
               "Why was this predicted?",
               "How can this be treated?",
               "What are other possible diseases?",
               "🔄 Start new diagnosis"
             ].map((opt, i) => (
               <button
                 key={`suggestion-${i}`}
                 onClick={() => {
                   if (opt.includes("Start new diagnosis")) {
                     handleStartNewDiagnosis();
                   } else {
                     handleOptionClick(opt);
                   }
                 }}
                 className="px-4 py-2 bg-emerald-600/10 text-emerald-400 border border-emerald-500/30 rounded-full text-sm hover:bg-emerald-600/20 transition-colors shadow-sm"
               >
                 {opt}
               </button>
             ))}
           </div>
        )}

        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto flex items-end gap-3">
          <div className="relative flex-1 bg-gray-800 rounded-2xl border border-gray-700 focus-within:ring-2 focus-within:ring-indigo-500 focus-within:border-transparent transition-all overflow-hidden shadow-lg">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  if (input.trim()) handleSubmit(e);
                }
              }}
              placeholder={
                !mlSessionId 
                  ? "Describe your symptoms..." 
                  : (chatStatus === 'chat_after_result' ? "Ask follow-up questions..." : "Type your answer...")
              }
              className="w-full max-h-48 min-h-[56px] py-4 pl-4 pr-12 bg-transparent text-gray-100 placeholder-gray-500 outline-none resize-none align-middle"
              rows="1"
            />
            <button
              type="submit"
              disabled={!input.trim() || isTyping}
              className="absolute right-2 bottom-3 p-1.5 rounded-xl bg-indigo-600 text-white hover:bg-indigo-500 disabled:opacity-50 disabled:hover:bg-indigo-600 transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </form>
        <p className="text-center text-xs text-gray-600 mt-3 font-medium">
          Arogya ML Model is for research and educational purposes. Always consult a real doctor.
        </p>
      </div>
    </div>
  );
}
