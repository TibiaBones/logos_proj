let slideIndex = 1;
showSlides(slideIndex)

let modalImg = document.getElementById("galleryModalImg");


function openModal() {
    document.getElementById("galleryModal").style.display = "block";
};

function closeModal() {
    document.getElementById("galleryModal").style.display = "none";
};

function switchSlide(n) {
    showSlides(slideIndex += n);
}

function showSlides(n) {
    let slides = document.getElementsByClassName("mainPage-img");
    let switchButtons = document.getElementsByClassName("switch");

    if (n > slides.length) {
        slideIndex = 1
    };

    if (n < 1) {
        slideIndex = slides.length
    };

    for (let i = 0; i < slides.length; i++) {
        slides[i].addEventListener("click", () => {
            slideIndex = i + 1;
            modalImg.src = slides[i].src;
        })
    };

    for (let i = 0; i < switchButtons.length; i++) {
        switchButtons[i].addEventListener("click", () => {
            modalImg.src = slides[slideIndex - 1].src;
            console.log(slideIndex);
        })
    }
}