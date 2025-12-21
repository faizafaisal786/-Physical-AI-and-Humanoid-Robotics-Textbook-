import React from 'react';
import Layout from '@theme/Layout';

export default function Chatbot() {
  return (
    <Layout
      title="Ask Questions - AI Chatbot"
      description="Ask questions about Physical AI and Humanoid Robotics using our AI-powered chatbot"
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          padding: '20px',
          minHeight: 'calc(100vh - 60px)',
        }}
      >
        <div
          style={{
            width: '100%',
            maxWidth: '1400px',
            textAlign: 'center',
            marginBottom: '20px',
          }}
        >
          <h1 style={{ fontSize: '36px', marginBottom: '10px' }}>
            AI Chatbot - Ask About the Textbook
          </h1>
          <p style={{ fontSize: '18px', color: '#666', marginBottom: '20px' }}>
            Ask questions about Physical AI and Humanoid Robotics. The chatbot uses RAG (Retrieval-Augmented Generation) to answer based on the textbook content.
          </p>
        </div>

        <div
          style={{
            width: '100%',
            maxWidth: '1400px',
            height: 'calc(100vh - 200px)',
            minHeight: '600px',
            border: '2px solid #e0e0e0',
            borderRadius: '12px',
            overflow: 'hidden',
            boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
          }}
        >
          <iframe
            src="https://faiza-faisal-physical-ai-and-humanoid-robotics-textbook.hf.space"
            style={{
              width: '100%',
              height: '100%',
              border: 'none',
            }}
            title="Physical AI Chatbot"
            allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking"
            sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"
          />
        </div>

        <div
          style={{
            marginTop: '20px',
            padding: '15px',
            background: '#f0f7ff',
            borderRadius: '8px',
            maxWidth: '1400px',
            width: '100%',
          }}
        >
          <p style={{ margin: 0, fontSize: '14px', color: '#555' }}>
            <strong>Note:</strong> This chatbot is powered by AI and uses information from the Physical AI & Humanoid Robotics Textbook.
            It can answer questions about ROS 2, simulation, hardware, VLA systems, and humanoid robotics design.
          </p>
        </div>
      </div>
    </Layout>
  );
}
