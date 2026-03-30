import { useState, useEffect } from 'react';
import { 
  collection,  
  query, 
  orderBy, 
  onSnapshot, 
  addDoc, 
  serverTimestamp, 
  doc, 
  deleteDoc, 
  updateDoc,
  arrayUnion
} from 'firebase/firestore';
import { db } from '../lib/firebase';
import { useAuth } from '../contexts/AuthContext';

export const useChats = () => {
  const { currentUser } = useAuth();
  const [chats, setChats] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch all chats for the current user
  useEffect(() => {
    if (!currentUser) {
      setChats([]);
      setLoading(false);
      return;
    }

    const chatsRef = collection(db, 'users', currentUser.uid, 'chats');
    const q = query(chatsRef, orderBy('updatedAt', 'desc'));

    const unsubscribe = onSnapshot(q, (snapshot) => {
      const chatData = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      setChats(chatData);
      setLoading(false);
    }, (error) => {
      console.error("Error fetching chats:", error);
      setLoading(false);
    });

    return () => unsubscribe();
  }, [currentUser]);

  // Create a new chat
  const createNewChat = async () => {
    if (!currentUser) return null;
    const chatsRef = collection(db, 'users', currentUser.uid, 'chats');
    const newChatRef = await addDoc(chatsRef, {
      messages: [],
      ml_session_id: null,
      status: 'collecting', // collecting, final, chat_after_result
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp()
    });
    return newChatRef.id;
  };

  // Update chat metadata (like ml_session_id and status)
  const updateChatMeta = async (chatId, meta) => {
    if (!currentUser) return;
    const chatRef = doc(db, 'users', currentUser.uid, 'chats', chatId);
    await updateDoc(chatRef, {
      ...meta,
      updatedAt: serverTimestamp()
    });
  };

  // Add a message to an existing chat
  const addMessage = async (chatId, text, sender, payload = null, optionalMeta = null) => {
    if (!currentUser) return;
    const chatRef = doc(db, 'users', currentUser.uid, 'chats', chatId);
    
    // Store message along with any rich ML payload (options, prediction stats, etc)
    let newMessage = {
      sender,
      text,
      payload, 
      timestamp: new Date().toISOString() 
    };

    // Firestore rejects 'undefined', so strip out undefined properties from payload
    if (payload) {
      newMessage.payload = JSON.parse(JSON.stringify(payload)); 
    }
    
    const updatePayload = {
      messages: arrayUnion(newMessage),
      updatedAt: serverTimestamp()
    };

    if (optionalMeta) {
      Object.assign(updatePayload, optionalMeta);
    }
    
    await updateDoc(chatRef, updatePayload);
  };

  // Reset a chat to clean state
  const resetChat = async (chatId) => {
    if (!currentUser) return;
    const chatRef = doc(db, 'users', currentUser.uid, 'chats', chatId);
    await updateDoc(chatRef, {
      messages: [],
      ml_session_id: null,
      status: 'collecting',
      updatedAt: serverTimestamp()
    });
  };

  // Delete a specific chat
  const deleteChat = async (chatId) => {
    if (!currentUser) return;
    const chatRef = doc(db, 'users', currentUser.uid, 'chats', chatId);
    await deleteDoc(chatRef);
  };

  // Delete all chats
  const deleteAllChats = async () => {
    if (!currentUser || chats.length === 0) return;
    
    const promises = chats.map(chat => deleteChat(chat.id));
    await Promise.all(promises);
  };

  return { 
    chats, 
    loading, 
    createNewChat, 
    updateChatMeta,
    addMessage, 
    resetChat,
    deleteChat, 
    deleteAllChats 
  };
};
