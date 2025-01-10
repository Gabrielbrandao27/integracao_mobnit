import { AppstoreOutlined, MailOutlined, SettingOutlined } from '@ant-design/icons';
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
      icon: <MailOutlined />,
      label: 'Viagens Completas',
      onClick: () => setSelectedChart('TripsCompletedChartData'),
    },
    {
      key: '2',
      icon: <AppstoreOutlined />,
      label: 'Distância Percorrida',
      onClick: () => setSelectedChart('TraveledKmChartData'),
    },
    {
      key: '3',
      icon: <SettingOutlined />,
      label: 'Climatização',
      onClick: () => setSelectedChart('ClimatizationChartData'),
    },
    {
      key: '4',
      icon: <AppstoreOutlined />,
      label: 'Frotas Disponíveis',
      onClick: () => setSelectedChart('AvaiableFleetchartData'),
    },
  ];

  return <Menu mode="inline" className="sidebar" items={items} />;
};

export default Sidebar;