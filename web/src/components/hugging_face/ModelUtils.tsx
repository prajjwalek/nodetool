import React from "react";
import { UnifiedModel } from "../../stores/ApiTypes";
import { Box, Button, Tooltip, Typography } from "@mui/material";
import DeleteButton from "../buttons/DeleteButton";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { client, isProduction } from "../../stores/ApiClient";
import ModelIcon from "../../icons/model.svg";
import DownloadIcon from "@mui/icons-material/Download";

export type OllamaModel = {
  name: string;
  modified_at: string;
  size: number;
  digest: string;
  details: {
    format: string;
    family: string;
    families: string[] | null;
    parameter_size: string;
    quantization_level: string;
  };
};

export const prettifyModelType = (type: string) => {
  if (type === "All") return type;

  if (type === "llama_model") {
    return (
      <>
        <img
          src="/ollama.png"
          alt="Ollama"
          style={{
            width: "16px",
            marginRight: "8px",
            filter: "invert(1)"
          }}
        />
        Ollama
      </>
    );
  }

  const parts = type.split(".");
  if (parts[0] === "hf") {
    parts.shift();
    return (
      <>
        <img
          src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg"
          alt="Hugging Face"
          style={{ width: "20px", marginRight: "8px" }}
        />
        {parts
          .map((part) =>
            part
              .split("_")
              .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
              .join(" ")
          )
          .join(" ")}
      </>
    );
  }

  return (
    <>
      <img
        src={ModelIcon}
        alt="Model"
        style={{
          width: "20px",
          marginRight: "8px",
          filter: "invert(1)"
        }}
      />
      {type
        .split("_")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ")}
    </>
  );
};

export interface ModelComponentProps {
  model: UnifiedModel;
  handleDelete?: (repoId: string) => void;
  onDownload?: () => void;
  compactView?: boolean;
}

export function formatId(id: string) {
  if (id.includes("/")) {
    const [owner, repo] = id.split("/");
    return (
      <>
        <span className="repo">
          {repo}
          <br />
        </span>
        <span className="owner">{owner}/</span>
      </>
    );
  }
  return <span className="repo">{id}</span>;
}

export const modelSize = (model: UnifiedModel) =>
  ((model.size_on_disk ?? 0) / 1024 / 1024).toFixed(2).toString() + " MB";

export const ModelDeleteButton: React.FC<{ onClick: () => void }> = ({
  onClick
}) => <>{!isProduction && <DeleteButton onClick={onClick} />}</>;

export const ModelDownloadButton: React.FC<{ onClick: () => void }> = ({
  onClick
}) => (
  <Button
    className="model-download-button"
    onClick={onClick}
    variant="outlined"
  >
    <DownloadIcon />
    Download
  </Button>
);

export const HuggingFaceLink: React.FC<{
  modelId: string;
}> = ({ modelId }) => (
  <Tooltip title="View on HuggingFace">
    <Button
      size="small"
      href={`https://huggingface.co/${modelId}`}
      className="model-external-link-icon huggingface-link"
      target="_blank"
      rel="noopener noreferrer"
    >
      <img
        src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg"
        alt="Hugging Face"
        style={{
          width: "1.5em",
          height: "auto"
        }}
      />
    </Button>
  </Tooltip>
);

export const OllamaLink: React.FC<{
  modelId: string;
}> = ({ modelId }) => (
  <Tooltip title="View on Ollama">
    <Button
      size="small"
      href={`https://ollama.com/library/${modelId.split(":")[0]}`}
      className="model-external-link-icon ollama-link"
      target="_blank"
      rel="noopener noreferrer"
    >
      <img
        src="/ollama.png"
        alt="Ollama"
        style={{
          width: "1.25em",
          height: "auto",
          filter: "invert(1)"
        }}
      />
    </Button>
  </Tooltip>
);

export const renderModelSecondaryInfo = (
  modelData: any,
  isHuggingFace: boolean
) => (
  <>
    {isHuggingFace && (
      <Typography variant="body2" className="text-license">
        {modelData.cardData?.license}
      </Typography>
    )}
    {!isHuggingFace && (
      <Typography variant="body2">
        {modelData.details?.parent_model} - {modelData.details?.format}
      </Typography>
    )}
  </>
);

export const renderModelActions = (
  props: ModelComponentProps,
  downloaded: boolean
) => (
  <Box
    className="model-actions"
    sx={{ display: "flex", gap: 1, alignItems: "center" }}
  >
    {props.onDownload && !downloaded && (
      <ModelDownloadButton onClick={props.onDownload} />
    )}
    {downloaded && (
      <Tooltip title="Model downloaded">
        <CheckCircleIcon
          className="model-downloaded-icon"
          fontSize="small"
          color="success"
        />
      </Tooltip>
    )}
    {props.handleDelete && (
      <ModelDeleteButton onClick={() => props.handleDelete!(props.model.id)} />
    )}
  </Box>
);

export async function fetchOllamaModelInfo(modelName: string) {
  const { data, error } = await client.GET("/api/models/ollama_model_info", {
    params: {
      query: {
        model_name: modelName
      }
    }
  });
  if (error) {
    throw error;
  }
  return data;
}

export const groupModelsByType = (models: UnifiedModel[]) => {
  return models.reduce((acc, model) => {
    const type = model.type || "Other";
    if (!acc[type]) {
      acc[type] = [];
    }
    acc[type].push(model);
    return acc;
  }, {} as Record<string, UnifiedModel[]>);
};

export const sortModelTypes = (types: string[]) => {
  return [
    "All",
    ...types.sort((a, b) => {
      if (a === "Other") return 1;
      if (b === "Other") return -1;
      if (a === "llama_model") return -1;
      if (b === "llama_model") return 1;
      return a.localeCompare(b);
    })
  ];
};
