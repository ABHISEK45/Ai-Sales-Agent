const API_URL = "http://127.0.0.1:8000";

const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");
const typingIndicator = document.getElementById("typingIndicator");
const errorToast = document.getElementById("errorToast");


// ============================================================
// SESSION
// ============================================================

let sessionId = localStorage.getItem("northstar_session_id");

if (!sessionId) {
    sessionId =
        "web-" +
        Date.now() +
        "-" +
        Math.random().toString(36).substring(2, 9);

    localStorage.setItem(
        "northstar_session_id",
        sessionId
    );
}


// ============================================================
// DOM HELPERS
// ============================================================

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function escapeHtml(text) {
    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


function addMessage(text, type) {
    const message = document.createElement("div");

    message.className =
        type === "user"
            ? "message user-message"
            : "message assistant-message";

    if (type === "user") {

        message.innerHTML = `
            <div class="message-content">
                <div class="message-bubble">
                    ${escapeHtml(text)}
                </div>
            </div>
        `;

    } else {

        message.innerHTML = `
            <div class="avatar">
                N
            </div>

            <div class="message-content">
                <div class="message-name">
                    Northstar Assistant
                </div>

                <div class="message-bubble">
                    ${escapeHtml(text)}
                </div>
            </div>
        `;
    }

    chatMessages.appendChild(message);

    scrollToBottom();
}


function setTyping(visible) {
    if (visible) {
        typingIndicator.classList.remove("hidden");
    } else {
        typingIndicator.classList.add("hidden");
    }

    scrollToBottom();
}


function showError(message) {
    errorToast.querySelector("span").textContent = message;

    errorToast.classList.remove("hidden");

    setTimeout(() => {
        errorToast.classList.add("hidden");
    }, 4000);
}


// ============================================================
// LEAD STATE
// ============================================================

function updateTextElement(id, value, fallback = "Not provided") {
    const element = document.getElementById(id);

    if (!element) {
        return;
    }

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        element.textContent = fallback;
        element.classList.add("empty");
    } else {
        element.textContent = value;
        element.classList.remove("empty");
    }
}


function updateLeadState(lead) {
    if (!lead) {
        return;
    }


    // --------------------------------------------------------
    // Qualification
    // --------------------------------------------------------

    updateTextElement(
        "configuration",
        lead.configuration
    );

    updateTextElement(
        "budget",
        lead.budget
    );

    updateTextElement(
        "purchaseTimeline",
        lead.purchase_timeline
    );


    updateTextElement(
        "interestLevel",
        lead.interest_level,
        "Not assessed"
    );


    // --------------------------------------------------------
    // Site Visit
    // --------------------------------------------------------

    const siteVisitStatus =
        document.getElementById("siteVisitStatus");

    const siteVisitDetails =
        document.getElementById("siteVisitDetails");

    const siteVisitCard =
        document.getElementById("siteVisitCard");


    if (lead.site_visit_status === "booked") {

        siteVisitStatus.textContent =
            "Site visit confirmed";

        const date =
            lead.site_visit_date || "Scheduled date";

        const time =
            lead.site_visit_time || "Scheduled time";

        siteVisitDetails.textContent =
            `${date} · ${time}`;

        siteVisitCard.classList.add("booked");

    } else if (
        lead.site_visit_status === "unavailable"
    ) {

        siteVisitStatus.textContent =
            "Requested slot unavailable";

        siteVisitDetails.textContent =
            "Please choose another date or time.";

        siteVisitCard.classList.remove("booked");

    } else {

        siteVisitStatus.textContent =
            "No visit scheduled";

        siteVisitDetails.textContent =
            "The assistant can schedule a visit for you.";

        siteVisitCard.classList.remove("booked");
    }


    // --------------------------------------------------------
    // Lead signals
    // --------------------------------------------------------

    updateSignal(
        "followUp",
        lead.follow_up_required
    );

    updateSignal(
        "escalation",
        lead.escalation_required
    );


    // --------------------------------------------------------
    // Conversation status
    // --------------------------------------------------------

    const conversationStatus =
        document.getElementById("conversationStatus");

    if (lead.conversation_ended) {

        conversationStatus.textContent = "Ended";

        conversationStatus.className =
            "signal-value neutral";

    } else {

        conversationStatus.textContent = "Active";

        conversationStatus.className =
            "signal-value positive";
    }


    // --------------------------------------------------------
    // Lead badge
    // --------------------------------------------------------

    updateLeadBadge(lead);
}


function updateSignal(id, value) {
    const element = document.getElementById(id);

    if (!element) {
        return;
    }

    if (value) {

        element.textContent = "Yes";

        element.className =
            "signal-value warning";

    } else {

        element.textContent = "No";

        element.className =
            "signal-value neutral";
    }
}


function updateLeadBadge(lead) {
    const badge =
        document.getElementById("leadStatusBadge");

    if (!badge) {
        return;
    }


    if (
        lead.site_visit_status === "booked"
    ) {

        badge.textContent = "Visit Booked";

        badge.className =
            "lead-status qualified";

        return;
    }


    if (
        lead.interest_level === "high"
        || lead.interest_level === "very high"
    ) {

        badge.textContent = "Qualified";

        badge.className =
            "lead-status qualified";

        return;
    }


    if (
        lead.configuration
        || lead.budget
        || lead.purchase_timeline
    ) {

        badge.textContent = "Engaged";

        badge.className =
            "lead-status qualified";

        return;
    }


    badge.textContent = "New Lead";

    badge.className =
        "lead-status";
}


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendMessage() {

    const message =
        messageInput.value.trim();

    if (!message) {
        return;
    }


    // Prevent duplicate requests
    sendButton.disabled = true;

    messageInput.disabled = true;


    addMessage(
        message,
        "user"
    );


    messageInput.value = "";

    messageInput.style.height = "auto";


    setTyping(true);


    try {

        const response =
            await fetch(
                `${API_URL}/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        session_id: sessionId,
                        message: message
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data =
            await response.json();


        setTyping(false);


        // ----------------------------------------------------
        // Agent response
        // ----------------------------------------------------

        if (data.response) {

            addMessage(
                data.response,
                "assistant"
            );
        }


        // ----------------------------------------------------
        // Lead state
        // ----------------------------------------------------

        if (data.lead_state) {

            updateLeadState(
                data.lead_state
            );
        }


    } catch (error) {

        console.error(
            "Chat error:",
            error
        );

        setTyping(false);

        showError(
            "Unable to connect to the AI assistant. Make sure the backend is running."
        );

    } finally {

        sendButton.disabled = false;

        messageInput.disabled = false;

        messageInput.focus();
    }
}


// ============================================================
// EVENT HANDLERS
// ============================================================

sendButton.addEventListener(
    "click",
    sendMessage
);


messageInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter"
            && !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);


messageInput.addEventListener(
    "input",
    () => {

        messageInput.style.height =
            "auto";

        messageInput.style.height =
            Math.min(
                messageInput.scrollHeight,
                100
            ) + "px";
    }
);