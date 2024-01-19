// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
  
      const targetId = this.getAttribute("href").substring(1);
      const targetElement = document.getElementById(targetId);
  
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 10, // Adjust for header height
          behavior: "smooth",
        });
      }
    });
  });
  function redirectToNewPage() {
    // Replace 'newpage.html' with the URL of the page you want to redirect to
    window.location.href = "/getdoc";
  }