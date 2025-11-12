import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Form, Input, InputNumber, Select, Button, Alert, Space } from 'antd';
import { apiCreateListing, apiGetListing, apiUpdateListing } from '../../api/listings';

const categories = [
  { value: 'automobiles', label: 'Автомобили' },
  { value: 'phones', label: 'Телефоны' },
  { value: 'realty', label: 'Недвижимость' },
];

export const ListingForm = ({ mode = 'create' }) => {
  const [form] = Form.useForm();
  const { id } = useParams();
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const load = async () => {
      if (mode === 'edit' && id) {
        const data = await apiGetListing(id);
        form.setFieldsValue({
          title: data.title,
          description: data.description,
          price: Number(data.price),
          phone: data.phone,
          category: data.category,
        });
      }
    };
    load();
  }, [id, mode]);

  const onFinish = async (values) => {
    setError(null); setLoading(true);
    try {
      if (mode === 'create') {
        const created = await apiCreateListing(values);
        navigate(`/listings/${created.id}`);
      } else {
        await apiUpdateListing(id, values);
        navigate(`/listings/${id}`);
      }
    } catch (e) {
      setError('Не удалось сохранить объявление. Проверьте данные и авторизацию.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title={mode === 'create' ? 'Новое объявление' : 'Редактирование объявления'} data-easytag="id7-src/components/listings/ListingForm.jsx">
      {error && <Alert type="error" message={error} style={{ marginBottom: 16 }} />}
      <Form layout="vertical" form={form} onFinish={onFinish}>
        <Form.Item label="Заголовок" name="title" rules={[{ required: true, message: 'Введите заголовок' }]}>
          <Input />
        </Form.Item>
        <Form.Item label="Описание" name="description" rules={[{ required: true, message: 'Введите описание' }]}>
          <Input.TextArea rows={6} />
        </Form.Item>
        <Form.Item label="Цена" name="price" rules={[{ required: true, message: 'Введите цену' }]}>
          <InputNumber min={0} style={{ width: '100%' }} />
        </Form.Item>
        <Form.Item label="Категория" name="category" rules={[{ required: true, message: 'Выберите категорию' }]}>
          <Select options={categories} />
        </Form.Item>
        <Form.Item label="Телефон" name="phone" rules={[{ required: true, message: 'Введите телефон' }]}>
          <Input />
        </Form.Item>
        {/* Изображения пока опускаем, места под них оставим пустыми */}
        <Space>
          <Button type="primary" htmlType="submit" loading={loading}>Сохранить</Button>
          <Button onClick={() => navigate(-1)}>Отмена</Button>
        </Space>
      </Form>
    </Card>
  );
};
