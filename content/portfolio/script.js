window.onload = () => {


    let isDarkTheme = false

    let root = document.querySelector(":root")

    document.getElementById("theme-button").addEventListener("click", () => {
        root.className = isDarkTheme ? "" : "dark-theme"
        isDarkTheme = !isDarkTheme
    });



    const slidesContainer = document.getElementById("slides-container");
    const slide = document.querySelector(".slide");
    const prevButton = document.getElementById("slide-arrow-prev");
    const nextButton = document.getElementById("slide-arrow-next");

    nextButton.addEventListener("click", () => {
        const slideWidth = slide.clientWidth;
        slidesContainer.scrollLeft += slideWidth;
    });

    prevButton.addEventListener("click", () => {
        const slideWidth = slide.clientWidth;
        slidesContainer.scrollLeft -= slideWidth;
    });

}





