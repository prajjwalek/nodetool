/** @jsxImportSource @emotion/react */
import useContextMenuStore from "../../stores/ContextMenuStore";
import { MoreHoriz } from "@mui/icons-material";
import { css } from "@emotion/react";
import { NodeStore, useNodeStore } from "../../stores/NodeStore";
import { memo, useCallback, useMemo } from "react";
import ThemeNodes from "../themes/ThemeNodes";
import { isEqual } from "lodash";
import { titleizeString } from "../../utils/titleizeString";
import ColorPicker from "../inputs/ColorPicker";
import { NodeData } from "../../stores/NodeData";
import { Tooltip } from "@mui/material";

export interface NodeHeaderProps {
  id: string;
  metadataTitle: string;
  hasParent?: boolean;
  parentColor?: string;
  showMenu?: boolean;
  data: NodeData;
  backgroundColor?: string;
}
// const tooltipStyle = css({
//   '[role~="tooltip"][data-microtip-position|="top"]::after': {
//     fontSize: "1.1em",
//     maxWidth: "250px",
//     padding: "1em",
//     textAlign: "left",
//     transform: "translate3d(-90%, -5px, 0)"
//   }
// });

export const headerStyle = (theme: any, hasParent: boolean) =>
  css({
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    width: "100%",
    minHeight: "24px",
    backgroundColor: hasParent
      ? theme.palette.c_node_header_bg_group
      : theme.palette.c_node_header_bg,
    color: theme.palette.c_white,
    margin: 0,
    borderRadius: "0.3em 0.3em 0 0",
    "& svg.MuiSvgIcon-root": {
      scale: 0.8,
      opacity: 1
    },
    "&:hover": {
      transition: "opacity 0.15s",
      color: theme.palette.c_gray6
    },
    ".node-title": {
      flexGrow: 1,
      textAlign: "left",
      maxWidth: 170,
      wordWrap: "break-word",
      lineHeight: "1em",
      fontFamily: theme.fontFamily1,
      fontSize: theme.fontSizeNormal,
      fontFeatureSettings: '"smcp"',
      padding: "8px 10px"
    },
    ".big": {
      flex: 1,
      maxWidth: 180,
      wordWrap: "break-word",
      lineHeight: "1em",
      fontSize: 28
    },
    ".menu-button": {
      height: "28px",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      marginLeft: "0.2em",
      padding: 0,
      color: theme.palette.c_gray6,
      backgroundColor: "transparent",
      border: "none",
      cursor: "pointer",
      "&:hover": {
        color: theme.palette.c_white
      }
    },
    ".menu-button svg": {
      scale: "0.5"
    },
    ".color-picker-button": {
      position: "absolute",
      right: "0.5em",
      pointerEvents: "all",
      margin: "5px",
      height: "1.1em",
      zIndex: 10000,
      backgroundColor: "transparent",
      borderRadius: "0",
      "& svg": {
        color: theme.palette.c_gray5,
        width: ".5em",
        height: ".5em",
        // scale: ".5",
        rotate: "-86deg"
      },
      "&:hover svg": {
        color: theme.palette.c_hl1
      }
    }
  });

export const NodeHeader: React.FC<NodeHeaderProps> = ({
  id,
  metadataTitle,
  hasParent,
  data,
  backgroundColor,
  showMenu = true
}: NodeHeaderProps) => {
  const openContextMenu = useContextMenuStore((state) => state.openContextMenu);
  // const getMetadata = useMetadataStore((state) => state.getMetadata);
  // const findNode = useNodeStore((state) => state.findNode);

  // const node = useMemo(() => findNode(id), [findNode, id]);
  // const metadata = getMetadata(node?.type || "");
  // const description = useMemo(
  //   () => metadata?.description.split("\n")[0] || "",
  //   [metadata]
  // );

  // const tooltipAttributes = useMemo(
  //   () =>
  //     description
  //       ? {
  //           "aria-label": description,
  //           "data-microtip-position": "top",
  //           "data-microtip-size": "medium",
  //           role: "tooltip"
  //         }
  //       : {},
  //   [description]
  // );
  const titleizedType = useMemo(
    () => (metadataTitle ? titleizeString(metadataTitle) : ""),
    [metadataTitle]
  );

  const memoizedHeaderStyle = useMemo(
    () => headerStyle(ThemeNodes, hasParent || false),
    [hasParent]
  );

  const handleOpenContextMenu = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      event.preventDefault();
      openContextMenu(
        "node-context-menu",
        id,
        event.clientX,
        event.clientY,
        "node-header"
      );
    },
    [id, openContextMenu]
  );

  const updateNode = useNodeStore((state: NodeStore) => state.updateNode);
  const handleHeaderClick = useCallback(() => {
    updateNode(id, { selected: true });
  }, [updateNode, id]);

  const updateNodeData = useNodeStore(
    (state: NodeStore) => state.updateNodeData
  );

  const handleColorChange = useCallback(
    (newColor: string) => {
      if (id) {
        updateNodeData(id, {
          color: newColor
        });
      }
    },
    [id, updateNodeData]
  );

  return (
    <div
      className="node-header"
      css={memoizedHeaderStyle}
      onClick={handleHeaderClick}
      style={{
        backgroundColor: backgroundColor
      }}
    >
      {data.title && (
        <span className="node-title">
          {data.title} ({titleizedType})
        </span>
      )}
      {!data.title && <span className="node-title">{titleizedType}</span>}
      {showMenu && (
        <>
          <ColorPicker
            label=""
            color={backgroundColor || ""}
            onColorChange={handleColorChange}
          />
          <div className="menu-button">
            <button className="menu-button" onClick={handleOpenContextMenu}>
              <MoreHoriz />
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default memo(NodeHeader, isEqual);
