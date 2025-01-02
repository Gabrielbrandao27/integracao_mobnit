export interface Report {
  payload: string;
}

export interface DashboardData {
  status: string;
  exception_payload: null;
  reports: Report[];
  processed_input_count: number;
}

export interface Criterios {
  de: string;
  ate: string;
}

export interface Dados {
  linha: string;
  frotaProgramada: number;
  frotaDisponivel: number;
}

export interface Payload {
  criterios: Criterios;
  dados: Dados[];
  complianceSubsidio: string;
  subsidioConcedido: number;
}
