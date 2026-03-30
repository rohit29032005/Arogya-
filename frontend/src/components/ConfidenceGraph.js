
// export default ConfidenceGraph;
// export default function ConfidenceGraph({ confidence, explanation }) {
//   if (!confidence || !explanation) return null;

//   return (
//     <div style={{
//       margin: "12px",
//       padding: "14px",
//       background: "#ecfeff",
//       borderRadius: 14,
//       border: "1px solid #67e8f9"
//     }}>
//       <h4 style={{ marginBottom: 6 }}>Why this diagnosis?</h4>

//       <b>Confidence Score</b>
//       <div style={{ fontSize: 28, fontWeight: 700 }}>
//         {confidence}
//       </div>

//       <div style={{ marginTop: 10 }}>
//         <b>Symptoms that matched</b>
//         <ul>
//           {explanation.symptom_match?.map((s, i) => (
//             <li key={i}>{s}</li>
//           ))}
//         </ul>

//         <b>Model reasoning</b>
//         <div>{explanation.model_reasoning}</div>

//         {explanation.why_previous_rejected && (
//           <>
//             <b>Why previous rejected</b>
//             <div>{explanation.why_previous_rejected}</div>
//           </>
//         )}
//       </div>
//     </div>
//   );
// }


//new feature abstracted

// export default function ConfidenceGraph({ confidence, explanation }) {
// if (confidence === undefined || !explanation) return null;
//   // Parse score number for progress bar
//   const scoreNum = parseFloat(confidence);
//   <span>{confidence}%</span>
//   // const pct = isNaN(scoreNum) ? null : Math.min(scoreNum * 100, 100);
//   const pct = isNaN(scoreNum) ? null : Math.min(scoreNum, 100);
//   return (
//     <div style={{
//       background: "linear-gradient(135deg, rgba(129,140,248,0.07), rgba(56,189,248,0.05))",
//       borderRadius: 16,
//       padding: "16px 18px",
//       border: "1px solid rgba(129,140,248,0.2)",
//       animation: "fadeIn 0.4s ease"
//     }}>
//       <style>{`
//         @keyframes fadeIn {
//           from { opacity: 0; transform: translateY(8px); }
//           to { opacity: 1; transform: translateY(0); }
//         }
//         @keyframes barGrow {
//           from { width: 0%; }
//           to { width: var(--w); }
//         }
//       `}</style>

//       {/* Title */}
//       <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14 }}>
//         <div style={{
//           width: 30,
//           height: 30,
//           borderRadius: 8,
//           background: "rgba(129,140,248,0.15)",
//           display: "flex",
//           alignItems: "center",
//           justifyContent: "center",
//           fontSize: 15
//         }}>🔬</div>
//         <div>
//           <div style={{ fontWeight: 700, fontSize: 14, color: "#a5b4fc" }}>
//             Diagnosis Confidence
//           </div>
//           <div style={{ fontSize: 11, color: "#475569", marginTop: 1 }}>
//             Why AI reached this conclusion
//           </div>
//         </div>
//       </div>

//       {/* Confidence Score */}
//       <div style={{
//         padding: "12px 14px",
//         background: "rgba(129,140,248,0.08)",
//         borderRadius: 12,
//         marginBottom: 14,
//         border: "1px solid rgba(129,140,248,0.15)"
//       }}>
//         <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
//           <span style={{ fontSize: 12, color: "#94a3b8", fontWeight: 500 }}>Confidence Score</span>
//           <span style={{ fontWeight: 800, fontSize: 22, color: "#818cf8", fontVariantNumeric: "tabular-nums" }}>
//             {confidence}
//           </span>
//         </div>
//         {pct !== null && (
//           <div style={{ height: 6, background: "rgba(255,255,255,0.06)", borderRadius: 10, overflow: "hidden" }}>
//             <div style={{
//               height: "100%",
//               width: `${pct}%`,
//               background: "linear-gradient(90deg, #818cf8, #38bdf8)",
//               borderRadius: 10,
//               animation: "barGrow 1s cubic-bezier(0.34,1.56,0.64,1) forwards",
//               "--w": `${pct}%`
//             }} />
//           </div>
//         )}
//       </div>

