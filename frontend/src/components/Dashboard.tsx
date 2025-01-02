import React, { useEffect, useState } from 'react';
import { fetchDashboardData } from '../api/dashboardService';
import { DashboardData, Payload } from '../types/DashboardData';
import { hex2str } from '../utils/ether';

const Dashboard: React.FC = () => {
  const [dados, setDados] = useState<Payload['dados'] | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const getData = async () => {
      try {
        const result: DashboardData = await fetchDashboardData();
        if (result.reports && result.reports.length > 0) {
          const hexPayload = result.reports[0].payload;
          const stringPayload = hex2str(hexPayload);
          const cleanedPayload = stringPayload.replace(/^\['|'\]$/g, '').replace(/\\n/g, '').replace(/\\'/g, "'");
          const jsonPayload: Payload = JSON.parse(cleanedPayload);
          setDados(jsonPayload.dados);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    getData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Dashboard Dados</h1>
      <pre>{JSON.stringify(dados, null, 2)}</pre>
    </div>
  );
};

export default Dashboard;