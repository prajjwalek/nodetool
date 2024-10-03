/** @jsxImportSource @emotion/react */
import { css, keyframes } from "@emotion/react";

import ThemeNodes from "../themes/ThemeNodes";
import { memo, useEffect, useState, useMemo, useCallback } from "react";
import { Node, NodeProps, NodeResizer, useStore } from "@xyflow/react";
import { isEqual } from "lodash";
import { Container } from "@mui/material";
import { NodeData } from "../../stores/NodeData";
import { useMetadata } from "../../serverState/useMetadata";
import { useNodeStore } from "../../stores/NodeStore";
import { NodeHeader } from "./NodeHeader";
import { NodeErrors } from "./NodeErrors";
import useStatusStore from "../../stores/StatusStore";
import useResultsStore from "../../stores/ResultsStore";
import OutputRenderer from "./OutputRenderer";
import { MIN_ZOOM } from "../../config/constants";
import ModelRecommendations from "./ModelRecommendations";
import { isProduction } from "../../stores/ApiClient";
import ApiKeyValidation from "./ApiKeyValidation";
import NodeStatus from "./NodeStatus";
import NodeContent from "./NodeContent";

// Tooltip timing constants
export const TOOLTIP_ENTER_DELAY = 650;
export const TOOLTIP_LEAVE_DELAY = 200;
export const TOOLTIP_ENTER_NEXT_DELAY = 350;

// Node sizing constants
const BASE_HEIGHT = 0; // Minimum height for the node
const INCREMENT_PER_OUTPUT = 25; // Height increase per output in the node
const MAX_NODE_WIDTH = 600;

/**
 * Split a camelCase string into a space separated string.
 */
export function titleize(str: string) {
  const s = str.replace(/([A-Z]+)([A-Z][a-z])/g, "$1 $2");
  return s.replace(/([a-z])([A-Z])/g, "$1 $2");
}

/**
 * BaseNode renders a single node in the workflow
 *
 * @param props
 */

const gradientAnimation = keyframes`
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
`;

const styles = (theme: any) =>
  css({
    // resizer
    ".node-resizer .react-flow__resize-control.top.line, .node-resizer .react-flow__resize-control.bottom.line":
      {
        display: "none"
      },
    ".node-resizer .react-flow__resize-control.handle": {
      opacity: 0
    },
    ".node-resizer .react-flow__resize-control.line": {
      opacity: 0,
      borderWidth: "1px",
      borderColor: theme.palette.c_gray2,
      transition: "all 0.15s ease-in-out"
    },
    ".node-resizer .react-flow__resize-control.line:hover": {
      opacity: 1
    },

    "&.loading": {
      position: "relative",
      "--glow-offset": "-3px",
      "&::before": {
        opacity: 0,
        content: '""',
        position: "absolute",
        top: "var(--glow-offset)",
        left: "var(--glow-offset)",
        right: "var(--glow-offset)",
        bottom: "var(--glow-offset)",
        background: "linear-gradient(45deg, #ff00ff, #00ffff, #ff00ff)",
        backgroundSize: "200% 200%",
        animation: `${gradientAnimation} 3s ease infinite`,
        borderRadius: "inherit",
        zIndex: -20,
        transition: "opacity 0.5s ease-in-out"
      }
    },
    "&.loading.is-loading": {
      "&::before": {
        opacity: 1
      }
    }
  });

