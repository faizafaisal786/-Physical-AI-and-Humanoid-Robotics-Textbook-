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
      >
        <img
          src="/img/icon.jpeg"
          alt="Chat Icon"
          className="chat-icon"
        />
      </button>
      {open && (
        <div className="chat-box">
          <div className="chat-header">
            <strong>Physical AI & Robotics Chatbot</strong>
            <button className="close-button" onClick={() => setOpen(false)}>
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
