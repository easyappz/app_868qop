import React, { useEffect, useMemo, useState } from 'react';
import { Card, Form, Input, Select, Button, Row, Col, List, Tag, Empty, DatePicker, InputNumber } from 'antd';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { apiListListings } from '../../api/listings';
import dayjs from 'dayjs';

const { RangePicker } = DatePicker;

const categories = [
  { value: 'automobiles', label: 'Автомобили' },
  { value: 'phones', label: 'Телефоны' },
  { value: 'realty', label: 'Недвижимость' },
];

export const Home = () => {
  const [form] = Form.useForm();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const load = async (params = {}) => {
    setLoading(true);
    try {
      const data = await apiListListings(params);
      setItems(data);
    } finally {
      setLoading(false);
    }
  };

  const currentParams = useMemo(() => Object.fromEntries([...searchParams]), [searchParams]);

  useEffect(() => {
    form.setFieldsValue({
      category: currentParams.category,
      search: currentParams.search,
      price_min: currentParams.price_min ? Number(currentParams.price_min) : undefined,
      price_max: currentParams.price_max ? Number(currentParams.price_max) : undefined,
      dates: currentParams.date_from && currentParams.date_to ? [dayjs(currentParams.date_from), dayjs(currentParams.date_to)] : undefined,
    });
    load(currentParams);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentParams]);

  const onSearch = (values) => {
    const params = { ...values };
    if (values.dates && values.dates.length === 2) {
      params.date_from = values.dates[0].format('YYYY-MM-DD');
      params.date_to = values.dates[1].format('YYYY-MM-DD');
    }
    delete params.dates;
    Object.keys(params).forEach((k) => (params[k] === undefined || params[k] === '' ? delete params[k] : null));
    setSearchParams(params);
  };

  const reset = () => {
    form.resetFields();
    setSearchParams({});
  };

  return (
    <div data-easytag="id5-src/components/Home/index.jsx">
      <Card style={{ marginBottom: 16 }}>
        <Form layout="vertical" form={form} onFinish={onSearch}>
          <Row gutter={12}>
            <Col xs={24} md={6}>
              <Form.Item label="Категория" name="category">
                <Select allowClear options={categories} placeholder="Выберите" />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item label="Цена от" name="price_min">
                <InputNumber min={0} style={{ width: '100%' }} placeholder="0" />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item label="Цена до" name="price_max">
                <InputNumber min={0} style={{ width: '100%' }} placeholder="100000" />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item label="По дате" name="dates">
                <RangePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={12}>
            <Col xs={24} md={18}>
              <Form.Item label="Поиск по тексту" name="search">
                <Input placeholder="Введите текст" />
              </Form.Item>
            </Col>
            <Col xs={24} md={6} style={{ display: 'flex', alignItems: 'flex-end' }}>
              <div style={{ width: '100%', display: 'flex', gap: 8 }}>
                <Button type="primary" htmlType="submit" block>Найти</Button>
                <Button onClick={reset} block>Сбросить</Button>
              </div>
            </Col>
          </Row>
        </Form>
      </Card>

      <Card title="Объявления" loading={loading}>
        {items.length === 0 ? (
          <Empty description="Объявлений не найдено" />
        ) : (
          <List
            itemLayout="vertical"
            dataSource={items}
            renderItem={(item) => (
              <List.Item key={item.id}
                extra={<div style={{ width: 160, height: 120, background: '#f0f0f0' }} />}
                actions={[<Tag key="cat">{categories.find(c => c.value === item.category)?.label}</Tag>]}
              >
                <List.Item.Meta
                  title={<Link to={`/listings/${item.id}`}>{item.title}</Link>}
                  description={`Цена: ${item.price} ₽ • Автор: ${item.author?.name || ''}`}
                />
                <div style={{ color: '#555' }}>{item.description?.slice(0, 160)}{item.description?.length > 160 ? '…' : ''}</div>
              </List.Item>
            )}
          />
        )}
      </Card>
    </div>
  );
};
