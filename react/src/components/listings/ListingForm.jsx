import React from 'react';
import { Typography } from 'antd';

export const ListingForm = ({ mode = 'create' }) => {
  const title = mode === 'edit' ? 'Редактирование объявления' : 'Новое объявление';
  return (
    <div data-easytag="id5-src/components/listings/ListingForm.jsx">
      <Typography.Title level={3}>{title}</Typography.Title>
      <p>Здесь будет форма объявления.</p>
    </div>
  );
};
