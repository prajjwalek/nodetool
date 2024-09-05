import React, { useState, useEffect, useRef, useCallback } from "react";
import { Typography, Box, Button, CircularProgress } from "@mui/material";
import { useHuggingFaceStore } from "../../stores/HuggingFaceStore";
import { keyframes } from "@emotion/react";

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
  const downloads = useHuggingFaceStore((state) => state.downloads);
  const cancelDownload = useHuggingFaceStore((state) => state.cancelDownload);
  const download = downloads[name];

  if (!download) return null;

  return (
    <Box
      mt={2}
      sx={{
        border: "1px solid #999",
        borderRadius: "4px",
        padding: "16px",
        background: "#444"
      }}
    >
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
        <Typography variant="body2" color="success">
          Download completed
        </Typography>
      )}
      {download.status === "cancelled" && (
        <Typography variant="body2" color="error">
          Download cancelled
        </Typography>
      )}
      {download.status === "error" && (
        <Typography variant="body2" color="error">
          Download error
        </Typography>
      )}
      {download.status === "progress" && (
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
            Current: {download.currentFile}
          </Typography>
          {download.speed !== null && (
            <Typography variant="body2" style={{ marginTop: "0.5em" }}>
              Speed: {(download.speed / 1024 / 1024).toFixed(2)} MB/s
            </Typography>
          )}
          <Button
            onClick={() => cancelDownload(name)}
            variant="outlined"
            color="secondary"
            size="small"
            style={{ marginTop: "1em" }}
          >
            Cancel
          </Button>
        </>
      )}
    </Box>
  );
};
