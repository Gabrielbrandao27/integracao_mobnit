import { BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, PointElement, Title, Tooltip } from 'chart.js';
import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { fetchAvailableFleetData, fetchClimatizationData, fetchCompletedTripsData, fetchTotalSubsidy, fetchTraveledKmData, } from '../api/dashboardService';
import { AvailableFleetData, ClimatizationData, dappResponseData, TotalSubsidyData, TraveledKmData, TripsCompletedData } from '../types/DashboardData';
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
  const [availableFleet, setAvailableFleet] = useState<AvailableFleetData | null>(null);
  const [totalSubsidy, setTotalSubsidy] = useState<TotalSubsidyData | null>(null);
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
        const result: dappResponseData = await fetchAvailableFleetData();
        if (result.reports && result.reports.length > 0) {
          const hexPayload = result.reports[0].payload;
          const stringPayload = hex2str(hexPayload);
          const jsonPayload: AvailableFleetData = JSON.parse(stringPayload);
          
          setAvailableFleet(jsonPayload);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    const getTotalSubsidy = async () => {
      try {
        const result: dappResponseData = await fetchTotalSubsidy();
        if (result.reports && result.reports.length > 0) {
          const hexPayload = result.reports[0].payload;
          const stringPayload = hex2str(hexPayload);
          const jsonPayload: TotalSubsidyData = JSON.parse(stringPayload);
          
          setTotalSubsidy(jsonPayload);
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
    getTotalSubsidy();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

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
        backgroundColor: 'rgba(54, 96, 235, 0.45)',
        borderColor: 'rgb(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânico',
        data: completedTrips
          ?.filter(
            (dado) =>
              dado.consorcium === 'transoceânico' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(245, 121, 43, 0.45)',
        borderColor: 'rgb(255, 0, 0, 1)',
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
        backgroundColor: 'rgba(54, 96, 235, 0.45)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânico',
        data: traveledKm
          ?.filter(
            (dado) =>
              dado.consorcium === 'transoceânico' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(245, 121, 43, 0.45)',
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
        backgroundColor: 'rgba(54, 96, 235, 0.45)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânico',
        data: climatization
          ?.filter(
            (dado) =>
              dado.consorcium === 'transoceânico' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(245, 121, 43, 0.45)',
        borderColor: 'rgba(255, 0, 0, 1)',
        borderWidth: 1,
      },
    ],
  };

  const AvailableFleetChartData = {
    labels: selectedDate
      ? [...new Set(availableFleet?.filter((dado) => dado.date === selectedDate).map((dado) => dado.date))] 
      : [...new Set(availableFleet?.map((dado) => dado.date))],
    datasets: [
      {
        label: 'TransNit',
        data: availableFleet
          ?.filter(
            (dado) =>
              dado.consorcium === 'transnit' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(54, 96, 235, 0.45)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânico',
        data: availableFleet
          ?.filter(
            (dado) =>
              dado.consorcium === 'transoceânico' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.subsidy) || [],
        backgroundColor: 'rgba(245, 121, 43, 0.45)',
        borderColor: 'rgba(255, 0, 0, 1)',
        borderWidth: 1,
      },
    ],
  };

  const TotalSubsidyChartData = {
    labels: selectedDate
      ? [...new Set(totalSubsidy?.filter((dado) => dado.date === selectedDate).map((dado) => dado.date))] 
      : [...new Set(totalSubsidy?.map((dado) => dado.date))],
    datasets: [
      {
        label: 'TransNit',
        data: totalSubsidy
          ?.filter(
            (dado) =>
              dado.consorcium === 'transnit' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.total_subsidy) || [],
        backgroundColor: 'rgba(54, 96, 235, 0.45)',
        borderColor: 'rgba(0, 0, 255, 1)',
        borderWidth: 1,
      },
      {
        label: 'TransOceânico',
        data: totalSubsidy
          ?.filter(
            (dado) =>
              dado.consorcium === 'transoceânico' &&
              (selectedDate ? dado.date === selectedDate : true)
          )
          .map((dado) => dado.total_subsidy) || [],
        backgroundColor: 'rgba(245, 121, 43, 0.45)',
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
          font: {
            size: 16, 
          },
        },
      },
      tooltip: {
        titleFont: {
          size: 16, 
        },
        bodyFont: {
          size: 16, 
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: 'black',
          font: {
            size: 16,
          },
        },
      },
      y: {
        ticks: {
          color: 'black',
          font: {
            size: 16,
          },
          min: 0,
          max: 100,
        },
      },
    },
  };

  const UniqueDates = [
    ...new Set([
      ...completedTrips?.map((dado) => dado.date) || [],
      ...traveledKm?.map((dado) => dado.date) || [],
      ...climatization?.map((dado) => dado.date) || [],
      ...availableFleet?.map((dado) => dado.date) || [],
    ]),
  ];

  const renderChart = () => {
    switch (selectedChart) {
      case 'TripsCompletedChartData':
        return <Bar data={TripsCompletedChartData} options={chartOptions} width={500} height={400} />;
      case 'TraveledKmChartData':
        return <Bar data={TraveledKmChartData} options={chartOptions} width={500} height={400} />;
      case 'ClimatizationChartData':
        return <Bar data={ClimatizationChartData} options={chartOptions} width={500} height={400} />;
      case 'AvailableFleetChartData':
        return <Bar data={AvailableFleetChartData} options={chartOptions} width={500} height={400} />;
      case 'TotalSubsidyChartData':
        return <Bar data={TotalSubsidyChartData} options={chartOptions} width={500} height={400} />;
      default:
        return <Bar data={TripsCompletedChartData} options={chartOptions} width={500} height={400} />;
    }
  };

  const expectedAndRecordedValues = () => {
    if (!selectedDate) {
      return (
        <div>Para Visualizar os valores esperados e registrados, selecione uma data</div>
      );
    }

    switch (selectedChart) {
      case 'TripsCompletedChartData':
        return (
          <div className="flex-container">
            <div>
              <h3>TransNit</h3>
              <p>Viagens Esperadas: {completedTrips?.filter(dado => dado.consorcium === 'transnit' && dado.date === selectedDate)[0]?.trips_scheduled}</p>
              <p>Viagens Registradas: {completedTrips?.filter(dado => dado.consorcium === 'transnit' && dado.date === selectedDate)[0]?.trips_completed}</p>
            </div>
            <div>
              <h3>TransOceânico</h3>
              <p>Viagens Esperadas: {completedTrips?.filter(dado => dado.consorcium === 'transoceânico' && dado.date === selectedDate)[0]?.trips_scheduled}</p>
              <p>Viagens Registradas: {completedTrips?.filter(dado => dado.consorcium === 'transoceânico' && dado.date === selectedDate)[0]?.trips_completed}</p>
            </div>
          </div>
        );
      case 'TraveledKmChartData':
        return (
          <div className="flex-container">
            <div>
              <h3>TransNit</h3>
              <p>Distância Percorrida Esperada: {traveledKm?.filter(dado => dado.consorcium === 'transnit' && dado.date === selectedDate)[0]?.km_scheduled}</p>
              <p>Distância Percorrida Registrada: {traveledKm?.filter(dado => dado.consorcium === 'transnit' && dado.date === selectedDate)[0]?.km_completed}</p>
            </div>
            <div>
              <h3>TransOceânico</h3>
              <p>Distância Percorrida Esperada: {traveledKm?.filter(dado => dado.consorcium === 'transoceânico' && dado.date === selectedDate)[0]?.km_scheduled}</p>
              <p>Distância Percorrida Registrada: {traveledKm?.filter(dado => dado.consorcium === 'transoceânico' && dado.date === selectedDate)[0]?.km_completed}</p>
            </div>
          </div>
        );
      case 'ClimatizationChartData':
        return (
          <div className="flex-container">
            <div>
              <h3>TransNit</h3>
              <p>Total de Ônibus: {climatization?.filter(dado => dado.consorcium === 'transnit' && dado.date === selectedDate)[0]?.total_busses}</p>
              <p>Ônibus sem Climatização: {climatization?.filter(dado => dado.consorcium === 'transnit' && dado.date === selectedDate)[0]?.busses_without_climatization}</p>
            </div>
            <div>
              <h3>TransOceânico</h3>
              <p>Total de Ônibus: {climatization?.filter(dado => dado.consorcium === 'transoceânico' && dado.date === selectedDate)[0]?.total_busses}</p>
              <p>Ônibus sem Climatização: {climatization?.filter(dado => dado.consorcium === 'transoceânico' && dado.date === selectedDate)[0]?.busses_without_climatization}</p>
            </div>
          </div>
        );
      case 'AvailableFleetChartData':
        return (
          <div className="flex-container">
            <div>
              <h3>TransNit</h3>
              <p>Frota Esperada: {availableFleet?.filter(dado => dado.consorcium === 'transnit' && dado.date === selectedDate)[0]?.scheduled_fleets}</p>
              <p>Frota Disponível: {availableFleet?.filter(dado => dado.consorcium === 'transnit' && dado.date === selectedDate)[0]?.recorded_fleets}</p>
            </div>
            <div>
              <h3>TransOceânico</h3>
              <p>Frota Esperada: {availableFleet?.filter(dado => dado.consorcium === 'transoceânico' && dado.date === selectedDate)[0]?.scheduled_fleets}</p>
              <p>Frota Disponível: {availableFleet?.filter(dado => dado.consorcium === 'transoceânico' && dado.date === selectedDate)[0]?.recorded_fleets}</p>
            </div>
          </div>
        );
      case 'TotalSubsidyChartData':
        return (
          <div className="flex-container">
            <div>
              <h3>TransNit</h3>
              <p>Total Subsidy: {totalSubsidy?.filter(dado => dado.consorcium === 'transnit')[0]?.total_subsidy}</p>
            </div>
            <div>
              <h3>TransOceânico</h3>
              <p>Total Subsidy: {totalSubsidy?.filter(dado => dado.consorcium === 'transoceânico')[0]?.total_subsidy}</p>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  const handleDateChange = (value: string | null) => {
    setSelectedDate(value);
  };

  return (
    <div>
      <HeaderBar/>
      <div className='dashboard'>
        <Sidebar setSelectedChart={setSelectedChart}/>
        <div className='expected-recorded-values'>
          {expectedAndRecordedValues()}
        </div>
        <div className='chart-and-select-container'>
          <div className='chart-container'>
            {renderChart()}
          </div>
          <SelectButton options={UniqueDates.map(date => ({ value: date, label: date}))} onChange={handleDateChange}/>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;