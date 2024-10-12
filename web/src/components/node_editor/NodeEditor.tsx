/** @jsxImportSource @emotion/react */
import { useCallback, useState, useRef, useEffect, useMemo, memo } from "react";
import {
  useStore,
  useReactFlow,
  Node,
  Background,
  BackgroundVariant,
  FitViewOptions,
  ReactFlow,
  Connection,
  SelectionMode,
  ConnectionMode
} from "@xyflow/react";

import { CircularProgress, Grid } from "@mui/material";
// store
import {
  NodeStore,
  useNodeStore,
  useTemporalStore
} from "../../stores/NodeStore";
import { HistoryManager } from "../../HistoryManager";
// store
import { useWorkflowStore } from "../../stores/WorkflowStore";
import useConnectionStore from "../../stores/ConnectionStore";
import { useSettingsStore } from "../../stores/SettingsStore";
import useNodeMenuStore from "../../stores/NodeMenuStore";
import useContextMenuStore from "../../stores/ContextMenuStore";
// components
import CommandMenu from "../menus/CommandMenu";
import ConnectionLine from "./ConnectionLine";
import NodeContextMenu from "../context_menus/NodeContextMenu";
import PaneContextMenu from "../context_menus/PaneContextMenu";
import SelectionContextMenu from "../context_menus/SelectionContextMenu";
import PropertyContextMenu from "../context_menus/PropertyContextMenu";
import OutputContextMenu from "../context_menus/OutputContextMenu";
import InputContextMenu from "../context_menus/InputContextMenu";
import CommentNode from "../node/CommentNode";
import PreviewNode from "../node/PreviewNode";
import PlaceholderNode from "../node_types/PlaceholderNode";
import AxisMarker from "./AxisMarker";
import LoopNode from "../node/LoopNode";
//utils
import { getMousePosition } from "../../utils/MousePosition";
//css
import { generateCSS } from "../themes/GenerateCSS";
import "../../styles/base.css";
import "../../styles/nodes.css";
import "../../styles/collapsed.css";
import "../../styles/properties.css";
import "../../styles/interactions.css";
import "../../styles/special_nodes.css";
import "../../styles/handle_edge_tooltip.css";

//hooks
import { useAssetUpload } from "../../serverState/useAssetUpload";
import { useMetadata, useNodeTypes } from "../../serverState/useMetadata";
import { useDropHandler } from "../../hooks/handlers/useDropHandler";
import { useCopyPaste } from "../../hooks/handlers/useCopyPaste";
import { useDuplicateNodes } from "../../hooks/useDuplicate";
import useAlignNodes from "../../hooks/useAlignNodes";
import useConnectionHandlers from "../../hooks/handlers/useConnectionHandlers";
import useEdgeHandlers from "../../hooks/handlers/useEdgeHandlers";
import useDragHandlers from "../../hooks/handlers/useDragHandlers";
// constants
import { MAX_ZOOM, MIN_ZOOM } from "../../config/constants";
import HuggingFaceDownloadDialog from "../hugging_face/HuggingFaceDownloadDialog";
import DraggableNodeDocumentation from "../content/Help/DraggableNodeDocumentation";
import { ErrorBoundary } from "@sentry/react";
import GroupNode from "../node/GroupNode";
import { useKeyPressedStore } from "../../stores/KeyPressedStore";
import { useSurroundWithGroup } from "../../hooks/nodes/useSurroundWithGroup";
import { useCombo } from "../../stores/KeyPressedStore";
import { useAddToGroup } from "../../hooks/nodes/useAddToGroup";
import { isEqual } from "lodash";
import ThemeNodes from "../themes/ThemeNodes";
import { useRenderLogger } from "../../hooks/useRenderLogger";

declare global {
  interface Window {
    __beforeUnloadListenerAdded?: boolean;
  }
}

