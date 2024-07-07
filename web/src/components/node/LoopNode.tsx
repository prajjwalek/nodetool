/** @jsxImportSource @emotion/react */
import { memo } from "react";
import { css } from "@emotion/react";
import { useNodeStore } from "../../stores/NodeStore";
import { NodeData } from "../../stores/NodeData";
import { Handle, NodeProps, NodeResizeControl, Position, ResizeDragEvent } from "reactflow";
import SouthEastIcon from "@mui/icons-material/SouthEast";
import ThemeNodetool from "../themes/ThemeNodetool";
import useKeyPressedListener from "../../utils/KeyPressedListener";
import { NodeHeader } from "./NodeHeader";
import { getMousePosition } from "../../utils/MousePosition";
import useNodeMenuStore from "../../stores/NodeMenuStore";
import { NodeInputs } from "./NodeInputs";
import { useMetadata } from "../../serverState/useMetadata";
import { NodeOutputs } from "./NodeOutputs";

const styles = (theme: any) =>
  css({
    "&": {
      boxShadow: "none",
      minWidth: "500px",
      minHeight: "350px"
    },
    "&.hovered.space-pressed": {
      border: "2px dashed black !important"
    },
    height: "100%",
    display: "flex",
    borderRadius: "5px",
    border: `1px solid ${theme.palette.c_gray1}`,
    backgroundColor: "#33333311",
    h6: {
      display: "block",
      position: "absolute",
      marginTop: "10px",
      left: "10px",
      top: "0px"
    },
    ".inputs": {
      // center child vertically
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
    },
    ".tools .react-flow__resize-control.handle.bottom.right": {
      opacity: 1,
      right: "-8px",
      bottom: "-8px",
      margin: 0,
      borderRadius: "0 0 5px 0",
      width: "1.5em",
      height: "1.5em",
      background: "#222 !important"
    },
    ".node-header": {
      height: "3em",
      backgroundColor: "rgba(0,0,0,0.1)"
    }
  });

const LoopNode = (props: NodeProps<NodeData>) => {
  const {
    data: metadata,
    isLoading: metadataLoading,
    error: metadataError
  } = useMetadata();
  const getInputEdges = useNodeStore((state) => state.getInputEdges);
  const updateNodeData = useNodeStore((state) => state.updateNodeData);
  const spaceKeyPressed = useKeyPressedListener(" ");
  const { openNodeMenu } = useNodeMenuStore();
  const nodeHovered = useNodeStore((state) =>
    state.hoveredNodes.includes(props.id)
  );
  const edges = getInputEdges(props.id)
  const handleResize = (event: ResizeDragEvent) => {
    const newWidth = event.x;
    const newHeight = event.y;
    updateNodeData(props.id, {
      ...props.data,
      size: { width: newWidth, height: newHeight }
    });
  };

  const handleOpenNodeMenu = (event?: React.MouseEvent<HTMLElement>) => {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    openNodeMenu(getMousePosition().x, getMousePosition().y, true, "", "");
  };
  if (!metadata) {
    return (
      <div>Loading...</div>
    );
  }
  const nodeMetadata = metadata?.metadataByType[props.type];

  return (
    <>
      <div className="inputs">
        <NodeInputs
          id={props.id}
          properties={nodeMetadata.properties}
          nodeType={props.type}
          data={props.data}
          onlyHandles={true}
          edges={edges} />
      </div>
      <div
        className={`loop-node ${nodeHovered ? "hovered" : ""} ${spaceKeyPressed ? "space-pressed" : ""
          } `}
        onDoubleClick={(e) => {
          e.stopPropagation();
          handleOpenNodeMenu();
        }}
        css={styles}
        style={
          nodeHovered
            ? { border: `2px solid ${ThemeNodetool.palette.c_hl1}` }
            : {}
        }
      >
        <NodeHeader id={props.id} nodeTitle={"Loop"} />
        <NodeOutputs id={props.id} outputs={nodeMetadata.outputs} />
        <div className="tools">
          <NodeResizeControl
            style={{ background: "transparent", border: "none" }}
            minWidth={500}
            minHeight={350}
            onResize={handleResize}
          >
            <SouthEastIcon />
          </NodeResizeControl>
        </div>
      </div >
    </>
  );
};

export default memo(LoopNode);
