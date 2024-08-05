import { Asset } from "../../stores/ApiTypes";

export type AssetOrDivider =
  | { isDivider: true; type: string }
  | (Asset & { isDivider: false; type: string });

export const getFooterHeight = (size: number): number => {
  switch (size) {
    case 1:
      return 5;
    case 2:
      return 40;
    case 3:
      return 40;
    case 4:
    case 5:
      return 30;
    default:
      return 10;
  }
};
export const DIVIDER_HEIGHT = 30;

export const calculateGridDimensions = (
  width: number,
  assetItemSize: number,
  itemSpacing: number
) => {
  const baseSize = 42; // Base size factor
  const minItemSize = baseSize * assetItemSize;
  const maxItemSize = minItemSize * 1.1;
  const maxColumns = 12;

  // Calculate the number of columns based on the available width and minimum item size
  let columns = Math.min(
    maxColumns,
    Math.max(1, Math.floor((width + itemSpacing) / (minItemSize + itemSpacing)))
  );

  // Adjust item size to fill the available space, but cap it at maxItemSize
  let itemWidth = Math.min(
    Math.floor((width - itemSpacing * (columns + 1)) / columns),
    maxItemSize
  );

  // If items are at max size and there's still room, add more columns up to maxColumns
  while (
    itemWidth === maxItemSize &&
    columns < maxColumns &&
    columns < Math.floor((width + itemSpacing) / (maxItemSize + itemSpacing))
  ) {
    columns++;
    itemWidth = Math.min(
      Math.floor((width - itemSpacing * (columns + 1)) / columns),
      maxItemSize
    );
  }

  const itemHeight = itemWidth; // 1:1 aspect ratio

  return { columns, itemWidth, itemHeight };
};

export const prepareItems = (
  filteredAssets: Record<string, Asset[]>
): AssetOrDivider[] => {
  const items: AssetOrDivider[] = [];
  Object.entries(filteredAssets).forEach(([type, assets]) => {
    if (assets.length > 0) {
      items.push({ type, isDivider: true });
      items.push(
        ...assets.map((asset) => ({ ...asset, isDivider: false, type }))
      );
    }
  });
  return items;
};

export const calculateRowCount = (
  preparedItems: AssetOrDivider[],
  columns: number
): number => {
  let count = 0;
  let currentRowItemCount = 0;
  preparedItems.forEach((item) => {
    if (item.isDivider) {
      if (currentRowItemCount > 0) {
        count++;
      }
      count++;
      currentRowItemCount = 0;
    } else {
      currentRowItemCount++;
      if (currentRowItemCount === columns) {
        count++;
        currentRowItemCount = 0;
      }
    }
  });
  if (currentRowItemCount > 0) {
    count++;
  }
  return count;
};

export const getItemsForRow = (
  preparedItems: AssetOrDivider[],
  rowIndex: number,
  columns: number
): AssetOrDivider[] => {
  let currentRow = 0;
  let itemsInCurrentRow = 0;
  let startIndex = 0;

  for (let i = 0; i < preparedItems.length; i++) {
    const item = preparedItems[i];
    if (item.isDivider) {
      if (itemsInCurrentRow > 0) {
        currentRow++;
        itemsInCurrentRow = 0;
      }
      if (currentRow === rowIndex) {
        return [item];
      }
      currentRow++;
      startIndex = i + 1;
    } else {
      itemsInCurrentRow++;
      if (itemsInCurrentRow === columns || i === preparedItems.length - 1) {
        if (currentRow === rowIndex) {
          return preparedItems.slice(startIndex, i + 1);
        }
        currentRow++;
        itemsInCurrentRow = 0;
        startIndex = i + 1;
      }
    }
  }
  return [];
};
