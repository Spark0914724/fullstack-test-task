"use client";

import { Pagination as BSPagination } from "react-bootstrap";

type Props = {
  page: number;
  total: number;
  pageSize: number;
  onPageChange: (page: number) => void;
};

export function Pagination({ page, total, pageSize, onPageChange }: Props) {
  const totalPages = Math.ceil(total / pageSize);
  if (totalPages <= 1) return null;

  return (
    <BSPagination className="mt-3 mb-0 justify-content-center">
      <BSPagination.Prev disabled={page === 1} onClick={() => onPageChange(page - 1)} />
      {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
        <BSPagination.Item key={p} active={p === page} onClick={() => onPageChange(p)}>
          {p}
        </BSPagination.Item>
      ))}
      <BSPagination.Next disabled={page === totalPages} onClick={() => onPageChange(page + 1)} />
    </BSPagination>
  );
}
