/** @jsxImportSource @emotion/react */
import { css } from "@emotion/react";
import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState
} from "react";
import { Box, Divider, Typography } from "@mui/material";
import { useAssetStore } from "../../hooks/AssetStore";
import useSessionStateStore from "../../stores/SessionStateStore";
import { useAssetDeletion } from "../../serverState/useAssetDeletion";
import { useAssetUpload } from "../../serverState/useAssetUpload";
import { useAssetUpdate } from "../../serverState/useAssetUpdate";
import useAssets from "../../serverState/useAssets";
import ThemeNodetool from "../themes/ThemeNodetool";
import { Asset } from "../../stores/ApiTypes";
import AudioPlayer from "../audio/AudioPlayer";
import Dropzone from "./Dropzone";
import AssetActions from "./AssetActions";
import AssetItemContextMenu from "../context_menus/AssetItemContextMenu";
import AssetDeleteConfirmation from "./AssetDeleteConfirmation";
import AssetRenameConfirmation from "./AssetRenameConfirmation";
import AssetUploadOverlay from "./AssetUploadOverlay";
import SearchInput from "../search/SearchInput";
import AssetMoveToFolderConfirmation from "./AssetMoveToFolderConfirmation";
import { useKeyPressedStore } from "../../stores/KeyPressedStore";
import AssetGridContent from "./AssetGridContent";
import { useNodeStore } from "../../stores/NodeStore";
import { prettyDate } from "../../utils/formatDateAndTime";

const styles = (theme: any) =>
  css({
    "&": {
      display: "flex",
      flexDirection: "column",
      justifyContent: "flex-start",
      height: "100%"
    },
    ".asset-menu": {
      margin: "0",
      display: "flex",
      flexWrap: "wrap",
      justifyContent: "start",
      alignItems: "start",
      gap: ".5em",
      transition: "max-height 0.5s ease-in-out"
    },
    ".dropzone": {
      display: "flex",
      flexDirection: "column",
      position: "relative",
      flexGrow: 1,
      flexShrink: 1,
      width: "100%",
      maxHeight: "calc(-273px + 100vh)"
    },
    ".selected-asset-info": {
      backgroundColor: theme.palette.c_gray1,
      minHeight: "100px",
      minWidth: "200px",
      overflowY: "auto",
      overflowX: "hidden",
      fontSize: ThemeNodetool.fontSizeSmall,
      padding: "0.1em 0.2em",
      color: theme.palette.c_gray5
    },
    ".file-upload-button button": {
      width: "100%",
      maxWidth: "155px"
    },
    ".current-folder": {
      minWidth: "100px",
      fontSize: ThemeNodetool.fontSizeSmall,
      color: theme.palette.c_gray5,
      padding: "0.5em 0 0 .25em"
    },
    ".folder-slash": {
      color: theme.palette.c_hl1,
      fontWeight: 600,
      marginRight: "0.25em",
      userSelect: "none"
    },
    ".selected-info": {
      fontSize: "12px !important",
      color: theme.palette.c_gray4,
      minHeight: "25px",
      display: "block"
    },
    ".audio-controls-container": {
      position: "absolute",
      display: "flex",
      flexDirection: "column",
      gap: "0.25em",
      zIndex: 5000,
      bottom: "0",
      left: "0",
      width: "100%",
      padding: "0.5em",
      backgroundColor: theme.palette.c_gray1
    }
  });

interface AssetGridProps {
  maxItemSize?: number;
  itemSpacing?: number;
}

