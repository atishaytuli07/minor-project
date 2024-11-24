const promptInput = document.querySelector("#prompt");
const submitBtn = document.querySelector("#submit");
const chatContainer = document.querySelector(".chat-container");
const imageBtn = document.querySelector("#p-img");
const selectedImage = document.querySelector("#selected-image");
const imageInput = document.querySelector("#image-input");
const clearBtn = document.querySelector("#Clear");
const shareBtn = document.querySelector("#Share");

const API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyDGlZocYC5XcVlajQD4Q5LrT82qIpe0RLU";

let user = {
    message: null,
    file: {
        mime_type: null,
        data: null,
    },
};

async function generateResponse(aiChatBox) {
    const aiChatText = aiChatBox.querySelector(".ai-chat-box");

    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            contents: [
                {
                    parts: [
                        { text: `Suggest Netflix movies or series for : ${user.message} with ratings and year of release` }
                    ]
                }
            ]
        })
    };

    try {
        const response = await fetch(API_URL, requestOptions);
        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log("Raw API Response:", data);

        let apiResponse = data?.candidates?.[0]?.content?.parts?.[0]?.text || "No response received.";
        apiResponse = refineResponse(apiResponse);

        aiChatText.innerHTML = sanitizeHTML(apiResponse); // Sanitize for safe display
    } catch (error) {
        console.error("Error generating AI response:", error);
        aiChatText.innerHTML = "Sorry, I couldn't process your request. Please try again later.";
    } finally {
        scrollToBottom();
        resetImageSelection();
    }
}


function refineResponse(apiResponse) {
    if (!apiResponse) return "No data available.";

    return apiResponse
        .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>") // Convert **bold** to <strong>
        .replace(/\*(.+?)\*/g, "<em>$1</em>")           // Convert *italic* to <em>
        .replace(/\n/g, "<br>")                         // Add line breaks for better readability
        .replace(/^\* (.+?)$/gm, "• $1<br>")            // Format bullet points
        // Highlight key sections (Movies:, Series:, etc.)
        .replace(/(Movies|Series|Important Note|Sweet & Lighthearted Vibe):/g, "<strong>$1:</strong>")
        .trim();
}

function sanitizeHTML(str) {
    const tempDiv = document.createElement("div");
    tempDiv.textContent = str; // Escape HTML to prevent injection
    
    const decoded = tempDiv.innerHTML;

    return decoded.replace(/&lt;(\/?(strong|br|em))&gt;/g, "<$1>");
}


function checkIfNetflixQuery(userMessage) {
    const netflixKeywords = [
        "Netflix", "movie", "series", "show", "recommend", "suggest",
        "comedy", "romantic", "action", "thriller", "trending", "genre",
        "watch", "good", "best", "suggestion", "film"
    ];
    const regex = new RegExp(netflixKeywords.join("|"), "i");
    return regex.test(userMessage);
}

function createChatBox(html, classes) {
    const div = document.createElement("div");
    div.innerHTML = html;
    div.classList.add(classes);
    return div;
}

function handleChatResponse(userMessage) {
    if (!userMessage.trim() && (!user.file || !user.file.data)) return;

    user.message = userMessage;
    const userHtml = `
        <img src="/static/resources/ai.png" alt="User Image" class="user-img">
        <div class="user-chat-box">
            ${sanitizeHTML(user.message)}
            ${user.file.data ? `<img src="data:${user.file.mime_type};base64,${user.file.data}" class="chooseimg" />` : ""}
        </div>
    `;
    promptInput.value = "";
    const userChatBox = createChatBox(userHtml, "user-box");
    chatContainer.appendChild(userChatBox);
    scrollToBottom();

    const aiHtml = `
        <img src="/static/resources/nlogo.png" alt="AI Image" class="ai-img">
        <div class="ai-chat-box">
            Netflix Conversa AI is thinking...
        </div>
    `;
    const aiChatBox = createChatBox(aiHtml, "ai-box");
    chatContainer.appendChild(aiChatBox);
    scrollToBottom();

    generateResponse(aiChatBox, userMessage);
}


function scrollToBottom() {
    requestAnimationFrame(() => {
        chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: "smooth" });
    });
}

function resetImageSelection() {
    selectedImage.src = "img.svg";
    selectedImage.classList.remove("visible");
    user.file = { mime_type: null, data: null };
}

promptInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleChatResponse(promptInput.value);
    }
});

submitBtn.addEventListener("click", () => {
    handleChatResponse(promptInput.value);
});

imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        const base64String = e.target.result.split(",")[1];
        user.file = {
            mime_type: file.type,
            data: base64String,
        };
        selectedImage.src = `data:${user.file.mime_type};base64,${user.file.data}`;
        selectedImage.classList.remove("hidden");
        selectedImage.classList.add("visible");
    };
    reader.readAsDataURL(file);
});

imageBtn.addEventListener("click", () => {
    imageInput.click();
});

clearBtn.addEventListener("click", () => {
    chatContainer.innerHTML = `
        <div class="ai-box">
            <img src="./resources/nlogo.png" alt="AI Image" class="ai-img">
            <div class="ai-chat-box">
                Hi there 👋, what do you want to know about Netflix Movies and Series?
            </div>
        </div>
    `;
});

shareBtn.addEventListener("click", () => {
    const chatContent = chatContainer.innerText;
    const blob = new Blob([chatContent], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "NetflixConversaAI.txt";
    link.click();
    URL.revokeObjectURL(link.href);
});
