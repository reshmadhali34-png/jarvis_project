async function sendMessage() {
    let input = document.getElementById("userInput").value;

    if (input === "") return;

    addMessage("You", input);

    let response = await fetch("/command", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ command: input })
    });

    let data = await response.json();

    addMessage("Jarvis", data.reply);

    document.getElementById("userInput").value = "";
}

function addMessage(sender, text) {
    let chatbox = document.getElementById("chatbox");

    let msg = document.createElement("div");
    msg.innerHTML = `<b>${sender}:</b> ${text}`;

    chatbox.appendChild(msg);

    chatbox.scrollTop = chatbox.scrollHeight;
}