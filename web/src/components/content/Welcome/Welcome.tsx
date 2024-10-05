/** @jsxImportSource @emotion/react */
import React, {
  useState,
  useCallback,
  ReactNode,
  useMemo,
  useEffect
} from "react";
import {
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  TextField,
  InputAdornment,
  Tabs,
  Tab,
  Box,
  Link,
  FormControlLabel,
  Tooltip,
  Checkbox,
  List,
  ListItem,
  ListItemText
} from "@mui/material";
import Fuse from "fuse.js";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import SearchIcon from "@mui/icons-material/Search";
import CloseButton from "../../buttons/CloseButton";
import { overviewContents, Section } from "./OverviewContent";
import { css } from "@emotion/react";
import { useSettingsStore } from "../../../stores/SettingsStore";
import WhatsNew from "./WhatsNew";
import useRemoteSettingsStore from "../../../stores/RemoteSettingStore";
import RemoteSettingsMenu from "../../menus/RemoteSettingsMenu";
import ThemeNodetool from "../../themes/ThemeNodetool";
import RecommendedModels from "../../hugging_face/RecommendedModels";
import { UnifiedModel } from "../../../stores/ApiTypes";
import { useModelDownloadStore } from "../../../stores/ModelDownloadStore";
import { DownloadProgress } from "../../hugging_face/DownloadProgress";
import OverallDownloadProgress from "../../hugging_face/OverallDownloadProgress";

enum TabValue {
  Overview = 0,
  WhatsNew = 1,
  Links = 2,
  Setup = 3
}

interface TabPanelProps {
  children: React.ReactNode;
  value: TabValue;
  index: TabValue;
}

const welcomeStyles = (theme: any) =>
  css({
    "&": {
      backgroundColor: "#222",
      padding: "2em",
      borderRadius: ".5em",
      position: "fixed",
      width: "100vw",
      height: "100vh",
      top: "0",
      left: "0",
      overflowY: "hidden",
      border: `8px solid ${theme.palette.c_gray0}`,
      display: "flex",
      flexDirection: "column"
    },
    ".panel-title": {
      paddingLeft: "0",
      margin: 0,
      color: theme.palette.c_white,
      marginBottom: "1em"
    },
    ".summary": {
      fontFamily: theme.fontFamily,
      fontSize: theme.fontSizeBigger,
      color: theme.palette.c_hl1,
      backgroundColor: theme.palette.c_gray1
    },
    ".content": {
      padding: "1em",
      color: theme.palette.c_white,
      fontFamily: theme.fontFamily,
      fontSize: theme.fontSizeBig
    },

    ".content ul": {
      marginLeft: "0",
      paddingLeft: "1em"
    },
    ".content ul li": {
      listStyleType: "square",
      marginLeft: "0",
      marginBottom: 0,
      fontSize: theme.fontSizeNormal,
      fontFamily: theme.fontFamily1
    },
    ".search": {
      marginBottom: "1em"
    },
    ".MuiAccordion-root": {
      background: "transparent",
      color: theme.palette.c_white,
      borderBottom: `1px solid ${theme.palette.c_gray3}`
    },
    ".MuiAccordionSummary-content.Mui-expanded": {
      margin: "0"
    },
    ".MuiAccordionSummary-root": {
      minHeight: "48px"
    },
    ".MuiAccordionSummary-content": {
      margin: "12px 0"
    },
    ".MuiTypography-root": {
      fontFamily: theme.fontFamily
    },
    ".MuiListItemText-primary": {
      fontWeight: "bold"
    },
    "ul, ol": {
      fontFamily: theme.fontFamily1,
      paddingLeft: "0"
    },
    ".highlight": {
      backgroundColor: theme.palette.c_hl1,
      color: theme.palette.c_black
    },
    ".tab-content": {
      marginTop: "1em"
    },
    ".link": {
      color: theme.palette.c_gray6,
      display: "inline-block",
      padding: "4px 8px",
      textDecoration: "none",
      backgroundColor: theme.palette.c_gray2,
      borderRadius: "4px",
      transition: "all 0.2s"
    },
    ".link:hover": {
      color: theme.palette.c_black,
      backgroundColor: theme.palette.c_hl1
    },

    ".link-body": {
      fontSize: theme.fontSizeNormal,
      backgroundColor: "transparent",
      color: theme.palette.c_gray6,
      marginTop: ".25em",
      marginBottom: "2em",
      display: "block"
    },

    ".header-container": {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    },
    ".header-right": {
      display: "flex",
      alignItems: "center",
      gap: "3em"
    },
    ".header": {
      position: "sticky",
      top: 0,
      backgroundColor: "#222",
      zIndex: 1,
      padding: "1em",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    },
    ".show-on-startup-toggle": {
      marginTop: "-1em"
    },
    ".content-area": {
      display: "flex",
      flexDirection: "column",
      height: "calc(100% - 60px)"
    },
    ".tabs-and-search": {
      position: "sticky",
      top: 0,
      backgroundColor: "#222",
      zIndex: 1,
      paddingBottom: "1em"
    },
    ".scrollable-content": {
      flex: 1,
      overflowY: "auto",
      padding: "1em"
    },
    ".fake-button": {
      color: "#fff",
      backgroundColor: theme.palette.c_gray2,
      textTransform: "uppercase",
      fontFamily: theme.fontFamily2,
      fontSize: theme.fontSizeNormal,
      margin: "0 .5em"
    },
    ".setup-tab h4, .setup-tab h5": {
      fontFamily: theme.fontFamily,
      marginBottom: "1em"
    },
    ".setup-tab .MuiListItemText-primary": {
      fontWeight: "bold",
      color: theme.palette.c_hl3
    },
    ".setup-tab .MuiListItemText-secondary": {
      color: theme.palette.c_white
    },
    ".remote-settings-container": {
      backgroundColor: theme.palette.c_gray1,
      padding: "1.5em",
      borderRadius: "8px"
    }
  });