export default memo(
  function BaseNode(props: NodeProps<Node<NodeData>>) {
    // Flow and zoom-related state
    const currentZoom = useStore((state) => state.transform[2]);
    const isMinZoom = currentZoom === MIN_ZOOM;

    // Metadata and loading state
    const {
      data: metadata, // Metadata for all node types
      isLoading: metadataLoading,
      error: metadataError
    } = useMetadata();

    // Node-specific data and relationships
    const nodedata = useNodeStore(
      useCallback((state) => state.findNode(props.id)?.data, [props.id])
    );
    const node = useNodeStore(
      useCallback((state) => state.findNode(props.id), [props.id])
    );
    const hasParent = node?.parentId !== undefined;
    const parentNode = useNodeStore(
      useCallback(
        (state) => (hasParent ? state.findNode(node?.parentId || "") : null),
        [hasParent, node?.parentId]
      )
    );
    const edges = useNodeStore(
      useCallback((state) => state.getInputEdges(props.id), [props.id])
    );

    // Workflow and status information
    const workflowId = useMemo(() => nodedata?.workflow_id || "", [nodedata]);
    const status = useStatusStore((state) =>
      state.getStatus(workflowId, props.id)
    );
    const isLoading =
      status === "running" || status === "starting" || status === "booting";

    // Node type flags
    const isConstantNode = props.type.startsWith("nodetool.constant");
    const isInputNode = props.type.startsWith("nodetool.input");
    const isOutputNode =
      props.type.startsWith("nodetool.output") ||
      props.type === "comfy.image.SaveImage" ||
      props.type === "comfy.image.PreviewImage";

    // UI state
    const [parentIsCollapsed, setParentIsCollapsed] = useState(false);

    useEffect(() => {
      // Set parentIsCollapsed state based on parent node
      if (hasParent) {
        setParentIsCollapsed(parentNode?.data.collapsed || false);
      }
    }, [hasParent, node?.parentId, parentNode?.data.collapsed]);

    const className = useMemo(
      () =>
        `node-body ${props.data.collapsed ? "collapsed" : ""}
      ${hasParent ? "has-parent" : ""}
      ${isInputNode ? " input-node" : ""} ${isOutputNode ? " output-node" : ""}
      ${props.data.dirty ? "dirty" : ""}
      ${isLoading ? " loading is-loading" : " loading"}`
          .replace(/\s+/g, " ")
          .trim(),
      [
        props.data.collapsed,
        hasParent,
        isInputNode,
        isOutputNode,
        props.data.dirty,
        isLoading
      ]
    );

    // Results and rendering
    const result = useResultsStore((state) =>
      state.getResult(props.data.workflow_id, props.id)
    );
    const renderedResult = useMemo(() => {
      if (result && typeof result === "object") {
        return Object.entries(result).map(([key, value]) => (
          <OutputRenderer key={key} value={value} />
        ));
      }
    }, [result]);

    // Node height calculation
    const minHeight = useMemo(() => {
      if (!metadata) return BASE_HEIGHT;
      const outputCount =
        metadata.metadataByType[props.type]?.outputs.length || 0;
      return BASE_HEIGHT + outputCount * INCREMENT_PER_OUTPUT;
    }, [metadata, props.type]);

    // Node metadata and properties
    const nodeMetadata = metadata?.metadataByType[props.type];
    const node_title = titleize(nodeMetadata?.title || "");
    const node_namespace = nodeMetadata?.namespace || "";
    const node_outputs = nodeMetadata?.outputs || [];
    const firstOutput =
      node_outputs.length > 0
        ? node_outputs[0]
        : {
            name: "output",
            type: {
              type: "string"
            }
          };

    if (!nodeMetadata || metadataLoading || metadataError) {
      return (
        <Container className={className}>
          <NodeHeader id={props.id} nodeTitle={node_title} />
        </Container>
      );
    }

    if (parentIsCollapsed) {
      return null;
    }

    return (
      <Container
        css={styles}
        className={className}
        style={{
          display: parentIsCollapsed ? "none" : "flex",
          minHeight: `${minHeight}px`,
          backgroundColor: hasParent
            ? ThemeNodes.palette.c_node_bg_group
            : ThemeNodes.palette.c_node_bg
        }}
      >
        <NodeHeader
          id={props.id}
          nodeTitle={node_title}
          hasParent={hasParent}
          isMinZoom={isMinZoom}
        />
        {!isMinZoom && (
          <>
            <NodeErrors id={props.id} />
            <NodeStatus status={status} />
            {!isProduction && <ModelRecommendations nodeType={props.type} />}
            {!isProduction && (
              <ApiKeyValidation nodeNamespace={node_namespace} />
            )}
          </>
        )}
        <NodeContent
          id={props.id}
          nodeType={props.type}
          nodeMetadata={nodeMetadata}
          isConstantNode={isConstantNode}
          isOutputNode={isOutputNode}
          data={props.data}
          edges={edges}
          status={status}
          workflowId={workflowId}
          renderedResult={renderedResult}
          isMinZoom={isMinZoom}
          firstOutput={firstOutput}
        />
        <div className="node-resizer">
          <NodeResizer
            minWidth={100}
            minHeight={100}
            maxWidth={MAX_NODE_WIDTH}
          />
        </div>
      </Container>
    );
  },
  (prevProps, nextProps) => isEqual(prevProps, nextProps)
);