const AssetGrid: React.FC<AssetGridProps> = ({
  maxItemSize = 100,
  itemSpacing = 2
}) => {
  console.log("AssetGrid rendering");
  const { sortedAssets, currentAssets, error } = useAssets();
  const selectedAssetIds = useSessionStateStore(
    (state) => state.selectedAssetIds
  );
  const setSelectedAssetIds = useSessionStateStore(
    (state) => state.setSelectedAssetIds
  );
  const selectedAssets = useSessionStateStore((state) => state.selectedAssets);

  const { mutation: deleteMutation } = useAssetDeletion();
  const { mutation: updateMutation } = useAssetUpdate();
  const { mutation: moveMutation } = useAssetUpdate();

  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [renameDialogOpen, setRenameDialogOpen] = useState(false);
  const [moveToFolderDialogOpen, setMoveToFolderDialogOpen] = useState(false);

  const [searchTerm, setSearchTerm] = useState("");
  const currentFolder = useAssetStore((state) => state.currentFolder);
  const currentFolderId = useAssetStore((state) => state.currentFolderId);
  const setCurrentFolderId = useAssetStore((state) => state.setCurrentFolderId);
  const [lastSelectedAssetId, setLastSelectedAssetId] = useState<string | null>(
    null
  );

  const [currentAudioAsset, setCurrentAudioAsset] = useState<Asset | null>(
    null
  );

  const F2KeyPressed = useKeyPressedStore((state) => state.isKeyPressed("F2"));
  const controlKeyPressed = useKeyPressedStore((state) =>
    state.isKeyPressed("control")
  );
  const metaKeyPressed = useKeyPressedStore((state) =>
    state.isKeyPressed("meta")
  );
  const shiftKeyPressed = useKeyPressedStore((state) =>
    state.isKeyPressed("shift")
  );
  const spaceKeyPressed = useKeyPressedStore((state) =>
    state.isKeyPressed(" ")
  );

  const containerRef = useRef<HTMLDivElement>(null);

  const { uploadAsset } = useAssetUpload();

  // const filteredAssets = useMemo(() => {
  //   const filtered = sortedAssets.filter((asset) =>
  //     asset.name.toLowerCase().includes(searchTerm.toLowerCase())
  //   );
  //   console.log("filteredAssets:", filtered);
  //   return filtered;
  // }, [sortedAssets, searchTerm]);

  const handleClickOutside = useCallback(
    (e: MouseEvent) => {
      const clickedElement = e.target as HTMLElement;
      if (!shiftKeyPressed && !controlKeyPressed && !metaKeyPressed) {
        if (
          !clickedElement.classList.contains("selected-asset-info") &&
          (clickedElement.classList.contains("content-type-header") ||
            clickedElement.classList.contains("selected-info") ||
            clickedElement.classList.contains("infinite-scroll-component") ||
            clickedElement.classList.contains("asset-grid-flex") ||
            clickedElement.classList.contains("divider") ||
            clickedElement.classList.contains("current-folder") ||
            clickedElement.classList.contains("asset-info") ||
            clickedElement.classList.contains("asset-grid-container") ||
            clickedElement.classList.contains("MuiTabs-flexContainer"))
        ) {
          if (selectedAssetIds.length > 0) {
            setSelectedAssetIds([]);
          }
        }
      }
    },
    [
      shiftKeyPressed,
      controlKeyPressed,
      metaKeyPressed,
      selectedAssetIds,
      setSelectedAssetIds
    ]
  );

  useEffect(() => {
    window.addEventListener("click", handleClickOutside);
    return () => {
      window.removeEventListener("click", handleClickOutside);
    };
  }, [handleClickOutside]);

  useEffect(() => {
    if (F2KeyPressed && selectedAssetIds.length > 0) {
      setRenameDialogOpen(true);
    }
  }, [F2KeyPressed, selectedAssetIds]);

  const handleSelectAsset = useCallback(
    (assetId: string) => {
      const selectedAssetIndex = sortedAssets.findIndex(
        (asset) => asset.id === assetId
      );
      const lastSelectedIndex = lastSelectedAssetId
        ? sortedAssets.findIndex((asset) => asset.id === lastSelectedAssetId)
        : -1;

      const selectedAsset = sortedAssets.find((asset) => asset.id === assetId);
      const isAudio = selectedAsset?.content_type.match("audio") !== null;

      if (shiftKeyPressed && lastSelectedIndex !== -1) {
        const start = Math.min(selectedAssetIndex, lastSelectedIndex);
        const end = Math.max(selectedAssetIndex, lastSelectedIndex);
        const newSelectedIds = sortedAssets
          .slice(start, end + 1)
          .map((asset) => asset.id);
        setSelectedAssetIds(newSelectedIds);
      } else if (controlKeyPressed || metaKeyPressed) {
        const newAssetIds = selectedAssetIds.includes(assetId)
          ? selectedAssetIds.filter((id) => id !== assetId)
          : [...selectedAssetIds, assetId];
        setSelectedAssetIds(newAssetIds);
      } else {
        if (selectedAssetIds[0] != assetId) {
          setSelectedAssetIds([assetId]);
        }
      }

      setLastSelectedAssetId(assetId);

      if (isAudio) {
        setCurrentAudioAsset(selectedAsset ? selectedAsset : null);
      } else {
        setCurrentAudioAsset(null);
      }
    },
    [
      lastSelectedAssetId,
      shiftKeyPressed,
      controlKeyPressed,
      metaKeyPressed,
      setSelectedAssetIds,
      selectedAssetIds,
      sortedAssets
    ]
  );

  useEffect(() => {
    if (selectedAssetIds.length === 0) {
      setCurrentAudioAsset(null);
    }
  }, [selectedAssetIds, setCurrentAudioAsset]);

  const handleSelectAllAssets = useCallback(() => {
    const allAssetIds = currentAssets.map((asset) => asset.id);
    setSelectedAssetIds(allAssetIds);
    setLastSelectedAssetId(null);
  }, [currentAssets, setSelectedAssetIds]);

  const handleDeselectAssets = useCallback(() => {
    setSelectedAssetIds([]);
    setLastSelectedAssetId(null);
  }, [setSelectedAssetIds]);

  const uploadFiles = useCallback(
    (files: File[]) => {
      const workflow = useNodeStore.getState().workflow;
      files.forEach((file: File) => {
        uploadAsset({
          file: file,
          workflow_id: workflow.id,
          parent_id: currentFolderId || undefined
        });
      });
    },
    [currentFolderId, uploadAsset]
  );

  const handleSearchChange = (newSearchTerm: string) => {
    setSearchTerm(newSearchTerm);
  };

  const handleSearchClear = () => {
    setSearchTerm("");
  };

  return (
    <Box css={styles} className="asset-grid-container" ref={containerRef}>
      {error && <Typography sx={{ color: "red" }}>{error.message}</Typography>}
      <AssetUploadOverlay />
      <div className="asset-menu">
        <SearchInput
          onSearchChange={handleSearchChange}
          onSearchClear={handleSearchClear}
          focusOnTyping={false}
          focusSearchInput={false}
          focusOnEscapeKey={false}
          maxWidth={"9em"}
        />
        <AssetActions
          setSelectedAssetIds={setSelectedAssetIds}
          handleSelectAllAssets={handleSelectAllAssets}
          handleDeselectAssets={handleDeselectAssets}
          maxItemSize={maxItemSize}
        />
        <Typography className="current-folder">
          <span className="folder-slash">/</span>
          {currentFolder && `${currentFolder.name}`}
        </Typography>
        <div className="selected-asset-info">
          <Typography variant="body1" className="selected-info">
            {selectedAssetIds.length > 0 && (
              <>
                {selectedAssetIds.length}{" "}
                {selectedAssetIds.length === 1 ? "item " : "items "}
                selected
              </>
            )}
          </Typography>
          {selectedAssetIds.length === 1 && (
            <Typography variant="body2" className="asset-info">
              <span
                style={{
                  color: "white",
                  fontSize: ThemeNodetool.fontSizeSmall
                }}
              >
                {selectedAssets[0]?.name}{" "}
              </span>
              <br />
              {selectedAssets[0]?.content_type}
              <br />
              {prettyDate(selectedAssets[0]?.created_at)}
            </Typography>
          )}
        </div>
      </div>
      <Dropzone onDrop={uploadFiles}>
        {/* <div style={{ height: "calc(100% - 40px)" }}> */}
        <div style={{ height: "100%" }}>
          <AssetGridContent
            selectedAssetIds={selectedAssetIds}
            handleSelectAsset={handleSelectAsset}
            setCurrentFolderId={setCurrentFolderId}
            setSelectedAssetIds={setSelectedAssetIds}
            openDeleteDialog={() => setDeleteDialogOpen(true)}
            openRenameDialog={() => setRenameDialogOpen(true)}
            setCurrentAudioAsset={setCurrentAudioAsset}
            itemSpacing={itemSpacing}
            searchTerm={searchTerm}
          />
        </div>
      </Dropzone>
      <Divider />
      {currentAudioAsset && (
        <AudioPlayer
          fontSize="small"
          alwaysShowControls={true}
          url={currentAudioAsset?.get_url || ""}
          filename={currentAudioAsset?.name}
          height={30}
          waveformHeight={30}
          barHeight={1.0}
          minimapHeight={20}
          minimapBarHeight={1.0}
          waveColor="#ddd"
          progressColor="#666"
          minPxPerSec={1}
          playOnLoad={spaceKeyPressed}
        />
      )}
      <AssetItemContextMenu
        openDeleteDialog={() => setDeleteDialogOpen(true)}
        openRenameDialog={() => setRenameDialogOpen(true)}
        openMoveToFolderDialog={() => setMoveToFolderDialogOpen(true)}
      />
      <AssetDeleteConfirmation
        mutation={deleteMutation}
        dialogOpen={deleteDialogOpen}
        setDialogOpen={setDeleteDialogOpen}
        assets={selectedAssetIds}
      />
      <AssetRenameConfirmation
        mutation={updateMutation}
        dialogOpen={renameDialogOpen}
        setDialogOpen={setRenameDialogOpen}
        assets={selectedAssetIds}
      />
      <AssetMoveToFolderConfirmation
        mutation={moveMutation}
        dialogOpen={moveToFolderDialogOpen}
        setDialogOpen={setMoveToFolderDialogOpen}
        assets={selectedAssetIds}
      />
    </Box>
  );
};

export default React.memo(AssetGrid);
