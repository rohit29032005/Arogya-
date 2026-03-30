import React, { useState } from 'react';
import ChatHistorySidebar from '../components/chat/ChatHistorySidebar';
import ChatBox from '../components/chat/ChatBox';

export default function ChatDashboard() {
  const [activeChatId, setActiveChatId] = useState(null);

  return (
    <div className="flex h-screen w-full bg-gray-950 overflow-hidden text-gray-100 font-sans">
      {/* Sidebar - Desktop & Tablet */}
      <div className="hidden md:flex h-full max-w-72">
        <ChatHistorySidebar 
          activeChatId={activeChatId} 
          setActiveChatId={setActiveChatId} 
        />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden w-full relative">
        {/* Mobile Header (Shows only on small screens) */}
        <div className="md:hidden flex items-center justify-between bg-gray-900 border-b border-gray-800 p-4 shrink-0 shadow-md z-10 w-full">
          <h1 className="text-xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
            Arogya AI
          </h1>
          {/* Mobile menu could be implemented here */}
        </div>

        {/* Chat Box */}
        <div className="flex-1 overflow-hidden">
          <ChatBox activeChatId={activeChatId} />
        </div>
      </div>
    </div>
  );
}
