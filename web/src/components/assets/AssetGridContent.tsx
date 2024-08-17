/** @jsxImportSource @emotion/react */
import { css } from "@emotion/react";
import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import AutoSizer from "react-virtualized-auto-sizer";
import { VariableSizeList as List } from "react-window";
import { useSettingsStore } from "../../stores/SettingsStore";
import useSessionStateStore from "../../stores/SessionStateStore";
import useAssets from "../../serverState/useAssets";
import { Asset } from "../../stores/ApiTypes";
import AssetGridRow from "./AssetGridRow";
import {
  getFooterHeight,
  calculateGridDimensions,
  prepareItems,
  calculateRowCount,
  getItemsForRow,
  DIVIDER_HEIGHT,
} from "./assetGridUtils";
import { useAssetSelection } from "../../hooks/assets/useAssetSelection";
import { useAssetDialog } from "../../hooks/assets/useAssetDialog";
import { useAssetStore } from "../../stores/AssetStore";

const styles = (theme: any) =>
  css({
    "&": {
      position: "relative",
      height: "100%",
      overflow: "hidden",
      paddingBottom: ".5em",
      display: "flex",
      flexDirection: "column",
    },
    ".asset-list": {
      flex: 1,
      overflow: "hidden",
    },
    ".autosizer-list": {
      paddingBottom: "10em",
    },
    ".content-type-header": {
      width: "100%",
      padding: "0.5em 0",
      backgroundColor: "transparent",
      fontSize: theme.fontSizeSmall,
      textTransform: "uppercase",
    },
    ".divider": {
      width: "100%",
      height: "2px",
      backgroundColor: theme.palette.divider,
    },
  });

interface AssetGridContentProps {
  itemSpacing?: number;
  assets?: Asset[];
}

const AssetGridContent: React.FC<AssetGridContentProps> = ({
  itemSpacing = 2,
  assets: propAssets,
}) => {
  const currentFolderId = useAssetStore((state) => state.currentFolderId);
  const selectedFolderId = useSessionStateStore(
    (state) => state.selectedFolderId
  );
  const { folderFilesFiltered } = useAssets(currentFolderId || "1");
  // const fetchAssets = useAssets(currentFolderId || "1").fetchAssets;

  const assetItemSize = useSettingsStore(
    (state) => state.settings.assetItemSize
  );

  const assets = useMemo(() => {
    if (propAssets) return propAssets;
    return folderFilesFiltered || [];
  }, [propAssets, folderFilesFiltered]);

  const { selectedAssetIds, setSelectedAssetIds, handleSelectAsset } =
    useAssetSelection(assets);
  const { openDeleteDialog, openRenameDialog } = useAssetDialog();

  const [gridDimensions, setGridDimensions] = useState({
    columns: 1,
    itemWidth: 0,
    itemHeight: 0,
  });

  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 });

  const listRef = useRef<List>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const footerHeight = useMemo(
    () => getFooterHeight(assetItemSize),
    [assetItemSize]
  );

  const preparedItems = useMemo(() => {
    return prepareItems({ other: assets || [] });
  }, [assets]);

  const updateGridDimensions = useCallback(
    (width: number) => {
      if (width > 0) {
        const dimensions = calculateGridDimensions(
          width,
          assetItemSize,
          itemSpacing
        );
        setGridDimensions((prevDimensions) => {
          if (
            prevDimensions.columns !== dimensions.columns ||
            prevDimensions.itemWidth !== dimensions.itemWidth ||
            prevDimensions.itemHeight !== dimensions.itemHeight
          ) {
            return dimensions;
          }
          return prevDimensions;
        });
      }
    },
    [assetItemSize, itemSpacing]
  );

  const rowCount = useMemo(
    () => calculateRowCount(preparedItems, gridDimensions.columns),
    [preparedItems, gridDimensions.columns]
  );

  const onDragStart = useCallback(
    (assetId: string): string[] => [...selectedAssetIds, assetId],
    [selectedAssetIds]
  );

  const getRowHeight = useCallback(
    (index: number) => {
      const rowItems = getItemsForRow(
        preparedItems,
        index,
        gridDimensions.columns
      );
      if (rowItems[0]?.isDivider) {
        return DIVIDER_HEIGHT;
      }
      return gridDimensions.itemHeight + footerHeight + itemSpacing * 2;
    },
    [preparedItems, gridDimensions, footerHeight, itemSpacing]
  );

  const itemData = useMemo(
    () => ({
      getItemsForRow: (index: number) =>
        getItemsForRow(preparedItems, index, gridDimensions.columns),
      gridDimensions,
      footerHeight,
      itemSpacing,
      selectedAssetIds,
      openDeleteDialog,
      openRenameDialog,
      handleSelectAsset,
      setSelectedAssetIds,
      onDragStart,
      // refetch: refetchAssets,
    }),
    [
      preparedItems,
      gridDimensions,
      footerHeight,
      itemSpacing,
      selectedAssetIds,
      openDeleteDialog,
      openRenameDialog,
      handleSelectAsset,
      setSelectedAssetIds,
      onDragStart,
      // refetchAssets,
    ]
  );

  // useEffect(() => {
  //   if (!propAssets) {
  //     fetchAssets().then(() => {});
  //   }
  // }, [selectedFolderId, fetchAssets, propAssets, assets]);

  useEffect(() => {
    if (containerRef.current) {
      const resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          setContainerSize({
            width: entry.contentRect.width,
            height: entry.contentRect.height,
          });
        }
      });

      resizeObserver.observe(containerRef.current);

      return () => {
        resizeObserver.disconnect();
      };
    }
  }, []);

  useEffect(() => {
    updateGridDimensions(containerSize.width);
  }, [containerSize, updateGridDimensions]);

  useEffect(() => {
    if (listRef.current) {
      listRef.current.resetAfterIndex(0);
    }
  }, [gridDimensions, assetItemSize, preparedItems]);

  return (
    <div
      className="asset-grid-content"
      css={styles}
      ref={containerRef}
      style={{ width: "100%", height: "100%" }}
    >
      <div className="asset-list">
        <AutoSizer>
          {({ height, width }: { height: number; width: number }) => (
            <List
              ref={listRef}
              className="autosizer-list"
              height={height}
              itemCount={rowCount}
              itemSize={getRowHeight}
              width={width}
              itemData={itemData}
            >
              {AssetGridRow}
            </List>
          )}
        </AutoSizer>
      </div>
    </div>
  );
};

export default AssetGridContent;
