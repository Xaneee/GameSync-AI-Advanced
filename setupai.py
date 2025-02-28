import { useState } from "react";

export default function Home() {
    const [message, setMessage] = useState("Welcome to GameSync AI!");

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <h1 className="text-4xl font-bold text-blue-600">{message}</h1>
            <p className="mt-4 text-lg text-gray-700">Your AI-powered gaming video processor is ready.</p>
            <button
                className="mt-6 px-6 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600"
                onClick={() => setMessage("GameSync AI is Ready to Sync!")}
            >
                Click to Start
            </button>
        </div>
    );
}
