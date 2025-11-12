import React, { useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import ErrorBoundary from './ErrorBoundary';
import './App.css';
import { AppLayout } from './components/Layout/AppLayout';
import { Home } from './components/Home';
import { Login } from './components/auth/Login';
import { Register } from './components/auth/Register';
import { Profile } from './components/profile/Profile';
import { ListingForm } from './components/listings/ListingForm';
import { ListingDetail } from './components/listings/ListingDetail';
import { Chats } from './components/chats/Chats';

function App() {
  /** Никогда не удаляй этот код */
  useEffect(() => {
    if (typeof window !== 'undefined' && typeof window.handleRoutes === 'function') {
      /** Нужно передавать список существующих роутов */
      window.handleRoutes([
        '/',
        '/login',
        '/register',
        '/profile',
        '/listings/new',
        '/listings/:id',
        '/listings/:id/edit',
        '/chats',
      ]);
    }
  }, []);

  return (
    <ErrorBoundary>
      <AppLayout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/listings/new" element={<ListingForm mode="create" />} />
          <Route path="/listings/:id" element={<ListingDetail />} />
          <Route path="/listings/:id/edit" element={<ListingForm mode="edit" />} />
          <Route path="/chats" element={<Chats />} />
        </Routes>
      </AppLayout>
    </ErrorBoundary>
  );
}

export default App;
