import React, { useState } from 'react';
import { Form, Input, Button, Alert, Card } from 'antd';
import { useNavigate, Link } from 'react-router-dom';
import { apiLogin } from '../../api/auth';

export const Login = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true); setError(null);
    try {
      const res = await apiLogin(values);
      localStorage.setItem('token', res.token);
      navigate('/profile');
    } catch (e) {
      setError(e?.response?.data?.detail || 'Ошибка авторизации');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Вход" style={{ maxWidth: 420, margin: '0 auto' }} data-easytag="id2-src/components/auth/Login.jsx">
      {error && <Alert type="error" message={error} style={{ marginBottom: 16 }} />}
      <Form layout="vertical" onFinish={onFinish}>
        <Form.Item label="Телефон" name="phone" rules={[{ required: true, message: 'Введите телефон' }]}>
          <Input placeholder="Например: +7 900 000 00 00" />
        </Form.Item>
        <Form.Item label="Пароль" name="password" rules={[{ required: true, message: 'Введите пароль' }]}>
          <Input.Password placeholder="Ваш пароль" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} block>Войти</Button>
        </Form.Item>
        <div>Нет аккаунта? <Link to="/register">Зарегистрироваться</Link></div>
      </Form>
    </Card>
  );
};
