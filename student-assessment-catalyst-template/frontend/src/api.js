const API_BASE = "https://your-api-gateway-url";

export const submitScores = async (scores) => {
  return fetch(\`\${API_BASE}/submit-scores\`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scores }),
  });
};

export const getLLMRecommendations = async (scores) => {
  return fetch(\`\${API_BASE}/llm-recommend\`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scores }),
  });
};