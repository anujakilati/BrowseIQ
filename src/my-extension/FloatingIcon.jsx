import { useEffect, useRef, useState } from "react";

export default function FloatingIcon({ targetRef }) {
  const iconRef = useRef(null);
  const [visible, setVisible] = useState(false);
  const [position, setPosition] = useState({ top: 0, left: 0 });

  useEffect(() => {
    function updatePosition() {
      if (!targetRef?.current) {
        setVisible(false);
        return;
      }

      const rect = targetRef.current.getBoundingClientRect();
      setPosition({
        top: rect.top + window.scrollY + rect.height / 2 - 20,
        left: rect.left + window.scrollX + rect.width + 10,
      });
      setVisible(true);
    }

    updatePosition();
    window.addEventListener("scroll", updatePosition, true);
    window.addEventListener("resize", updatePosition);

    return () => {
      window.removeEventListener("scroll", updatePosition, true);
      window.removeEventListener("resize", updatePosition);
    };
  }, [targetRef]);

  if (!visible) return null;

  return (
    <div
      ref={iconRef}
      style={{
        position: "absolute",
        top: position.top,
        left: position.left,
        width: 30,
        height: 30,
        borderRadius: "50%",
        background: "#4f46e5",
        color: "#fff",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontWeight: "bold",
        cursor: "pointer",
        zIndex: 9999,
        boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
      }}
      title="Suggestion"
    >
      
    </div>
  );
}
