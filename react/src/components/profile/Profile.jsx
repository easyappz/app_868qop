import React, { useEffect, useState } from 'react';
import { Card, Descriptions, Button, Modal, Form, Input, Alert } from 'antd';
import { apiGetMe, apiUpdateMe } from '../../api/profile';

export const Profile = () => {
  const [me, setMe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);

  const load = async () => {
    setLoading(true); setError(null);
    try {
      const data = await apiGetMe();
      setMe(data);
    } catch (e) {
      setError('Не удалось загрузить профиль. Авторизуйтесь.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const onFinish = async (values) => {
    try {
      const data = await apiUpdateMe(values);
      setMe(data);
      setOpen(false);
    } catch (e) {
      setError('Не удалось сохранить профиль');
    }
  };

  return (
    <Card title="Профиль" loading={loading} data-easytag="id4-src/components/profile/Profile.jsx">
      {error && <Alert type="error" message={error} style={{ marginBottom: 16 }} />}
      {me && (
        <>
          <Descriptions bordered column={1} size="middle">
            <Descriptions.Item label="Имя">{me.name}</Descriptions.Item>
            <Descriptions.Item label="Телефон">{me.phone}</Descriptions.Item>
            <Descriptions.Item label="О себе">{me.about || '—'}</Descriptions.Item>
            <Descriptions.Item label="Дата регистрации">{new Date(me.date_joined).toLocaleString()}</Descriptions.Item>
          </Descriptions>
          <div style={{ marginTop: 16 }}>
            <Button type="primary" onClick={() => setOpen(true)}>Редактировать</Button>
          </div>
          <Modal title="Редактирование профиля" open={open} onCancel={() => setOpen(false)} footer={null}>
            <Form layout="vertical" onFinish={onFinish} initialValues={{ name: me.name, phone: me.phone, about: me.about }}>
              <Form.Item label="Имя" name="name" rules={[{ required: true, message: 'Введите имя' }]}>
                <Input />
              </Form.Item>
              <Form.Item label="Телефон" name="phone" rules={[{ required: true, message: 'Введите телефон' }]}>
                <Input />
              </Form.Item>
              <Form.Item label="О себе" name="about">
                <Input.TextArea rows={4} />
              </Form.Item>
              <Form.Item>
                <Button type="primary" htmlType="submit">Сохранить</Button>
              </Form.Item>
            </Form>
          </Modal>
        </>
      )}
    </Card>
  );
};
