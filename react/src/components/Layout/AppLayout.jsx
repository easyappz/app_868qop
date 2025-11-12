import React from 'react';
import { Layout, Menu } from 'antd';
import { Link, useLocation, useNavigate } from 'react-router-dom';

const { Header, Content, Footer } = Layout;

export const AppLayout = ({ children }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

  const onLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <Layout style={{ minHeight: '100vh' }} data-easytag="id1-src/components/Layout/AppLayout.jsx">
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{ color: '#fff', fontWeight: 600, marginRight: 24 }}>Доска объявлений</div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={[
            { key: '/', label: <Link to="/">Главная</Link> },
            { key: '/listings/new', label: <Link to="/listings/new">Новое объявление</Link> },
            { key: '/chats', label: <Link to="/chats">Чаты</Link> },
            token
              ? { key: '/profile', label: <Link to="/profile">Профиль</Link> }
              : { key: '/login', label: <Link to="/login">Войти</Link> },
          ]}
        />
        {token && (
          <div style={{ marginLeft: 'auto', color: '#fff', cursor: 'pointer' }} onClick={onLogout}>
            Выйти
          </div>
        )}
      </Header>
      <Content style={{ padding: '24px', maxWidth: 1200, margin: '0 auto', width: '100%' }}>
        {children}
      </Content>
      <Footer style={{ textAlign: 'center' }}>Easyappz ©2025</Footer>
    </Layout>
  );
};
