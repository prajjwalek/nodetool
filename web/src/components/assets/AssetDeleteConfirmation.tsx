/** @jsxImportSource @emotion/react */

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Dialog,
  DialogActions,
  DialogTitle,
  Button,
  LinearProgress,
  Typography
} from "@mui/material";
import { getMousePosition } from "../../utils/MousePosition";
import { UseMutationResult } from "react-query";
import dialogStyles from "../../styles/DialogStyles";
import { Asset } from "../../stores/ApiTypes";
import useAssets from "../../serverState/useAssets";

interface AssetDeleteConfirmationProps {
  dialogOpen: boolean;
  assets: string[];
  setDialogOpen: (open: boolean) => void;
  mutation: UseMutationResult<any, unknown, string[], unknown>;
}

const AssetDeleteConfirmation = ({
  dialogOpen,
  setDialogOpen,
  assets,
  mutation
}: AssetDeleteConfirmationProps) => {
  const [dialogPosition, setDialogPosition] = useState({ x: 0, y: 0 });
  const [hasNonEmptyFolder, setHasNonEmptyFolder] = useState(false);
  const { getAssetsById, loadFolderId } = useAssets();
  const assetItems = useMemo(
    () => getAssetsById(assets),
    [assets, getAssetsById]
  );

  const checkFolders = useCallback(async () => {
    const folders = assetItems.filter(
      (asset) => asset.content_type === "folder"
    );

    let hasNonEmpty = false;
    for (const folder of folders) {
      const childAssets = await loadFolderId(folder.id);
      if (childAssets.assets.length > 0) {
        hasNonEmpty = true;
        break;
      }
    }

    setHasNonEmptyFolder(hasNonEmpty);
  }, [assetItems, loadFolderId]);

  useEffect(() => {
    if (dialogOpen) {
      const mousePosition = getMousePosition();
      setDialogPosition({ x: mousePosition.x, y: mousePosition.y });

      if (assetItems.length > 0) {
        checkFolders();
      }
    }
  }, [dialogOpen, assetItems, checkFolders]);

  const executeDeletion = useCallback(async () => {
    await mutation.mutateAsync(assets);
    setDialogOpen(false);
  }, [mutation, assets, setDialogOpen]);

  const screenWidth = window.innerWidth;
  const objectWidth = 250;
  const leftPosition = dialogPosition.x - objectWidth;

  const safeLeft = Math.min(
    Math.max(leftPosition, 0),
    screenWidth - objectWidth
  );

  return (
    <Dialog
      css={dialogStyles}
      open={dialogOpen}
      onClose={() => setDialogOpen(false)}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
      componentsProps={{
        backdrop: {
          style: {
            backgroundColor: "transparent"
          }
        }
      }}
      sx={{
        left: `${safeLeft}px`,
        top: `${dialogPosition.y - 300}px`
      }}
    >
      <DialogTitle className="dialog-title" id="alert-dialog-title">
        {mutation.isLoading && (
          <>
            <Typography variant="h5" color="error">
              {"deleting assets..."}
            </Typography>
            <LinearProgress aria-label="deleting-assets" color="secondary" />
          </>
        )}
        {mutation.isError && (
          <Typography variant="h5" color="error">
            {"Error deleting assets."}
          </Typography>
        )}
        {mutation.isIdle && (
          <>
            <span>
              {`${assets?.length} ${assets?.length === 1 ? "asset" : "assets"}`}
            </span>
            {" will be deleted"}
          </>
        )}
      </DialogTitle>
      {hasNonEmptyFolder && (
        <Typography className="error-message">
          {"Cannot delete folders that are not empty."}
        </Typography>
      )}
      <ul className="asset-names">
        {assetItems?.map((asset: Asset) => (
          <li key={asset.id}>{asset.name}</li>
        ))}
      </ul>
      <DialogActions className="dialog-actions">
        <Button className="button-cancel" onClick={() => setDialogOpen(false)}>
          Cancel
        </Button>
        <Button
          disabled={hasNonEmptyFolder}
          className="button-confirm"
          onClick={executeDeletion}
          autoFocus
        >
          Delete
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AssetDeleteConfirmation;
