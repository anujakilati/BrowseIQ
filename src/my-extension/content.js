function createFloatingBox() {
    const box = document.createElement("div");
    box.id = "floating-box";
    box.textContent = "💡 Suggestion";
    document.body.appendChild(box);
    return box;
  }
  
  const box = createFloatingBox();
  
  function positionBox(target) {
    const rect = target.getBoundingClientRect();
    box.style.top = `${window.scrollY + rect.top - 40}px`;
    box.style.left = `${window.scrollX + rect.left + rect.width - 100}px`;
    box.style.display = "block";
  }
  
  document.addEventListener("focusin", (e) => {
    if (e.target.matches("input[type='text'], textarea")) {
      positionBox(e.target);
    } else {
      box.style.display = "none";
    }
  });
  
  document.addEventListener("scroll", () => {
    const active = document.activeElement;
    if (active && (active.matches("input[type='text'], textarea"))) {
      positionBox(active);
    }
  }, true);

  