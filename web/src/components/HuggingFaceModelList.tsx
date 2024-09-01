/** @jsxImportSource @emotion/react */
import { css } from "@emotion/react";

import React from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { client } from "../stores/ApiClient";
import {
  Box,
  Button,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Typography,
} from "@mui/material";
import DeleteButton from "./buttons/DeleteButton";

const styles = (theme: any) =>
  css({
    "&.huggingface-model-list": {
      height: "70vh",
      overflow: "auto",
      backgroundColor: theme.palette.c_gray1,
      padding: 0,
    },
    ".model-item": {
      borderBottom: `1px solid ${theme.palette.c_gray0}`,
      marginBottom: theme.spacing(1),
      "&:hover": {
        backgroundColor: theme.palette.c_gray2,
      },
    },
    ".model-text": {
      wordBreak: "break-word",
      maxHeight: "3.5em",
      overflow: "hidden",
    },
    ".model-text span": {
      maxHeight: "2.5em",
      overflow: "hidden",
    },
    ".model-text p": {
      paddingTop: theme.spacing(1),
    },
    button: {
      color: theme.palette.c_gray5,
    },
  });

const HuggingFaceModelList: React.FC = () => {
  const {
    data: models,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["huggingFaceModels"],
    queryFn: async () => {
      const { data, error } = await client.GET(
        "/api/models/huggingface_models",
        {}
      );
      if (error) throw error;
      return data;
    },
  });

  // delete mutation
  const deleteModel = async (repoId: string) => {
    const { error } = await client.DELETE("/api/models/huggingface_model", {
      params: { query: { repo_id: repoId } },
    });
    if (error) throw error;
  };
  const mutation = useMutation({
    mutationFn: deleteModel,
  });

  if (isLoading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error"> {error.message} </Typography>;
  }

  const modelList = models?.map((model) => (
    <ListItem className="model-item" key={model.repo_id}>
      <ListItemText
        className="model-text"
        primary={model.repo_id}
        secondary={`${(model.size_on_disk / 1024 / 1024).toFixed(2)} MB`}
      />
      <DeleteButton onClick={(e) => mutation.mutate(model.repo_id)} />
    </ListItem>
  ));
  return (
    <Box className="huggingface-model-list" css={styles}>
      {mutation.isPending && <CircularProgress />}
      {mutation.isError && (
        <Typography color="error">{mutation.error.message}</Typography>
      )}
      {mutation.isSuccess && (
        <Typography color="success">Model deleted successfully</Typography>
      )}
      <List>{modelList}</List>
    </Box>
  );
};

export default HuggingFaceModelList;
