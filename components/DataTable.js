"use client";

import { Table } from "@heroui/react";
import { useEffect, useMemo, useRef, useState } from "react";

export function DataTable({ data, label = "Tabla" }) {
  const { cols, rows } = data;
  const wrapRef = useRef(null);

  const [sortDescriptor, setSortDescriptor] = useState({
    column: "__none__",
    direction: "ascending",
  });

  useEffect(() => {
    const el = wrapRef.current?.querySelector(".table__scroll-container");
    if (el) el.scrollLeft = 0;
  }, []);

  const sortedRows = useMemo(() => {
    const col = cols.indexOf(sortDescriptor.column);
    if (col === -1) return rows;
    return [...rows].sort((a, b) => {
      const first = String(a[col] ?? "");
      const second = String(b[col] ?? "");
      let cmp = first.localeCompare(second, "es", { numeric: true });
      if (sortDescriptor.direction === "descending") cmp *= -1;
      return cmp;
    });
  }, [cols, rows, sortDescriptor]);

  return (
    <div ref={wrapRef}>
      <Table>
        <Table.ScrollContainer>
          <Table.Content
            aria-label={label}
            className="min-w-[640px]"
            sortDescriptor={sortDescriptor}
            onSortChange={setSortDescriptor}
          >
            <Table.Header>
              {cols.map((c, i) => (
                <Table.Column key={c} allowsSorting isRowHeader={i === 0} id={c}>
                  {({ sortDirection }) => (
                    <Table.SortableColumnHeader sortDirection={sortDirection}>
                      {c}
                    </Table.SortableColumnHeader>
                  )}
                </Table.Column>
              ))}
            </Table.Header>
            <Table.Body>
              {sortedRows.map((row, idx) => (
                <Table.Row key={idx} id={idx}>
                  {cols.map((c, i) => (
                    <Table.Cell key={c}>{row[i]}</Table.Cell>
                  ))}
                </Table.Row>
              ))}
            </Table.Body>
          </Table.Content>
        </Table.ScrollContainer>
      </Table>
    </div>
  );
}
