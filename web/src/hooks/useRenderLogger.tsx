import { useRef, useMemo } from "react";
import { DEBUG_RENDER_LOGGING } from "../config/constants";

// Custom hook for logging render triggers
export const useRenderLogger = (
  name: string,
  dependencies: Record<string, any>
) => {
  const prevDeps = useRef(dependencies);

  return useMemo(() => {
    if (DEBUG_RENDER_LOGGING) {
      const changedDeps = Object.entries(dependencies).filter(
        ([key, value]) => prevDeps.current[key] !== value
      );

      if (changedDeps.length > 0) {
        console.log(
          `${name} render triggered by:`,
          changedDeps.map(([key]) => key).join(", ")
        );
      }

      prevDeps.current = dependencies;
    }
  }, [dependencies, name]);
};
