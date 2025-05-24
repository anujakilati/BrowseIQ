import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

// ✅ Create and inject the root container
const container = document.createElement("div");
container.id = "floating-extension-root";
document.body.appendChild(container);
container.style.position = "absolute"; // or "fixed" if you want it always on screen
container.style.top = "0";
container.style.left = "0";
container.style.zIndex = "9999";

// ✅ Safe to render now
createRoot(container).render(<App />);


