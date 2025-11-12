import React, { useEffect, useState } from 'react';
import { Card, List, Input, Button, Row, Col, Empty } from 'antd';
import { apiListChats, apiListMessages, apiSendMessage } from '../../api/chats';

export const Chats = () => {
  const [threads, setThreads] = useState([]);
  const [current, setCurrent] = useState(null);
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState('');

  const loadThreads = async () => {
    try {
      const data = await apiListChats();
      setThreads(data);
      if (data.length && !current) setCurrent(data[0]);
    } catch (_) {}
  };

  const loadMessages = async (thread) => {
    if (!thread) return;
    try {
      const data = await apiListMessages(thread.id);
      setMessages(data);
    } catch (_) {}
  };

  useEffect(() => { loadThreads(); }, []);
  useEffect(() => { loadMessages(current); }, [current]);

  const send = async () => {
    if (!text.trim() || !current) return;
    await apiSendMessage(current.id, text.trim());
    setText('');
    await loadMessages(current);
  };

  return (
    <Row gutter={12} data-easytag="id8-src/components/chats/Chats.jsx">
      <Col xs={24} md={8}>
        <Card title="Диалоги">
          <List
            dataSource={threads}
            renderItem={(t) => (
              <List.Item onClick={() => setCurrent(t)} style={{ cursor: 'pointer', background: current?.id === t.id ? '#f5f5f5' : 'transparent' }}>
                <List.Item.Meta
                  title={`Чат #${t.id}${t.listing ? ' • Объявление ' + t.listing : ''}`}
                  description={`${t.member_a?.name} ↔ ${t.member_b?.name}`}
                />
              </List.Item>
            )}
          />
        </Card>
      </Col>
      <Col xs={24} md={16}>
        <Card title={current ? `Сообщения чата #${current.id}` : 'Выберите диалог'}>
          {!current ? (
            <Empty description="Нет выбранного диалога" />
          ) : (
            <>
              <div style={{ height: 360, overflowY: 'auto', border: '1px solid #eee', padding: 12, marginBottom: 12 }}>
                {messages.map((m) => (
                  <div key={m.id} style={{ marginBottom: 8 }}>
                    <b>{m.sender?.name}:</b> {m.content}
                    <div style={{ fontSize: 12, color: '#888' }}>{new Date(m.created_at).toLocaleString()}</div>
                  </div>
                ))}
              </div>
              <div style={{ display: 'flex', gap: 8 }}>
                <Input value={text} onChange={(e) => setText(e.target.value)} placeholder="Введите сообщение" onPressEnter={send} />
                <Button type="primary" onClick={send}>Отправить</Button>
              </div>
            </>
          )}
        </Card>
      </Col>
    </Row>
  );
};
