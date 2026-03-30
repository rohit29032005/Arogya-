// import { useState } from "react";

// export default function ChatBox() {
//   const [messages, setMessages] = useState([]);
//   const [currentQuestion, setCurrentQuestion] = useState(null);
//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [started, setStarted] = useState(false);

//   async function startConsultation() {
//     if (!input.trim()) return;

//     setStarted(true);
//     setMessages(m => [...m, { text: input, sender: "user" }]);
//     setLoading(true);

//     const res = await fetch("http://127.0.0.1:5000/predict", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ symptoms: input })
//     }).then(r => r.json());

//     setLoading(false);

//     setMessages(m => [
//       ...m,
//       { text: `Possible condition: ${res.predicted_disease}`, sender: "bot" }
//     ]);

//     if (res.status === "need_clarification") {
//       setCurrentQuestion(res.question);
//       setMessages(m => [...m, { text: res.question, sender: "bot" }]);
//     }

//     setInput("");
//   }

//   async function answerQuestion(ans) {
//     setMessages(m => [...m, { text: ans, sender: "user" }]);
//     setLoading(true);

//     const res = await fetch("http://127.0.0.1:5000/predict", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ answer: ans })
//     }).then(r => r.json());

//     setLoading(false);

//     if (res.status === "need_clarification") {
//       setCurrentQuestion(res.question);
//       setMessages(m => [...m, { text: res.question, sender: "bot" }]);
//     } else {
//       setCurrentQuestion(null);
//       setMessages(m => [
//         ...m,
//         { text: JSON.stringify(res, null, 2), sender: "bot" }
//       ]);
//     }
//   }

//   return (
//     <div>
//       {messages.map((m, i) => (
//         <div
//           key={i}
//           style={{
//             textAlign: m.sender === "user" ? "right" : "left",
//             margin: "8px"
//           }}
//         >
//           {m.text}
//         </div>
//       ))}

//       {!started && (
//         <div>
//           <input
//             value={input}
//             onChange={e => setInput(e.target.value)}
//             placeholder="Describe your symptoms..."
//           />
//           <button onClick={startConsultation}>
//             Start Consultation
//           </button>
//         </div>
//       )}

//       {currentQuestion && (
//         <div>
//           <button onClick={() => answerQuestion("yes")}>Yes</button>
//           <button onClick={() => answerQuestion("no")}>No</button>
//           <button onClick={() => answerQuestion("not sure")}>Not Sure</button>
//         </div>
//       )}

//       {loading && <p>Doctor is thinking...</p>}
//     </div>
//   );
// }


// addding uuuid concept

// import { useState } from "react";

// export default function ChatBox() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [currentQuestion, setCurrentQuestion] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [started, setStarted] = useState(false);
//   const [sessionId, setSessionId] = useState(null);

//   // 🔹 Start new consultation
//   async function startConsultation() {
//     if (!input.trim()) return;

//     setStarted(true);
//     setMessages([{ text: input, sender: "user" }]);
//     setLoading(true);

//     const res = await fetch("http://127.0.0.1:5000/predict", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({
//         symptoms: input,
//         session_id: sessionId
//       })
//     }).then(r => r.json());

//     setLoading(false);

//     // 🔹 Store session id from backend
//     if (res.session_id) {
//       setSessionId(res.session_id);
//     }

//     setMessages(m => [
//       ...m,
//       {
//         text: `Possible condition: ${res.predicted_disease}`,
//         sender: "bot"
//       },
//       {
//         text: res.question,
//         sender: "bot"
//       }
//     ]);

//     setCurrentQuestion(res.question);
//     setInput("");
//   }

//   // 🔹 Answer current question
//   async function answerQuestion(ans) {
//     setMessages(m => [...m, { text: ans, sender: "user" }]);
//     setLoading(true);

//     const res = await fetch("http://127.0.0.1:5000/predict", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({
//         answer: ans,
//         session_id: sessionId
//       })
//     }).then(r => r.json());

//     setLoading(false);

//     // 🔹 Update session if backend sends again
//     if (res.session_id) {
//       setSessionId(res.session_id);
//     }

//     if (res.status === "need_clarification") {
//       setCurrentQuestion(res.question);
//       setMessages(m => [...m, { text: res.question, sender: "bot" }]);
//       return;
//     }

//     // 🔹 Final / alternative response
//     setCurrentQuestion(null);
//     setStarted(false);
//     setSessionId(null);

//     setMessages(m => [
//       ...m,
//       {
//         text: JSON.stringify(res, null, 2),
//         sender: "bot"
//       }
//     ]);
//   }

//   // 🔹 Restart consultation
//   function resetChat() {
//     setMessages([]);
//     setInput("");
//     setCurrentQuestion(null);
//     setStarted(false);
//     setSessionId(null);
//   }

//   return (
//     <div style={{ maxWidth: "600px", margin: "auto" }}>
//       <h2>Arogya AI – Doctor Chat</h2>

//       <div style={{ minHeight: "300px", border: "1px solid #ccc", padding: "10px" }}>
//         {messages.map((m, i) => (
//           <div
//             key={i}
//             style={{
//               textAlign: m.sender === "user" ? "right" : "left",
//               margin: "6px 0"
//             }}
//           >
//             <b>{m.sender === "user" ? "You" : "Doctor"}:</b> {m.text}
//           </div>
//         ))}
//         {loading && <p>Doctor is thinking…</p>}
//       </div>