function TabPanel(props: TabPanelProps) {
  const { children, value, index } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`overview-tabpanel-${index}`}
      aria-labelledby={`overview-tab-${index}`}
    >
      {value === index && <Box className="tab-content">{children}</Box>}
    </div>
  );
}

const recommendedModels: UnifiedModel[] = [
  {
    id: "SG161222/Realistic_Vision_V5.1_noVAE",
    name: "Realistic Vision V6",
    type: "hf.stable_diffusion",
    repo_id: "SG161222/Realistic_Vision_V5.1_noVAE",
    path: "Realistic_Vision_V5.1_fp16-no-ema.safetensors"
  },
  {
    id: "stabilityai/sd-x2-latent-upscaler",
    name: "SD XL Latent Upscaler",
    type: "hf.stable_diffusion",
    repo_id: "stabilityai/sd-x2-latent-upscaler",
    allow_patterns: ["**/*.json", "**/*.txt", "**/*.json"]
  },
  {
    id: "Qwen 2",
    name: "qwen2:0.5b",
    type: "llama_model",
    repo_id: "qwen2:0.5b"
  },
  {
    id: "whisper-large-v3",
    name: "whisper-large-v3",
    type: "hf.automatic_speech_recognition",
    repo_id: "openai/whisper-large-v3"
  }
];

const extractText = (node: ReactNode): string => {
  if (typeof node === "string") return node;
  if (React.isValidElement(node)) {
    return React.Children.toArray(node.props.children)
      .map(extractText)
      .join(" ");
  }
  if (Array.isArray(node)) {
    return node.map(extractText).join(" ");
  }
  return "";
};

