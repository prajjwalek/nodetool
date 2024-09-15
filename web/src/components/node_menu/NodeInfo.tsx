/** @jsxImportSource @emotion/react */
import { css } from "@emotion/react";
import React, { useMemo } from "react";
import { Typography, Divider, Tooltip } from "@mui/material";
import { NodeMetadata } from "../../stores/ApiTypes";
import { titleize } from "../node/BaseNode";
import { colorForType, descriptionForType } from "../../config/data_types";
import { TOOLTIP_DELAY } from "../../config/constants";

interface NodeInfoProps {
  nodeMetadata: NodeMetadata;
}

const nodeInfoStyles = (theme: any) =>
  css({
    display: "flex",
    flexDirection: "column",
    overflowY: "auto",
    gap: ".5em",
    paddingRight: "1em",
    maxHeight: "60vh",
    ".node-title": {
      fontSize: "0.8em",
      fontWeight: "600",
      color: theme.palette.c_hl1
    },
    h4: {
      fontSize: "0.8em",
      fontWeight: "600",
      color: theme.palette.c_hl1
    },
    ".node-description": {
      fontSize: "0.8em",
      fontWeight: "400",
      color: theme.palette.c_white
    },
    ".node-tags": {
      fontSize: theme.fontSizeSmall,
      color: theme.palette.c_gray4
    },
    ".node-usecases div": {
      fontSize: "0.8em",
      fontWeight: "300",
      color: theme.palette.c_gray6,
      lineHeight: "1.3em"
    },
    ".inputs-outputs": {
      paddingBottom: "1em"
    },
    ".inputs, .outputs": {
      display: "flex",
      justifyContent: "space-between",
      flexDirection: "column",
      gap: 0
    },
    ".inputs-outputs .item": {
      padding: ".25em 0 .25em 0",
      display: "flex",
      justifyContent: "space-between",
      fontFamily: theme.fontFamily2,
      fontSize: "0.7em",
      flexDirection: "row",
      gap: ".5em",
      cursor: "default"
    },
    ".inputs-outputs .item:nth-of-type(odd)": {
      backgroundColor: "#1e1e1e"
    },
    ".inputs-outputs .item .type": {
      color: theme.palette.c_white,
      textAlign: "right",
      borderRight: `4px solid ${theme.palette.c_gray4}`,
      paddingRight: ".5em"
    },
    ".inputs-outputs .item .property": {
      color: theme.palette.c_gray6
    },
    ".inputs-outputs .item .property.description": {
      color: theme.palette.c_white
    },
    ".preview-image": {
      width: "100%",
      height: "auto",
      maxHeight: "320px",
      objectFit: "contain"
    }
  });

const parseDescription = (description: string) => {
  const lines = description.split("\n");
  return {
    desc: lines[0],
    tags: lines.length > 0 ? lines[1] : [],
    useCases: lines.length > 1 ? lines.slice(2) : []
  };
};

const NodeInfo: React.FC<NodeInfoProps> = ({ nodeMetadata }) => {
  const description = useMemo(
    () => parseDescription(nodeMetadata?.description || ""),
    [nodeMetadata]
  );

  return (
    <div css={nodeInfoStyles}>
      <Typography className="node-title">
        {titleize(nodeMetadata.title)}
      </Typography>
      <Typography className="node-description">{description.desc}</Typography>
      <Typography className="node-tags">Tags: {description.tags}</Typography>
      <Typography component="div" className="node-usecases">
        {description.useCases.map((useCase, i) => (
          <div key={i}>{useCase}</div>
        ))}
      </Typography>

      {nodeMetadata.model_info.cover_image_url && (
        <img
          className="preview-image"
          src={nodeMetadata.model_info.cover_image_url}
          alt={nodeMetadata.title}
        />
      )}

      <Divider />

      <div className="inputs-outputs">
        <div className="inputs">
          <Typography variant="h4">Inputs</Typography>
          {nodeMetadata.properties.map((property) => (
            <div key={property.name} className="item">
              <Tooltip
                enterDelay={TOOLTIP_DELAY}
                placement="top-start"
                title={property.description}
              >
                <Typography
                  className={
                    property.description ? "property description" : "property"
                  }
                >
                  {property.name}
                </Typography>
              </Tooltip>
              <Tooltip
                enterDelay={TOOLTIP_DELAY}
                placement="top-end"
                title={descriptionForType(property.type.type || "")}
              >
                <Typography
                  className="type"
                  style={{
                    borderColor: colorForType(property.type.type)
                  }}
                >
                  {property.type.type}
                </Typography>
              </Tooltip>
            </div>
          ))}
        </div>
        <div className="outputs">
          <Typography variant="h4">Outputs</Typography>
          {nodeMetadata.outputs.map((property) => (
            <div key={property.name} className="item">
              <Typography className="property">{property.name}</Typography>
              <Tooltip
                enterDelay={TOOLTIP_DELAY}
                placement="top-end"
                title={descriptionForType(property.type.type || "")}
              >
                <Typography
                  className="type"
                  style={{
                    borderColor: colorForType(property.type.type)
                  }}
                >
                  {property.type.type}
                </Typography>
              </Tooltip>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default NodeInfo;