//       {/* Matched symptoms */}
//       {explanation.symptom_match?.length > 0 && (
//         <div style={{ marginBottom: 12 }}>
//           <div style={{ fontSize: 11, color: "#38bdf8", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 8 }}>
//             Symptoms Matched
//           </div>
//           <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
//             {explanation.symptom_match.map((s, i) => (
//               <span key={i} style={{
//                 padding: "4px 10px",
//                 background: "rgba(56,189,248,0.1)",
//                 border: "1px solid rgba(56,189,248,0.2)",
//                 borderRadius: 20,
//                 fontSize: 12,
//                 color: "#7dd3fc",
//                 lineHeight: 1.4
//               }}>
//                 {s}
//               </span>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Model reasoning */}
//       {explanation.model_reasoning && (
//         <div style={{ marginBottom: 10 }}>
//           <div style={{ fontSize: 11, color: "#a5b4fc", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 6 }}>
//             Model Reasoning
//           </div>
//           <div style={{
//             fontSize: 13,
//             color: "#94a3b8",
//             lineHeight: 1.6,
//             padding: "10px 12px",
//             background: "rgba(255,255,255,0.02)",
//             borderRadius: 10,
//             border: "1px solid rgba(129,140,248,0.1)"
//           }}>
//             {explanation.model_reasoning}
//           </div>
//         </div>
//       )}

//       {/* Why previous rejected */}
//       {explanation.why_previous_rejected && (
//         <div style={{
//           padding: "10px 12px",
//           background: "rgba(245,158,11,0.06)",
//           borderRadius: 10,
//           borderLeft: "3px solid #f59e0b",
//           marginTop: 4
//         }}>
//           <div style={{ fontSize: 11, color: "#fbbf24", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 4 }}>
//             Previous Hypothesis Rejected
//           </div>
//           <div style={{ fontSize: 12, color: "#94a3b8", lineHeight: 1.5 }}>
//             {explanation.why_previous_rejected}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }





///////////just to add new grpah //////////////

// export default function ConfidenceGraph({ confidence, explanation }) {

//   // FIX 3: safer check
//   // if (confidence === undefined || !explanation) return null;
//   if (confidence === undefined || !explanation || !explanation.symptom_match) return null;
//   //  FIX 1: remove *100 (backend already gives %)
//   const scoreNum = parseFloat(confidence);
//   const pct = isNaN(scoreNum) ? 0 : Math.min(scoreNum, 100);

//   return (
//     <div style={{
//       background: "linear-gradient(135deg, rgba(129,140,248,0.07), rgba(56,189,248,0.05))",
//       borderRadius: 16,
//       padding: "16px 18px",
//       border: "1px solid rgba(129,140,248,0.2)",
//       animation: "fadeIn 0.4s ease"
//     }}>
//       <style>{`
//         @keyframes fadeIn {
//           from { opacity: 0; transform: translateY(8px); }
//           to { opacity: 1; transform: translateY(0); }
//         }
//         @keyframes barGrow {
//           from { width: 0%; }
//           to { width: var(--w); }
//         }
//       `}</style>

//       {/* Title */}
//       <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14 }}>
//         <div style={{
//           width: 30,
//           height: 30,
//           borderRadius: 8,
//           background: "rgba(129,140,248,0.15)",
//           display: "flex",
//           alignItems: "center",
//           justifyContent: "center",
//           fontSize: 15
//         }}>🔬</div>

//         <div>
//           <div style={{ fontWeight: 700, fontSize: 14, color: "#a5b4fc" }}>
//             Diagnosis Confidence
//           </div>
//           <div style={{ fontSize: 11, color: "#475569", marginTop: 1 }}>
//             Why AI reached this conclusion
//           </div>
//         </div>
//       </div>

//       {/* Confidence Score */}
//       <div style={{
//         padding: "12px 14px",
//         background: "rgba(129,140,248,0.08)",
//         borderRadius: 12,
//         marginBottom: 14,
//         border: "1px solid rgba(129,140,248,0.15)"
//       }}>
//         <div style={{
//           display: "flex",
//           justifyContent: "space-between",
//           alignItems: "center",
//           marginBottom: 8
//         }}>
//           <span style={{
//             fontSize: 12,
//             color: "#94a3b8",
//             fontWeight: 500
//           }}>
//             Confidence Score
//           </span>