//       {!started && (
//         <div style={{ marginTop: "10px" }}>
//           <input
//             value={input}
//             onChange={e => setInput(e.target.value)}
//             placeholder="Describe your symptoms..."
//             style={{ width: "70%" }}
//           />
//           <button onClick={startConsultation}>Start Consultation</button>
//         </div>
//       )}

//       {currentQuestion && (
//         <div style={{ marginTop: "10px" }}>
//           <button onClick={() => answerQuestion("yes")}>Yes</button>
//           <button onClick={() => answerQuestion("no")}>No</button>
//           <button onClick={() => answerQuestion("not sure")}>Not Sure</button>
//         </div>
//       )}

//       <div style={{ marginTop: "10px" }}>
//         <button onClick={resetChat}>Restart</button>
//       </div>
//     </div>
//   );
// }

//rendering now the llm explanation

// import { useState } from "react";
// import MessageBubble from "./MessageBubble";
// import AyurvedaCard from "./AyurvedaCard";
// import ConfidenceGraph from "./ConfidenceGraph";

// export default function ChatBox() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [sessionId, setSessionId] = useState(null);
//   const [finalData, setFinalData] = useState(null);

//   const send = async () => {
//     if (!input.trim()) return;

//     setMessages(prev => [...prev, { sender: "user", text: input }]);

//     const payload = sessionId
//       ? { session_id: sessionId, answer: input }
//       : { symptoms: input };

//     const res = await fetch("http://127.0.0.1:5000/predict", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(payload)
//     });

//     const data = await res.json();

//     if (data.session_id) setSessionId(data.session_id);

//     if (data.question) {
//       setMessages(prev => [...prev, { sender: "doctor", text: data.question }]);
//     }

//     if (data.status === "final") {
//       setMessages(prev => [
//         ...prev,
//         { sender: "doctor", text: `Final condition: ${data.predicted_disease}` }
//       ]);

//       if (data.llm_explanation) {
//         setMessages(prev => [
//           ...prev,
//           { sender: "doctor", text: data.llm_explanation }
//         ]);
//       }

//       setFinalData(data);
//     }

//     if (data.status === "hypothesis_rejected") {
//       setMessages(prev => [
//         ...prev,
//         { sender: "doctor", text: data.message }
//       ]);
//     }

//     setInput("");
//   };

//   return (
//     <div className="chat-container">
//       <div className="chat-box">
//         {messages.map((m, i) => (
//           <MessageBubble key={i} sender={m.sender} text={m.text} />
//         ))}
//       </div>

//       <input
//         value={input}
//         onChange={e => setInput(e.target.value)}
//         placeholder="Describe your symptoms..."
//       />
//       <button onClick={send}>Start Consultation</button>

//       {finalData && (
//         <>
//           <ConfidenceGraph data={finalData} />
//           <AyurvedaCard ayurveda={finalData.ayurveda} />
//         </>
//       )}
//     </div>
//   );
// }
////here
// import { useState } from "react";
// import MessageBubble from "./MessageBubble";
// import AyurvedaCard from "./AyurvedaCard";
// import ConfidenceGraph from "./ConfidenceGraph";

// export default function ChatBox() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [sessionId, setSessionId] = useState(null);
//   const [finalResult, setFinalResult] = useState(null);

//   const send = async () => {
//     if (!input.trim()) return;

//     // user message
//     setMessages(prev => [...prev, { sender: "user", text: input }]);

//     const payload = sessionId
//       ? { session_id: sessionId, answer: input }
//       : { symptoms: input };

//     const res = await fetch("http://127.0.0.1:5000/predict", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(payload)
//     });

//     const data = await res.json();

//     // store session id
//     if (data.session_id) {
//       setSessionId(data.session_id);
//     }

//     // agentic questions
//     if (data.question) {
//       setMessages(prev => [
//         ...prev,
//         { sender: "doctor", text: data.question }
//       ]);
//     }

//     // hypothesis rejected
//     if (data.status === "hypothesis_rejected") {
//       setMessages(prev => [
//         ...prev,
//         { sender: "doctor", text: data.message }
//       ]);
//     }

//     // final diagnosis
//     if (data.status === "final") {
//       setMessages(prev => [
//         ...prev,
//         {
//           sender: "doctor",
//           text: `Final condition: ${data.predicted_disease}`
//         }
//       ]);

//       if (data.llm_explanation) {
//         setMessages(prev => [
//           ...prev,
//           { sender: "doctor", text: data.llm_explanation }
//         ]);
//       }

//       setFinalResult(data);
//     }

//     setInput("");
//   };

//   return (
//     <div className="chat-container">
//       <div className="chat-box">
//         {messages.map((m, i) => (
//           <MessageBubble key={i} sender={m.sender} text={m.text} />
//         ))}
//       </div>

//       <input
//         value={input}
//         onChange={e => setInput(e.target.value)}
//         placeholder="Describe your symptoms..."
//       />
//       <button onClick={send}>Start Consultation</button>

//       {/* 🔍 Explainable AI – Confidence Reasoning */}
//       {finalResult && finalResult.confidence_explanation && (
//         <ConfidenceGraph
//           confidence={finalResult.confidence}
//           explanation={finalResult.confidence_explanation}
//         />
//       )}

