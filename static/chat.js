function scrollToBottom() {
  const chatContainer = document.getElementById('chatContainer');
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

document.getElementById('submitButton').addEventListener('click', function() {
  sendMessage();
});

document.getElementById('messageInput').addEventListener('keypress', function(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
  }
});

function sendMessage() {
  const message = document.getElementById('messageInput').value.trim();
  if (message !== '') {
      displayMessage(message, 'user');
      // Here you can send the message to a backend or process it further
      simulateResponse(); // Simulate a response from the chatbot
      document.getElementById('messageInput').value = ''; // Clear the textarea
  }
}

function displayMessage(message, sender) {
  const chatContainer = document.getElementById('chatContainer');
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', sender);
  messageElement.textContent = message;
  chatContainer.appendChild(messageElement);
  scrollToBottom(); // Scroll to bottom after displaying message
}

function simulateResponse() {
  const response = generateRandomResponse(); // Generate a random response
  setTimeout(function() {
      displayMessage(response, 'bot');
  }, 500); // Simulate a delay before displaying the response
}

function generateRandomResponse() {
  const responses = [
      "Hello! How can I assist you?",
      "I'm here to help. What do you need?",
      "Feel free to ask me anything.",
      "That's an interesting question. Let me find the answer for you.",
      "I'm sorry, I didn't understand. Can you please rephrase your question?",
      "Thank you for reaching out. Let me provide you with some information.",
      "Sure thing! Let me get back to you in a moment.",
      "Please wait while I process your request."
  ];
  const randomIndex = Math.floor(Math.random() * responses.length);
  return responses[randomIndex];
}