//           {/* FIX 2: add % sign */}
//           <span style={{
//             fontWeight: 800,
//             fontSize: 22,
//             color: "#818cf8",
//             fontVariantNumeric: "tabular-nums"
//           }}>
//             {confidence}%
//           </span>
//         </div>

//         {/* Progress Bar */}
//         {pct !== null && (
//           <div style={{
//             height: 6,
//             background: "rgba(255,255,255,0.06)",
//             borderRadius: 10,
//             overflow: "hidden"
//           }}>
//             <div style={{
//               height: "100%",
//               width: `${pct}%`,   // now correct
//               background: "linear-gradient(90deg, #818cf8, #38bdf8)",
//               borderRadius: 10,
//               animation: "barGrow 1s cubic-bezier(0.34,1.56,0.64,1) forwards",
//               "--w": `${pct}%`
//             }} />
//           </div>
//         )}
//       </div>

//       {/* Symptoms matched */}
//       {explanation.symptom_match?.length > 0 && (
//         <div style={{ marginBottom: 12 }}>
//           <div style={{
//             fontSize: 11,
//             color: "#38bdf8",
//             fontWeight: 600,
//             textTransform: "uppercase",
//             letterSpacing: "0.06em",
//             marginBottom: 8
//           }}>
//             Symptoms Matched
//           </div>

//           <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
//             {explanation.symptom_match.map((s, i) => (
//               <span key={i} style={{
//                 padding: "4px 10px",
//                 background: "rgba(56,189,248,0.1)",
//                 border: "1px solid rgba(56,189,248,0.2)",
//                 borderRadius: 20,
//                 fontSize: 12,
//                 color: "#7dd3fc"
//               }}>
//                 {s}
//               </span>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Model reasoning */}
//       {explanation.model_reasoning && (
//         <div style={{ marginBottom: 10 }}>
//           <div style={{
//             fontSize: 11,
//             color: "#a5b4fc",
//             fontWeight: 600,
//             textTransform: "uppercase",
//             marginBottom: 6
//           }}>
//             Model Reasoning
//           </div>

//           <div style={{
//             fontSize: 13,
//             color: "#94a3b8",
//             lineHeight: 1.6,
//             padding: "10px 12px",
//             background: "rgba(255,255,255,0.02)",
//             borderRadius: 10,
//             border: "1px solid rgba(129,140,248,0.1)"
//           }}>
//             {explanation.model_reasoning}
//           </div>
//         </div>
//       )}

//       {/* Why rejected */}
//       {explanation.why_previous_rejected && (
//         <div style={{
//           padding: "10px 12px",
//           background: "rgba(245,158,11,0.06)",
//           borderRadius: 10,
//           borderLeft: "3px solid #f59e0b"
//         }}>
//           <div style={{
//             fontSize: 11,
//             color: "#fbbf24",
//             fontWeight: 600,
//             marginBottom: 4
//           }}>
//             Previous Hypothesis Rejected
//           </div>

//           <div style={{
//             fontSize: 12,
//             color: "#94a3b8"
//           }}>
//             {explanation.why_previous_rejected}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

//////////////////////////////////          to  add new feature ????????????????????????? ???????????///////////////////////////////

// export default function ConfidenceGraph({ confidence, explanation }) {

//   // ── BUG 1 FIX: confidence=0 is falsy, use explicit undefined/null check ──
//   if (confidence === undefined || confidence === null || !explanation) return null;

//   // ── BUG 2 FIX: backend sends integer (e.g. 72), don't multiply by 100 ──
//   const scoreNum = parseFloat(confidence);
//   const pct = isNaN(scoreNum) ? 0 : Math.min(scoreNum, 100);

//   // ── Colour changes based on confidence level ──
//   const barColor =
//     pct >= 75 ? "linear-gradient(90deg, #34d399, #10b981)" :
//     pct >= 50 ? "linear-gradient(90deg, #818cf8, #38bdf8)" :
//                 "linear-gradient(90deg, #f59e0b, #ef4444)";

