import { BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, PointElement, Title, Tooltip } from 'chart.js';
import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { fetchAvaiableFleetData, fetchClimatizationData, fetchCompletedTripsData, fetchTraveledKmData, } from '../api/dashboardService';
import { AvaiableFleetData, ClimatizationData, dappResponseData, TraveledKmData, TripsCompletedData } from '../types/DashboardData';
import { hex2str } from '../utils/ether';
import HeaderBar from './Header';
import SelectButton from './SelectButton';
import Sidebar from './Sidebar';
import './styles.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, BarElement, Title, Tooltip, Legend);

const Dashboard: React.FC = () => {
  const [selectedChart, setSelectedChart] = useState('TripsCompletedChartData');
  const [loading, setLoading] = useState<boolean>(true);
  const [completedTrips, setCompletedTrips] = useState<TripsCompletedData | null>(null);
  const [traveledKm, setTraveledKm] = useState<TraveledKmData | null>(null);
  const [climatization, setClimatization] = useState<ClimatizationData | null>(null);
  const [avaiableFleet, setAvaibleFleet] = useState<AvaiableFleetData | null>(null);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  
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

  const filterDataByDate = (data) => {
    if (!selectedDate) return data;
    return data.filter((dado) => dado.date === selectedDate);
  };
  
  const TripsCompletedChartData = {
    labels: selectedDate
      ? [...new Set(completedTrips?.filter((dado) => dado.date === selectedDate).map((dado) => dado.date))] 
      : [...new Set(completedTrips?.map((dado) => dado.date))],
    datasets: [
      {
        label: 'TransNit',
        data: completedTrips
          ?.filter(
            (dado) =>
              dado.consorcium === 'transnit' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(0, 0, 255, 0.2)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânica',
        data: completedTrips
          ?.filter(
            (dado) =>
              dado.consorcium === 'transoceânico' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(255, 0, 0, 0.2)',
        borderColor: 'rgba(255, 0, 0, 1)',
        borderWidth: 1,
      },
    ],
  };

  const TraveledKmChartData = {
    labels: selectedDate
      ? [...new Set(traveledKm?.filter((dado) => dado.date === selectedDate).map((dado) => dado.date))] 
      : [...new Set(traveledKm?.map((dado) => dado.date))],
    datasets: [
      {
        label: 'TransNit',
        data: traveledKm
          ?.filter(
            (dado) =>
              dado.consorcium === 'transnit' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(0, 0, 255, 0.2)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânica',
        data: traveledKm
          ?.filter(
            (dado) =>
              dado.consorcium === 'transoceânico' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(255, 0, 0, 0.2)',
        borderColor: 'rgba(255, 0, 0, 1)',
        borderWidth: 1,
      },
    ],
  };

  const ClimatizationChartData = {
    labels: selectedDate
      ? [...new Set(climatization?.filter((dado) => dado.date === selectedDate).map((dado) => dado.date))] 
      : [...new Set(climatization?.map((dado) => dado.date))],
    datasets: [
      {
        label: 'TransNit',
        data: climatization
          ?.filter(
            (dado) =>
              dado.consorcium === 'transnit' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(0, 0, 255, 0.2)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânica',
        data: climatization
          ?.filter(
            (dado) =>
              dado.consorcium === 'transoceânico' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(255, 0, 0, 0.2)',
        borderColor: 'rgba(255, 0, 0, 1)',
        borderWidth: 1,
      },
    ],
  };

  const AvaiableFleetchartData = {
    labels: selectedDate
      ? [...new Set(avaiableFleet?.filter((dado) => dado.date === selectedDate).map((dado) => dado.date))] 
      : [...new Set(avaiableFleet?.map((dado) => dado.date))],
    datasets: [
      {
        label: 'TransNit',
        data: avaiableFleet
          ?.filter(
            (dado) =>
              dado.consorcium === 'transnit' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(0, 0, 255, 0.2)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânica',
        data: avaiableFleet
          ?.filter(
            (dado) =>
              dado.consorcium === 'transoceânico' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
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

  const UniqueDates = [
    ...new Set([
      ...completedTrips?.map((dado) => dado.date) || [],
      ...traveledKm?.map((dado) => dado.date) || [],
      ...climatization?.map((dado) => dado.date) || [],
      ...avaiableFleet?.map((dado) => dado.date) || [],
    ]),
  ];

  console.log(TripsCompletedChartData)

  const renderChart = () => {
    switch (selectedChart) {
      case 'TripsCompletedChartData':
        return <Bar data={TripsCompletedChartData} options={chartOptions} width={500} height={400} />;
      case 'TraveledKmChartData':
        return <Bar data={TraveledKmChartData} options={chartOptions} width={500} height={400} />;
      case 'ClimatizationChartData':
        return <Bar data={ClimatizationChartData} options={chartOptions} width={500} height={400} />;
      case 'AvaiableFleetchartData':
        return <Bar data={AvaiableFleetchartData} options={chartOptions} width={500} height={400} />;
      default:
        return <Bar data={TripsCompletedChartData} options={chartOptions} width={500} height={400} />;
    }
  };

  console.log(selectedChart)

  const handleDateChange = (value) => {
    setSelectedDate(value);
  };

  return (
    <div>
      <HeaderBar/>
      <div className='dashboard'>
        <Sidebar setSelectedChart={setSelectedChart}/>
        <div className='chart-container'>
          {renderChart()}
        </div>
        <SelectButton options={UniqueDates.map(date => ({ value: date, label: date}))} onChange={handleDateChange}/>
      </div>
    </div>
  );
};

export default Dashboard;