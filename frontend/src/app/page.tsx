"use client";

import { useEffect, useState } from "react";
import { Alert, Badge, Button, Card, Col, Container, Row } from "react-bootstrap";
import { useFiles } from "@/hooks/useFiles";
import { useAlerts } from "@/hooks/useAlerts";
import { FileTable } from "@/components/FileTable";
import { AlertTable } from "@/components/AlertTable";
import { UploadModal } from "@/components/UploadModal";

const PAGE_SIZE = 20;

export default function Page() {
  const [showModal, setShowModal] = useState(false);
  const files = useFiles(PAGE_SIZE);
  const alerts = useAlerts(PAGE_SIZE);

  useEffect(() => {
    void files.load(1);
    void alerts.load(1);
  }, []);

  function handleRefresh() {
    void files.load(files.page);
    void alerts.load(alerts.page);
  }

  function handleUploadSuccess() {
    void files.load(1);
  }

  const errorMessage = files.error ?? alerts.error;

  return (
    <Container fluid className="py-4 px-4 bg-light min-vh-100">
      <Row className="justify-content-center">
        <Col xxl={10} xl={11}>
          <Card className="shadow-sm border-0 mb-4">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start gap-3 flex-wrap">
                <div>
                  <h1 className="h3 mb-2">Управление файлами</h1>
                  <p className="text-secondary mb-0">
                    Загрузка файлов, просмотр статусов обработки и ленты алертов.
                  </p>
                </div>
                <div className="d-flex gap-2">
                  <Button variant="outline-secondary" onClick={handleRefresh}>Обновить</Button>
                  <Button variant="primary" onClick={() => setShowModal(true)}>Добавить файл</Button>
                </div>
              </div>
            </Card.Body>
          </Card>

          {errorMessage && <Alert variant="danger" className="shadow-sm">{errorMessage}</Alert>}

          <Card className="shadow-sm border-0 mb-4">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <div className="d-flex justify-content-between align-items-center">
                <h2 className="h5 mb-0">Файлы</h2>
                <Badge bg="secondary">{files.data?.total ?? 0}</Badge>
              </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              <FileTable
                items={files.data?.items ?? []}
                total={files.data?.total ?? 0}
                page={files.page}
                pageSize={PAGE_SIZE}
                isLoading={files.isLoading}
                onPageChange={files.setPage}
              />
            </Card.Body>
          </Card>

          <Card className="shadow-sm border-0">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <div className="d-flex justify-content-between align-items-center">
                <h2 className="h5 mb-0">Алерты</h2>
                <Badge bg="secondary">{alerts.data?.total ?? 0}</Badge>
              </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              <AlertTable
                items={alerts.data?.items ?? []}
                total={alerts.data?.total ?? 0}
                page={alerts.page}
                pageSize={PAGE_SIZE}
                isLoading={alerts.isLoading}
                onPageChange={alerts.setPage}
              />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <UploadModal
        show={showModal}
        onHide={() => setShowModal(false)}
        onSuccess={handleUploadSuccess}
      />
    </Container>
  );
}
