"use client";

import { Badge, Button, Spinner, Table } from "react-bootstrap";
import { FileItem } from "@/types";
import { getDownloadUrl } from "@/api/files";
import { Pagination } from "./Pagination";

type Props = {
  items: FileItem[];
  total: number;
  page: number;
  pageSize: number;
  isLoading: boolean;
  onPageChange: (page: number) => void;
};

function formatDate(value: string) {
  return new Intl.DateTimeFormat("ru-RU", { dateStyle: "short", timeStyle: "short" }).format(new Date(value));
}

function formatSize(size: number) {
  if (size < 1024) return `${size} B`;
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
  return `${(size / (1024 * 1024)).toFixed(1)} MB`;
}

function getProcessingVariant(status: string) {
  if (status === "failed") return "danger";
  if (status === "processing") return "warning";
  if (status === "processed") return "success";
  return "secondary";
}

export function FileTable({ items, total, page, pageSize, isLoading, onPageChange }: Props) {
  if (isLoading) {
    return <div className="d-flex justify-content-center py-5"><Spinner animation="border" /></div>;
  }

  return (
    <>
      <div className="table-responsive">
        <Table hover bordered className="align-middle mb-0">
          <thead className="table-light">
            <tr>
              <th>Название</th>
              <th>Файл</th>
              <th>MIME</th>
              <th>Размер</th>
              <th>Статус</th>
              <th>Проверка</th>
              <th>Создан</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan={8} className="text-center py-4 text-secondary">Файлы пока не загружены</td>
              </tr>
            ) : (
              items.map((file) => (
                <tr key={file.id}>
                  <td>
                    <div className="fw-semibold">{file.title}</div>
                    <div className="small text-secondary">{file.id}</div>
                  </td>
                  <td>{file.original_name}</td>
                  <td>{file.mime_type}</td>
                  <td>{formatSize(file.size)}</td>
                  <td>
                    <Badge bg={getProcessingVariant(file.processing_status)}>{file.processing_status}</Badge>
                  </td>
                  <td>
                    <div className="d-flex flex-column gap-1">
                      <Badge bg={file.requires_attention ? "warning" : "success"}>
                        {file.scan_status ?? "pending"}
                      </Badge>
                      <span className="small text-secondary">{file.scan_details ?? "Ожидает обработки"}</span>
                    </div>
                  </td>
                  <td>{formatDate(file.created_at)}</td>
                  <td className="text-nowrap">
                    <Button
                      as="a"
                      href={getDownloadUrl(file.id)}
                      variant="outline-primary"
                      size="sm"
                    >
                      Скачать
                    </Button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </Table>
      </div>
      <Pagination page={page} total={total} pageSize={pageSize} onPageChange={onPageChange} />
    </>
  );
}
