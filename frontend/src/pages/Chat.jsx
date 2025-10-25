import React, { useState, useRef, useEffect } from 'react';
import { FiUser, FiSend, FiMessageSquare } from 'react-icons/fi';
import { IoSparklesSharp } from 'react-icons/io5';
import { BsLightbulb } from 'react-icons/bs';

function Chat({ studentLevel }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          student_level: studentLevel
        })
      });

      const data = await response.json();
      const botMessage = { role: 'assistant', content: data.response };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { 
        role: 'assistant', 
        content: 'Error: Could not connect to API. Make sure the backend is running.' 
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  const sampleQueries = [
    "What skills should I learn as a " + studentLevel + "?",
    "Show me resources for learning Python",
    "What's trending in GenAI?",
    "Give me a 3-month learning roadmap"
  ];

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">
          <FiMessageSquare style={{ marginRight: '0.5rem', display: 'inline' }} />
          Chat Assistant
        </h1>
        <p className="page-subtitle">Powered by Agentic RAG with multi-step reasoning for {studentLevel} students</p>
      </div>

      {/* Chat Container */}
      <div className="chat-container">
        {/* Messages Area */}
        <div className="messages-area">
          {messages.length === 0 ? (
            <div className="empty-state">
              <IoSparklesSharp className="empty-icon" />
              <h3>Start a conversation!</h3>
              <p>Ask me anything about IT skills, learning paths, or career advice.</p>
              
              <div className="sample-queries">
                <p><strong>Try these:</strong></p>
                {sampleQueries.map((query, idx) => (
                  <button 
                    key={idx}
                    className="sample-query-btn"
                    onClick={() => setInput(query)}
                  >
                    {query}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg, idx) => (
                <div key={idx} className={`message ${msg.role}`}>
                  <div className="message-avatar">
                    {msg.role === 'user' ? <FiUser /> : <IoSparklesSharp />}
                  </div>
                  <div className="message-content">
                    <div className="message-text">{msg.content}</div>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="message assistant">
                  <div className="message-avatar">
                    <IoSparklesSharp />
                  </div>
                  <div className="message-content">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input Area */}
        <div className="input-area">
          <input
            type="text"
            className="chat-input"
            placeholder="Ask me anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
            disabled={loading}
          />
          <button 
            className="send-btn"
            onClick={sendMessage}
            disabled={loading || !input.trim()}
          >
            <FiSend />
          </button>
        </div>
      </div>

      {/* Info Box */}
      <div className="info-box">
        <BsLightbulb style={{ marginRight: '0.5rem', fontSize: '1.25rem' }} />
        <strong>Tip:</strong> This chatbot uses Agentic RAG, which means it analyzes your intent, 
        plans a search strategy, retrieves relevant data, reasons about it, and refines the response 
        before showing you. Not just simple chunk retrieval!
      </div>
    </div>
  );
}

export default Chat;

