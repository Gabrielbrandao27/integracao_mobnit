import { LineChartOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Menu } from 'antd';
import React from 'react';

type MenuItem = Required<MenuProps>['items'][number];

interface SidebarProps {
  setSelectedChart: (chart: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ setSelectedChart }) => {
  const items: MenuItem[] = [
    {
      key: '1',
      icon: <LineChartOutlined style={{color: 'orange'}}/>,
      label: (
        <span style={{
          color: 'orange',
          fontFamily: 'Arial, sans-serif',
          fontSize: '20px',
          fontWeight: 'bold'
        }}>Viagens Completas</span>
      ),
      onClick: () => setSelectedChart('TripsCompletedChartData'),
    },
    {
      key: '2',
      icon: <LineChartOutlined style={{color: 'orange'}}/>,
      label: (
        <span style={{
          color: 'orange',
          fontFamily: 'Arial, sans-serif',
          fontSize: '20px',
          fontWeight: 'bold'
        }}>Distância Percorrida</span>
      ),
      onClick: () => setSelectedChart('TraveledKmChartData'),
    },
    {
      key: '3',
      icon: <LineChartOutlined style={{color: 'orange'}}/>,
      label: (
        <span style={{
          color: 'orange',
          fontFamily: 'Arial, sans-serif',
          fontSize: '20px',
          fontWeight: 'bold'
        }}>Climatização</span>
      ),
      onClick: () => setSelectedChart('ClimatizationChartData'),
    },
    {
      key: '4',
      icon: <LineChartOutlined style={{color: 'orange'}}/>,
      label: (
        <span style={{
          color: 'orange',
          fontFamily: 'Arial, sans-serif',
          fontSize: '20px',
          fontWeight: 'bold'
        }}>Frotas Disponíveis</span>
      ),
      onClick: () => setSelectedChart('AvaiableFleetchartData'),
    },
  ];

  return <Menu mode="inline" className="sidebar" items={items} />;
};

export default Sidebar;