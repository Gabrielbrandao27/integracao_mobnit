import { CategoryScale, Chart as ChartJS, Legend, LinearScale, LineElement, PointElement, Title, Tooltip } from 'chart.js';
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { fetchAvaiableFleetData, fetchClimatizationData, fetchCompletedTripsData, fetchTraveledKmData, } from '../api/dashboardService';
import { AvaiableFleetData, ClimatizationData, dappResponseData, TraveledKmData, TripsCompletedData } from '../types/DashboardData';
import { hex2str } from '../utils/ether';
import './styles.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [completedTrips, setCompletedTrips] = useState<TripsCompletedData | null>(null);
  const [traveledKm, setTraveledKm] = useState<TraveledKmData | null>(null);
  const [climatization, setClimatization] = useState<ClimatizationData | null>(null);
  const [avaiableFleet, setAvaibleFleet] = useState<AvaiableFleetData | null>(null);
  
  useEffect(() => {
    const getCompletedTripsData = async () => {
      try {
        const result: dappResponseData = await fetchCompletedTripsData();
        if (result.reports && result.reports.length > 0) {
          const hexPayload = result.reports[0].payload;
          const stringPayload = hex2str(hexPayload);
          const jsonPayload: TripsCompletedData = JSON.parse(stringPayload);
          
          setCompletedTrips(jsonPayload);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    const getTraveledKmData = async () => {
      try {
        const result: dappResponseData = await fetchTraveledKmData();
        if (result.reports && result.reports.length > 0) {
          const hexPayload = result.reports[0].payload;
          const stringPayload = hex2str(hexPayload);
          const jsonPayload: TraveledKmData = JSON.parse(stringPayload);
          
          setTraveledKm(jsonPayload);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    const getClimatizationData = async () => {
      try {
        const result: dappResponseData = await fetchClimatizationData();
        if (result.reports && result.reports.length > 0) {
          const hexPayload = result.reports[0].payload;
          const stringPayload = hex2str(hexPayload);
          const jsonPayload: ClimatizationData = JSON.parse(stringPayload);
          
          setClimatization(jsonPayload);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

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

    getCompletedTripsData();
    getTraveledKmData();
    getClimatizationData();
    getFleetData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }
  
  const TripsCompletedChartData = {
    labels: completedTrips?.filter(
      (obj, index) =>
        completedTrips.findIndex((item) => item.date === obj.date) === index).map((dado) => dado.date) || [],
    datasets: [
      {
        label: 'TransNit',
        data: completedTrips?.filter((dado) => dado.consorcium === 'TransNit').map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(0, 0, 255, 0.2)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânica',
        data: completedTrips?.filter((dado) => dado.consorcium === 'TransOceanica').map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(255, 0, 0, 0.2)',
        borderColor: 'rgba(255, 0, 0, 1)',
        borderWidth: 1,
      },
    ],
  };

  const TraveledKmChartData = {
    labels: traveledKm?.filter(
      (obj, index) =>
        traveledKm.findIndex((item) => item.date === obj.date) === index).map((dado) => dado.date) || [],
    datasets: [
      {
        label: 'TransNit',
        data: traveledKm?.filter((dado) => dado.consorcium === 'TransNit').map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(0, 0, 255, 0.2)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânica',
        data: traveledKm?.filter((dado) => dado.consorcium === 'TransOceanica').map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(255, 0, 0, 0.2)',
        borderColor: 'rgba(255, 0, 0, 1)',
        borderWidth: 1,
      },
    ],
  };

  const ClimatizationChartData = {
    labels: climatization?.filter(
      (obj, index) =>
        climatization.findIndex((item) => item.date === obj.date) === index).map((dado) => dado.date) || [],
    datasets: [
      {
        label: 'TransNit',
        data: climatization?.filter((dado) => dado.consorcium === 'TransNit').map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(0, 0, 255, 0.2)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânica',
        data: climatization?.filter((dado) => dado.consorcium === 'TransOceanica').map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(255, 0, 0, 0.2)',
        borderColor: 'rgba(255, 0, 0, 1)',
        borderWidth: 1,
      },
    ],
  };

  const AvaiableFleetchartData = {
    labels: avaiableFleet?.filter(
      (obj, index) =>
        avaiableFleet.findIndex((item) => item.date === obj.date) === index).map((dado) => dado.date) || [],
    datasets: [
      {
        label: 'TransNit',
        data: avaiableFleet?.filter((dado) => dado.consorcium === 'TransNit').map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(0, 0, 255, 0.2)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânica',
        data: avaiableFleet?.filter((dado) => dado.consorcium === 'TransOceanica').map((dado) => dado.subsidy) || [],
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
        min: 0,
        max: 100,
      },
    },
  };

  return (
    <div className='dashboard-title'>
      <h2>Dashboard Subsídios</h2>
      <div className='charts-grid'>
        <div className='chart-container'>
          Viagens Completas
          <Line data={TripsCompletedChartData} options={chartOptions} width={500} height={400} />
        </div>
        <div className='chart-container'>
          Distância Percorrida
          <Line data={TraveledKmChartData} options={chartOptions} width={500} height={400} />
        </div>
        <div className='chart-container'>
          Climatização
          <Line data={ClimatizationChartData} options={chartOptions} width={500} height={400} />
        </div>
        <div className='chart-container'>
          Frotas Disponíveis
          <Line data={AvaiableFleetchartData} options={chartOptions} width={500} height={400} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;