/** @jsxImportSource @emotion/react */
import { css } from "@emotion/react";

import React, { useMemo, useCallback } from "react";
import { motion } from "framer-motion";
import { Box, ListItemButton, ListItemText, Typography } from "@mui/material";
import ThemeNodes from "../themes/ThemeNodes";
import useNodeMenuStore from "../../stores/NodeMenuStore";

interface NamespaceTree {
  [key: string]: {
    children: NamespaceTree;
  };
}

interface RenderNamespacesProps {
  tree: NamespaceTree;
  currentPath?: string[];
  handleNamespaceClick: (newPath: string[]) => void;
}

const namespaceStyles = (theme: any) =>
  css({
    ".list-item": {
      padding: "0.2em 0.8em",
      borderLeft: "1px solid #444",
      transition: "all 0.25s",

      p: {
        fontSize: theme.fontSizeSmall,
        fontFamily: "Inter"
      }
    },
    ".list-item.Mui-selected": {
      backgroundColor: theme.palette.c_hl1,
      color: theme.palette.c_black
    },
    ".list-item.Mui-selected p": {
      fontWeight: 600
    },
    ".sublist": {
      paddingLeft: "1em"
    },
    p: {
      fontFamily: "Inter"
    }
  });

const listVariants = {
  expanded: {
    p: {
      fontFamily: "Inter"
    },
    maxHeight: "200vh",
    opacity: 1,
    transition: {
      when: "beforeChildren",
      staggerChildren: 0.1,
      ease: "easeIn",
      duration: 0
    }
  },
  collapsed: {
    p: {
      fontFamily: "Inter"
    },
    maxHeight: 0,
    opacity: 0,
    transition: {
      when: "afterChildren",
      ease: "easeOut",
      duration: 0
    }
  }
};

function toPascalCase(input: string): string {
  return input.split("_").reduce((result, word, index) => {
    const add = word.toLowerCase();
    return result + (add[0].toUpperCase() + add.slice(1));
  }, "");
}

const RenderNamespaces: React.FC<RenderNamespacesProps> = React.memo(
  ({ tree, currentPath = [], handleNamespaceClick }) => {
    const { highlightedNamespaces, selectedPath, activeNode } =
      useNodeMenuStore((state) => ({
        highlightedNamespaces: state.highlightedNamespaces,
        selectedPath: state.selectedPath,
        activeNode: state.activeNode
      }));

    const memoizedTree = useMemo(
      () =>
        Object.keys(tree).map((namespace) => {
          const currentFullPath = [...currentPath, namespace].join(".");
          const isHighlighted = highlightedNamespaces.includes(currentFullPath);
          const isExpanded =
            currentPath.length > 0
              ? selectedPath.includes(currentPath[currentPath.length - 1])
              : true;
          const newPath = [...currentPath, namespace];
          const hasChildren = Object.keys(tree[namespace].children).length > 0;
          const state = isExpanded ? "expanded" : "collapsed";
          const namespaceStyle = isHighlighted
            ? { borderLeft: `2px solid ${ThemeNodes.palette.c_hl1}` }
            : {};

          return {
            namespace,
            currentFullPath,
            isHighlighted,
            isExpanded,
            newPath,
            hasChildren,
            state,
            namespaceStyle
          };
        }),
      [tree, currentPath, highlightedNamespaces, selectedPath]
    );

    const memoizedHandleClick = useCallback(
      (newPath: string[]) => {
        handleNamespaceClick(newPath);
      },
      [handleNamespaceClick]
    );

    return (
      <div className="namespaces" css={namespaceStyles}>
        {memoizedTree.map(
          ({ namespace, newPath, state, namespaceStyle, hasChildren }) => (
            <NamespaceItem
              key={newPath.join(".")}
              namespace={namespace}
              newPath={newPath}
              state={state}
              namespaceStyle={namespaceStyle}
              hasChildren={hasChildren}
              tree={tree}
              selectedPath={selectedPath}
              activeNode={activeNode || "---"}
              handleNamespaceClick={memoizedHandleClick}
            />
          )
        )}
      </div>
    );
  }
);

interface NamespaceItemProps {
  namespace: string;
  newPath: string[];
  state: string;
  namespaceStyle: React.CSSProperties;
  hasChildren: boolean;
  tree: NamespaceTree;
  selectedPath: string[];
  activeNode: string;
  handleNamespaceClick: (newPath: string[]) => void;
}
const NamespaceItem = React.memo(
  ({
    namespace,
    newPath,
    state,
    namespaceStyle,
    hasChildren,
    tree,
    selectedPath,
    activeNode,
    handleNamespaceClick
  }: NamespaceItemProps) => {
    return (
      <motion.div initial="collapsed" animate={state} variants={listVariants}>
        <ListItemButton
          style={namespaceStyle}
          className={`list-item ${state}`}
          selected={
            selectedPath.join(".") === newPath.join(".") ||
            newPath.join(".").includes(activeNode || "---")
          }
          onClick={() => handleNamespaceClick(newPath)}
        >
          <ListItemText
            primary={
              <Typography fontSize="small">
                {toPascalCase(namespace)}
              </Typography>
            }
          />
        </ListItemButton>
        {hasChildren && (
          <Box className="sublist">
            <RenderNamespaces
              tree={tree[namespace].children}
              currentPath={newPath}
              handleNamespaceClick={handleNamespaceClick}
            />
          </Box>
        )}
      </motion.div>
    );
  }
);

export default RenderNamespaces;
