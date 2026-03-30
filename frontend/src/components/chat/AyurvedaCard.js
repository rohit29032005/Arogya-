import React from 'react';
import { Leaf, Flame, UtensilsCrossed } from 'lucide-react';

export default function AyurvedaCard({ ayurvedaData }) {
  if (!ayurvedaData || ayurvedaData === "No data available") {
    return null;
  }

  return (
    <div className="bg-emerald-950/20 border border-emerald-900/50 rounded-2xl overflow-hidden shadow-lg mt-4 w-full">
       <div className="bg-emerald-900/40 p-4 border-b border-emerald-800/30 flex items-center">
         <Leaf className="w-5 h-5 text-emerald-400 mr-2" />
         <h3 className="text-emerald-100 font-bold tracking-wide">Ayurvedic Protocol</h3>
       </div>
       
       <div className="p-5 space-y-4">
         
         {/* Herbs */}
         {ayurvedaData.herbs && ayurvedaData.herbs !== "NA" && (
           <div className="flex items-start">
             <div className="p-2 bg-emerald-500/10 rounded-lg mr-4 border border-emerald-500/20">
               <Leaf className="w-5 h-5 text-emerald-400" />
             </div>
             <div>
               <h4 className="text-emerald-200 text-xs font-semibold uppercase tracking-wider mb-1">Recommended Herbs</h4>
               <p className="text-emerald-100/80 text-sm leading-relaxed">{ayurvedaData.herbs}</p>
             </div>
           </div>
         )}

         {/* Therapies */}
         {ayurvedaData.therapy && ayurvedaData.therapy !== "NA" && (
           <div className="flex items-start">
             <div className="p-2 bg-orange-500/10 rounded-lg mr-4 border border-orange-500/20">
               <Flame className="w-5 h-5 text-orange-400" />
             </div>
             <div>
               <h4 className="text-orange-200 text-xs font-semibold uppercase tracking-wider mb-1">Prescribed Therapies (Panchakarma)</h4>
               <p className="text-orange-100/80 text-sm leading-relaxed">{ayurvedaData.therapy}</p>
             </div>
           </div>
         )}

         {/* Diet */}
         {ayurvedaData.diet && ayurvedaData.diet !== "NA" && (
           <div className="flex items-start">
             <div className="p-2 bg-yellow-500/10 rounded-lg mr-4 border border-yellow-500/20">
               <UtensilsCrossed className="w-5 h-5 text-yellow-400" />
             </div>
             <div>
               <h4 className="text-yellow-200 text-xs font-semibold uppercase tracking-wider mb-1">Dietary Guidelines</h4>
               <p className="text-yellow-100/80 text-sm leading-relaxed">{ayurvedaData.diet}</p>
             </div>
           </div>
         )}
       </div>
       
       <div className="bg-emerald-900/20 px-5 py-3 border-t border-emerald-900/30">
          <p className="text-[10px] text-emerald-400/60 uppercase tracking-widest text-center">
             Arogya AI - Holistic Recommendations
          </p>
       </div>
    </div>
  );
}
