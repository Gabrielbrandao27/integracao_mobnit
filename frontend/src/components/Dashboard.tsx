import { CategoryScale, Chart as ChartJS, Legend, LinearScale, LineElement, PointElement, Title, Tooltip } from 'chart.js';
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { fetchDashboardData } from '../api/dashboardService';
import { DashboardData, Payload } from '../types/DashboardData';
import { hex2str } from '../utils/ether';
import './styles.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

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

  const chartData = {
    labels: dados?.map((dado) => dado.linha) || [],
    datasets: [
      {
        label: 'Frota Programada',
        data: dados?.map((dado) => dado.frotaProgramada) || [],
        backgroundColor: 'rgba(0, 0, 255, 0.2)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'Frota Disponível',
        data: dados?.map((dado) => dado.frotaDisponivel) || [],
        backgroundColor: 'rgba(255, 0, 0, 0.2)',
        borderColor: 'rgba(255, 0, 0, 1)',
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    plugins: {
      legend: {
        labels: {
          color: 'black',
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: 'black',
        },
      },
      y: {
        ticks: {
          color: 'black',
        },
      },
    },
  };

  return (
    <div className='dashboard-title'>
      <h1>Dashboard Dados</h1>
      <div className='charts-grid'>
        <div className='chart-container'>
          <Line data={chartData} options={chartOptions} width={500} height={400} />
        </div>
        <div className='chart-container'>
          <Line data={chartData} options={chartOptions} width={500} height={400} />
        </div>
        <div className='chart-container'>
          <Line data={chartData} options={chartOptions} width={500} height={400} />
        </div>
        <div className='chart-container'>
          <Line data={chartData} options={chartOptions} width={500} height={400} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;