//   const scoreColor =
//     pct >= 75 ? "#34d399" :
//     pct >= 50 ? "#818cf8" :
//                 "#f59e0b";

//   const levelLabel =
//     pct >= 75 ? "High Confidence" :
//     pct >= 50 ? "Moderate Confidence" :
//                 "Low Confidence — consult a doctor";

//   return (
//     <div style={{
//       background: "linear-gradient(135deg, rgba(129,140,248,0.07), rgba(56,189,248,0.05))",
//       borderRadius: 16,
//       padding: "16px 18px",
//       border: "1px solid rgba(129,140,248,0.2)",
//       animation: "fadeIn 0.4s ease"
//     }}>
//       <style>{`
//         @keyframes fadeIn {
//           from { opacity: 0; transform: translateY(8px); }
//           to   { opacity: 1; transform: translateY(0); }
//         }
//         @keyframes barGrow {
//           from { width: 0%; }
//           to   { width: var(--target-w); }
//         }
//       `}</style>

//       {/* ── Header ── */}
//       <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14 }}>
//         <div style={{
//           width: 30, height: 30, borderRadius: 8,
//           background: "rgba(129,140,248,0.15)",
//           display: "flex", alignItems: "center", justifyContent: "center",
//           fontSize: 15
//         }}>🔬</div>

//         <div>
//           <div style={{ fontWeight: 700, fontSize: 14, color: "#a5b4fc" }}>
//             Diagnosis Confidence
//           </div>
//           <div style={{ fontSize: 11, color: "#475569", marginTop: 1 }}>
//             Why the AI reached this conclusion
//           </div>
//         </div>
//       </div>

//       {/* ── Confidence Score + Bar ── */}
//       <div style={{
//         padding: "12px 14px",
//         background: "rgba(129,140,248,0.08)",
//         borderRadius: 12,
//         marginBottom: 14,
//         border: "1px solid rgba(129,140,248,0.15)"
//       }}>
//         <div style={{
//           display: "flex", justifyContent: "space-between",
//           alignItems: "center", marginBottom: 4
//         }}>
//           <div>
//             <span style={{ fontSize: 12, color: "#94a3b8", fontWeight: 500 }}>
//               Confidence Score
//             </span>
//             {/* ── BUG 3 FIX: show level label next to score ── */}
//             <div style={{ fontSize: 10, color: scoreColor, marginTop: 2, fontWeight: 600 }}>
//               {levelLabel}
//             </div>
//           </div>

//           <span style={{
//             fontWeight: 800, fontSize: 26,
//             color: scoreColor,
//             fontVariantNumeric: "tabular-nums"
//           }}>
//             {pct}%
//           </span>
//         </div>

//         {/* Progress bar */}
//         <div style={{
//           height: 7, background: "rgba(255,255,255,0.06)",
//           borderRadius: 10, overflow: "hidden", marginTop: 8
//         }}>
//           <div style={{
//             height: "100%",
//             width: `${pct}%`,
//             background: barColor,
//             borderRadius: 10,
//             animation: `barGrow 1s cubic-bezier(0.34,1.56,0.64,1) forwards`,
//             "--target-w": `${pct}%`
//           }} />
//         </div>
//       </div>

//       {/* ── Symptoms Matched ── */}
//       {/* BUG 4 FIX: backend key is "symptom_match" — using correct key */}
//       {Array.isArray(explanation.symptom_match) && explanation.symptom_match.length > 0 && (
//         <div style={{ marginBottom: 12 }}>
//           <div style={{
//             fontSize: 11, color: "#38bdf8", fontWeight: 600,
//             textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 8
//           }}>
//             Symptoms You Reported
//           </div>

//           <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
//             {explanation.symptom_match.map((s, i) => (
//               <span key={i} style={{
//                 padding: "4px 10px",
//                 background: "rgba(56,189,248,0.1)",
//                 border: "1px solid rgba(56,189,248,0.2)",
//                 borderRadius: 20, fontSize: 12, color: "#7dd3fc"
//               }}>
//                 {s.replace(/_/g, " ")}
//               </span>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* ── Model Reasoning ── */}
//       {explanation.model_reasoning && (
//         <div style={{ marginBottom: 12 }}>
//           <div style={{
//             fontSize: 11, color: "#a5b4fc", fontWeight: 600,
//             textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 6
//           }}>
//             How the AI decided
//           </div>

