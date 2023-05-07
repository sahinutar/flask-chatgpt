
document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    // const datachatInput = document.getElementById("data-chat-input");
    const chatContainer = document.querySelector(".chat-container");
    const clearChatButton = document.getElementById("clear-chat");

    function formatResponse(responseText) {
        const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
        const formattedText = responseText.replace(codeBlockRegex, (match, language, code) => {
          const languageClass = language ? 'language-' + language : '';
          return '<pre><code class="' + languageClass + '">' + code.trim() + '</code></pre>';
        });
        return formattedText;
      }
    function addMessage(message, className) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message", className);

        const messageText = document.createElement("span");
        messageText.textContent = message;
        messageText.innerHTML = formatResponse(message); // Calls formatResponse with the 'message' parameter
        messageElement.appendChild(messageText);
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    chatForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const userMessage = chatInput.value.trim();
        if (!userMessage) return;

        addMessage(userMessage, "user-message");
        chatInput.value = "";

        // const datauserMessage = datachatInput.value.trim();
        // if (!datauserMessage) return;

        // addMessage(datauserMessage, "user-message");
        // datachatInput.value = "";

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `user_input=${encodeURIComponent(userMessage)}`,
        });



        const data = await response.json();
        addMessage(data.response, "bot-message");
    });
    clearChatButton.addEventListener("click", function () {
        chatContainer.innerHTML = "";
    });

    
});

