import { CategoryScale, Chart as ChartJS, Legend, LinearScale, LineElement, PointElement, Title, Tooltip } from 'chart.js';
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { fetchAvaiableFleetData } from '../api/dashboardService';
import { AvaiableFleetData, dappResponseData } from '../types/DashboardData';
import { hex2str } from '../utils/ether';
import './styles.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [avaiableFleet, setAvaibleFleet] = useState<AvaiableFleetData | null>(null);
  
  useEffect(() => {
    const getFleetData = async () => {
      try {
        const result: dappResponseData = await fetchAvaiableFleetData();
        if (result.reports && result.reports.length > 0) {
          const hexPayload = result.reports[0].payload;
          const stringPayload = hex2str(hexPayload);
          const jsonPayload: AvaiableFleetData = JSON.parse(stringPayload);
          
          setAvaibleFleet(jsonPayload);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    getFleetData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  const chartData = {
    labels: avaiableFleet?.map((dado) => dado.line_id) || [],
    datasets: [
      {
        label: 'Frota Programada',
        data: avaiableFleet?.map((dado) => dado.expected_bus_amount) || [],
        backgroundColor: 'rgba(0, 0, 255, 0.2)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'Frota Disponível',
        data: avaiableFleet?.map((dado) => dado.recorded_bus_amount) || [],
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
      <h2>Dashboard Subsídios</h2>
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