//       {/* 🌿 Ayurveda Card – only after final confirmation */}
//       {finalResult && finalResult.ayurveda && (
//         <AyurvedaCard ayurveda={finalResult.ayurveda} />
//       )}
//     </div>
//   );
// }
// import { useState } from "react";
// import MessageBubble from "./MessageBubble";
// import AyurvedaCard from "./AyurvedaCard";
// import ConfidenceGraph from "./ConfidenceGraph";

// export default function ChatBox() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [sessionId, setSessionId] = useState(null);
//   const [finalData, setFinalData] = useState(null);
//   const [typing, setTyping] = useState(false);

//   const send = async () => {
//     if (!input.trim()) return;

//     setMessages(prev => [...prev, { sender: "user", text: input }]);
//     setInput("");
//     setTyping(true);

//     const payload = sessionId
//       ? { session_id: sessionId, answer: input }
//       : { symptoms: input };

//     const res = await fetch("http://127.0.0.1:5000/predict", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(payload)
//     });

//     const data = await res.json();
//     setTyping(false);

//     if (data.session_id) setSessionId(data.session_id);

//     if (data.question) {
//       setMessages(prev => [...prev, { sender: "doctor", text: data.question }]);
//     }

//     if (data.status === "final") {
//       setMessages(prev => [
//         ...prev,
//         { sender: "doctor", text: `Final condition: ${data.predicted_disease}` }
//       ]);

//       if (data.llm_explanation) {
//         setMessages(prev => [
//           ...prev,
//           { sender: "doctor", text: data.llm_explanation }
//         ]);
//       }

//       setFinalData(data);
//     }

//     if (data.status === "hypothesis_rejected") {
//       setMessages(prev => [
//         ...prev,
//         { sender: "doctor", text: data.message }
//       ]);
//     }
//   };

//   return (
//     <div className="chat-container">
//       <div className="chat-header">Arogya AI – Doctor Chat</div>

//       <div className="chat-box">
//         {messages.map((m, i) => (
//           <MessageBubble key={i} sender={m.sender} text={m.text} />
//         ))}

//         {typing && <div className="typing">Doctor is typing…</div>}
//       </div>

//       <div className="chat-input">
//         <input
//           value={input}
//           onChange={e => setInput(e.target.value)}
//           placeholder="Type your symptoms here..."
//         />
//         <button onClick={send}>Send</button>
//       </div>

//       {finalData && (
//         <>
//           <ConfidenceGraph data={finalData} />
//           <AyurvedaCard ayurveda={finalData.ayurveda} />
//         </>
//       )}
//     </div>
//   );
// }
// import { useState } from "react";
// import MessageBubble from "./MessageBubble";
// import AyurvedaCard from "./AyurvedaCard";
// import ConfidenceGraph from "./ConfidenceGraph";

// export default function ChatBox() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [sessionId, setSessionId] = useState(null);
//   const [finalData, setFinalData] = useState(null);
//   const [typing, setTyping] = useState(false);

//   const send = async () => {
//     if (!input.trim()) return;

//     setMessages(prev => [...prev, { sender: "user", text: input }]);
//     setInput("");
//     setTyping(true);

//     const payload = sessionId
//       ? { session_id: sessionId, answer: input }
//       : { symptoms: input };

//     const res = await fetch("http://127.0.0.1:5000/predict", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(payload)
//     });

//     const data = await res.json();
//     setTyping(false);

//     if (data.session_id) setSessionId(data.session_id);

//     if (data.question) {
//       setMessages(prev => [...prev, { sender: "doctor", text: data.question }]);
//     }

//     if (data.status === "final") {
//       setMessages(prev => [
//         ...prev,
//         { sender: "doctor", text: `Final condition: ${data.predicted_disease}` }
//       ]);

//       if (data.llm_explanation) {
//         setMessages(prev => [
//           ...prev,
//           { sender: "doctor", text: data.llm_explanation }
//         ]);
//       }

//       setFinalData(data);
//     }

//     if (data.status === "hypothesis_rejected") {
//       setMessages(prev => [
//         ...prev,
//         { sender: "doctor", text: data.message }
//       ]);
//     }
//   };

//   return (
//     <div className="chat-container">
//       <div className="chat-header">Arogya AI – Doctor Chat</div>

//       <div className="chat-box">
//         {messages.map((m, i) => (
//           <MessageBubble key={i} sender={m.sender} text={m.text} />
//         ))}
//         {typing && <div className="typing">Doctor is typing…</div>}
//       </div>

//       <div className="chat-input">
//         <input
//           value={input}
//           onChange={e => setInput(e.target.value)}
//           placeholder="Type your symptoms here..."
//         />
//         <button onClick={send}>Send</button>
//       </div>

//       {/* ✅ CONFIDENCE + AYURVEDA RESTORED */}
//       {finalData && (
//         <>
//           {finalData.confidence_explanation && (
//             <ConfidenceGraph
//               confidence={finalData.confidence}
//               explanation={finalData.confidence_explanation}
//             />
//           )}
//           {finalData.ayurveda && <AyurvedaCard ayurveda={finalData.ayurveda} />}
//         </>
//       )}
//     </div>
//   );
// }

///new updated//////////


