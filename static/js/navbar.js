let navManualControl = false;

document.addEventListener("DOMContentLoaded", function () {
  const nav = document.querySelector("#nav");
  const hamburgerSwitch = document.querySelector("#hamburger-switch");
  const navButtons = document.querySelectorAll(".item-expand__button");
  const collapseContainers = document.querySelectorAll(".collapse");
  const bodyContent = document.querySelector("#body-content");

  hamburgerSwitch.addEventListener("click", function () {
    navManualControl = true;
    nav.classList.toggle("active");
    hideNavElements();
  });

  bodyContent.addEventListener("click", function () {
    if (!navManualControl)
    {
      nav.classList.remove("active");
      hideNavElements();
    }
  });

  navButtons.forEach((button) => {
    button.addEventListener("click", function () {
      nav.classList.add("active");
    });
  });

  //IF USER DOESN'T  MANUALLY SWITCH NAV SIZE

    window.addEventListener("resize", function () {
      if (navManualControl == false){
        if (window.innerWidth < 1000) {
          nav.classList.remove("active");
          hideNavElements();
        } else nav.classList.add("active");
      }
    });

//   FUNCTION USED TO HIDE ALL NAV ELEMENTS
  function hideNavElements() {
    navButtons.forEach((button) => {
      if (!button.classList.contains("collapsed"))
        button.classList.add("collapsed");
    });
    collapseContainers.forEach((container) => {
      if (container.classList.contains("show"))
      container.classList.remove("show");
    });
  }
});
