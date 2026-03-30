
// export default function MessageBubble({ sender, text }) {
//   const isUser = sender === "user";

//   return (
//     <div style={{
//       display: "flex",
//       justifyContent: isUser ? "flex-end" : "flex-start",
//       marginBottom: 12
//     }}>
//       <div>
//         <div style={{
//           fontSize: 11,
//           color: "#6b7280",
//           marginBottom: 2,
//           textAlign: isUser ? "right" : "left"
//         }}>
//           {isUser ? "You" : "Doctor"}
//         </div>

//         <div style={{
//           maxWidth: 260,
//           padding: "10px 14px",
//           borderRadius: 16,
//           background: isUser ? "#2563eb" : "#f1f5f9",
//           color: isUser ? "#ffffff" : "#0f172a",
//           fontSize: 14,
//           lineHeight: 1.4,
//           whiteSpace: "pre-wrap"
//         }}>
//           {text}
//         </div>
//       </div>
//     </div>
//   );
// }

//new updated code 

export default function MessageBubble({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div style={{
      display: "flex",
      justifyContent: isUser ? "flex-end" : "flex-start",
      marginBottom: 10,
      animation: "fadeIn 0.3s ease",
      gap: 8,
      alignItems: "flex-end"
    }}>
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>

      {/* Avatar for doctor */}
      {!isUser && (
        <div style={{
          width: 28,
          height: 28,
          borderRadius: "50%",
          background: "linear-gradient(135deg, #38bdf8, #818cf8)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 13,
          flexShrink: 0,
          boxShadow: "0 0 10px rgba(56,189,248,0.3)"
        }}>
          🌿
        </div>
      )}

      <div style={{ maxWidth: "72%" }}>
        {/* Sender label */}
        <div style={{
          fontSize: 10,
          color: isUser ? "#818cf8" : "#38bdf8",
          fontWeight: 600,
          marginBottom: 4,
          textAlign: isUser ? "right" : "left",
          letterSpacing: "0.05em",
          textTransform: "uppercase"
        }}>
          {isUser ? "You" : "Arogya AI"}
        </div>

        {/* Bubble */}
        <div style={{
          padding: "11px 16px",
          borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
          background: isUser
            ? "linear-gradient(135deg, #2563eb, #4f46e5)"
            : "#1e293b",
          color: isUser ? "#ffffff" : "#e2e8f0",
          fontSize: 14,
          lineHeight: 1.6,
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
          boxShadow: isUser
            ? "0 4px 16px rgba(79,70,229,0.3)"
            : "0 2px 8px rgba(0,0,0,0.3)",
          border: isUser
            ? "none"
            : "1px solid rgba(99,179,237,0.1)"
        }}>
          {text}
        </div>
      </div>

      {/* Spacer for user side alignment */}
      {isUser && <div style={{ width: 28, flexShrink: 0 }} />}
    </div>
  );
}