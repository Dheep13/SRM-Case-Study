import React from 'react';

function MarkdownRenderer({ content }) {
  if (!content) return null;

  // Simple markdown to HTML conversion
  const formatMarkdown = (text) => {
    let formatted = text;

    // Headers
    formatted = formatted.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    formatted = formatted.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    formatted = formatted.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Bold
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Links
    formatted = formatted.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

    // Lists
    formatted = formatted.replace(/^\* (.*$)/gim, '<li>$1</li>');
    formatted = formatted.replace(/^- (.*$)/gim, '<li>$1</li>');
    formatted = formatted.replace(/^\d+\. (.*$)/gim, '<li>$1</li>');

    // Wrap consecutive list items in ul
    formatted = formatted.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');

    // Line breaks
    formatted = formatted.replace(/\n\n/g, '</p><p>');
    formatted = formatted.replace(/\n/g, '<br>');

    // Wrap in paragraphs
    formatted = '<p>' + formatted + '</p>';

    return formatted;
  };

  const htmlContent = formatMarkdown(content);

  return (
    <div 
      className="markdown-content"
      dangerouslySetInnerHTML={{ __html: htmlContent }}
      style={{
        lineHeight: '1.6',
        fontSize: '14px'
      }}
    />
  );
}

export default MarkdownRenderer;