// import { useState } from "react";
// import MessageBubble from "./MessageBubble";
// import AyurvedaCard from "./AyurvedaCard";
// import ConfidenceGraph from "./ConfidenceGraph";

// export default function ChatBox() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [sessionId, setSessionId] = useState(null);
//   const [finalData, setFinalData] = useState(null);
//   const [typing, setTyping] = useState(false);

//   const send = async () => {
//     if (!input.trim()) return;

//     // user message
//     setMessages(prev => [...prev, { sender: "user", text: input }]);
//     setTyping(true);

//     const payload = sessionId
//       ? { session_id: sessionId, answer: input }
//       : { symptoms: input };

//     try {
//       const res = await fetch("http://127.0.0.1:5000/predict", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(payload)
//       });

//       const data = await res.json();
//       setTyping(false);

//       // save session id
//       if (data.session_id) setSessionId(data.session_id);

//       /* -------------------------
//          QUESTION FLOW
//       --------------------------*/
//       if (data.question) {
//         setMessages(prev => [
//           ...prev,
//           { sender: "doctor", text: data.question }
//         ]);
//         setInput("");
//         return;
//       }

//       /* -------------------------
//          HYPOTHESIS REJECTED
//       --------------------------*/
//       if (data.status === "hypothesis_rejected") {
//         setMessages(prev => [
//           ...prev,
//           { sender: "doctor", text: data.message }
//         ]);
//         setInput("");
//         return;
//       }

//       /* -------------------------
//          FINAL RESULT
//       --------------------------*/
//       if (data.status === "final") {
//         setMessages(prev => [
//           ...prev,
//           {
//             sender: "doctor",
//             text: `Final condition: ${data.predicted_disease}`
//           }
//         ]);

//         // LLM explanation (important)
//         if (data.llm_explanation) {
//           setMessages(prev => [
//             ...prev,
//             { sender: "doctor", text: data.llm_explanation }
//           ]);
//         }

//         setFinalData(data);
//       }
//     } catch (err) {
//       setTyping(false);
//       setMessages(prev => [
//         ...prev,
//         { sender: "doctor", text: "Something went wrong. Please try again." }
//       ]);
//     }

//     setInput("");
//   };

//   return (
//   <div className="chat-container">
//     {/* HEADER */}
//     <div className="chat-header">Arogya AI – Doctor Chat</div>

//     {/* CHAT AREA */}
//     <div className="chat-wrapper">
//       <div className="chat-box">
//         {messages.map((m, i) => (
//           <MessageBubble key={i} sender={m.sender} text={m.text} />
//         ))}

//         {typing && (
//           <div className="typing">
//             Doctor is typing<span className="dots">...</span>
//           </div>
//         )}
//       </div>
//     </div>

//     {/* INPUT BAR */}
//     <div className="chat-input">
//       <input
//         value={input}
//         onChange={e => setInput(e.target.value)}
//         placeholder="Type your symptoms here..."
//         onKeyDown={e => e.key === "Enter" && send()}
//       />
//       <button onClick={send}>Send</button>
//     </div>

//     {/* RESULT SECTION (SEPARATE FLOW) */}
//     {finalData && (
//       <div className="result-section">
//         {finalData.confidence_explanation && (
//           <ConfidenceGraph
//             confidence={finalData.confidence}
//             explanation={finalData.confidence_explanation}
//           />
//         )}

//         {finalData.ayurveda && (
//           <AyurvedaCard ayurveda={finalData.ayurveda} />
//         )}
//       </div>
//     )}
//   </div>
// );

// }


//new function intiliazed /////////


// import { useState, useRef, useEffect } from "react";
// import MessageBubble from "./MessageBubble";
// import AyurvedaCard from "./AyurvedaCard";
// import ConfidenceGraph from "./ConfidenceGraph";

// export default function ChatBox() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [sessionId, setSessionId] = useState(null);
//   const [finalData, setFinalData] = useState(null);
//   const [typing, setTyping] = useState(false);
//   const bottomRef = useRef(null);

//   // Auto-scroll to latest message
//   useEffect(() => {
//     bottomRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [messages, typing]);

//   const send = async () => {
//     if (!input.trim()) return;

//     setMessages(prev => [...prev, { sender: "user", text: input }]);
//     setTyping(true);

//     const payload = sessionId
//       ? { session_id: sessionId, answer: input }
//       : { symptoms: input };

//     try {
//       const res = await fetch("http://127.0.0.1:5000/predict", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(payload)
//       });

//       const data = await res.json();
//       setTyping(false);

//       if (data.session_id) setSessionId(data.session_id);

//       if (data.question) {
//         setMessages(prev => [...prev, { sender: "doctor", text: data.question }]);
//         setInput("");
//         return;
//       }

//       if (data.status === "hypothesis_rejected") {
//         setMessages(prev => [...prev, { sender: "doctor", text: data.message }]);
//         setInput("");
//         return;
//       }

//       if (data.status === "final") {
//         setMessages(prev => [
//           ...prev,
//           { sender: "doctor", text: `Final condition: ${data.predicted_disease}` }
//         ]);

//         if (data.llm_explanation) {
//           setMessages(prev => [
//             ...prev,
//             { sender: "doctor", text: data.llm_explanation }
//           ]);
//         }

