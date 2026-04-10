"use client";

import { FormEvent, useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { useUpload } from "@/hooks/useUpload";

type Props = {
  show: boolean;
  onHide: () => void;
  onSuccess: () => void;
};

export function UploadModal({ show, onHide, onSuccess }: Props) {
  const [title, setTitle] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { isSubmitting, error, submit } = useUpload(() => {
    onSuccess();
    onHide();
    setTitle("");
    setSelectedFile(null);
  });

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!title.trim() || !selectedFile) return;
    await submit(title.trim(), selectedFile);
  }

  return (
    <Modal show={show} onHide={onHide} centered>
      <Form onSubmit={handleSubmit}>
        <Modal.Header closeButton>
          <Modal.Title>Добавить файл</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {error && <div className="alert alert-danger">{error}</div>}
          <Form.Group className="mb-3">
            <Form.Label>Название</Form.Label>
            <Form.Control
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Например, Договор с подрядчиком"
            />
          </Form.Group>
          <Form.Group>
            <Form.Label>Файл</Form.Label>
            <Form.Control
              type="file"
              onChange={(e) => setSelectedFile((e.target as HTMLInputElement).files?.[0] ?? null)}
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="outline-secondary" onClick={onHide}>Отмена</Button>
          <Button type="submit" variant="primary" disabled={isSubmitting}>
            {isSubmitting ? "Загрузка..." : "Сохранить"}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
}