const NodeEditor: React.FC<unknown> = () => {
  const {
    nodes,
    edges,
    onConnect,
    onNodesChange,
    onEdgesChange,
    onEdgeUpdate,
    updateNodeData
  } = useNodeStore((state) => ({
    nodes: state.nodes,
    edges: state.edges,
    onConnect: state.onConnect,
    onNodesChange: state.onNodesChange,
    onEdgesChange: state.onEdgesChange,
    onEdgeUpdate: state.onEdgeUpdate,
    updateNodeData: state.updateNodeData
  }));

  const { handleOnConnect, onConnectStart, onConnectEnd } =
    useConnectionHandlers();
  /* OPTIONS */
  const proOptions = {
    //https://reactflow.dev/docs/guides/remove-attribution/
    hideAttribution: true
  };

  const triggerOnConnect = useCallback(
    (connection: Connection) => {
      onConnect(connection);
      handleOnConnect(connection);
    },
    [onConnect, handleOnConnect]
  );

  const connecting = useConnectionStore((state) => state.connecting);

  /* REACTFLOW */
  const reactFlowWrapper = useRef<HTMLDivElement | null>(null);
  const ref = useRef<HTMLDivElement | null>(null);
  const reactFlowInstance = useReactFlow();

  /* USE STORE */
  const { data: queryMetadata, isLoading: loadingMetadata } = useMetadata();
  const metadata = queryMetadata?.metadata;
  const nodeTypes = useNodeTypes();
  const { isUploading } = useAssetUpload();
  const nodeHistory: HistoryManager = useTemporalStore((state) => state);
  const { shouldFitToScreen, setShouldFitToScreen } = useWorkflowStore(
    (state: any) => state
  );

  /* DEFINE NODE TYPES */
  nodeTypes["nodetool.group.Loop"] = LoopNode;
  nodeTypes["nodetool.workflows.base_node.Group"] = GroupNode;
  nodeTypes["nodetool.workflows.base_node.Comment"] = CommentNode;
  nodeTypes["nodetool.workflows.base_node.Preview"] = PreviewNode;
  nodeTypes["default"] = PlaceholderNode;

  /* STATE */
  const [openCommandMenu, setOpenCommandMenu] = useState(false);

  /* UTILS */
  const { handleCopy, handlePaste, handleCut } = useCopyPaste();
  const alignNodes = useAlignNodes();
  const getSelectedNodeIds = useNodeStore((state) => state.getSelectedNodeIds);
  const duplicateNodes = useDuplicateNodes();
  const surroundWithGroup = useSurroundWithGroup();

  /* DUPLICATE SELECTION */
  const handleDuplicate = useCallback(() => {
    const selectedNodeIds = getSelectedNodeIds();
    if (selectedNodeIds.length) {
      duplicateNodes(selectedNodeIds);
    }
  }, [getSelectedNodeIds, duplicateNodes]);

  /* SETTINGS */
  const settings = useSettingsStore((state) => state.settings);

  /* ON DROP*/
  const { onDrop } = useDropHandler();

  /* HISTORY */
  const history: HistoryManager = useTemporalStore((state) => state);

  /* LOADING*/
  const showLoading = loadingMetadata || metadata?.length === 0;

  // OPEN NODE MENU
  const {
    openNodeMenu,
    closeNodeMenu,
    isMenuOpen,
    selectedNodeType,
    documentationPosition,
    showDocumentation,
    closeDocumentation
  } = useNodeMenuStore((state) => ({
    openNodeMenu: state.openNodeMenu,
    closeNodeMenu: state.closeNodeMenu,
    isMenuOpen: state.isMenuOpen,
    selectedNodeType: state.selectedNodeType,
    documentationPosition: state.documentationPosition,
    showDocumentation: state.showDocumentation,
    closeDocumentation: state.closeDocumentation
  }));

  const handleDoubleClick = useCallback(
    (e: React.MouseEvent) => {
      const clickedElement = e.target as HTMLElement;
      if (clickedElement.classList.contains("react-flow__pane")) {
        if (isMenuOpen) {
          closeNodeMenu();
        } else {
          openNodeMenu(e.clientX, e.clientY);
        }
      } else {
        closeNodeMenu();
      }
    },
    [closeNodeMenu, isMenuOpen, openNodeMenu]
  );
  // CLOSE NODE MENU
  const handleClick = useCallback(
    (e: React.MouseEvent) => {
      const clickedElement = e.target as HTMLElement;
      if (clickedElement.classList.contains("react-flow__pane")) {
        if (isMenuOpen) {
          closeNodeMenu();
        }
      }
    },
    [closeNodeMenu, isMenuOpen]
  );

  /* CONTEXT MENUS */
  const openContextMenu = useContextMenuStore((state) => state.openContextMenu);
  const openMenuType = useContextMenuStore((state) => state.openMenuType);
  const handleNodeContextMenu = useCallback(
    (event: React.MouseEvent, node: Node) => {
      event.preventDefault();
      event.stopPropagation();
      openContextMenu(
        "node-context-menu",
        "",
        event.clientX,
        event.clientY,
        "node-header"
      );
    },
    [openContextMenu]
  );

  const handlePaneContextMenu = useCallback(
    (event: any) => {
      event.preventDefault();
      event.stopPropagation();
      requestAnimationFrame(() => {
        openContextMenu(
          "pane-context-menu",
          "",
          event.clientX,
          event.clientY,
          "react-flow__pane"
        );
      });
    },
    [openContextMenu]
  );

  const handleSelectionContextMenu = useCallback(
    (event: React.MouseEvent) => {
      event.preventDefault();
      openContextMenu(
        "selection-context-menu",
        "",
        event.clientX,
        event.clientY,
        "react-flow__nodesselection"
      );
    },
    [openContextMenu]
  );

  // ON MOVE START | DRAG PANE
  const handleOnMoveStart = useCallback(() => {
    // This also triggers on click, which will mess up the state of isMenuOpen
    closeNodeMenu();
  }, [closeNodeMenu]);

  // ON NODES CHANGE
  const handleNodesChange = useCallback(
    (changes: any) => {
      onNodesChange(changes);
      closeNodeMenu();
    },
    [onNodesChange, closeNodeMenu]
  );

  /* KEY LISTENER */
  // const { spaceKeyPressed } = useKeyPressedStore((state) => ({
  //   spaceKeyPressed: state.isKeyPressed(" ")
  // }));

  useCombo(["Space", "a"], () => {
    alignNodes({ arrangeSpacing: true });
  });

  useCombo(["Meta", "a"], () => alignNodes({ arrangeSpacing: true }));

  useCombo(["Control", "c"], handleCopy);
  useCombo(["Control", "v"], handlePaste);
  useCombo(["Control", "x"], handleCut);
  useCombo(["Meta", "c"], handleCopy); // for mac
  useCombo(["Meta", "v"], handlePaste); // for mac
  useCombo(["Meta", "x"], handleCut); // for mac

  useCombo(["Space", "d"], handleDuplicate);

  useCombo(
    ["Space", "g"],
    useCallback(() => {
      const selectedNodeIds = getSelectedNodeIds();
      if (selectedNodeIds.length) {
        surroundWithGroup({ selectedNodeIds });
      }
    }, [surroundWithGroup, getSelectedNodeIds])
  );

  useCombo(["Control", "z"], nodeHistory.undo);
  useCombo(["Control", "Shift", "z"], nodeHistory.redo);
  useCombo(["Meta", "z"], nodeHistory.undo);
  useCombo(["Meta", "Shift", "z"], nodeHistory.redo);

  useCombo(
    ["Alt", "k"],
    useCallback(() => setOpenCommandMenu(true), [setOpenCommandMenu])
  );
  useCombo(
    ["Meta", "k"],
    useCallback(() => setOpenCommandMenu(true), [setOpenCommandMenu])
  );

  useCombo(
    ["Control", " "],
    useCallback(
      () => openNodeMenu(getMousePosition().x, getMousePosition().y),
      [openNodeMenu]
    )
  );

  const setExplicitSave = useNodeStore(
    (state: NodeStore) => state.setExplicitSave
  );

  // RESUME HISTORY
  const resumeHistoryAndSave = useCallback(() => {
    setExplicitSave(true);
    history.resume();
    setExplicitSave(false);
  }, [history, setExplicitSave]);

  // EDGE HANDLER
  const {
    onEdgeMouseEnter,
    onEdgeMouseLeave,
    onEdgeContextMenu,
    onEdgeUpdateEnd,
    onEdgeUpdateStart
  } = useEdgeHandlers(resumeHistoryAndSave);

  // DRAG HANDLER
  const {
    onSelectionDragStart,
    onSelectionDrag,
    onSelectionDragStop,
    onSelectionStart,
    onSelectionEnd,
    onNodeDragStart,
    onNodeDragStop,
    panOnDrag,
    onNodeDrag,
    onDragOver
  } = useDragHandlers(resumeHistoryAndSave);

  /* COLLAPSE NODE */
  const onNodeDoubleClick = useCallback(
    (event: React.MouseEvent, node: Node) => {
      const clickedElement = event.target as HTMLElement;
      if (clickedElement.classList.contains("node-title")) {
        updateNodeData(node.id, {
          properties: node.data.properties ? { ...node.data.properties } : {},
          workflow_id: node.data.workflow_id as any,
          collapsed: !node.data.collapsed
        });
      }
    },
    [updateNodeData]
  );

  /* VIEWPORT */
  const currentZoom = useStore((state) => state.transform[2]);
  const defaultViewport = useMemo(() => ({ x: 0, y: 0, zoom: 1.5 }), []);

  /* ZOOM BOUNDS */
  // const isMaxZoom = currentZoom === MAX_ZOOM;
  const isMinZoom = useMemo(() => currentZoom === MIN_ZOOM, [currentZoom]);

  // FIT SCREEN
  const fitViewOptions = useMemo<FitViewOptions>(
    () => ({
      maxZoom: MAX_ZOOM,
      minZoom: MIN_ZOOM,
      padding: 0.6
    }),
    []
  );

  const fitScreen = useCallback(() => {
    const fitOptions: FitViewOptions = {
      maxZoom: 2,
      minZoom: 0.5,
      padding: 0.6
    };

    if (reactFlowInstance) {
      reactFlowInstance.fitView(fitOptions);
      setShouldFitToScreen(false);
    }
  }, [reactFlowInstance, setShouldFitToScreen]);

  useEffect(() => {
    if (shouldFitToScreen) {
      requestAnimationFrame(() => {
        fitScreen();
      });
    }
  }, [fitScreen, shouldFitToScreen]);

  // INIT
  const handleOnInit = useCallback(() => {
    setTimeout(() => {
      fitScreen();
    }, 10);
    // const loadHuggingFaceModels = useModelStore(
    //   (state) => state.loadHuggingFaceModels
    // );
    // loadHuggingFaceModels().then((models) => {
    //   const files = workflowModels
    //     .filter((model) => model.path && model.repo_id)
    //     .map((model) => ({
    //       repo_id: model.repo_id as string,
    //       path: model.path as string
    //     }));
    //   tryCacheFiles(files).then((files) => {
    //     console.log("cached", files);
    //   });
    // });
  }, [fitScreen]);

  // Use the custom hook to log render triggers
  useRenderLogger("NodeEditor", {
    edges,
    onConnect,
    onNodesChange,
    onEdgesChange,
    onEdgeUpdate,
    updateNodeData,
    connecting,
    metadata,
    nodeTypes,
    isUploading,
    shouldFitToScreen,
    settings,
    isMenuOpen,
    selectedNodeType,
    documentationPosition,
    showDocumentation,
    openMenuType,
    isMinZoom
  });

  // LOADING OVERLAY
  if (showLoading) {
    return (
      <div className="loading-overlay">
        <CircularProgress size={48} style={{ margin: "auto" }} />
      </div>
    );
  }
  return (
    <>
      <CommandMenu
        open={openCommandMenu}
        setOpen={setOpenCommandMenu}
        undo={nodeHistory.undo}
        redo={nodeHistory.redo}
        reactFlowWrapper={reactFlowWrapper}
      />
      {showDocumentation && selectedNodeType && (
        <DraggableNodeDocumentation
          nodeType={selectedNodeType}
          position={documentationPosition}
          onClose={closeDocumentation}
        />
      )}
      <div className="node-editor" css={generateCSS}>
        <Grid
          container
          spacing={2}
          margin={2}
          sx={{
            margin: "8px",
            height: "calc(100vh - 80px)",
            width: "calc(100vw - 10px)",
            overflow: "hidden"
          }}
        >
          {isUploading && (
            <div className="loading-overlay">
              <CircularProgress />
            </div>
          )}
          <div className="reactflow-wrapper" ref={reactFlowWrapper}>
            <ErrorBoundary
              fallback={({ error }) => (
                <div
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    flexDirection: "column",
                    alignItems: "center",
                    height: "100%"
                  }}
                >
                  <h2>Error loading workflow</h2>
                  <p>{error.message}</p>
                </div>
              )}
            >
              <ReactFlow
                ref={ref}
                className={
                  isMinZoom
                    ? "zoomed-out"
                    : " " + (connecting ? "is-connecting" : "")
                }
                minZoom={MIN_ZOOM}
                maxZoom={MAX_ZOOM}
                zoomOnDoubleClick={false}
                fitView
                fitViewOptions={fitViewOptions}
                nodes={nodes}
                edges={edges}
                nodeTypes={nodeTypes}
                snapToGrid={true}
                snapGrid={[settings.gridSnap, settings.gridSnap]}
                defaultViewport={defaultViewport}
                panOnDrag={panOnDrag}
                {...(settings.panControls === "RMB"
                  ? { selectionOnDrag: true }
                  : {})}
                elevateEdgesOnSelect={true}
                connectionLineComponent={ConnectionLine}
                connectionRadius={settings.connectionSnap}
                attributionPosition="bottom-left"
                selectNodesOnDrag={settings.selectNodesOnDrag}
                onClick={handleClick}
                onDrop={onDrop}
                onDragOver={onDragOver}
                onNodeDrag={onNodeDrag}
                onSelectionDragStart={onSelectionDragStart}
                onSelectionDrag={onSelectionDrag}
                onSelectionDragStop={onSelectionDragStop}
                onSelectionStart={onSelectionStart}
                onSelectionEnd={onSelectionEnd}
                onSelectionContextMenu={handleSelectionContextMenu}
                selectionMode={settings.selectionMode as SelectionMode}
                onEdgesChange={onEdgesChange}
                onEdgeMouseEnter={onEdgeMouseEnter}
                onEdgeMouseLeave={onEdgeMouseLeave}
                onEdgeContextMenu={onEdgeContextMenu}
                connectionMode={ConnectionMode.Strict}
                onConnect={triggerOnConnect}
                onConnectStart={onConnectStart}
                onConnectEnd={onConnectEnd}
                onReconnect={onEdgeUpdate}
                onReconnectStart={onEdgeUpdateStart}
                onReconnectEnd={onEdgeUpdateEnd}
                onNodesChange={handleNodesChange}
                onNodeDragStart={onNodeDragStart}
                onNodeDragStop={onNodeDragStop}
                onNodeContextMenu={handleNodeContextMenu}
                onPaneContextMenu={handlePaneContextMenu}
                onNodeDoubleClick={onNodeDoubleClick}
                onMoveStart={handleOnMoveStart}
                onDoubleClick={handleDoubleClick}
                proOptions={proOptions}
                onInit={handleOnInit}
                // edgeTypes={edgeTypes}
                // onNodeClick={onNodeClick}
                deleteKeyCode={["Delete", "Backspace"]}
              >
                <Background
                  id="1"
                  gap={100}
                  offset={0.15}
                  size={8}
                  color={ThemeNodes.palette.c_editor_grid_color}
                  lineWidth={1}
                  style={{
                    backgroundColor: ThemeNodes.palette.c_editor_bg_color
                  }}
                  variant={BackgroundVariant.Cross}
                />
                {reactFlowInstance && <AxisMarker />}
                {openMenuType === "node-context-menu" && <NodeContextMenu />}
                {openMenuType === "pane-context-menu" && <PaneContextMenu />}
                {openMenuType === "property-context-menu" && (
                  <PropertyContextMenu />
                )}
                {openMenuType === "selection-context-menu" && (
                  <SelectionContextMenu />
                )}
                {openMenuType === "output-context-menu" && (
                  <OutputContextMenu />
                )}
                {openMenuType === "input-context-menu" && <InputContextMenu />}
                <HuggingFaceDownloadDialog />
              </ReactFlow>
            </ErrorBoundary>
          </div>
        </Grid>
      </div>
    </>
  );
};
export default memo(NodeEditor, isEqual);