//           <div style={{
//             fontSize: 13, color: "#94a3b8", lineHeight: 1.65,
//             padding: "10px 12px",
//             background: "rgba(255,255,255,0.02)",
//             borderRadius: 10,
//             border: "1px solid rgba(129,140,248,0.1)"
//           }}>
//             {explanation.model_reasoning}
//           </div>
//         </div>
//       )}

//       {/* ── Why previous rejected (only shown if non-empty) ── */}
//       {explanation.why_previous_rejected && (
//         <div style={{
//           padding: "10px 12px",
//           background: "rgba(245,158,11,0.06)",
//           borderRadius: 10,
//           borderLeft: "3px solid #f59e0b"
//         }}>
//           <div style={{
//             fontSize: 11, color: "#fbbf24", fontWeight: 600, marginBottom: 4
//           }}>
//             Other Conditions Considered
//           </div>
//           <div style={{ fontSize: 12, color: "#94a3b8" }}>
//             {explanation.why_previous_rejected}
//           </div>
//         </div>
//       )}

//       {/* ── Disclaimer ── */}
//       <div style={{
//         marginTop: 12,
//         padding: "8px 12px",
//         background: "rgba(239,68,68,0.05)",
//         borderRadius: 8,
//         border: "1px solid rgba(239,68,68,0.1)",
//         fontSize: 11,
//         color: "#94a3b8",
//         lineHeight: 1.5
//       }}>
//         This is an AI screening tool, not a medical diagnosis. Always consult a qualified doctor.
//       </div>
//     </div>
//   );
// }

////////////////////// new idea unlocked /////////////////

// export default function ConfidenceGraph({ confidence, explanation }) {

//   if (confidence === undefined || confidence === null || !explanation) return null;

//   const scoreNum = parseFloat(confidence);
//   const pct = isNaN(scoreNum) ? 0 : Math.min(scoreNum, 100);

//   const barColor =
//     pct >= 75 ? "linear-gradient(90deg, #34d399, #10b981)" :
//     pct >= 50 ? "linear-gradient(90deg, #818cf8, #38bdf8)" :
//                 "linear-gradient(90deg, #f59e0b, #ef4444)";

//   const scoreColor =
//     pct >= 75 ? "#34d399" :
//     pct >= 50 ? "#818cf8" : "#f59e0b";

//   const levelLabel =
//     pct >= 75 ? "High Confidence" :
//     pct >= 50 ? "Moderate Confidence" :
//                 "Low — please see a doctor";

//   return (
//     <div style={{
//       background: "#1e1b4b",
//       borderRadius: 16,
//       padding: "16px 18px",
//       border: "1px solid rgba(129,140,248,0.4)",
//       marginBottom: 12,
//       animation: "cgFadeIn 0.4s ease"
//     }}>
//       <style>{`
//         @keyframes cgFadeIn {
//           from { opacity: 0; transform: translateY(8px); }
//           to   { opacity: 1; transform: translateY(0); }
//         }
//         @keyframes cgBarGrow {
//           from { width: 0%; }
//           to   { width: var(--cg-w); }
//         }
//       `}</style>

//       {/* Header */}
//       <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14 }}>
//         <div style={{
//           width: 32, height: 32, borderRadius: 8,
//           background: "rgba(129,140,248,0.25)",
//           display: "flex", alignItems: "center", justifyContent: "center",
//           fontSize: 16, flexShrink: 0
//         }}>🔬</div>
//         <div>
//           <div style={{ fontWeight: 700, fontSize: 14, color: "#a5b4fc" }}>
//             Diagnosis Confidence
//           </div>
//           <div style={{ fontSize: 11, color: "#64748b", marginTop: 1 }}>
//             Why the AI reached this conclusion
//           </div>
//         </div>
//       </div>