//         setFinalData(data);
//       }
//     } catch (err) {
//       setTyping(false);
//       setMessages(prev => [
//         ...prev,
//         { sender: "doctor", text: "Something went wrong. Please try again." }
//       ]);
//     }

//     setInput("");
//   };

//   return (
//     <div className="chat-container">

//       {/* ── HEADER ── */}
//       <div className="chat-header">
//         <div style={{ position: "relative" }}>
//           <div style={{
//             width: 38,
//             height: 38,
//             borderRadius: "50%",
//             background: "linear-gradient(135deg, #38bdf8, #818cf8)",
//             display: "flex",
//             alignItems: "center",
//             justifyContent: "center",
//             fontSize: 18,
//             boxShadow: "0 0 16px rgba(56,189,248,0.4)"
//           }}>🌿</div>
//           {/* Online dot */}
//           <div style={{
//             position: "absolute",
//             bottom: 1,
//             right: 1,
//             width: 9,
//             height: 9,
//             borderRadius: "50%",
//             background: "#10b981",
//             border: "2px solid #111827",
//             boxShadow: "0 0 6px #10b981"
//           }} />
//         </div>

//         <div style={{ flex: 1 }}>
//           <div style={{
//             fontWeight: 700,
//             fontSize: 16,
//             color: "#f0f6ff",
//             letterSpacing: "-0.01em"
//           }}>
//             Arogya AI
//           </div>
//           <div style={{
//             fontSize: 11,
//             color: "#38bdf8",
//             fontWeight: 500,
//             letterSpacing: "0.04em",
//             textTransform: "uppercase",
//             marginTop: 1
//           }}>
//             AI Health Assistant · Online
//           </div>
//         </div>

//         {/* Pulse ring decoration */}
//         <div style={{
//           width: 8,
//           height: 8,
//           borderRadius: "50%",
//           background: "#818cf8",
//           boxShadow: "0 0 10px #818cf8",
//           animation: "pulse 2s infinite"
//         }} />

//         <style>{`
//           @keyframes pulse {
//             0%, 100% { opacity: 1; transform: scale(1); }
//             50% { opacity: 0.4; transform: scale(0.7); }
//           }
//           @keyframes dotBounce {
//             0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
//             40% { transform: translateY(-5px); opacity: 1; }
//           }
//           @keyframes fadeIn {
//             from { opacity: 0; transform: translateY(6px); }
//             to { opacity: 1; transform: translateY(0); }
//           }
//         `}</style>
//       </div>

//       {/* ── CHAT BOX ── */}
//       <div className="chat-box">
//         {messages.length === 0 && (
//           <div style={{
//             flex: 1,
//             display: "flex",
//             flexDirection: "column",
//             alignItems: "center",
//             justifyContent: "center",
//             padding: "40px 20px",
//             gap: 12,
//             opacity: 0.6,
//             animation: "fadeIn 0.6s ease"
//           }}>
//             <div style={{ fontSize: 42 }}>🩺</div>
//             <div style={{ color: "#94a3b8", fontSize: 14, textAlign: "center", lineHeight: 1.6 }}>
//               Describe your symptoms below<br />and I'll help diagnose & guide you
//             </div>
//           </div>
//         )}

//         {messages.map((m, i) => (
//           <MessageBubble key={i} sender={m.sender} text={m.text} />
//         ))}

//         {typing && (
//           <div className="typing">
//             <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
//               <div style={{
//                 width: 28,
//                 height: 28,
//                 borderRadius: "50%",
//                 background: "linear-gradient(135deg, #38bdf8, #818cf8)",
//                 display: "flex",
//                 alignItems: "center",
//                 justifyContent: "center",
//                 fontSize: 12
//               }}>🌿</div>
//               <div style={{
//                 background: "#1e293b",
//                 borderRadius: "12px 12px 12px 3px",
//                 padding: "10px 16px",
//                 display: "flex",
//                 gap: 5,
//                 alignItems: "center"
//               }}>
//                 {[0, 0.18, 0.36].map((delay, i) => (
//                   <div key={i} style={{
//                     width: 6,
//                     height: 6,
//                     borderRadius: "50%",
//                     background: "#38bdf8",
//                     animation: `dotBounce 1s ${delay}s infinite`
//                   }} />
//                 ))}
//               </div>
//             </div>
//           </div>
//         )}

//         <div ref={bottomRef} />
//       </div>

//       {/* ── INPUT BAR ── */}
//       <div className="chat-input">
//         <input
//           value={input}
//           onChange={e => setInput(e.target.value)}
//           placeholder="Describe your symptoms..."
//           onKeyDown={e => e.key === "Enter" && send()}
//         />
//         <button onClick={send}>
//           <span style={{ marginRight: 6 }}>↑</span>Send
//         </button>
//       </div>

//       {/* ── RESULT CARDS ── */}
//       {finalData && (
//         <div className="result-section">
//           {finalData.confidence_explanation && (
//             <ConfidenceGraph
//               confidence={finalData.confidence}
//               explanation={finalData.confidence_explanation}
//             />
//           )}
//           {finalData.ayurveda && (
//             <AyurvedaCard ayurveda={finalData.ayurveda} />
//           )}
//         </div>
//       )}
//     </div>
//   );
// }

// new upadte for the graph visiblity ////////////////////

