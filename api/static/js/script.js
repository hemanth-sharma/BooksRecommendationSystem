document.addEventListener("DOMContentLoaded", function () {
    const readMoreButtons = document.querySelectorAll(".read-more-btn");
  
    readMoreButtons.forEach((button) => {
      button.addEventListener("click", function () {
        const description = this.parentElement;
        const shortText = description.querySelector(".short-text");
        const fullText = description.querySelector(".full-text");
  
        if (fullText.style.display === "none" || fullText.style.display === "") {
          fullText.style.display = "inline";
          shortText.style.display = "none";
          this.textContent = "Read Less";
        } else {
          fullText.style.display = "none";
          shortText.style.display = "inline";
          this.textContent = "Read More";
        }
      });
    });
  });
  