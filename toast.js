function showToast(msg, type = "error") {
    const box = document.createElement("div");
    box.classList.add("toast");
    box.classList.add(type);
    box.innerText = msg;

    document.body.appendChild(box);

    setTimeout(() => {
        box.style.opacity = "0";
        setTimeout(() => box.remove(), 400);
    }, 3000);
}

const style = document.createElement("style");
style.innerHTML = `
.toast {
    position: fixed;
    top: 20px;
    right: 20px;
    background: #dc3545;
    padding: 12px 18px;
    border-radius: 10px;
    font-weight: bold;
    color: white;
    z-index: 9999;
    animation: slide 0.3s ease;
}
.toast.success { background: #16a34a; }

@keyframes slide {
    from { transform: translateX(40px); opacity: 0; }
    to   { transform: translateX(0); opacity: 1; }
}
`;
document.head.appendChild(style);
