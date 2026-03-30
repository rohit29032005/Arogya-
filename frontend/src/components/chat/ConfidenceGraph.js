import React from 'react';
import { Activity, ShieldCheck, HelpCircle } from 'lucide-react';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export default function ConfidenceGraph({ disease, confidence, explanation, alternatives }) {
  // Determine color based on confidence rating
  const isHigh = confidence >= 80;
  const colorClass = isHigh ? "text-emerald-400" : "text-amber-400";
  const bgClass = isHigh ? "bg-emerald-500" : "bg-amber-500";
  
  return (
    <div className="bg-gray-900 border border-gray-700/50 rounded-2xl overflow-hidden shadow-xl mt-4 w-full">
      
      {/* Header section */}
      <div className="bg-gray-800/80 p-5 border-b border-gray-700/50">
        <h3 className="text-gray-400 text-xs font-semibold tracking-wider uppercase mb-1 flex items-center">
          <Activity className="w-4 h-4 mr-2" />
          Predicted Condition
        </h3>
        <div className="flex items-end justify-between">
          <h2 className="text-2xl font-bold text-white tracking-tight">
            {disease || "Unknown Condition"}
          </h2>
          <div className="flex flex-col items-end">
            <span className={cn("text-2xl font-black font-mono leading-none", colorClass)}>
              {confidence}%
            </span>
            <span className="text-[10px] text-gray-500 font-medium tracking-wide uppercase mt-1">
              Confidence Score
            </span>
          </div>
        </div>

        {/* Custom Progress Bar */}
        <div className="w-full bg-gray-950 rounded-full h-2.5 mt-5 overflow-hidden shadow-inner border border-gray-800/50">
          <div 
            className={cn("h-2.5 rounded-full transition-all duration-1000 ease-out", bgClass)} 
            style={{ width: `${confidence}%` }}
          ></div>
        </div>
      </div>

      {/* Explanation Section */}
      {explanation && (
        <div className="p-5 space-y-4">
          
          {/* Key Symptoms matched */}
          {explanation.symptom_match && explanation.symptom_match.length > 0 && (
            <div>
               <h4 className="text-xs font-semibold uppercase text-gray-500 flex items-center mb-2">
                 <ShieldCheck className="w-3.5 h-3.5 mr-1.5 align-text-bottom text-indigo-400" />
                 Matched Symptoms
               </h4>
               <div className="flex flex-wrap gap-2">
                 {explanation.symptom_match.map((symp, i) => (
                   <span key={i} className="px-2 py-1 bg-indigo-500/10 border border-indigo-500/30 rounded-md text-xs text-indigo-300">
                     {symp}
                   </span>
                 ))}
               </div>
            </div>
          )}

          {/* Model Reasoning Text */}
          {explanation.model_reasoning && (
             <p className="text-sm text-gray-300 leading-relaxed bg-gray-800/30 p-3 rounded-lg border border-gray-700/30">
               {explanation.model_reasoning}
             </p>
          )}

          {/* Alternative considerations */}
          {explanation.why_previous_rejected && (
            <div className="bg-orange-500/5 border border-orange-500/20 rounded-lg p-3">
               <h4 className="text-xs font-semibold uppercase text-orange-400 flex items-center mb-1.5">
                 <HelpCircle className="w-3.5 h-3.5 mr-1.5 align-text-bottom" />
                 Differential Diagnosis
               </h4>
               <p className="text-xs text-gray-400 leading-relaxed">
                 {explanation.why_previous_rejected}
               </p>
            </div>
          )}
        </div>
      )}

      {/* Top 3 Alternative Candidates (If provided in the array outside of explanation) */}
      {alternatives && alternatives.length > 1 && (
        <div className="px-5 pb-5">
           <div className="w-full h-px bg-gradient-to-r from-transparent via-gray-700/50 to-transparent mb-4"></div>
           <h4 className="text-xs font-semibold uppercase text-gray-500 text-center mb-3">Other Top Possibilities</h4>
           <div className="grid grid-cols-2 gap-2">
             {alternatives.slice(1, 3).map((alt, idx) => (
                <div key={idx} className="flex justify-between items-center bg-gray-950 p-2 rounded border border-gray-800">
                  <span className="text-xs text-gray-300 font-medium truncate pr-2" title={alt.disease}>{alt.disease}</span>
                  <span className="text-[10px] text-gray-500 font-mono">{alt.confidence}%</span>
                </div>
             ))}
           </div>
        </div>
      )}

    </div>
  );
}