const Welcome = ({ handleClose }: { handleClose: () => void }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [tabValue, setTabValue] = useState<TabValue>(TabValue.Overview);
  const sections: Section[] = overviewContents.map((section) => ({
    ...section,
    originalContent: section.content
  }));
  const { downloads } = useModelDownloadStore();
  const { settings, updateSettings } = useSettingsStore();
  const { settings: remoteSettings, secrets } = useRemoteSettingsStore();

  const hasSetupKeys = useMemo(() => {
    return !!(
      secrets.OPENAI_API_KEY &&
      secrets.REPLICATE_API_TOKEN &&
      secrets.ANTHROPIC_API_KEY
    );
  }, [secrets]);

  const theme = ThemeNodetool;

  // Add this useEffect to set the initial tab value
  useEffect(() => {
    if (!hasSetupKeys) {
      setTabValue(TabValue.Setup);
    }
  }, [hasSetupKeys]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: TabValue) => {
    setTabValue(newValue);
  };

  const { startDownload, openDialog } = useModelDownloadStore();

  const highlightText = (text: string, term: string) => {
    if (!term) return text;
    const parts = text.split(new RegExp(`(${term})`, "gi"));
    return parts.map((part, index) =>
      part.toLowerCase() === term.toLowerCase() ? (
        <span key={index} className="highlight">
          {part}
        </span>
      ) : (
        part
      )
    );
  };

  const performSearch = useCallback(
    (searchTerm: string) => {
      if (searchTerm.length > 1) {
        const fuseOptions = {
          keys: [
            { name: "title", weight: 0.4 },
            { name: "content", weight: 0.6 }
          ],
          includeMatches: true,
          ignoreLocation: true,
          threshold: 0.2,
          distance: 100,
          shouldSort: true,
          includeScore: true,
          minMatchCharLength: 2,
          useExtendedSearch: true,
          tokenize: true,
          matchAllTokens: false
        };

        const entries = sections.map((section) => ({
          ...section,
          content: extractText(section.content)
        }));

        const fuse = new Fuse(entries, fuseOptions);
        const filteredData = fuse
          .search(searchTerm)
          .map((result) => result.item);

        return filteredData;
      }
      return searchTerm.length === 0 ? sections : [];
    },
    [sections]
  );

  const filteredSections = useMemo(
    () => performSearch(searchTerm),
    [performSearch, searchTerm]
  );

  const renderContent = (content: ReactNode): ReactNode => {
    if (typeof content === "string") {
      return highlightText(content, searchTerm);
    }
    if (React.isValidElement(content)) {
      return React.cloneElement(
        content,
        {},
        React.Children.map(content.props.children, (child) =>
          typeof child === "string"
            ? highlightText(child, searchTerm)
            : renderContent(child)
        )
      );
    }
    if (Array.isArray(content)) {
      return content.map((item, index) => (
        <React.Fragment key={index}>{renderContent(item)}</React.Fragment>
      ));
    }
    return content;
  };

  const handleToggleWelcomeOnStartup = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    updateSettings({ showWelcomeOnStartup: event.target.checked });
  };

  return (
    <div css={welcomeStyles}>
      <div className="header">
        <Typography className="panel-title" variant="h2">
          NODETOOL
        </Typography>

        <div className="header-right">
          <div className="show-on-startup-toggle">
            <Tooltip
              title="You can always open this screen from the Nodetool logo in the top left."
              arrow
            >
              <FormControlLabel
                control={
                  <Checkbox
                    checked={settings.showWelcomeOnStartup}
                    onChange={handleToggleWelcomeOnStartup}
                    name="showWelcomeOnStartup"
                  />
                }
                label="Show on Startup"
              />
            </Tooltip>
          </div>
          <CloseButton onClick={handleClose} />
        </div>
      </div>

      <div className="content-area">
        <div className="tabs-and-search">
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            aria-label="overview tabs"
          >
            <Tab label="Overview" id="tab-0" aria-controls="tabpanel-0" />
            <Tab label="Whats New" id="tab-1" aria-controls="tabpanel-1" />
            <Tab label="Links" id="tab-2" aria-controls="tabpanel-2" />
            <Tab label="Setup" id="tab-3" aria-controls="tabpanel-3" />
          </Tabs>

          {tabValue === TabValue.Overview && (
            <TextField
              className="search"
              fullWidth
              variant="outlined"
              placeholder="Search"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                )
              }}
            />
          )}
        </div>

        <div className="scrollable-content">
          <TabPanel value={tabValue} index={TabValue.Overview}>
            {(searchTerm === "" ? sections : filteredSections).map(
              (section, index) => (
                <Accordion key={section.id} defaultExpanded={index === 0}>
                  <AccordionSummary
                    className="summary"
                    expandIcon={<ExpandMoreIcon />}
                  >
                    <Typography>
                      {highlightText(section.title, searchTerm)}
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails className="content">
                    {renderContent(section.originalContent)}
                  </AccordionDetails>
                </Accordion>
              )
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={TabValue.WhatsNew}>
            <WhatsNew />
          </TabPanel>

          <TabPanel value={tabValue} index={TabValue.Links}>
            <Link
              href="https://forum.nodetool.ai"
              target="_blank"
              rel="noopener noreferrer"
              className="link"
            >
              Forum
            </Link>
            <div className="link-body">
              Go to the NodeTool forum for help and advice or share what you
              made.
            </div>
            <Link
              href="https://github.com/nodetool-ai/nodetool"
              target="_blank"
              rel="noopener noreferrer"
              className="link"
            >
              GitHub
            </Link>
            <div className="link-body">
              Want to run Nodetool locally or contribute to its development?
              <br />
              Nodetool is open-source and available on GitHub.
              <br />
              You can customize it, add new nodes, or integrate it into your own
              AI workflows.
              <br />
              Check out the repository for installation instructions and
              documentation.
              <br />
              Let us know what you build!
            </div>
          </TabPanel>

          <TabPanel value={tabValue} index={TabValue.Setup}>
            <Box sx={{ display: "flex", flexDirection: "column", gap: "2em" }}>
              <Typography variant="h4" sx={{ color: theme.palette.c_hl1 }}>
                Welcome to Nodetool
              </Typography>

              <Box sx={{ display: "flex", gap: "2em" }}>
                <Box sx={{ flex: 1 }}>
                  <Typography
                    variant="h5"
                    sx={{ mb: 2, color: theme.palette.c_hl2 }}
                  >
                    How to Use AI Models
                  </Typography>
                  <Typography variant="body1" gutterBottom>
                    You can use both local and remote AI models in Nodetool:
                  </Typography>
                  <List>
                    <ListItem
                      sx={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "flex-start",
                        mb: 2
                      }}
                    >
                      <ListItemText
                        primary={
                          <Typography
                            variant="subtitle1"
                            sx={{
                              fontWeight: "bold",
                              color: theme.palette.c_hl1
                            }}
                          >
                            1. Use Local Models via HuggingFace
                          </Typography>
                        }
                        secondary={
                          <Box sx={{ mt: 1 }}>
                            <Typography variant="body2">
                              • Download and run models locally for privacy and
                              offline use.
                            </Typography>
                            <Typography variant="body2">
                              • Look for the{" "}
                              <span className="fake-button">
                                Recommended Models
                              </span>{" "}
                              button on compatible nodes.
                            </Typography>
                            <Typography variant="body2">
                              • Use the{" "}
                              <span className="fake-button">Models</span> button
                              in the top panel to manage all models.
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    <ListItem
                      sx={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "flex-start"
                      }}
                    >
                      <ListItemText
                        primary={
                          <Typography
                            variant="subtitle1"
                            sx={{
                              fontWeight: "bold",
                              color: theme.palette.c_hl1
                            }}
                          >
                            2. Use Remote Models
                          </Typography>
                        }
                        secondary={
                          <Box sx={{ mt: 1 }}>
                            <Typography variant="body2">
                              • Set up API keys to access cloud-based AI models.
                            </Typography>
                            <Typography variant="body2">
                              • Ideal for more powerful models or when local
                              resources are limited.
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                  </List>
                  <Typography variant="body1" sx={{ mt: 2 }}>
                    Choose the option that best suits your needs and project
                    requirements.
                  </Typography>
                  <Typography variant="body1" sx={{ mt: 1 }}>
                    You can enter your API keys now or access them later via the{" "}
                    <span className="fake-button">Settings</span> menu.
                  </Typography>
                </Box>

                <Box
                  sx={{
                    flex: 1,
                    color: theme.palette.c_hl2,
                    backgroundColor: theme.palette.c_gray1,
                    padding: "20px",
                    borderRadius: "20px"
                  }}
                >
                  <Typography variant="h5">Recommended Models</Typography>
                  <RecommendedModels
                    recommendedModels={recommendedModels}
                    initialViewMode="list"
                    startDownload={startDownload}
                    compactView={true}
                  />
                  <Box mt={2}>
                    {Object.keys(downloads).map((name) => (
                      <DownloadProgress key={name} name={name} />
                    ))}
                  </Box>
                </Box>

                <Box
                  sx={{
                    flex: 1,
                    backgroundColor: theme.palette.c_gray1,
                    p: 3,
                    borderRadius: "20px"
                  }}
                >
                  <Typography
                    variant="h5"
                    sx={{ mb: 2, color: theme.palette.c_hl2 }}
                  >
                    Remote Model Setup
                  </Typography>
                  <RemoteSettingsMenu />
                </Box>
              </Box>
            </Box>
          </TabPanel>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