// import { useState, useRef, useEffect } from "react";
// import MessageBubble from "./MessageBubble";
// import AyurvedaCard from "./AyurvedaCard";
// import ConfidenceGraph from "./ConfidenceGraph";

// export default function ChatBox() {
//   const [messages, setMessages]   = useState([]);
//   const [input, setInput]         = useState("");
//   const [sessionId, setSessionId] = useState(null);
//   const [finalData, setFinalData] = useState(null);
//   const [typing, setTyping]       = useState(false);

//   // ── BUG FIX 3: track whether we are in post-result chat mode ──
//   const [chatMode, setChatMode]   = useState(false);

//   const bottomRef = useRef(null);

//   useEffect(() => {
//     bottomRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [messages, typing]);

//   const send = async () => {
//     if (!input.trim()) return;

//     const userText = input.trim();
//     setMessages(prev => [...prev, { sender: "user", text: userText }]);
//     setInput("");
//     setTyping(true);

//     // ── BUG FIX 1: after result, use "message" key not "answer" ──
//     // Backend chat handler checks: if "message" in data
//     // But old ChatBox always sent "answer" — so chat was never triggered
//     let payload;
//     if (chatMode && sessionId) {
//       payload = { session_id: sessionId, message: userText };
//     } else if (sessionId) {
//       payload = { session_id: sessionId, answer: userText };
//     } else {
//       payload = { symptoms: userText };
//     }

//     try {
//       const res  = await fetch("http://127.0.0.1:5000/predict", {
//         method:  "POST",
//         headers: { "Content-Type": "application/json" },
//         body:    JSON.stringify(payload),
//       });

//       const data = await res.json();
//       setTyping(false);

//       // Always save session id when backend sends one
//       if (data.session_id) setSessionId(data.session_id);

//       // ── POST-RESULT CHAT REPLY ──
//       if (data.status === "chat" && data.reply) {
//         setMessages(prev => [...prev, { sender: "doctor", text: data.reply }]);
//         return;
//       }

//       // ── COLLECTING QUESTIONS ──
//       if (data.status === "collecting" && data.question) {
//         setMessages(prev => [...prev, { sender: "doctor", text: data.question }]);
//         return;
//       }

//       // ── FINAL RESULT ──
//       if (data.status === "final") {
//         // Show diagnosis message
//         setMessages(prev => [
//           ...prev,
//           {
//             sender: "doctor",
//             text:   `Predicted condition: ${data.predicted_disease} (${data.confidence}% confidence)`,
//           },
//         ]);

//         // Show LLM explanation as a separate bubble
//         if (data.llm_explanation) {
//           setMessages(prev => [
//             ...prev,
//             { sender: "doctor", text: data.llm_explanation },
//           ]);
//         }

//         // Show chat hint so user knows they can ask follow-up questions
//         if (data.chat_hint) {
//           setMessages(prev => [
//             ...prev,
//             { sender: "doctor", text: data.chat_hint },
//           ]);
//         }

//         // ── BUG FIX 2: save finalData and switch to chat mode ──
//         // Old code never set chatMode = true so follow-up messages
//         // were sent as "answer" (intake key) not "message" (chat key)
//         setFinalData(data);
//         setChatMode(true);
//         return;
//       }

//       // ── ERROR FROM BACKEND ──
//       if (data.error) {
//         setMessages(prev => [
//           ...prev,
//           { sender: "doctor", text: `Error: ${data.error}` },
//         ]);
//         return;
//       }

//     } catch (err) {
//       setTyping(false);
//       setMessages(prev => [
//         ...prev,
//         { sender: "doctor", text: "Something went wrong. Please try again." },
//       ]);
//     }
//   };

//   // Reset everything for a new consultation
//   const reset = () => {
//     setMessages([]);
//     setInput("");
//     setSessionId(null);
//     setFinalData(null);
//     setChatMode(false);
//   };

//   return (
//     <div className="chat-container">

//       {/* ── HEADER ── */}
//       <div className="chat-header">
//         <div style={{ position: "relative" }}>
//           <div style={{
//             width: 38, height: 38, borderRadius: "50%",
//             background: "linear-gradient(135deg, #38bdf8, #818cf8)",
//             display: "flex", alignItems: "center", justifyContent: "center",
//             fontSize: 18, boxShadow: "0 0 16px rgba(56,189,248,0.4)"
//           }}>🌿</div>
//           <div style={{
//             position: "absolute", bottom: 1, right: 1,
//             width: 9, height: 9, borderRadius: "50%",
//             background: "#10b981", border: "2px solid #111827",
//             boxShadow: "0 0 6px #10b981"
//           }} />
//         </div>

//         <div style={{ flex: 1 }}>
//           <div style={{ fontWeight: 700, fontSize: 16, color: "#f0f6ff", letterSpacing: "-0.01em" }}>
//             Arogya AI
//           </div>
//           <div style={{
//             fontSize: 11, color: "#38bdf8", fontWeight: 500,
//             letterSpacing: "0.04em", textTransform: "uppercase", marginTop: 1
//           }}>
//             {chatMode ? "Follow-up chat active · ask anything" : "AI Health Assistant · Online"}
//           </div>
//         </div>

//         {/* New consultation button — only shown after result */}
//         {chatMode && (
//           <button
//             onClick={reset}
//             style={{
//               fontSize: 11, color: "#94a3b8",
//               background: "rgba(255,255,255,0.05)",
//               border: "1px solid rgba(255,255,255,0.1)",
//               borderRadius: 8, padding: "4px 10px",
//               cursor: "pointer"
//             }}
//           >
//             New
//           </button>
//         )}

