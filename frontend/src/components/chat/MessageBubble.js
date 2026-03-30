import React from 'react';
import { Bot, User } from 'lucide-react';
import { format } from 'date-fns';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';
import ConfidenceGraph from './ConfidenceGraph';
import AyurvedaCard from './AyurvedaCard';

// Utility for merging tailwind classes safely
function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export default function MessageBubble({ message }) {
  const isUser = message.sender === 'user';
  
  // Format timestamp (assume it's ISO string or Firestore timestamp fallback)
  let timeStr = '';
  try {
    const d = typeof message.timestamp === 'string' 
      ? new Date(message.timestamp) 
      : message.timestamp?.toDate ? message.timestamp.toDate() : new Date();
    timeStr = format(d, 'h:mm a');
  } catch (e) {
    timeStr = '';
  }

  return (
    <div className={cn(
      "flex w-full mt-4 space-x-3 max-w-4xl mx-auto",
      isUser ? "justify-end" : "justify-start"
    )}>
      {/* Bot Avatar (Left) */}
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center mt-1">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}

      {/* Message Content */}
      <div className={cn(
        "flex flex-col space-y-1 text-sm max-w-[80%]",
        isUser ? "items-end" : "items-start"
      )}>
        <div className={cn(
          "px-4 py-3 rounded-2xl shadow-sm whitespace-pre-wrap",
          isUser 
            ? "bg-indigo-600 text-white rounded-tr-sm" 
            : "bg-gray-800 text-gray-100 border border-gray-700 rounded-tl-sm w-full"
        )}>
          {message.text}

          {/* Render Rich ML Results if Available */}
          {!isUser && message.payload && message.payload.isFinal && (
            <div className="w-full mt-3 flex flex-col gap-3">
              <ConfidenceGraph 
                disease={message.payload.predicted_disease}
                confidence={message.payload.confidence}
                explanation={message.payload.confidence_explanation}
                alternatives={message.payload.alternatives}
              />
              <AyurvedaCard 
                ayurvedaData={message.payload.ayurveda}
              />
            </div>
          )}
        </div>
        <span className="text-xs text-gray-500 px-1">
          {timeStr}
        </span>
      </div>

      {/* User Avatar (Right) */}
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center mt-1">
          <User className="w-5 h-5 text-gray-300" />
        </div>
      )}
    </div>
  );
}
