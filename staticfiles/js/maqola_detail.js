document.addEventListener("DOMContentLoaded", () => {
    const openBtn = document.querySelector(".open-full-btn");
    if (!openBtn) return console.error("Toliq ochish tugmasi topilmadi");

    openBtn.addEventListener("click", () => {
        console.log("Tugma bosildi, fayl yoki rasm alohida oynada ochiladi...");

        // URLni aniqlash: PDF, boshqa fayl yoki rasm
        let fileUrl = "";

        // PDF yoki boshqa fayl <iframe> yoki <a> orqali
        const fileIframe = document.querySelector(".maqola-file iframe");
        const fileLink = document.querySelector(".maqola-file a");

        if (fileIframe && fileIframe.src) {
            fileUrl = fileIframe.src;
        } else if (fileLink && fileLink.href) {
            fileUrl = fileLink.href;
        } else {
            // Agar file bo‘lmasa, rasmni ochish
            const img = document.querySelector(".maqola-image img");
            if (img && img.src) fileUrl = img.src;
        }

        if (fileUrl) {
            window.open(fileUrl, "_blank", "width=900,height=700,resizable=yes,scrollbars=yes");
        } else {
            console.warn("Hech qanday fayl yoki rasm topilmadi.");
        }
    });
});

// Ulashish tugmasi
function shareMaqola() {
    const url = window.location.href;
    if (navigator.share) {
        navigator.share({
            title: document.title,
            text: 'Ushbu maqolani ko‘ring:',
            url: url
        }).then(() => console.log('Maqola ulashildi'))
          .catch((err) => console.error('Xatolik:', err));
    } else {
        prompt('Ushbu linkni nusxalab ulashing:', url);
    }
}
