/** @jsxImportSource @emotion/react */
import { css } from "@emotion/react";
import React from "react";
import FolderIcon from "@mui/icons-material/Folder";
import NorthWest from "@mui/icons-material/NorthWest";
import { ButtonGroup, Typography } from "@mui/material";
import { Asset } from "../../stores/ApiTypes";
import { useAssetActions } from "./useAssetActions";
import DeleteButton from "../buttons/DeleteButton";

const styles = (theme: any) =>
  css({
    "&": {
      position: "relative",
      display: "flex",
      flexDirection: "row",
      alignItems: "flex-start",
      justifyContent: "start",
      // padding: "0.5em 0",
      gap: ".5em",
      width: "100%",
      height: "auto",
      cursor: "pointer",
      boxSizing: "border-box",
      // backgroundColor: theme.palette.c_gray1,
      backgroundColor: "transparent",
      transition: "background-color 0.3s ease",
    },
    ".folder-icon": {
      width: "25px",
      height: "100%",
      left: "0",
      color: theme.palette.c_gray2,
    },
    "&.selected .folder-icon": {
      color: theme.palette.c_hl2,
    },
    ".parent-icon": {
      position: "absolute",
      color: theme.palette.c_folder,
      width: "30%",
      height: "30%",
      bottom: "10%",
      right: "10%",
    },
    ".name": {
      marginTop: "0.4em",
      fontSize: theme.fontSizeSmall,
      textAlign: "left",
      verticalAlign: "middle",
      wordBreak: "break-word",
      maxWidth: "100%",
      maxHeight: "2.5em",
      overflow: "hidden",
      color: theme.palette.c_white,
    },
    "&.selected .name": {
      color: theme.palette.c_hl1,
    },
    "&:hover": {
      color: theme.palette.c_gray5,
    },
    "&:hover .delete-button": {
      opacity: 0,
    },
    "&.drag-hover": {
      backgroundColor: theme.palette.c_gray3,
    },
    ".delete-button": {
      position: "absolute",
      zIndex: 10,
      opacity: 0,
      width: "20px",
      minWidth: "20px",
      height: "20px",
      right: "0",
      top: "0",
      border: "none",
      color: theme.palette.c_gray4,
    },
    ".delete-button:hover": {
      border: "none",
      color: theme.palette.c_delete,
    },
  });

export interface FolderItemProps {
  folder: Asset;
  isParent?: boolean;
  isSelected?: boolean;
  onSelect: () => void;
  onClickParent?: (id: string) => void;
  enableContextMenu?: boolean;
  showDeleteButton?: boolean;
  openDeleteDialog?: () => void;
}

const FolderItem: React.FC<FolderItemProps> = ({
  folder,
  isParent,
  isSelected,
  enableContextMenu = true,
  showDeleteButton = true,
  onSelect,
  // openDeleteDialog,
}) => {
  const {
    isDragHovered,
    handleDrag,
    handleDragOver,
    handleDragEnter,
    handleDragLeave,
    handleDrop,
    handleContextMenu,
    handleDelete,
  } = useAssetActions(folder);

  return (
    <div
      css={styles}
      className={`folder-item ${isSelected ? "selected" : ""} ${
        isParent ? "parent" : ""
      } ${isDragHovered ? "drag-hover" : ""}`}
      onClick={onSelect}
      // onDoubleClick={() => handleDoubleClick(folder)}
      onDragStart={handleDrag}
      onDragOver={handleDragOver}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onContextMenu={(e) => handleContextMenu(e, enableContextMenu)}
      draggable
    >
      <FolderIcon className="folder-icon" />
      {isParent && <NorthWest className="parent-icon" />}
      <Typography className="name">{folder.name}</Typography>
      {showDeleteButton && (
        <ButtonGroup className="asset-item-actions" size="small">
          <DeleteButton<Asset>
            className="asset-delete"
            item={folder}
            onClick={() => handleDelete()}
          />
        </ButtonGroup>
      )}
    </div>
  );
};

export default FolderItem;
