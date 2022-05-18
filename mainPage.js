let modal = document.getElementById("galleryModal");

//вот тут нужно написать шнягу, которая будет находить все фотки в галерее и по клику на конкретную будет запускать функцию
// let img = document.getElementById("galleryImg");
// let modalImg = document.getElementById("galleryModalImg");
// img.onclick = function() {
//     modal.style.display = "block";
//     modalImg.src = this.src;
// }


let img = document.getElementsByClassName("mainPage-img");
let modalImg = document.getElementById("galleryModalImg");
img.onclick = function() {
    modal.style.display = "block";
    modalImg.src = this.src;
}




let modalClose = document.getElementById("galleryModal-close");
modalClose.onclick = function() {
    modal.style.display = "none"
}