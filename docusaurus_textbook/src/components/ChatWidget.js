import { useState } from 'react';
import './chat.css';

export default function ChatWidget() {
  const [open, setOpen] = useState(false);

  return (
    <div className="chat-container">
      <button
        className="chat-button"
        onClick={() => setOpen(!open)}
        aria-label="Open AI Chatbot"
        title="Ask AI Assistant"
      >
        <svg
          width="35"
          height="35"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          style={{ color: 'white' }}
        >
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          <circle cx="9" cy="10" r="1" fill="white"></circle>
          <circle cx="15" cy="10" r="1" fill="white"></circle>
          <path d="M9 14c.5.5 1.5 1 3 1s2.5-.5 3-1"></path>
        </svg>
      </button>
      {open && (
        <div className="chat-box">
          <div className="chat-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                <line x1="9" y1="9" x2="9.01" y2="9"></line>
                <line x1="15" y1="9" x2="15.01" y2="9"></line>
              </svg>
              <strong>AI Assistant - Ask Anything!</strong>
            </div>
            <button className="close-button" onClick={() => setOpen(false)} title="Close">
              ✕
            </button>
          </div>
          <div className="chat-iframe-container">
            <iframe
              src="https://faiza-faisal-physical-ai-and-humanoid-robotics-textbook.hf.space"
              className="chat-iframe"
              title="Physical AI Chatbot"
              allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking"
              sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"
            />
          </div>
        </div>
      )}
    </div>
  );
}
