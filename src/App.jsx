import { useEffect, useState } from "react";
import FloatingIcon from "./my-extension/FloatingIcon";
import React from 'react';

function App() {
  const [target, setTarget] = useState(null);
  
  useEffect(() => {
    function handleFocus(e) {
      if (
        e.target.matches("textarea, input[type=text], input[type=search]")
        
      ) {
        console.log("🔍 focusing search or text input");
        setTarget(e.target);
      } else {
        setTarget(null);
      }
    }

    document.addEventListener("focusin", handleFocus);
   


    handleFocus({ target: document.activeElement });
    return () => document.removeEventListener("focusin", handleFocus);
  }, []);


  return (
    <>
      {target && <FloatingIcon targetRef={{ current: target }} />}
    </>
  );
  
}

export default App;
