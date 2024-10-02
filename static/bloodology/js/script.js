var images = [
    "{% static 'bloodology/image/img1.png' %}",
    "{% static 'bloodology/image/img2.png' %}",
    "{% static 'bloodology/image/img3.png' %}",
    "{% static 'bloodology/image/img6.png' %}",
    "{% static 'bloodology/image/img7.png' %}",
];
var currentIndex = 0;
var image = document.getElementById("image");
setInterval(function () {
    currentIndex = (currentIndex + 1) % images.length;
    image.src = images[currentIndex];
}, 3000);