//         <div style={{
//           width: 8, height: 8, borderRadius: "50%",
//           background: "#818cf8", boxShadow: "0 0 10px #818cf8",
//           animation: "pulse 2s infinite"
//         }} />

//         <style>{`
//           @keyframes pulse {
//             0%, 100% { opacity: 1; transform: scale(1); }
//             50%       { opacity: 0.4; transform: scale(0.7); }
//           }
//           @keyframes dotBounce {
//             0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
//             40%           { transform: translateY(-5px); opacity: 1; }
//           }
//           @keyframes fadeIn {
//             from { opacity: 0; transform: translateY(6px); }
//             to   { opacity: 1; transform: translateY(0); }
//           }
//         `}</style>
//       </div>

//       {/* ── CHAT BOX ── */}
//       <div className="chat-box">
//         {messages.length === 0 && (
//           <div style={{
//             flex: 1, display: "flex", flexDirection: "column",
//             alignItems: "center", justifyContent: "center",
//             padding: "40px 20px", gap: 12, opacity: 0.6,
//             animation: "fadeIn 0.6s ease"
//           }}>
//             <div style={{ fontSize: 42 }}>🩺</div>
//             <div style={{ color: "#94a3b8", fontSize: 14, textAlign: "center", lineHeight: 1.6 }}>
//               Describe your symptoms below<br />and I'll help diagnose & guide you
//             </div>
//           </div>
//         )}

//         {messages.map((m, i) => (
//           <MessageBubble key={i} sender={m.sender} text={m.text} />
//         ))}

//         {typing && (
//           <div className="typing">
//             <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
//               <div style={{
//                 width: 28, height: 28, borderRadius: "50%",
//                 background: "linear-gradient(135deg, #38bdf8, #818cf8)",
//                 display: "flex", alignItems: "center", justifyContent: "center",
//                 fontSize: 12
//               }}>🌿</div>
//               <div style={{
//                 background: "#1e293b", borderRadius: "12px 12px 12px 3px",
//                 padding: "10px 16px", display: "flex", gap: 5, alignItems: "center"
//               }}>
//                 {[0, 0.18, 0.36].map((delay, i) => (
//                   <div key={i} style={{
//                     width: 6, height: 6, borderRadius: "50%",
//                     background: "#38bdf8",
//                     animation: `dotBounce 1s ${delay}s infinite`
//                   }} />
//                 ))}
//               </div>
//             </div>
//           </div>
//         )}

//         <div ref={bottomRef} />
//       </div>

//       {/* ── INPUT BAR ── */}
//       <div className="chat-input">
//         <input
//           value={input}
//           onChange={e => setInput(e.target.value)}
//           placeholder={
//             chatMode
//               ? "Ask a follow-up question about your diagnosis..."
//               : "Describe your symptoms..."
//           }
//           onKeyDown={e => e.key === "Enter" && send()}
//         />
//         <button onClick={send}>
//           <span style={{ marginRight: 6 }}>↑</span>Send
//         </button>
//       </div>

//       {/* ── RESULT CARDS ──
//           BUG FIX 4: finalData is preserved even during follow-up chat
//           so ConfidenceGraph and AyurvedaCard stay visible ── */}
//       {finalData && (
//         <div className="result-section">
//           {finalData.confidence_explanation && (
//             <ConfidenceGraph
//               confidence={finalData.confidence}
//               explanation={finalData.confidence_explanation}
//             />
//           )}
//           {finalData.ayurveda && (
//             <AyurvedaCard ayurveda={finalData.ayurveda} />
//           )}
//         </div>
//       )}
//     </div>
//   );
// }

//////////////////////////new updated /////////////////////////

import { useState, useRef, useEffect } from "react";
import MessageBubble from "./MessageBubble";
import AyurvedaCard from "./AyurvedaCard";
import ConfidenceGraph from "./ConfidenceGraph";

