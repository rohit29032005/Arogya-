// export default function AyurvedaCard({ data }) {
//   if (!data) return null;

//   return (
//     <div style={{ border: "1px solid #ccc", padding: 10, marginTop: 10 }}>
//       <h3>Ayurvedic Plan</h3>
//       <p><b>Herbs:</b> {data.herbs}</p>
//       <p><b>Therapy:</b> {data.therapy}</p>
//       <p><b>Diet:</b> {data.diet}</p>
//       <p><b>Effect:</b> {data.body_type_effect}</p>
//     </div>
//   );
// }
//here
// export default function AyurvedaCard({ ayurveda }) {
//   if (!ayurveda) return null;

//   return (
//     <div className="card">
//       <h3>Ayurvedic Guidance</h3>

//       <p><b>Herbs:</b> {ayurveda.herbs}</p>
//       <p><b>Therapy:</b> {ayurveda.therapy}</p>
//       <p><b>Diet:</b> {ayurveda.diet}</p>

//       <span className="badge">
//         {ayurveda.body_type_effect}
//       </span>
//     </div>
//   );
// }
export default function AyurvedaCard({ ayurveda }) {
  if (!ayurveda) return null;

  return (
    <div style={{
      marginTop: 24,
      background: "#ecfdf5",
      borderRadius: 14,
      padding: 18,
      border: "1px solid #a7f3d0"
    }}>
      <h3 style={{ marginBottom: 12 }}>🌿 Ayurvedic Guidance</h3>

      <p><strong>Herbs:</strong> {ayurveda.herbs}</p>
      <p><strong>Therapy:</strong> {ayurveda.therapy}</p>
      <p><strong>Diet:</strong> {ayurveda.diet}</p>
      <p style={{ marginTop: 8, fontStyle: "italic" }}>
        {ayurveda.body_type_effect}
      </p>
    </div>
  );
}
