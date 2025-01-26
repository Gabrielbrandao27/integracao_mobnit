import { BarChartOutlined } from '@ant-design/icons';
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
      icon: <BarChartOutlined style={{color: 'rgb(245, 121, 43)'}}/>,
      label: (
        <span style={{
          color: 'rgb(245, 121, 43)',
          fontFamily: 'Arial, sans-serif',
          fontSize: '20px',
          fontWeight: 'bold'
        }}>Viagens Completas</span>
      ),
      onClick: () => setSelectedChart('TripsCompletedChartData'),
    },
    {
      key: '2',
      icon: <BarChartOutlined style={{color: 'rgb(245, 121, 43)'}}/>,
      label: (
        <span style={{
          color: 'rgb(245, 121, 43)',
          fontFamily: 'Arial, sans-serif',
          fontSize: '20px',
          fontWeight: 'bold'
        }}>Distância Percorrida</span>
      ),
      onClick: () => setSelectedChart('TraveledKmChartData'),
    },
    {
      key: '3',
      icon: <BarChartOutlined style={{color: 'rgb(245, 121, 43)'}}/>,
      label: (
        <span style={{
          color: 'rgb(245, 121, 43)',
          fontFamily: 'Arial, sans-serif',
          fontSize: '20px',
          fontWeight: 'bold'
        }}>Climatização</span>
      ),
      onClick: () => setSelectedChart('ClimatizationChartData'),
    },
    {
      key: '4',
      icon: <BarChartOutlined style={{color: 'rgb(245, 121, 43)'}}/>,
      label: (
        <span style={{
          color: 'rgb(245, 121, 43)',
          fontFamily: 'Arial, sans-serif',
          fontSize: '20px',
          fontWeight: 'bold'
        }}>Frotas Disponíveis</span>
      ),
      onClick: () => setSelectedChart('AvailableFleetChartData'),
    },
    {
      key: '5',
      icon: <BarChartOutlined style={{color: 'rgb(245, 121, 43)'}}/>,
      label: (
        <span style={{
          color: 'rgb(245, 121, 43)',
          fontFamily: 'Arial, sans-serif',
          fontSize: '20px',
          fontWeight: 'bold'
        }}>Subsídio Total</span>
      ),
      onClick: () => setSelectedChart('TotalSubsidyChartData'),
    },
  ];

  return <Menu mode="inline" className="sidebar" items={items} />;
};

export default Sidebar;