/** @jsxImportSource @emotion/react */
import { memo } from "react";
import useWorkflowRunnner from "../../stores/WorkflowRunner";
import { css } from "@emotion/react";
import { useClipboard } from "../../hooks/browser/useClipboard";
import { Button } from "@mui/material";

export const errorStyles = (theme: any) =>
  css({
    position: "relative",
    backgroundColor: theme.palette.c_error,
    borderRadius: "1px",
    padding: "0",
    margin: "1em",
    transition: "background-color 0.2s",
    maxWidth: "160px",

    ".error-text": {
      maxHeight: "4em",
      wordSpacing: "-0.3em",
      fontSize: theme.fontSizeTiny,
      color: theme.palette.c_black,
      cursor: "auto",
      userSelect: "text",
      lineHeight: "1.2em",
      padding: "0.25em",
      overflowX: "visible",
      overflowY: "auto",
      "&::selection": {
        backgroundColor: theme.palette.c_white
      }
    },
    button: {
      position: "absolute",
      left: "-.3em",
      top: "-1.1em",
      height: "1em",
      padding: ".1em .4em 0",
      borderRadius: "1px",
      fontSize: theme.fontSizeTinyer,
      color: theme.palette.c_black,
      backgroundColor: theme.palette.c_white,
      "&:hover": {
        backgroundColor: theme.palette.c_gray5
      }
    }
  });

export const NodeErrors = memo(function NodeErrors({ id }: { id: string }) {
  const errors = useWorkflowRunnner((state) => state.errors);
  const error = errors[id];
  const { writeClipboard } = useClipboard();

  if (!error) {
    return null;
  }
  return (
    <div css={errorStyles} className="node-error nodrag nowheel">
      <Button
        size="small"
        onClick={() => writeClipboard(error, true)}
        title="Copy error to clipboard"
      >
        COPY
      </Button>
      <div className="error-text">{error}</div>
    </div>
  );
});
