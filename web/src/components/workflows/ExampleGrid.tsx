/** @jsxImportSource @emotion/react */

import { Typography, Box, CircularProgress } from "@mui/material";
import { useWorkflowStore } from "../../stores/WorkflowStore";
import { useCallback } from "react";
import { Workflow, WorkflowList } from "../../stores/ApiTypes";
import { useNavigate } from "react-router-dom";
import ThemeNodetool from "../themes/ThemeNodetool";
import { useQuery } from "@tanstack/react-query";
import { ErrorOutlineRounded } from "@mui/icons-material";
import { css } from "@emotion/react";

const styles = () =>
  css({
    ".container": {
      display: "flex",
      flexWrap: "wrap"
    },
    ".workflow": {
      flex: "1 0 200px",
      margin: "20px",
      maxWidth: "200px",
      cursor: "pointer"
    },
    ".loading-indicator": {
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      flexDirection: "column",
      height: "50vh",
      width: "100%"
    },
    ".image-wrapper": {
      width: "200px",
      height: "200px",
      overflow: "hidden",
      position: "relative"
    },
    ".workflow img": {
      width: "100%",
      height: "100%",
      objectFit: "cover"
    }
  });

const ExampleGrid = () => {
  const navigate = useNavigate();
  const copyWorkflow = useWorkflowStore((state) => state.copy);
  const loadWorkflows = useWorkflowStore((state) => state.loadExamples);

  const { data, isLoading, isError, error } = useQuery<WorkflowList, Error>({
    queryKey: ["examples"],
    queryFn: loadWorkflows
  });

  const onClickWorkflow = useCallback(
    (workflow: Workflow) => {
      // setShouldAutoLayout(true);
      copyWorkflow(workflow).then((workflow) => {
        navigate("/editor/" + workflow.id);
      });
    },
    [copyWorkflow, navigate]
  );

  return (
    <div className="workflow-grid" css={styles}>
      <Typography variant="h4" component="h1" sx={{ ml: 5, mt: 5 }}>
        Example Workflows
      </Typography>
      <Box className="container">
        {isLoading && (
          <div className="loading-indicator">
            <CircularProgress />
            <Typography variant="h4">Loading Examples</Typography>
          </div>
        )}
        {isError && (
          <ErrorOutlineRounded>
            <Typography>{error?.message}</Typography>
          </ErrorOutlineRounded>
        )}
        {data?.workflows.map((workflow) => (
          <Box
            key={workflow.id}
            className="workflow"
            onClick={() => onClickWorkflow(workflow)}
          >
            <Box className="image-wrapper">
              {workflow.thumbnail_url && (
                <img
                  width="200px"
                  src={workflow.thumbnail_url}
                  alt={workflow.name}
                />
              )}
            </Box>
            <Typography variant="h4" component={"h4"}>
              {workflow.name}
            </Typography>
            <Typography style={{ fontFamily: ThemeNodetool.fontFamily1 }}>
              {workflow.description}
            </Typography>
          </Box>
        ))}
      </Box>
    </div>
  );
};

export default ExampleGrid;