//       {/* Score */}
//       <div style={{
//         padding: "12px 14px",
//         background: "rgba(129,140,248,0.12)",
//         borderRadius: 12, marginBottom: 14,
//         border: "1px solid rgba(129,140,248,0.2)"
//       }}>
//         <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
//           <div>
//             <div style={{ fontSize: 12, color: "#94a3b8", fontWeight: 500 }}>Confidence Score</div>
//             <div style={{ fontSize: 10, color: scoreColor, marginTop: 2, fontWeight: 600 }}>{levelLabel}</div>
//           </div>
//           <span style={{ fontWeight: 800, fontSize: 28, color: scoreColor, fontVariantNumeric: "tabular-nums" }}>
//             {pct}%
//           </span>
//         </div>
//         <div style={{ height: 8, background: "rgba(255,255,255,0.06)", borderRadius: 10, overflow: "hidden", marginTop: 8 }}>
//           <div style={{
//             height: "100%", width: `${pct}%`, background: barColor, borderRadius: 10,
//             animation: "cgBarGrow 1.2s cubic-bezier(0.34,1.56,0.64,1) forwards",
//             "--cg-w": `${pct}%`
//           }} />
//         </div>
//       </div>

//       {/* Symptoms */}
//       {Array.isArray(explanation.symptom_match) && explanation.symptom_match.length > 0 && (
//         <div style={{ marginBottom: 12 }}>
//           <div style={{ fontSize: 11, color: "#38bdf8", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 8 }}>
//             Symptoms You Reported
//           </div>
//           <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
//             {explanation.symptom_match.map((s, i) => (
//               <span key={i} style={{
//                 padding: "4px 10px", background: "rgba(56,189,248,0.15)",
//                 border: "1px solid rgba(56,189,248,0.3)", borderRadius: 20, fontSize: 12, color: "#7dd3fc"
//               }}>
//                 {s.replace(/_/g, " ")}
//               </span>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Reasoning */}
//       {explanation.model_reasoning && (
//         <div style={{ marginBottom: 12 }}>
//           <div style={{ fontSize: 11, color: "#a5b4fc", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 6 }}>
//             How the AI decided
//           </div>
//           <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.65, padding: "10px 12px", background: "rgba(255,255,255,0.03)", borderRadius: 10, border: "1px solid rgba(129,140,248,0.15)" }}>
//             {explanation.model_reasoning}
//           </div>
//         </div>
//       )}

//       {/* Alternatives */}
//       {explanation.why_previous_rejected && (
//         <div style={{ padding: "10px 12px", background: "rgba(245,158,11,0.08)", borderRadius: 10, borderLeft: "3px solid #f59e0b", marginBottom: 12 }}>
//           <div style={{ fontSize: 11, color: "#fbbf24", fontWeight: 600, marginBottom: 4 }}>Other Conditions Considered</div>
//           <div style={{ fontSize: 12, color: "#94a3b8", lineHeight: 1.5 }}>{explanation.why_previous_rejected}</div>
//         </div>
//       )}

//       {/* Disclaimer */}
//       <div style={{ padding: "8px 12px", background: "rgba(239,68,68,0.07)", borderRadius: 8, border: "1px solid rgba(239,68,68,0.15)", fontSize: 11, color: "#94a3b8", lineHeight: 1.5 }}>
//         ⚠️ AI screening tool only — not a medical diagnosis. Always consult a qualified doctor.
//       </div>
//     </div>
//   );
// }


///////////////new update /////////////////////

