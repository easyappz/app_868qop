import React, { useState } from 'react';
import { Form, Input, Button, Alert, Card } from 'antd';
import { useNavigate, Link } from 'react-router-dom';
import { apiRegister } from '../../api/auth';

export const Register = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true); setError(null);
    try {
      await apiRegister(values);
      navigate('/login');
    } catch (e) {
      setError(e?.response?.data?.detail || 'Ошибка регистрации');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Регистрация" style={{ maxWidth: 480, margin: '0 auto' }} data-easytag="id3-src/components/auth/Register.jsx">
      {error && <Alert type="error" message={error} style={{ marginBottom: 16 }} />}
      <Form layout="vertical" onFinish={onFinish}>
        <Form.Item label="Имя" name="name" rules={[{ required: true, message: 'Введите имя' }]}>
          <Input placeholder="Ваше имя" />
        </Form.Item>
        <Form.Item label="Телефон" name="phone" rules={[{ required: true, message: 'Введите телефон' }]}>
          <Input placeholder="Например: +7 900 000 00 00" />
        </Form.Item>
        <Form.Item label="Пароль" name="password" rules={[{ required: true, message: 'Введите пароль' }, { min: 6, message: 'Минимум 6 символов' }]}>
          <Input.Password placeholder="Придумайте пароль" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} block>Зарегистрироваться</Button>
        </Form.Item>
        <div>Уже есть аккаунт? <Link to="/login">Войти</Link></div>
      </Form>
    </Card>
  );
};
