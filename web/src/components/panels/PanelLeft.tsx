import { Drawer, IconButton, Tooltip } from "@mui/material";
import WorkflowForm from "../workflows/WorkflowForm";
import CodeIcon from "@mui/icons-material/Code";
import useKeyListener from "../../utils/KeyListener";
import { useResizePanel } from "../../hooks/handlers/useResizePanel";
import { TOOLTIP_ENTER_DELAY } from "../node/BaseNode";
import "../../styles/panel.css";

function PanelLeft() {
  const {
    ref: panelRef,
    size: panelSize,
    isDragging,
    handleMouseDown,
    handlePanelToggle
  } = useResizePanel(0, 800, 300, "horizontal", "left");

  useKeyListener("1", () => {
    if (document.activeElement === document.body) {
      handlePanelToggle();
    }
  });

  return (
    <div className={`panel-container ${panelSize > 80 ? "open" : "closed"}`}>
      <Tooltip
        className="tooltip-1"
        title={
          <span className="tooltip-1">
            Drag to scale <br /> Click to open/close
          </span>
        }
        placement="right"
        enterDelay={TOOLTIP_ENTER_DELAY}
      >
        <IconButton
          disableRipple={true}
          className={"panel-button panel-button-left"}
          edge="start"
          color="inherit"
          aria-label="menu"
          onMouseDown={(e) => {
            e.stopPropagation();
            handleMouseDown(e);
          }}
          onClick={handlePanelToggle}
          style={{ left: `${Math.max(panelSize + 10, 25)}px` }}
        >
          <CodeIcon />
        </IconButton>
      </Tooltip>
      <Drawer
        PaperProps={{
          ref: panelRef,
          className: `panel panel-left ${isDragging ? "dragging" : ""}`,
          style: { width: `${panelSize}px` }
        }}
        variant="persistent"
        anchor="left"
        open={true}
      >
        <WorkflowForm />
      </Drawer>
    </div>
  );
}

export default PanelLeft;
