import React, { useCallback, useMemo } from "react";
import {
  Typography,
  Box,
  Button,
  CircularProgress,
  IconButton
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { useModelDownloadStore } from "../../stores/ModelDownloadStore";
import { keyframes } from "@emotion/react";
import ThemeNodetool from "../themes/ThemeNodetool";

const pulse = keyframes`
  0% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.8;
  }
`;

const moveRight = keyframes`
  0% {
    background-position: 0% 0;
  }
  100% {
    background-position: 100% 0;
  }
`;

export const DownloadProgress: React.FC<{ name: string }> = ({ name }) => {
  const downloads = useModelDownloadStore((state) => state.downloads);
  const cancelDownload = useModelDownloadStore((state) => state.cancelDownload);
  const removeDownload = useModelDownloadStore((state) => state.removeDownload);
  const download = downloads[name];

  const handleRemove = useCallback(() => {
    removeDownload(name);
  }, [name, removeDownload]);

  const eta = useMemo(() => {
    if (download.speed && download.speed > 0) {
      const remainingBytes = download.totalBytes - download.downloadedBytes;
      const remainingSeconds = remainingBytes / download.speed;
      const minutes = Math.floor(remainingSeconds / 60);
      const seconds = Math.floor(remainingSeconds % 60);
      return `${minutes}m ${seconds}s`;
    }
    return null;
  }, [download.speed, download.totalBytes, download.downloadedBytes]);

  const showDetails =
    download.status === "start" ||
    download.status === "idle" ||
    download.status === "pending" ||
    download.status === "running" ||
    download.status === "progress";

  if (!download) return null;

  return (
    <Box
      mt={2}
      sx={{
        border: "1px solid #999",
        borderRadius: "4px",
        padding: "16px",
        background: "#444",
        position: "relative" // Add this
      }}
    >
      <IconButton
        onClick={handleRemove}
        size="small"
        sx={{
          position: "absolute",
          top: 8,
          right: 8,
          color: "white"
        }}
      >
        <CloseIcon fontSize="small" />
      </IconButton>

      <Typography variant="subtitle1">{name}</Typography>
      {download.message && (
        <Typography variant="body2">{download.message}</Typography>
      )}
      {(download.status === "start" || download.status === "pending") && (
        <Box display="flex" alignItems="center">
          <CircularProgress
            size={20}
            style={{ marginRight: "0.5em", color: "white" }}
          />
          <Typography variant="body2">
            {download.status === "start"
              ? "Starting download..."
              : "Pending download..."}
          </Typography>
        </Box>
      )}
      {download.status === "completed" && (
        <Typography variant="body2" color={ThemeNodetool.palette.c_success}>
          Download completed
        </Typography>
      )}
      {download.status === "cancelled" && (
        <Typography variant="body2" color={ThemeNodetool.palette.c_error}>
          Download cancelled
        </Typography>
      )}
      {download.status === "error" && (
        <Typography variant="body2" color={ThemeNodetool.palette.c_error}>
          Download error
        </Typography>
      )}
      {showDetails && download.totalBytes >= 0 && (
        <>
          <Box
            sx={{
              height: "6px",
              borderRadius: "3px",
              overflow: "hidden",
              position: "relative",
              background: "#555",
              marginTop: "1em"
            }}
          >
            <Box
              sx={{
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                width: `${
                  (download.downloadedBytes / download.totalBytes) * 100
                }%`,
                background: "linear-gradient(90deg, #3a6ba5, #5a9bd5)",
                backgroundSize: "200% 100%",
                animation: `${pulse} 3s ease-in-out infinite, ${moveRight} 8s linear infinite`,
                transformOrigin: "right center"
              }}
            />
          </Box>
          <Typography variant="body2" style={{ marginTop: "1em" }}>
            Size: {(download.downloadedBytes / 1024 / 1024).toFixed(2)} MB /{" "}
            {(download.totalBytes / 1024 / 1024).toFixed(2)} MB
          </Typography>
          <Typography variant="body2" style={{ marginTop: "0.5em" }}>
            Files: {download.downloadedFiles} / {download.totalFiles}
          </Typography>
          <Typography variant="body2" style={{ marginTop: "0.5em" }}>
            Downloading: {download.currentFiles?.join(", ")}
          </Typography>
          {download.speed !== null && (
            <>
              <Typography variant="body2" style={{ marginTop: "0.5em" }}>
                Speed: {(download.speed / 1024 / 1024).toFixed(2)} MB/s
              </Typography>
              {eta && (
                <Typography variant="body2" style={{ marginTop: "0.5em" }}>
                  ETA: {eta}
                </Typography>
              )}
            </>
          )}
          <Button
            onClick={() => cancelDownload(name)}
            variant="contained"
            color="secondary"
            size="small"
            style={{ padding: "1em", marginTop: "1em" }}
          >
            Cancel
          </Button>
        </>
      )}
    </Box>
  );
};