export default function ConfidenceGraph({ confidence, explanation }) {

  if (confidence === undefined || confidence === null || !explanation || !explanation.symptom_match) return null;

  const scoreNum = Number(confidence);
  const pct = isNaN(scoreNum) ? 0 : Math.min(scoreNum, 100);

  const barColor =
    pct >= 75 ? "linear-gradient(90deg, #34d399, #10b981)" :
    pct >= 50 ? "linear-gradient(90deg, #818cf8, #38bdf8)" :
                "linear-gradient(90deg, #f59e0b, #ef4444)";

  const scoreColor =
    pct >= 75 ? "#34d399" :
    pct >= 50 ? "#818cf8" : "#f59e0b";

  const levelLabel =
    pct >= 75 ? "High Confidence" :
    pct >= 50 ? "Moderate Confidence" :
                "Low — please see a doctor";

  return (
    <div style={{
      background: "#1e1b4b",
      borderRadius: 16,
      padding: "16px 18px",
      border: "1px solid rgba(129,140,248,0.4)",
      marginBottom: 12,
      animation: "cgFadeIn 0.4s ease"
    }}>
      <style>{`
        @keyframes cgFadeIn {
          from { opacity: 0; transform: translateY(8px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes cgBarGrow {
          from { width: 0%; }
          to   { width: var(--cg-w); }
        }
      `}</style>

      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14 }}>
        <div style={{
          width: 32, height: 32, borderRadius: 8,
          background: "rgba(129,140,248,0.25)",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 16, flexShrink: 0
        }}>🔬</div>
        <div>
          <div style={{ fontWeight: 700, fontSize: 14, color: "#a5b4fc" }}>
            Diagnosis Confidence
          </div>
          <div style={{ fontSize: 11, color: "#64748b", marginTop: 1 }}>
            Why the AI reached this conclusion
          </div>
        </div>
      </div>

      <div style={{
        padding: "12px 14px",
        background: "rgba(129,140,248,0.12)",
        borderRadius: 12, marginBottom: 14,
        border: "1px solid rgba(129,140,248,0.2)"
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
          <div>
            <div style={{ fontSize: 12, color: "#94a3b8", fontWeight: 500 }}>Confidence Score</div>
            <div style={{ fontSize: 10, color: scoreColor, marginTop: 2, fontWeight: 600 }}>{levelLabel}</div>
          </div>
          <span style={{ fontWeight: 800, fontSize: 28, color: scoreColor, fontVariantNumeric: "tabular-nums" }}>
            {pct}%
          </span>
        </div>
        <div style={{ height: 8, background: "rgba(255,255,255,0.06)", borderRadius: 10, overflow: "hidden", marginTop: 8 }}>
          <div style={{
            height: "100%", width: `${pct}%`, background: barColor, borderRadius: 10,
            animation: "cgBarGrow 1.2s cubic-bezier(0.34,1.56,0.64,1) forwards",
            "--cg-w": `${pct}%`
          }} />
        </div>
      </div>

      {Array.isArray(explanation.symptom_match) && explanation.symptom_match.length > 0 && (
        <div style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 11, color: "#38bdf8", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 8 }}>
            Symptoms You Reported
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {explanation.symptom_match.map((s, i) => (
              <span key={i} style={{
                padding: "4px 10px", background: "rgba(56,189,248,0.15)",
                border: "1px solid rgba(56,189,248,0.3)", borderRadius: 20, fontSize: 12, color: "#7dd3fc"
              }}>
                {String(s).replace(/_/g, " ")}
              </span>
            ))}
          </div>
        </div>
      )}

      {explanation.model_reasoning && (
        <div style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 11, color: "#a5b4fc", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 6 }}>
            How the AI decided
          </div>
          <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.65, padding: "10px 12px", background: "rgba(255,255,255,0.03)", borderRadius: 10, border: "1px solid rgba(129,140,248,0.15)" }}>
            {explanation.model_reasoning}
          </div>
        </div>
      )}

      {explanation.why_previous_rejected !== undefined && explanation.why_previous_rejected !== "" && (
        <div style={{ padding: "10px 12px", background: "rgba(245,158,11,0.08)", borderRadius: 10, borderLeft: "3px solid #f59e0b", marginBottom: 12 }}>
          <div style={{ fontSize: 11, color: "#fbbf24", fontWeight: 600, marginBottom: 4 }}>Other Conditions Considered</div>
          <div style={{ fontSize: 12, color: "#94a3b8", lineHeight: 1.5 }}>{explanation.why_previous_rejected}</div>
        </div>
      )}

      <div style={{ padding: "8px 12px", background: "rgba(239,68,68,0.07)", borderRadius: 8, border: "1px solid rgba(239,68,68,0.15)", fontSize: 11, color: "#94a3b8", lineHeight: 1.5 }}>
         AI screening tool only — not a medical diagnosis. Always consult a qualified doctor.
      </div>
    </div>
  );
}