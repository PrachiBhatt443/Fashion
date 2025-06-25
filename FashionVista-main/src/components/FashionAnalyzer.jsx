import React, { useState } from "react";

export default function FashionAnalyzer() {
  const [imageURL, setImageURL] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    setAnalysis(null);
    try {
      const res = await fetch("http://localhost:5001/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image_url: imageURL }),
      });
      const data = await res.json();
      setAnalysis(data);
    } catch (err) {
      console.error("Error:", err);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 px-4 py-8">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Fashion Image Analyzer</h1>
        <div className="flex flex-col md:flex-row gap-4 justify-center items-center mb-6">
          <input
            type="text"
            placeholder="Paste image URL here"
            value={imageURL}
            onChange={(e) => setImageURL(e.target.value)}
            className="w-full md:w-2/3 px-4 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleAnalyze}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            Analyze
          </button>
        </div>

        {loading && <p className="text-gray-600 text-lg">Analyzing...</p>}

        {analysis && (
          <div className="mt-10 flex flex-col md:flex-row items-start gap-8">
            {/* Image */}
            <img
              src={analysis.image_url}
              alt="Fashion"
              className="w-full md:w-1/2 rounded-xl shadow-md object-cover"
            />

            {/* Results */}
            <div className="flex-1 text-left">
              <h2 className="text-2xl font-semibold mb-4">Dominant Colors</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {analysis.colors.map((color, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <div
                      className="w-10 h-10 rounded shadow-md border"
                      style={{ backgroundColor: color.hex }}
                    ></div>
                    <div>
                      <p className="font-mono">{color.hex}</p>
                      <p className="text-sm text-gray-600">{(color.percentage * 100).toFixed(1)}%</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-6">
                <h3 className="text-xl font-medium">Pattern</h3>
                <p className="text-lg text-gray-700">
                  {analysis.predictions.pattern.predicted}
                </p>
              </div>

              <div className="mt-4">
                <h3 className="text-xl font-medium">Style</h3>
                <p className="text-lg text-gray-700">
                  {analysis.predictions.style.predicted}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}