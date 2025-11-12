import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Card, Descriptions, Button, Space, Tag, message } from 'antd';
import { apiGetListing, apiDeleteListing } from '../../api/listings';
import { apiStartChat } from '../../api/chats';

const categoryLabel = (v) => ({ automobiles: 'Автомобили', phones: 'Телефоны', realty: 'Недвижимость' }[v] || v);

export const ListingDetail = () => {
  const { id } = useParams();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const load = async () => {
    setLoading(true);
    try {
      const data = await apiGetListing(id);
      setItem(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [id]);

  const meId = null; // could be fetched on Profile if needed

  const onChat = async () => {
    try {
      const recipient_id = item?.author?.id;
      if (!recipient_id) return;
      const thread = await apiStartChat({ recipient_id, listing_id: Number(id) });
      navigate('/chats');
    } catch (e) {
      message.error('Не удалось начать чат. Требуется авторизация.');
    }
  };

  const onDelete = async () => {
    try {
      await apiDeleteListing(id);
      navigate('/');
    } catch (e) {
      message.error('Не удалось удалить объявление');
    }
  };

  return (
    <Card title="Объявление" loading={loading} data-easytag="id6-src/components/listings/ListingDetail.jsx">
      {item && (
        <>
          <Descriptions bordered column={1}>
            <Descriptions.Item label="Заголовок">{item.title}</Descriptions.Item>
            <Descriptions.Item label="Категория"><Tag>{categoryLabel(item.category)}</Tag></Descriptions.Item>
            <Descriptions.Item label="Описание">{item.description}</Descriptions.Item>
            <Descriptions.Item label="Цена">{item.price} ₽</Descriptions.Item>
            <Descriptions.Item label="Телефон для связи">{item.phone}</Descriptions.Item>
            <Descriptions.Item label="Автор">
              {item.author?.name} • {item.author?.phone}
            </Descriptions.Item>
          </Descriptions>
          <Space style={{ marginTop: 16 }}>
            <Button type="primary" onClick={onChat}>Написать</Button>
            <Button onClick={() => navigate(`/listings/${id}/edit`)}>Редактировать</Button>
            <Button danger onClick={onDelete}>Удалить</Button>
            <Link to="/">Назад</Link>
          </Space>
        </>
      )}
    </Card>
  );
};
