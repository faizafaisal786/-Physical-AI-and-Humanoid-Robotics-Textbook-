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
          <h1 style={{
            fontSize: '36px',
            marginBottom: '10px',
            background: 'linear-gradient(135deg, #1e40af, #7c3aed)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            fontWeight: 'bold'
          }}>
            AI Chatbot - Ask About the Textbook
          </h1>
          <p style={{ fontSize: '18px', color: '#64748b', marginBottom: '20px', lineHeight: '1.6' }}>
            Ask questions about Physical AI and Humanoid Robotics. The chatbot uses RAG (Retrieval-Augmented Generation) to answer based on the textbook content.
          </p>
        </div>

        <div
          style={{
            width: '100%',
            maxWidth: '1400px',
            height: 'calc(100vh - 200px)',
            minHeight: '600px',
            border: '3px solid #1e40af',
            borderRadius: '16px',
            overflow: 'hidden',
            boxShadow: '0 10px 30px rgba(30, 64, 175, 0.2)',
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
            padding: '20px',
            background: 'linear-gradient(135deg, rgba(30, 64, 175, 0.08), rgba(124, 58, 237, 0.08))',
            borderRadius: '12px',
            maxWidth: '1400px',
            width: '100%',
            borderLeft: '4px solid #1e40af',
          }}
        >
          <p style={{ margin: 0, fontSize: '15px', color: '#1e293b', lineHeight: '1.6' }}>
            <strong style={{ color: '#1e40af' }}>Note:</strong> This chatbot is powered by AI and uses information from the Physical AI & Humanoid Robotics Textbook.
            It can answer questions about ROS 2, simulation, hardware, VLA systems, and humanoid robotics design.
          </p>
        </div>
      </div>
    </Layout>
  );
}