export default function ChatBox() {
  const [messages, setMessages]   = useState([]);
  const [input, setInput]         = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [finalData, setFinalData] = useState(null);
  const [typing, setTyping]       = useState(false);
  const [chatMode, setChatMode]   = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typing]);

  const send = async () => {
    if (!input.trim()) return;

    const userText = input.trim();
    setMessages(prev => [...prev, { sender: "user", text: userText }]);
    setInput("");
    setTyping(true);

    let payload;
    if (chatMode && sessionId) {
      payload = { session_id: sessionId, message: userText };
    } else if (sessionId) {
      payload = { session_id: sessionId, answer: userText };
    } else {
      payload = { symptoms: userText };
    }

    try {
      const res  = await fetch("http://127.0.0.1:5000/predict", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify(payload),
      });

      const data = await res.json();
      setTyping(false);

      if (data.session_id) setSessionId(data.session_id);

      // Post-result chat reply
      if (data.status === "chat" && data.reply) {
        setMessages(prev => [...prev, { sender: "doctor", text: data.reply }]);
        return;
      }

      // Intake question
      if (data.status === "collecting" && data.question) {
        setMessages(prev => [...prev, { sender: "doctor", text: data.question }]);
        return;
      }

      // Final result
      if (data.status === "final") {
        setMessages(prev => [
          ...prev,
          { sender: "doctor", text: `Predicted condition: ${data.predicted_disease} (${data.confidence}% confidence)` },
        ]);

        if (data.llm_explanation) {
          setMessages(prev => [...prev, { sender: "doctor", text: data.llm_explanation }]);
        }

        // Use chat_hint if backend sends it, otherwise use fallback
        // ROOT CAUSE FIX: old code rendered data.chat_hint directly which
        // threw a React error when field was absent, crashing result-section render
        const hint = data.chat_hint ||
          `You can now ask me anything about ${data.predicted_disease}. Try: "Why was this predicted?", "How is it treated?", "Is it serious?"`;

        setMessages(prev => [...prev, { sender: "doctor", text: hint }]);

        setFinalData(data);
        setChatMode(true);
        return;
      }

      if (data.error) {
        setMessages(prev => [...prev, { sender: "doctor", text: `Error: ${data.error}` }]);
      }

    } catch (err) {
      setTyping(false);
      setMessages(prev => [...prev, { sender: "doctor", text: "Something went wrong. Please try again." }]);
    }
  };

  const reset = () => {
    setMessages([]);
    setInput("");
    setSessionId(null);
    setFinalData(null);
    setChatMode(false);
  };

  return (
    <div className="chat-container">

      {/* Header */}
      <div className="chat-header">
        <div style={{ position: "relative" }}>
          <div style={{
            width: 38, height: 38, borderRadius: "50%",
            background: "linear-gradient(135deg, #38bdf8, #818cf8)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 18, boxShadow: "0 0 16px rgba(56,189,248,0.4)"
          }}>🌿</div>
          <div style={{ position: "absolute", bottom: 1, right: 1, width: 9, height: 9, borderRadius: "50%", background: "#10b981", border: "2px solid #111827", boxShadow: "0 0 6px #10b981" }} />
        </div>

        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 700, fontSize: 16, color: "#f0f6ff", letterSpacing: "-0.01em" }}>Arogya AI</div>
          <div style={{ fontSize: 11, color: "#38bdf8", fontWeight: 500, letterSpacing: "0.04em", textTransform: "uppercase", marginTop: 1 }}>
            {chatMode ? "Follow-up chat active · ask anything" : "AI Health Assistant · Online"}
          </div>
        </div>

        {chatMode && (
          <button onClick={reset} style={{ fontSize: 11, color: "#94a3b8", background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8, padding: "4px 10px", cursor: "pointer" }}>
            New
          </button>
        )}

        <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#818cf8", boxShadow: "0 0 10px #818cf8", animation: "pulse 2s infinite" }} />

        <style>{`
          @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.7)} }
          @keyframes dotBounce { 0%,80%,100%{transform:translateY(0);opacity:0.4} 40%{transform:translateY(-5px);opacity:1} }
          @keyframes fadeIn { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }
        `}</style>
      </div>

      {/* Chat messages */}
      <div className="chat-box">
        {messages.length === 0 && (
          <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "40px 20px", gap: 12, opacity: 0.6, animation: "fadeIn 0.6s ease" }}>
            <div style={{ fontSize: 42 }}>🩺</div>
            <div style={{ color: "#94a3b8", fontSize: 14, textAlign: "center", lineHeight: 1.6 }}>
              Describe your symptoms below<br />and I'll help diagnose & guide you
            </div>
          </div>
        )}

        {messages.map((m, i) => (
          <MessageBubble key={i} sender={m.sender} text={m.text} />
        ))}
        {typing && (
          <div className="typing">
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <div style={{ width: 28, height: 28, borderRadius: "50%", background: "linear-gradient(135deg, #38bdf8, #818cf8)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12 }}>🌿</div>
              <div style={{ background: "#1e293b", borderRadius: "12px 12px 12px 3px", padding: "10px 16px", display: "flex", gap: 5, alignItems: "center" }}>
                {[0, 0.18, 0.36].map((delay, i) => (
                  <div key={i} style={{ width: 6, height: 6, borderRadius: "50%", background: "#38bdf8", animation: `dotBounce 1s ${delay}s infinite` }} />
                ))}
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div className="chat-input">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder={chatMode ? "Ask a follow-up question..." : "Describe your symptoms..."}
          onKeyDown={e => e.key === "Enter" && send()}
        />
        <button onClick={send}><span style={{ marginRight: 6 }}>↑</span>Send</button>
      </div>

      {/* Result cards — ConfidenceGraph + AyurvedaCard */}
      {/* {finalData && (
        <div className="result-section">
          {finalData.confidence_explanation && (
            <ConfidenceGraph
              confidence={finalData.confidence}
              explanation={finalData.confidence_explanation}
            />
          )}
          {finalData.ayurveda && (
            <AyurvedaCard ayurveda={finalData.ayurveda} />
          )}
        </div>
      )} */}
      {finalData && (
  <div className="result-section">

    {finalData.confidence !== undefined && finalData.confidence_explanation && (
      <ConfidenceGraph
        confidence={finalData.confidence}
        explanation={finalData.confidence_explanation}
      />
    )}

    {finalData.ayurveda && (
      <AyurvedaCard ayurveda={finalData.ayurveda} />
    )}

  </div>
)}
    </div>
  );
}

