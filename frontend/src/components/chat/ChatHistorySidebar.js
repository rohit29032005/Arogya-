import React, { useState } from 'react';
import { 
  Plus, 
  MessageSquare, 
  Trash2, 
  LogOut, 
  AlertTriangle 
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { useChats } from '../../hooks/useChats';
import { formatDistanceToNow } from 'date-fns';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export default function ChatHistorySidebar({ activeChatId, setActiveChatId }) {
  const { currentUser, logout } = useAuth();
  const { chats, createNewChat, deleteChat, deleteAllChats } = useChats();
  const [showConfirmDelete, setShowConfirmDelete] = useState(null); // 'all' or chatId
  
  const handleNewChat = async () => {
    const newChatId = await createNewChat();
    if (newChatId) {
      setActiveChatId(newChatId);
    }
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (id === 'all') {
      await deleteAllChats();
      setActiveChatId(null);
    } else {
      await deleteChat(id);
      if (activeChatId === id) {
        setActiveChatId(null);
      }
    }
    setShowConfirmDelete(null);
  };

  const confirmDelete = (id, e) => {
    e.stopPropagation();
    setShowConfirmDelete(id);
  };

  return (
    <div className="w-72 bg-gray-900 border-r border-gray-800 flex flex-col h-full overflow-hidden shrink-0">
      {/* Sidebar Header */}
      <div className="p-4 border-b border-gray-800">
        <button
          onClick={handleNewChat}
          className="w-full flex items-center justify-center space-x-2 bg-indigo-600 hover:bg-indigo-500 text-white py-2.5 px-4 rounded-xl transition-all font-medium text-sm shadow-lg shadow-indigo-500/25"
        >
          <Plus className="w-5 h-5" />
          <span>New Chat</span>
        </button>
      </div>

      {/* Chat List */}
      <div className="flex-1 overflow-y-auto w-full p-2 space-y-1 custom-scrollbar">
        {chats.length === 0 ? (
          <div className="text-gray-500 text-center mt-10 text-sm">
            No chats yet. Start a conversation!
          </div>
        ) : (
          chats.map(chat => {
            const firstMsgStr = chat.messages?.[0]?.text || "New Conversation";
            // Timestamp formatting
            let timeAgo = '';
            try {
              if (chat.updatedAt?.toDate) {
                timeAgo = formatDistanceToNow(chat.updatedAt.toDate(), { addSuffix: true });
              } else if (chat.updatedAt) {
                timeAgo = formatDistanceToNow(new Date(chat.updatedAt), { addSuffix: true });
              }
            } catch(e) {}

            return (
              <div
                key={chat.id}
                onClick={() => setActiveChatId(chat.id)}
                className={cn(
                  "group relative w-full flex flex-col items-start p-3 rounded-xl cursor-pointer transition-colors border",
                  activeChatId === chat.id 
                    ? "bg-gray-800 border-gray-700" 
                    : "bg-transparent border-transparent hover:bg-gray-800/50"
                )}
              >
                <div className="flex items-center w-full justify-between">
                  <div className="flex items-center truncate">
                    <MessageSquare className="w-4 h-4 text-gray-400 mr-2 flex-shrink-0" />
                    <span className="text-sm text-gray-200 font-medium truncate">
                      {firstMsgStr.substring(0, 30)}
                      {firstMsgStr.length > 30 ? '...' : ''}
                    </span>
                  </div>
                  
                  {/* Delete Button */}
                  {showConfirmDelete !== chat.id ? (
                    <button
                      onClick={(e) => confirmDelete(chat.id, e)}
                      className="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-400 transition-all rounded"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  ) : (
                    <div className="flex space-x-1" onClick={(e) => e.stopPropagation()}>
                       <button onClick={(e) => handleDelete(chat.id, e)} className="text-xs bg-red-500/20 text-red-500 px-2 py-1 rounded">Yes</button>
                       <button onClick={(e) => {e.stopPropagation(); setShowConfirmDelete(null)}} className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded">No</button>
                    </div>
                  )}
                </div>
                <div className="text-xs text-gray-500 mt-1 ml-6">
                  {timeAgo}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Delete All Option */}
      {chats.length > 0 && (
        <div className="px-4 py-2">
          {showConfirmDelete === 'all' ? (
             <div className="flex items-center justify-between text-sm bg-red-500/10 p-2 rounded-lg border border-red-500/20">
               <span className="text-red-400">Delete all chats?</span>
               <div className="flex space-x-2">
                 <button onClick={(e) => handleDelete('all', e)} className="text-red-400 hover:text-red-300 font-bold">Yes</button>
                 <button onClick={() => setShowConfirmDelete(null)} className="text-gray-400 hover:text-gray-300">No</button>
               </div>
             </div>
          ) : (
             <button
              onClick={() => setShowConfirmDelete('all')}
              className="text-xs text-gray-500 hover:text-red-400 flex items-center transition-colors w-full p-2 rounded-lg hover:bg-gray-800/50"
             >
              <AlertTriangle className="w-3 h-3 mr-2" /> Delete All Conversations
            </button>
          )}
        </div>
      )}

      {/* User Profile */}
      <div className="p-4 border-t border-gray-800 bg-gray-950/20">
        <div className="flex flex-col">
          <div className="flex items-center justify-between w-full">
            <div className="flex items-center space-x-3 truncate">
              <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-emerald-500 to-teal-500 flex items-center justify-center flex-shrink-0 text-white font-bold shadow-md">
                {currentUser?.displayName ? currentUser.displayName[0].toUpperCase() : currentUser?.email[0].toUpperCase()}
              </div>
              <div className="flex flex-col truncate">
                <span className="text-sm font-medium text-gray-200 truncate">
                  {currentUser?.displayName || 'User'}
                </span>
                <span className="text-xs text-gray-500 truncate">
                  {currentUser?.email}
                </span>
              </div>
            </div>
            <button
               onClick={logout}
               className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors flex-shrink-0 ml-2"
               title="Sign Out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
