import { Drawer, IconButton, Tooltip, Tabs, Tab } from "@mui/material";
import CodeIcon from "@mui/icons-material/Code";
import { useResizePanel } from "../../hooks/handlers/useResizePanel";
import { TOOLTIP_ENTER_DELAY } from "../node/BaseNode";
import "../../styles/panel.css";
import { useHotkeys } from "react-hotkeys-hook";
import HelpChat from "../assistants/HelpChat";
import WorkflowChat from "../assistants/WorkflowChat";
import { useState, useCallback } from "react";
import { useNodeStore } from "../../stores/NodeStore";

function PanelLeft() {
  const [activeTab, setActiveTab] = useState(0);
  const {
    ref: panelRef,
    size: panelSize,
    isDragging,
    handleMouseDown,
    handlePanelToggle
  } = useResizePanel("left");

  const workflowId = useNodeStore((state) => state.workflow.id);

  useHotkeys("1", () => {
    if (
      document.activeElement &&
      document.activeElement.tagName.toLowerCase() !== "input" &&
      document.activeElement.tagName.toLowerCase() !== "div" &&
      document.activeElement.tagName.toLowerCase() !== "textarea"
    ) {
      handlePanelToggle();
    }
  });

  const handleTabChange = useCallback(
    (event: React.SyntheticEvent, newValue: number) => {
      setActiveTab(newValue);
    },
    []
  );

  return (
    <div className={`panel-container ${panelSize > 80 ? "open" : "closed"}`}>
      <Tooltip
        className="tooltip-1"
        title={
          <span className="tooltip-1">
            Drag to scale <br /> Click to open/close <br /> Keyboard shortcut: 1
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
        <Tabs value={activeTab} onChange={handleTabChange}>
          <Tab label="Help" />
          <Tab label="Workflow" />
        </Tabs>
        {activeTab === 0 && <HelpChat />}
        {activeTab === 1 && <WorkflowChat workflow_id={workflowId} />}
      </Drawer>
    </div>
  );
}

export default PanelLeft;
