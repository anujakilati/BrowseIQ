import { useEffect, useState } from "react";
import FloatingIcon from "./my-extension/FloatingIcon";
import React from 'react';

function App() {
  const [target, setTarget] = useState(null);
  
  useEffect(() => {
    function handleFocus(e) {
      if (
        e.target.tagName === "TEXTAREA" ||
        (e.target.tagName === "INPUT" && e.target.type === "text")
        
      ) {
        setTarget(e.target);
      } else {
        setTarget(null);
      }
    }

    document.addEventListener("focusin", handleFocus);
    return () => document.removeEventListener("focusin", handleFocus);
  }, []);


  return (
    <>
      {target && <FloatingIcon targetRef={{ current: target }} />}
    </>
  );
  
}

export default App;
