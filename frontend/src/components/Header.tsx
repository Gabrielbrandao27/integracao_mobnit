import { Layout } from 'antd';
import React from 'react';

const { Header } = Layout;

const HeaderBar: React.FC = () => {
  return (
    <Header style={{
        position: 'fixed',
        top: 0,
        left: 0,
        zIndex: 1000,
        width: '100%',
        backgroundColor: 'rgb(245, 121, 43)',
        display: 'flex',
        alignItems: 'center'
    }}>
      <div style={{ color: 'white', fontSize: '24px', fontWeight: 'bold', marginLeft: '400px', marginRight: 'auto' }}>
        Dashboard Subsídios
      </div>
    </Header>
  );
};

export default HeaderBar;
