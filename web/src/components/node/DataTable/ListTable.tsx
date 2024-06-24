/** @jsxImportSource @emotion/react */
import { css } from "@emotion/react";
import { useState, useMemo, useRef, useCallback, useEffect } from "react";
import {
  TabulatorFull as Tabulator,
  CellComponent,
  Formatter,
  ColumnDefinitionAlign,
  StandardValidatorType
} from "tabulator-tables";
import "tabulator-tables/dist/css/tabulator.min.css";
import "tabulator-tables/dist/css/tabulator_midnight.css";
import { useClipboard } from "../../../hooks/browser/useClipboard";
import { useNotificationStore } from "../../../stores/NotificationStore";
import {
  Button,
  ToggleButton,
  ToggleButtonGroup,
  Tooltip
} from "@mui/material";
import { integerEditor, floatEditor, datetimeEditor } from "./DataTableEditors";
import { styles } from "./TableStyles";

export type ListDataType = "int" | "string" | "datetime" | "float";
export type ListTableProps = {
  data: any[];
  editable: boolean;
  onDataChange?: (newData: any[]) => void;
  data_type: ListDataType;
};

const defaultValueForType = (type: ListDataType) => {
  switch (type) {
    case "int":
      return 0;
    case "float":
      return 0.0;
    case "datetime":
      return new Date();
    default:
      return "";
  }
};

const coerceValue = (value: any, type: ListDataType) => {
  switch (type) {
    case "int":
      return parseInt(value);
    case "float":
      return parseFloat(value);
    case "datetime":
      return new Date(value);
    default:
      return value;
  }
};

const ListTable: React.FC<ListTableProps> = ({
  data,
  editable,
  data_type,
  onDataChange
}) => {
  const tableRef = useRef<HTMLDivElement>(null);
  const { writeClipboard } = useClipboard();
  const addNotification = useNotificationStore(
    (state) => state.addNotification
  );
  const [selectedRows, setSelectedRows] = useState<any[]>([]);
  const [showSelect, setShowSelect] = useState(true);

  const columns = useMemo(
    () => [
      ...(showSelect
        ? [
          {
            title: "",
            field: "select",
            formatter: "rowSelection" as Formatter,
            titleFormatter: "rowSelection" as Formatter,
            hozAlign: "left" as ColumnDefinitionAlign,
            headerSort: false,
            width: 25,
            minWidth: 25,
            resizable: false,
            frozen: true,
            cellClick: function (e: any, cell: CellComponent) {
              cell.getRow().toggleSelect();
            },
            editable: false,
            cssClass: "row-select"
          }
        ]
        : []),
      {
        title: "Index",
        field: "rownum",
        formatter: "rownum" as Formatter,
        hozAlign: "left" as ColumnDefinitionAlign,
        headerSort: false,
        resizable: true,
        frozen: true,
        rowHandle: true,
        editable: false,
        cssClass: "row-numbers"
      },
      {
        title: "Value",
        field: "value",
        editable: editable,
        frozen: !editable,
        editor:
          data_type === "int"
            ? integerEditor
            : data_type === "float"
              ? floatEditor
              : data_type === "datetime"
                ? datetimeEditor
                : "input",
        headerHozAlign: "left" as ColumnDefinitionAlign,
        cssClass: data_type,
        validator:
          data_type === "int"
            ? (["required", "integer"] as StandardValidatorType[])
            : data_type === "float"
              ? (["required", "numeric"] as StandardValidatorType[])
              : data_type === "datetime"
                ? (["required", "date"] as StandardValidatorType[])
                : undefined
      }
    ],
    [data_type, editable, showSelect]
  );

  const onCellEdited = useCallback(
    (cell: CellComponent) => {
      const { rownum, value } = cell.getData();
      const newData = data.map((row, index) => {
        if (index === rownum) {
          return value;
        } else {
          return row;
        }
      });
      if (onDataChange) {
        onDataChange(newData);
      }
    },
    [data, onDataChange]
  );

  const addRow = useCallback(() => {
    if (!onDataChange) return;
    onDataChange([...data, defaultValueForType(data_type)]);
  }, [data, data_type, onDataChange]);

  const removeSelectedRows = useCallback(() => {
    if (!onDataChange) return;
    const newData = data.filter((_, index) => {
      return !selectedRows.some((row) => row.getData().rownum === index);
    });
    onDataChange(newData);
  }, [data, onDataChange, selectedRows]);

  useEffect(() => {
    if (!tableRef.current) return;

    const tabulatorInstance = new Tabulator(tableRef.current, {
      height: "300px",
      data: data.map((value, index) => ({
        rownum: index,
        value: coerceValue(value, data_type)
      })),
      columns: columns,
      columnDefaults: {
        headerSort: true,
        hozAlign: "left",
        headerHozAlign: "left",
        editor: "input",
        resizable: true,
        editorParams: {
          elementAttributes: { spellcheck: "false" }
        }
      },
      movableRows: true
    });

    tabulatorInstance.on("cellEdited", onCellEdited);
    tabulatorInstance.on("rowSelectionChanged", (data, rows) => {
      setSelectedRows(rows);
    });

    return () => {
      tabulatorInstance.destroy();
    };
  }, [data, columns, onCellEdited, data_type]);

  const copyData = useCallback(() => {
    const dataToCopy = data.map((row) => row.value);
    writeClipboard(JSON.stringify(dataToCopy), true);
    addNotification({
      content: "Copied to clipboard",
      type: "success",
      alert: true
    });
  }, [data, writeClipboard, addNotification]);

  return (
    <div className="listtable nowheel nodrag" css={styles}>
      <div className="table-actions">
        <Tooltip title="Copy table data to clipboard">
          <Button variant="outlined" onClick={copyData}>
            Copy Data
          </Button>
        </Tooltip>
        <Tooltip title="Show Select column">
          <ToggleButtonGroup
            className="toggle select-row"
            value={showSelect ? "selected" : null}
            exclusive
            onChange={() => setShowSelect(!showSelect)}
          >
            <ToggleButton value="selected">Show Select</ToggleButton>
          </ToggleButtonGroup>
        </Tooltip>

        {editable && (
          <>
            <Tooltip title="Add a new row">
              <Button variant="outlined" onClick={addRow}>
                Add Row
              </Button>
            </Tooltip>
            <Tooltip title="Remove selected rows">
              <>
                <Button
                  variant="outlined"
                  onClick={removeSelectedRows}
                  disabled={selectedRows.length === 0}
                >
                  Remove Selected
                </Button>
              </>
            </Tooltip>
          </>
        )}
      </div>
      <div ref={tableRef} className="listtable" />
    </div>
  );
};

export default ListTable;
